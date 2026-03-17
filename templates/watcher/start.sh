#!/usr/bin/env bash
# Start the Zero Trust Watcher dashboard
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/watcher.pid"
LOG_FILE="$SCRIPT_DIR/watcher.log"

# Check if already running
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    echo "Watcher already running (PID $PID)"
    echo "Dashboard: http://127.0.0.1:9999"
    exit 0
  else
    rm -f "$PID_FILE"
  fi
fi

# Start server in background
echo "Starting Zero Trust Watcher..."
/usr/bin/python3 "$SCRIPT_DIR/server.py" > "$LOG_FILE" 2>&1 &
WATCHER_PID=$!
echo "$WATCHER_PID" > "$PID_FILE"

# Wait for server to be ready
for i in $(seq 1 10); do
  if curl -s http://127.0.0.1:9999/api/health > /dev/null 2>&1; then
    break
  fi
  sleep 0.3
done

echo "Watcher running (PID $WATCHER_PID)"
echo "Dashboard: http://127.0.0.1:9999"

# Open browser
if command -v open &>/dev/null; then
  open "http://127.0.0.1:9999"
elif command -v xdg-open &>/dev/null; then
  xdg-open "http://127.0.0.1:9999"
fi
