#!/usr/bin/env bash
# Start the Zero Trust Watcher dashboard
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/watcher.pid"
LOG_FILE="$SCRIPT_DIR/watcher.log"
SERVER_PATH="$SCRIPT_DIR/server.py"
WATCHER_HOST="${WATCHER_HOST:-127.0.0.1}"
WATCHER_PORT="${WATCHER_PORT:-9999}"
WATCHER_URL="http://${WATCHER_HOST}:${WATCHER_PORT}"
BROWSER_HOST="$WATCHER_HOST"
if [ "$BROWSER_HOST" = "0.0.0.0" ]; then
  BROWSER_HOST="127.0.0.1"
fi
BROWSER_URL="http://${BROWSER_HOST}:${WATCHER_PORT}"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3 || command -v python || true)}"

if [ -z "$PYTHON_BIN" ]; then
  echo "Watcher start failed: python3 was not found on PATH" >&2
  exit 1
fi

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

write_pid_metadata() {
  local pid="$1"
  cat > "$PID_FILE" <<EOF
PID=$pid
HOST=$WATCHER_HOST
PORT=$WATCHER_PORT
SERVER=$SERVER_PATH
EOF
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

# Check if already running
if [ -f "$PID_FILE" ]; then
  PID_META_RAW="$(read_pid_metadata)"
  PID="$(printf '%s\n' "$PID_META_RAW" | sed -n '1p')"
  EXISTING_HOST="$(printf '%s\n' "$PID_META_RAW" | sed -n '2p')"
  EXISTING_PORT="$(printf '%s\n' "$PID_META_RAW" | sed -n '3p')"
  EXISTING_SERVER="$(printf '%s\n' "$PID_META_RAW" | sed -n '4p')"
  EXISTING_SERVER="${EXISTING_SERVER:-$SERVER_PATH}"
  EXISTING_PORT="${EXISTING_PORT:-$WATCHER_PORT}"

  if is_watcher_process "$PID" "$EXISTING_SERVER" "$EXISTING_PORT"; then
    if [ "$EXISTING_PORT" = "$WATCHER_PORT" ] && curl -fsS "$WATCHER_URL/api/health" > /dev/null 2>&1; then
      echo "Watcher already running (PID $PID)"
      echo "Dashboard: $BROWSER_URL"
      exit 0
    fi

    kill "$PID" 2>/dev/null || true
  fi

  rm -f "$PID_FILE"
fi

echo "Starting Zero Trust Watcher..."
"$PYTHON_BIN" "$SERVER_PATH" --host "$WATCHER_HOST" --port "$WATCHER_PORT" > "$LOG_FILE" 2>&1 &
WATCHER_PID=$!
write_pid_metadata "$WATCHER_PID"

READY=0
for i in $(seq 1 40); do
  if curl -fsS "$WATCHER_URL/api/health" > /dev/null 2>&1; then
    READY=1
    break
  fi
  if ! is_watcher_process "$WATCHER_PID" "$SERVER_PATH" "$WATCHER_PORT"; then
    break
  fi
  sleep 0.25
done

if [ "$READY" -ne 1 ]; then
  if is_watcher_process "$WATCHER_PID" "$SERVER_PATH" "$WATCHER_PORT"; then
    kill "$WATCHER_PID" 2>/dev/null || true
  fi
  rm -f "$PID_FILE"
  echo "Watcher failed to start or did not become healthy at $WATCHER_URL" >&2
  if [ -f "$LOG_FILE" ]; then
    tail -n 40 "$LOG_FILE" >&2 || true
  fi
  exit 1
fi

echo "Watcher running (PID $WATCHER_PID)"
echo "Dashboard: $BROWSER_URL"

# Open browser
if command -v open &>/dev/null; then
  open "$BROWSER_URL"
elif command -v xdg-open &>/dev/null; then
  xdg-open "$BROWSER_URL"
fi
