#!/usr/bin/env bash
# Stop the Zero Trust Watcher dashboard
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/watcher.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "Watcher is not running (no PID file)"
  exit 0
fi

PID=$(cat "$PID_FILE")
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "Watcher stopped (PID $PID)"
else
  echo "Watcher was not running (stale PID $PID)"
fi

rm -f "$PID_FILE"
