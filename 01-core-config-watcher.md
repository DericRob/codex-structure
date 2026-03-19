# Prompt 01 — Codex Core Config + Watcher

Use this prompt to recreate the Codex-native core setup on a new machine.

## Create these paths

```text
~/.codex/
├── alerts.jsonl                 # optional; watcher writes this as alerts occur
├── launcher/
│   ├── start-codex.ps1
│   └── start-codex.sh
├── watcher/
│   ├── append_event.py
│   ├── dashboard.html
│   ├── server.py
│   ├── start.sh
│   └── stop.sh
└── skills/                      # design skill installed in Prompt 03

~/Documents/
├── CODEX.md
└── .mcp.json
```

## Source templates to copy

Copy these repo files to the matching destination paths:

| Repo file | Destination |
|---|---|
| `templates/watcher/server.py` | `~/.codex/watcher/server.py` |
| `templates/watcher/dashboard.html` | `~/.codex/watcher/dashboard.html` |
| `templates/watcher/start.sh` | `~/.codex/watcher/start.sh` |
| `templates/watcher/stop.sh` | `~/.codex/watcher/stop.sh` |
| `templates/launcher/start-codex.ps1` | `~/.codex/launcher/start-codex.ps1` |
| `templates/launcher/start-codex.sh` | `~/.codex/launcher/start-codex.sh` |
| `templates/docs/CODEX.md` | `~/Documents/CODEX.md` |
| `templates/config/mcp.json` | `~/Documents/.mcp.json` |
| `templates/watcher/append_event.py` | `~/.codex/watcher/append_event.py` |

## Notes

- This setup intentionally does **not** rely on Claude hook events or plugin marketplaces.
- The watcher is a local-only Python HTTP server that reads Codex session logs from `~/.codex/sessions/**/*.jsonl`.
- `append_event.py` is only for legacy/manual testing and is not part of the live data path.
- Start Codex through `~/.codex/launcher/start-codex.ps1` on Windows or `~/.codex/launcher/start-codex.sh` on macOS/Linux. The wrapper reads `~/Documents/CODEX.md` and injects it into the initial session prompt so the file is loaded every time.

## Post-copy commands

```bash
mkdir -p ~/.codex/launcher
mkdir -p ~/.codex/watcher
chmod +x ~/.codex/launcher/start-codex.sh
chmod +x ~/.codex/watcher/*.sh ~/.codex/watcher/server.py ~/.codex/watcher/append_event.py
~/.codex/watcher/start.sh
```
