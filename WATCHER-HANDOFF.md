# Watcher Handoff

## Current Work

- Added Windows watcher launchers at `templates/watcher/start.ps1` and `templates/watcher/stop.ps1`.
- Updated `01-core-config-watcher.md` and `README.md` to document Windows and Unix watcher startup.
- Updated `templates/watcher/server.py` to bound startup history loading, cap in-memory event growth, and serve requests concurrently.
- Fixed the Windows launcher so it detaches cleanly and returns promptly by launching `pythonw.exe` when available.
- Added watcher host/port overrides in `server.py` and both launcher paths so repo-local validation can run on an isolated port.
- Hardened PID handling so watcher start/stop scripts only manage processes whose command lines match the watcher server.

## Current Risk

- A separate global watcher in `~/.codex/watcher` may already be serving on port `9999`.
- Validation should use an isolated port when testing the repo template scripts so results are not confused with the live watcher.
- PowerShell launchers are documented and hardened, but they still need confirmation on a real Windows host.

## Execution Plan

1. Validate `templates/watcher/start.ps1` and `templates/watcher/stop.ps1` on a real Windows machine using an isolated port.
2. Confirm the PID-file metadata behaves correctly across stop/start/restart cycles.
3. Keep repo-local validation isolated from any already-installed global watcher.
4. If Windows validation exposes launcher-specific issues, test `templates/watcher/server.py` directly to separate launcher problems from server problems.
