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
- Date: 2026-03-30
- Files changed: `templates/skills/`, `templates/agents/`, `templates/docs/AGENT-PLAYBOOKS.md`, `README.md`, `AIOSx-README-DRAFT.md`
- Behavior changed: the repo now includes portable engineering skills (`security-audit`, `quality-gate`, `pair-programming`, `skill-builder`) plus Codex-friendly agent playbooks for coordination, planning, research, implementation, review, testing, and production validation
- Why the change was made: incorporate the best reusable ideas from Ruflo without importing its Claude-specific swarm machinery or repo sprawl
- Date: 2026-03-30
- Files changed: `03-design-skill.md`, `05-aios-workflow-skills.md`, `06-engineering-quality-skills.md`, `07-productivity-skills.md`, `README.md`, `01-core-config-watcher.md`
- Behavior changed: the repo now has install docs for all portable skill packs, and the main skill prompt explains what each skill group is used for
- Why the change was made: make the setup docs match the expanded skill library and make skill purpose visible during installation
- Date: 2026-03-30
- Files changed: `03-design-skill.md`, `05-aios-workflow-skills.md`, `06-engineering-quality-skills.md`, `07-productivity-skills.md`
- Behavior changed: each skill-pack prompt now includes explicit per-skill descriptions instead of only a summary table
- Why the change was made: the first pass was too terse and made the intended use of each skill easy to miss

## To Do

- [ ] Keep this worklog updated as changes are made
- [ ] Validate the PowerShell watcher launchers on a real Windows host
- [ ] Review whether the presentation and `AIOSx` drafts should remain in this repo long-term or move to a separate repo
- [ ] Decide whether the new agent playbooks should stay as templates here or move into a future standalone `AIOSx` runtime repo
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

- Commands run: `python3 -m py_compile`, watcher launcher smoke tests with isolated host/port settings, HTML/local-link validation, skill-doc structure checks
- Manual checks: reviewed Ruflo skill and agent patterns, mapped them to Codex-native workflows, scaffolded new portable skills and agent playbooks, created install docs for each skill pack, and refreshed README/AIOSx draft docs
- Remaining risks: PowerShell launcher behavior still needs live validation on a Windows machine; the new agent playbooks are guidance templates and not yet wired into a runtime-specific orchestration layer

## Notes For The Next Session

- Important context to load first: `WORKLOG.md`, `README.md`, `03-design-skill.md`, `05-aios-workflow-skills.md`, `06-engineering-quality-skills.md`, `07-productivity-skills.md`
- Active decisions and constraints: keep this repo focused on Codex bootstrap and portable workflow patterns; treat `AIOSx` as a separate future repo if runtime/kernel work begins
- Open questions: whether to standardize frontmatter across all older skills next, whether to add repo-local validation/examples for the new playbooks, and whether to split `AIOSx` materials into their own repo
