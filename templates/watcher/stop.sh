#!/usr/bin/env bash
# Stop the Zero Trust Watcher dashboard
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/watcher.pid"
SERVER_PATH="$SCRIPT_DIR/server.py"

read_pid_metadata() {
  local pid="" host="" port="" server=""
  if [ ! -f "$PID_FILE" ]; then
    printf '%s\n%s\n%s\n%s\n' "$pid" "$host" "$port" "$server"
    return
  fi

  if grep -q '=' "$PID_FILE"; then
    pid="$(sed -n 's/^PID=//p' "$PID_FILE" | head -n1 | tr -d '[:space:]')"
    host="$(sed -n 's/^HOST=//p' "$PID_FILE" | head -n1 | tr -d '[:space:]')"
    port="$(sed -n 's/^PORT=//p' "$PID_FILE" | head -n1 | tr -d '[:space:]')"
    server="$(sed -n 's/^SERVER=//p' "$PID_FILE" | head -n1)"
  else
    pid="$(head -n1 "$PID_FILE" | tr -d '[:space:]')"
  fi

  printf '%s\n%s\n%s\n%s\n' "$pid" "$host" "$port" "$server"
}

process_command() {
  local pid="$1"
  ps -p "$pid" -o command= 2>/dev/null || true
}

is_watcher_process() {
  local pid="$1"
  local expected_server="$2"
  local expected_port="${3:-}"
  local cmd

  [ -n "$pid" ] || return 1
  cmd="$(process_command "$pid")"
  [ -n "$cmd" ] || return 1

  case "$cmd" in
    *"$expected_server"*) ;;
    *) return 1 ;;
  esac

  if [ -n "$expected_port" ]; then
    case "$cmd" in
      *"--port $expected_port"*) ;;
      *) return 1 ;;
    esac
  fi

  return 0
}

if [ ! -f "$PID_FILE" ]; then
  echo "Watcher is not running (no PID file)"
  exit 0
fi

PID_META_RAW="$(read_pid_metadata)"
PID="$(printf '%s\n' "$PID_META_RAW" | sed -n '1p')"
PORT="$(printf '%s\n' "$PID_META_RAW" | sed -n '3p')"
SERVER="$(printf '%s\n' "$PID_META_RAW" | sed -n '4p')"
SERVER="${SERVER:-$SERVER_PATH}"

if is_watcher_process "$PID" "$SERVER" "$PORT"; then
  kill "$PID"
  echo "Watcher stopped (PID $PID)"
elif [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
  echo "Watcher PID file points to a different process; refusing to stop PID $PID"
else
  echo "Watcher was not running (stale PID $PID)"
fi

rm -f "$PID_FILE"
