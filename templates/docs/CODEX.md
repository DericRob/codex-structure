# CODEX.md

This file provides workspace guidance for Codex and other coding agents when working from this Documents directory.

Launch Codex through `~/.codex/launcher/start-codex.ps1` on Windows or `~/.codex/launcher/start-codex.sh` on macOS/Linux so this file is injected into every new session prompt.

## Directory Overview

This is a personal Documents folder containing multiple independent projects, business files, and media. It is not a single repository. Navigate to the relevant project directory before doing work.

## Active Software Projects

Each active project should keep its own local notes, memory, or agent guidance. Read those before making changes.

Each active project should also keep a repo-local `WORKLOG.md` that records:

- what changed
- next tasks
- mistakes made
- root cause
- fixes applied
- verification status

Update that file during work, not only at the end.

Document your own project list here if you want a machine-local workspace index, but do not commit private project names, paths, or internal descriptions to a public template repo.

## Cross-Project Notes

- Never run two polling instances of the same bot/integration at once.
- Each project manages its own secrets in ignored config files.
- Treat security review as part of implementation, not a follow-up task.
