#!/usr/bin/env python3
"""Zero Trust Watcher - Real-time dashboard for Codex session logs.

Monitors ~/.codex/sessions/**/*.jsonl and serves a live dashboard at localhost:9999.
Python 3 stdlib only - no external dependencies.
"""

import hashlib
import http.server
import json
import pathlib
import queue
import subprocess
import threading
import time
import urllib.parse
from collections import defaultdict
from datetime import datetime

# --- Configuration ---
PORT = 9999
HOST = "127.0.0.1"
SESSIONS_ROOT = pathlib.Path.home() / ".codex" / "sessions"
ALERTS_LOG = pathlib.Path.home() / ".codex" / "alerts.jsonl"
DASHBOARD_PATH = pathlib.Path(__file__).parent / "dashboard.html"
POLL_INTERVAL = 1.0

# --- In-memory state ---
events = []  # Normalized events for the dashboard
alerts = []  # Anomaly detections
sse_clients = []  # Queue per SSE client
lock = threading.Lock()


class SessionLogMonitor:
    """Tracks Codex session JSONL files and emits normalized watcher events."""

    def __init__(self, sessions_root):
        self.sessions_root = sessions_root
        self.file_offsets = {}
        self.seen_event_ids = set()
        self.session_agents = defaultdict(dict)

    def load_existing_events(self):
        """Read all existing session files once at startup."""
        normalized = []
        for path in sorted(self._session_files()):
            normalized.extend(self._read_new_lines(path, from_start=True))
        return normalized

    def poll(self):
        """Read only new lines appended since the last poll."""
        normalized = []
        for path in sorted(self._session_files()):
            normalized.extend(self._read_new_lines(path, from_start=False))
        return normalized

    def _session_files(self):
        if not self.sessions_root.exists():
            return []
        return self.sessions_root.rglob("*.jsonl")

    def _read_new_lines(self, path, from_start):
        if from_start:
            offset = 0
        else:
            offset = self.file_offsets.get(path)
            if offset is None:
                offset = path.stat().st_size

        normalized = []
        with path.open("r", encoding="utf-8") as f:
            f.seek(offset)
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    raw_event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                normalized.extend(self._normalize_event(raw_event, path))
            self.file_offsets[path] = f.tell()
        return normalized

    def _normalize_event(self, raw_event, path):
        raw_type = raw_event.get("type")
        timestamp = raw_event.get("timestamp", "")
        payload = raw_event.get("payload", {})

        if raw_type == "session_meta":
            session_id = payload.get("id", "no-session")
            return [self._event(
                raw_event,
                event="session_start",
                session_id=session_id,
                timestamp=payload.get("timestamp") or timestamp,
                tool="Session",
                detail=f"{payload.get('source', 'unknown')} @ {payload.get('cwd', '')}",
                cwd=payload.get("cwd", ""),
                agent_id="main",
                agent_type=payload.get("originator", "codex"),
            )]

        if raw_type == "turn_context":
            turn_id = payload.get("turn_id", "")
            return [self._event(
                raw_event,
                event="turn_context",
                session_id=self._session_id_from_path(path),
                timestamp=timestamp,
                tool="Turn",
                detail=f"{payload.get('approval_policy', 'unknown')} / {payload.get('model', 'unknown')}",
                cwd=payload.get("cwd", ""),
                turn_id=turn_id,
            )]

        if raw_type == "event_msg":
            inner_type = payload.get("type")
            if inner_type == "user_message":
                return [self._event(
                    raw_event,
                    event="user_message",
                    session_id=self._session_id_from_path(path),
                    timestamp=timestamp,
                    tool="User",
                    detail=payload.get("message", "").strip(),
                )]
            if inner_type == "agent_message":
                return [self._event(
                    raw_event,
                    event="assistant_message",
                    session_id=self._session_id_from_path(path),
                    timestamp=timestamp,
                    tool="Assistant",
                    detail=payload.get("message", "").strip(),
                    phase=payload.get("phase", ""),
                )]
            if inner_type == "task_started":
                return [self._event(
                    raw_event,
                    event="task_started",
                    session_id=self._session_id_from_path(path),
                    timestamp=timestamp,
                    tool="Task",
                    detail=payload.get("turn_id", ""),
                    turn_id=payload.get("turn_id", ""),
                )]
            if inner_type == "task_complete":
                return [self._event(
                    raw_event,
                    event="task_complete",
                    session_id=self._session_id_from_path(path),
                    timestamp=timestamp,
                    tool="Task",
                    detail=(payload.get("last_agent_message") or "").strip(),
                    turn_id=payload.get("turn_id", ""),
                )]
            return []

        if raw_type != "response_item":
            return []

        payload_type = payload.get("type")
        session_id = self._session_id_from_path(path)
        if payload_type == "function_call":
            tool_name = self._tool_name(payload.get("name", "unknown"))
            detail = self._tool_detail(payload)
            return [self._event(
                raw_event,
                event="tool_use",
                session_id=session_id,
                timestamp=timestamp,
                tool=tool_name,
                detail=detail,
                call_id=payload.get("call_id", ""),
            )]

        if payload_type == "function_call_output":
            output = payload.get("output", "")
            if "Permission denied" in output or "sandbox" in output.lower():
                return [self._event(
                    raw_event,
                    event="tool_blocked",
                    session_id=session_id,
                    timestamp=timestamp,
                    tool="shell_command",
                    detail="Sandbox or permission failure",
                    decision="deny",
                    reason=self._first_nonempty_line(output),
                    call_id=payload.get("call_id", ""),
                )]
            return []

        if payload_type == "message" and payload.get("role") == "assistant":
            phase = payload.get("phase", "")
            text = self._assistant_text(payload)
            if not text:
                return []
            return [self._event(
                raw_event,
                event="assistant_message",
                session_id=session_id,
                timestamp=timestamp,
                tool="Assistant",
                detail=text,
                phase=phase,
            )]

        if payload_type == "reasoning":
            summary = self._reasoning_summary(payload)
            if not summary:
                return []
            return [self._event(
                raw_event,
                event="reasoning",
                session_id=session_id,
                timestamp=timestamp,
                tool="Reasoning",
                detail=summary,
            )]

        return []

    @staticmethod
    def _first_nonempty_line(output):
        for line in output.splitlines():
            line = line.strip()
            if line:
                return line
        return "Command blocked"

    @staticmethod
    def _assistant_text(payload):
        content = payload.get("content", [])
        texts = []
        for item in content:
            if item.get("type") == "output_text":
                text = item.get("text", "").strip()
                if text:
                    texts.append(text)
        return " ".join(texts)

    @staticmethod
    def _reasoning_summary(payload):
        summaries = []
        for item in payload.get("summary", []):
            if item.get("type") == "summary_text":
                text = item.get("text", "").strip()
                if text:
                    summaries.append(text)
        return " ".join(summaries)

    @staticmethod
    def _tool_name(raw_name):
        mapping = {
            "shell_command": "Bash",
            "apply_patch": "Edit",
            "request_user_input": "AskUserQuestion",
            "spawn_agent": "TaskCreate",
            "send_input": "TaskUpdate",
            "wait_agent": "Task",
            "close_agent": "Task",
            "resume_agent": "Task",
            "view_image": "Read",
        }
        return mapping.get(raw_name, raw_name)

    def _tool_detail(self, payload):
        name = payload.get("name", "")
        try:
            arguments = json.loads(payload.get("arguments", "{}"))
        except json.JSONDecodeError:
            arguments = {}

        if name == "shell_command":
            return arguments.get("command", "")
        if name == "apply_patch":
            return "apply_patch"
        if name in {"spawn_agent", "send_input"}:
            return arguments.get("message", "") or arguments.get("id", "")
        if name == "wait_agent":
            ids = arguments.get("ids", [])
            return ", ".join(ids)
        if name == "view_image":
            return arguments.get("path", "")
        return json.dumps(arguments, sort_keys=True)

    @staticmethod
    def _session_id_from_path(path):
        stem = path.stem
        if "rollout-" in stem:
            return stem.split("-")[-1]
        return stem

    def _event(self, raw_event, **fields):
        digest = hashlib.sha1(
            json.dumps(raw_event, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()
        fields["id"] = digest
        return fields


monitor = SessionLogMonitor(SESSIONS_ROOT)


# --- Anomaly Detection Engine ---
class AnomalyDetector:
    """Evaluates each new event against security rules."""

    def __init__(self):
        self._session_tools = defaultdict(list)
        self._session_env_reads = defaultdict(int)
        self._tool_output_by_call = {}
        self._no_session_alerted = False

    def check(self, event):
        new_alerts = []
        ts = event.get("timestamp", "")
        sid = event.get("session_id", "unknown")
        tool = event.get("tool", "")
        detail = event.get("detail", "")
        evt_type = event.get("event", "")

        if evt_type == "tool_use":
            self._session_tools[sid].append((ts, tool))

        if sid == "no-session" and evt_type == "tool_use" and not self._no_session_alerted:
            self._no_session_alerted = True
            new_alerts.append(self._alert(
                "info", "No session context",
                "Session metadata unavailable in the stream", ts
            ))

        if evt_type == "tool_blocked":
            decision = event.get("decision", "")
            reason = event.get("reason", "")
            severity = "critical" if decision == "deny" else "warning"
            if "secret" in reason.lower() or "credential" in reason.lower():
                severity = "critical"
            new_alerts.append(self._alert(
                severity, f"Tool gate: {decision}",
                f"{tool} - {reason}", ts
            ))

        if evt_type == "tool_use" and tool == "Read" and ".env" in detail:
            self._session_env_reads[sid] += 1
            if self._session_env_reads[sid] == 4:
                new_alerts.append(self._alert(
                    "high", "Excessive .env access",
                    f"Session {sid[:12]}... read .env files {self._session_env_reads[sid]} times",
                    ts
                ))

        if evt_type == "tool_use":
            recent = [t for t, _ in self._session_tools[sid]
                      if self._time_diff(t, ts) < 60]
            if len(recent) > 20 and len(recent) == 21:
                new_alerts.append(self._alert(
                    "warning", "Tool call burst",
                    f"Session {sid[:12]}... made {len(recent)} calls in 60s", ts
                ))

        if evt_type == "tool_use":
            tools_list = [t for _, t in self._session_tools[sid]]
            if len(tools_list) >= 10:
                bash_pct = tools_list.count("Bash") / len(tools_list)
                if bash_pct > 0.7 and len(tools_list) % 10 == 0:
                    new_alerts.append(self._alert(
                        "warning", "Bash-heavy session",
                        f"Session {sid[:12]}... - {bash_pct:.0%} Bash ({len(tools_list)} total calls)",
                        ts
                    ))

        if evt_type == "tool_use" and tool in ("Write", "Edit"):
            write_times = [t for t, tl in self._session_tools[sid]
                           if tl in ("Write", "Edit") and self._time_diff(t, ts) < 30]
            if len(write_times) == 11:
                new_alerts.append(self._alert(
                    "warning", "Rapid file writes",
                    f"Session {sid[:12]}... made {len(write_times)} writes in 30s", ts
                ))

        return new_alerts

    def _alert(self, severity, title, description, timestamp):
        alert = {
            "severity": severity,
            "title": title,
            "description": description,
            "timestamp": timestamp,
            "id": f"alert-{len(alerts) + 1}"
        }
        if severity in ("critical", "high"):
            self._notify(severity, title, description)
        return alert

    @staticmethod
    def _notify(severity, title, description):
        try:
            icon = "CRITICAL" if severity == "critical" else "HIGH"
            subprocess.Popen(
                ["osascript", "-e",
                 f'display notification "{description}" '
                 f'with title "Zero Trust Watcher [{icon}]" '
                 f'subtitle "{title}" '
                 f'sound name "Sosumi"'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except OSError:
            pass

    @staticmethod
    def _time_diff(ts1, ts2):
        try:
            t1 = datetime.fromisoformat(ts1.replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(ts2.replace("Z", "+00:00"))
            return abs((t2 - t1).total_seconds())
        except (ValueError, AttributeError):
            return 999999


detector = AnomalyDetector()


def publish_event(event, persist_alerts):
    """Add a normalized event, evaluate alerts, and fan out to SSE clients."""
    if event["id"] in monitor.seen_event_ids:
        return
    monitor.seen_event_ids.add(event["id"])
    events.append(event)
    new_alerts = detector.check(event)
    alerts.extend(new_alerts)

    if persist_alerts:
        for alert in new_alerts:
            try:
                with ALERTS_LOG.open("a", encoding="utf-8") as af:
                    af.write(json.dumps(alert) + "\n")
            except OSError:
                pass

    sse_data = json.dumps({"event": event, "alerts": new_alerts})
    dead = []
    for i, q in enumerate(sse_clients):
        try:
            q.put_nowait(sse_data)
        except queue.Full:
            dead.append(i)
    for i in reversed(dead):
        sse_clients.pop(i)


def tail_session_logs():
    """Continuously scan Codex session logs for new lines."""
    while not SESSIONS_ROOT.exists():
        time.sleep(POLL_INTERVAL)

    with lock:
        for event in monitor.load_existing_events():
            publish_event(event, persist_alerts=False)

    while True:
        new_events = monitor.poll()
        if new_events:
            with lock:
                for event in new_events:
                    publish_event(event, persist_alerts=True)
        time.sleep(POLL_INTERVAL)


def compute_stats():
    """Compute aggregated statistics from normalized watcher events."""
    with lock:
        total = len(events)
        sessions = set()
        tool_counts = defaultdict(int)
        blocked_count = 0
        hourly = defaultdict(int)
        agents = {}
        last_ts = ""

        for e in events:
            sid = e.get("session_id", "")
            if sid and sid != "no-session":
                sessions.add(sid)
            if e.get("event") == "tool_use":
                tool_counts[e.get("tool", "unknown")] += 1
            if e.get("event") == "tool_blocked":
                blocked_count += 1
            if e.get("event") == "session_start":
                agents["main"] = {
                    "agent_id": "main",
                    "agent_type": e.get("agent_type", "codex"),
                    "session_id": sid,
                    "timestamp": e.get("timestamp", ""),
                    "tool_count": 0
                }
            ts = e.get("timestamp", "")
            if ts:
                last_ts = ts
                try:
                    hour = ts[:13]
                    hourly[hour] += 1
                except (IndexError, TypeError):
                    pass

        alert_count = len(alerts)

    return {
        "total_events": total,
        "session_count": len(sessions),
        "active_alerts": alert_count,
        "last_event": last_ts,
        "tool_counts": dict(tool_counts),
        "blocked_count": blocked_count,
        "hourly_activity": dict(sorted(hourly.items())),
        "agents": list(agents.values())
    }


class WatcherHandler(http.server.BaseHTTPRequestHandler):
    """Handles all HTTP requests for the watcher dashboard."""

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self._serve_dashboard()
        elif path == "/api/events":
            self._serve_events(params)
        elif path == "/api/stats":
            self._serve_stats()
        elif path == "/api/alerts":
            self._serve_alerts(params)
        elif path == "/api/stream":
            self._serve_sse()
        elif path == "/api/health":
            self._json_response({"status": "ok", "uptime": time.time()})
        else:
            self.send_error(404)

    def _serve_dashboard(self):
        try:
            content = DASHBOARD_PATH.read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self._security_headers()
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(500, "dashboard.html not found")

    def _serve_events(self, params):
        offset = int(params.get("offset", ["0"])[0])
        limit = int(params.get("limit", ["100"])[0])
        limit = min(limit, 500)
        with lock:
            page = events[offset:offset + limit]
            total = len(events)
        self._json_response({
            "events": page,
            "total": total,
            "offset": offset,
            "limit": limit
        })

    def _serve_stats(self):
        self._json_response(compute_stats())

    def _serve_alerts(self, params):
        severity = params.get("severity", [None])[0]
        with lock:
            if severity:
                filtered = [a for a in alerts if a["severity"] == severity]
            else:
                filtered = list(alerts)
        self._json_response({"alerts": filtered[-100:], "total": len(filtered)})

    def _serve_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self._security_headers()
        self.end_headers()

        q = queue.Queue(maxsize=200)
        with lock:
            sse_clients.append(q)

        try:
            self.wfile.write(b"event: connected\ndata: {\"status\":\"connected\"}\n\n")
            self.wfile.flush()

            while True:
                try:
                    data = q.get(timeout=15)
                    self.wfile.write(f"event: audit\ndata: {data}\n\n".encode())
                    self.wfile.flush()
                except queue.Empty:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            with lock:
                try:
                    sse_clients.remove(q)
                except ValueError:
                    pass

    def _json_response(self, data):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-cache")
        self._security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _security_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")


class ThreadedHTTPServer(http.server.HTTPServer):
    """Handle each request in a separate thread for SSE support."""

    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        pass


def main():
    tailer = threading.Thread(target=tail_session_logs, daemon=True)
    tailer.start()

    time.sleep(0.3)

    server = ThreadedHTTPServer((HOST, PORT), WatcherHandler)
    print(f"Zero Trust Watcher running at http://{HOST}:{PORT}")
    print(f"Monitoring: {SESSIONS_ROOT}")
    with lock:
        print(f"Loaded {len(events)} existing events, {len(alerts)} alerts")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down watcher...")
        server.shutdown()


if __name__ == "__main__":
    main()
