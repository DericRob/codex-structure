# WORKLOG.md

## Current Status

- Project state: active
- Current objective: maintain AIOS as a reproducible Codex bootstrap repo while documenting the `AIOSx` direction
- Current branch: main
- Last verified result: watcher launcher fixed on Windows and validated on an isolated port; `AIOSx` comparison and slides updated

## What Changed

- Date: 2026-03-20
- Files changed: watcher scripts, watcher server, docs, slide deck, handoff notes, `AIOSx` plan, worklog template wiring
- Behavior changed: Windows watcher startup now returns promptly and can be tested on an isolated port; repo now includes a standard worklog pattern
- Why the change was made: reduce ambiguity, preserve execution context, and avoid losing lessons between sessions

## To Do

- [ ] Keep this worklog updated as changes are made
- [ ] Decide whether to commit the `AIOSx` plan and slide updates after the latest revisions
- [ ] If `AIOSx` moves forward, scaffold it as a separate repo instead of extending this repo indefinitely

## Mistakes And Fixes

### Mistake

- Watcher testing was allowed to become open-ended and mixed repo-local validation with an already-running global watcher.
- A PowerShell check attempted to assign to the reserved `$PID` variable.

### Root Cause

- The initial test path did not isolate the repo-local watcher from the live installed watcher.
- The launcher design on Windows used a process pattern that did not detach cleanly.
- Test commands were written too quickly in one case and hit a reserved shell variable.

### Fix

- Added a Windows launcher path that uses `pythonw.exe` when available.
- Added host/port overrides so repo-local watcher validation can use an isolated port.
- Added handoff notes and this worklog pattern to preserve execution context.

### Prevention

- Use bounded tests with explicit health, PID, and cleanup checks.
- Prefer isolated ports when a live local service may already exist.
- Record mistakes and fixes in `WORKLOG.md` as they happen.

## Verification

- Commands run: watcher start, health check, stop, pid cleanup check, `python -m py_compile`
- Manual checks: reviewed transcript-based comparison and reordered slides to match the direct comparison logic
- Remaining risks: slide deck and `AIOSx` materials may need another pass if they are repurposed for leadership or an external audience

## Notes For The Next Session

- Important context to load first: `WORKLOG.md`, `WATCHER-HANDOFF.md`, `AIOSx-PLAN.md`
- Active decisions and constraints: keep this repo focused on Codex bootstrap and observability; treat `AIOSx` as a separate future repo
- Open questions: whether to scaffold `AIOSx` locally next and whether to expand the slides into a fuller briefing
