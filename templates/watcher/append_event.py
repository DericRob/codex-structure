#!/usr/bin/env python3
"""Append synthetic events to a manual Codex session log for watcher testing."""
import json
import pathlib
import sys
from datetime import datetime, timezone

SESSIONS_DIR = pathlib.Path.home() / ".codex" / "sessions" / "manual"
SESSION_LOG = SESSIONS_DIR / "manual-test.jsonl"
SESSION_ID = "manual-test"

DISPLAY_TO_RAW_TOOL = {
    "Bash": "shell_command",
    "Edit": "apply_patch",
    "AskUserQuestion": "request_user_input",
    "TaskCreate": "spawn_agent",
    "TaskUpdate": "send_input",
    "Task": "wait_agent",
}


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def encode_arguments(raw_tool, detail):
    if raw_tool == "shell_command":
        return {"command": detail}
    if raw_tool == "apply_patch":
        return {"patch_summary": detail}
    if raw_tool in {"spawn_agent", "send_input"}:
        return {"message": detail}
    if raw_tool == "wait_agent":
        return {"ids": [detail] if detail else []}
    return {"detail": detail}


def ensure_session_meta():
    if SESSION_LOG.exists() and SESSION_LOG.stat().st_size > 0:
        return
    session_meta = {
        "timestamp": now_iso(),
        "type": "session_meta",
        "payload": {
            "id": SESSION_ID,
            "timestamp": now_iso(),
            "cwd": str(pathlib.Path.cwd()),
            "source": "manual-test",
            "originator": "append_event.py",
        },
    }
    with SESSION_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(session_meta) + "\n")


SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
tool = "Bash"
detail = "echo hello world"

if len(sys.argv) > 1:
    tool = sys.argv[1]
if len(sys.argv) > 2:
    detail = " ".join(sys.argv[2:])

raw_tool = DISPLAY_TO_RAW_TOOL.get(tool, tool)
payload = {
    "timestamp": now_iso(),
    "type": "response_item",
    "payload": {
        "type": "function_call",
        "name": raw_tool,
        "arguments": json.dumps(encode_arguments(raw_tool, detail)),
        "call_id": f"manual-{int(datetime.now(timezone.utc).timestamp() * 1000)}",
    },
}

ensure_session_meta()

with SESSION_LOG.open("a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\n")
print(f"Appended synthetic event to {SESSION_LOG}")
