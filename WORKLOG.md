# WORKLOG.md

## Current Status

- Project state: active
- Current objective: maintain AIOS as a reproducible Codex bootstrap repo while documenting the `AIOSx` direction
- Current branch: main
- Last verified result: watcher server now handles requests concurrently; launcher scripts honor isolated host/port settings and refuse to kill unrelated PID-reuse processes

## What Changed

- Date: 2026-03-20
- Files changed: watcher scripts, watcher server, docs, slide deck, handoff notes, `AIOSx` plan, worklog template wiring, `AIOSx` README draft, stakeholder architecture brief
- Behavior changed: Windows watcher startup now returns promptly and can be tested on an isolated port; repo now includes a standard worklog pattern and initial `AIOSx` positioning documents
- Why the change was made: reduce ambiguity, preserve execution context, and avoid losing lessons between sessions
- Date: 2026-03-30
- Files changed: `AIOS-DEMO-PRESENTATION-V2.html`, presentation notes, and presentation assets
- Behavior changed: the main demo deck now frames use cases as AIOS-only business scenarios instead of AIOSx-style runtime examples
- Why the change was made: align the presentation with the actual scope of `AIOS` before syncing the repo to GitHub
- Date: 2026-03-30
- Files changed: watcher launchers, watcher server, README/setup docs, `WORKLOG.md`, `WATCHER-HANDOFF.md`
- Behavior changed: the watcher server is now actually threaded, Unix launcher health checks follow configured host/port, and start/stop scripts validate watcher identity before killing a PID
- Why the change was made: fix false-positive startup messages, reduce PID-reuse risk, and keep the repo docs aligned with the current watcher behavior

## To Do

- [ ] Keep this worklog updated as changes are made
- [ ] Validate the PowerShell watcher launchers on a real Windows host
- [ ] Review whether the presentation and `AIOSx` drafts should remain in this repo long-term or move to a separate repo
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
- Hardened watcher PID handling so start/stop scripts only manage processes whose command lines match the watcher server.
- Fixed the server class so SSE clients do not block all other requests behind a single HTTP connection.
- Added handoff notes and this worklog pattern to preserve execution context.

### Prevention

- Use bounded tests with explicit health, PID, and cleanup checks.
- Prefer isolated ports when a live local service may already exist.
- Record mistakes and fixes in `WORKLOG.md` as they happen.

## Verification

- Commands run: `python3 -m py_compile`, watcher launcher smoke tests with isolated host/port settings, HTML/local-link validation
- Manual checks: reviewed transcript-based comparison, reordered slides to match the direct comparison logic, created repo-facing plus leadership-facing `AIOSx` documents, and refreshed watcher docs/worklog notes
- Remaining risks: PowerShell launcher behavior still needs live validation on a Windows machine; `AIOSx` materials may still need a naming, scope, and audience pass before external use

## Notes For The Next Session

- Important context to load first: `WORKLOG.md`, `WATCHER-HANDOFF.md`, `AIOSx-PLAN.md`, `AIOSx-README-DRAFT.md`, `AIOSx-ARCHITECTURE-BRIEF.md`
- Active decisions and constraints: keep this repo focused on Codex bootstrap and observability; treat `AIOSx` as a separate future repo
- Open questions: whether to scaffold `AIOSx` locally next, whether to convert the draft README into a true repo root README, and whether to expand the brief into leadership slides
