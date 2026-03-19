#!/usr/bin/env python3
"""Append a single event to ~/.codex/audit.jsonl for legacy local watcher testing."""
import json
import pathlib
import sys
from datetime import datetime, timezone

out = pathlib.Path.home() / '.codex' / 'audit.jsonl'
out.parent.mkdir(parents=True, exist_ok=True)

payload = {
    'event': 'tool_use',
    'tool': 'Bash',
    'detail': 'echo hello world',
    'session_id': 'sess-demo-001',
    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'cwd': str(pathlib.Path.cwd()),
}

if len(sys.argv) > 1:
    payload['tool'] = sys.argv[1]
if len(sys.argv) > 2:
    payload['detail'] = ' '.join(sys.argv[2:])

with out.open('a', encoding='utf-8') as f:
    f.write(json.dumps(payload) + '\n')
print(f'Appended event to {out}')
