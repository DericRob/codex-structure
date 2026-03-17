#!/usr/bin/env python3
"""Zero Trust Watcher — Real-time audit dashboard server.

Monitors ~/.codex/audit.jsonl and serves a live dashboard at localhost:9999.
Python 3 stdlib only — no external dependencies.
"""

import http.server
import json
import os
import pathlib
import queue
import subprocess
import threading
import time
import urllib.parse
from collections import defaultdict
from datetime import datetime, timezone

# --- Configuration ---
PORT = 9999
HOST = "127.0.0.1"
AUDIT_LOG = pathlib.Path.home() / ".codex" / "audit.jsonl"
ALERTS_LOG = pathlib.Path.home() / ".codex" / "alerts.jsonl"
DASHBOARD_PATH = pathlib.Path(__file__).parent / "dashboard.html"

# --- In-memory state ---
events = []  # All parsed audit events
alerts = []  # Anomaly detections
sse_clients = []  # Queue per SSE client
lock = threading.Lock()


# --- Anomaly Detection Engine ---
class AnomalyDetector:
    """Evaluates each new event against security rules."""

    def __init__(self):
        self._session_tools = defaultdict(list)  # session_id -> [(timestamp, tool)]
        self._session_env_reads = defaultdict(int)  # session_id -> count of .env reads
        self._no_session_alerted = False  # Only alert once for no-session

    def check(self, event):
        """Run all rules against a new event. Returns list of alert dicts."""
        new_alerts = []
        ts = event.get("timestamp", "")
        sid = event.get("session_id", "unknown")
        tool = event.get("tool", "")
        detail = event.get("detail", "")
        evt_type = event.get("event", "")

        # Track tool calls per session
        if evt_type == "tool_use":
            self._session_tools[sid].append((ts, tool))

        # Rule: Unknown session (fire once, not per-event)
        if sid == "no-session" and evt_type == "tool_use" and not self._no_session_alerted:
            self._no_session_alerted = True
            new_alerts.append(self._alert(
                "info", "No session context",
                "Session metadata unavailable in the audit stream", ts
            ))

        # Rule: Blocked events are always alerts
        if evt_type == "tool_blocked":
            decision = event.get("decision", "")
            reason = event.get("reason", "")
            severity = "critical" if decision == "deny" else "warning"
            # Elevate secret-related blocks
            if "secret" in reason.lower() or "credential" in reason.lower():
                severity = "critical"
            new_alerts.append(self._alert(
                severity, f"Tool gate: {decision}",
                f"{tool} — {reason}", ts
            ))

        # Rule: Secret access (>3 .env reads in one session)
        if evt_type == "tool_use" and tool == "Read" and ".env" in detail:
            self._session_env_reads[sid] += 1
            if self._session_env_reads[sid] == 4:
                new_alerts.append(self._alert(
                    "high", "Excessive .env access",
                    f"Session {sid[:12]}... read .env files {self._session_env_reads[sid]} times",
                    ts
                ))

        # Rule: Burst (>20 tool calls in 60 seconds)
        if evt_type == "tool_use":
            recent = [t for t, _ in self._session_tools[sid]
                      if self._time_diff(t, ts) < 60]
            if len(recent) > 20:
                # Only fire once per burst
                if len(recent) == 21:
                    new_alerts.append(self._alert(
                        "warning", "Tool call burst",
                        f"Session {sid[:12]}... made {len(recent)} calls in 60s", ts
                    ))

        # Rule: Bash heavy (>70% of calls are Bash, min 10 calls)
        if evt_type == "tool_use":
            tools_list = [t for _, t in self._session_tools[sid]]
            if len(tools_list) >= 10:
                bash_pct = tools_list.count("Bash") / len(tools_list)
                if bash_pct > 0.7 and len(tools_list) % 10 == 0:
                    new_alerts.append(self._alert(
                        "warning", "Bash-heavy session",
                        f"Session {sid[:12]}... — {bash_pct:.0%} Bash ({len(tools_list)} total calls)",
                        ts
                    ))

        # Rule: Rapid file writes (>10 Write/Edit in 30 seconds)
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
        """Send macOS desktop notification for critical/high alerts."""
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

    def _time_diff(self, ts1, ts2):
        """Approximate time diff in seconds between two ISO timestamps."""
        try:
            t1 = datetime.fromisoformat(ts1.replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(ts2.replace("Z", "+00:00"))
            return abs((t2 - t1).total_seconds())
        except (ValueError, AttributeError):
            return 999999


detector = AnomalyDetector()


# --- Audit Log Tailer ---
def tail_audit_log():
    """Continuously tail the audit log file, parsing new lines."""
    # Wait for file to exist
    while not AUDIT_LOG.exists():
        time.sleep(1)

    with open(AUDIT_LOG, "r") as f:
        # Read existing content first
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                with lock:
                    events.append(event)
                    new_alerts = detector.check(event)
                    alerts.extend(new_alerts)
            except json.JSONDecodeError:
                continue

        # Now tail for new lines
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                with lock:
                    events.append(event)
                    new_alerts = detector.check(event)
                    alerts.extend(new_alerts)
                    # Persist alerts
                    for alert in new_alerts:
                        try:
                            with open(ALERTS_LOG, "a") as af:
                                af.write(json.dumps(alert) + "\n")
                        except OSError:
                            pass
                    # Push to SSE clients
                    sse_data = json.dumps({
                        "event": event,
                        "alerts": new_alerts
                    })
                    dead = []
                    for i, q in enumerate(sse_clients):
                        try:
                            q.put_nowait(sse_data)
                        except queue.Full:
                            dead.append(i)
                    for i in reversed(dead):
                        sse_clients.pop(i)
            except json.JSONDecodeError:
                continue


# --- Stats Computation ---
def compute_stats():
    """Compute aggregated statistics from events."""
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
            if e.get("event") == "agent_start":
                aid = e.get("agent_id", "unknown")
                agents[aid] = {
                    "agent_id": aid,
                    "agent_type": e.get("agent_type", "unknown"),
                    "session_id": e.get("session_id", ""),
                    "timestamp": e.get("timestamp", ""),
                    "tool_count": 0
                }
            ts = e.get("timestamp", "")
            if ts:
                last_ts = ts
                try:
                    hour = ts[:13]  # YYYY-MM-DDTHH
                    hourly[hour] += 1
                except (IndexError, TypeError):
                    pass

        # Count tools per agent (approximate — agents use the same session)
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


# --- HTTP Handler ---
class WatcherHandler(http.server.BaseHTTPRequestHandler):
    """Handles all HTTP requests for the watcher dashboard."""

    def log_message(self, format, *args):
        """Suppress default access logging."""
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
        limit = min(limit, 500)  # Cap at 500
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
            # Send initial connected event
            self.wfile.write(b"event: connected\ndata: {\"status\":\"connected\"}\n\n")
            self.wfile.flush()

            while True:
                try:
                    data = q.get(timeout=15)
                    self.wfile.write(f"event: audit\ndata: {data}\n\n".encode())
                    self.wfile.flush()
                except queue.Empty:
                    # Send keepalive
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


# --- Threaded Server ---
class ThreadedHTTPServer(http.server.HTTPServer):
    """Handle each request in a separate thread for SSE support."""
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        """Suppress broken pipe errors from SSE disconnects."""
        pass


def main():
    # Start audit log tailer in background
    tailer = threading.Thread(target=tail_audit_log, daemon=True)
    tailer.start()

    # Give the tailer a moment to load existing events
    time.sleep(0.3)

    server = ThreadedHTTPServer((HOST, PORT), WatcherHandler)
    print(f"Zero Trust Watcher running at http://{HOST}:{PORT}")
    print(f"Monitoring: {AUDIT_LOG}")
    with lock:
        print(f"Loaded {len(events)} existing events, {len(alerts)} alerts")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down watcher...")
        server.shutdown()


if __name__ == "__main__":
    main()
