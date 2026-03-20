# Watcher Handoff

## Current Work

- Added Windows watcher launchers at `templates/watcher/start.ps1` and `templates/watcher/stop.ps1`.
- Updated `01-core-config-watcher.md` and `README.md` to document Windows and Unix watcher startup.
- Updated `templates/watcher/server.py` to bound startup history loading and cap in-memory event growth.
- Fixed the Windows launcher so it detaches cleanly and returns promptly by launching `pythonw.exe` when available.
- Added watcher host/port overrides in `server.py` so repo-local validation can run on an isolated port.

## Current Risk

- Prior watcher tests left repo-local runtime artifacts (`watcher.pid`, `watcher.out.log`, `watcher.err.log`).
- A separate global watcher in `~/.codex/watcher` may already be serving on port `9999`.
- Validation should use an isolated port when testing the repo template scripts so results are not confused with the live watcher.

## Execution Plan

1. Clean stale watcher runtime artifacts from the repo template directory.
2. Run a bounded launcher test through `templates/watcher/start.ps1`.
3. Verify `/api/health`, the bound port, and PID state.
4. Stop the watcher cleanly and confirm cleanup.
5. If launcher validation fails, run `templates/watcher/server.py` directly to isolate launcher vs server behavior.
6. Prefer an isolated port for repo-local validation when a live global watcher exists.
7. Fix the identified issue, re-run validation, then commit the final changes.
