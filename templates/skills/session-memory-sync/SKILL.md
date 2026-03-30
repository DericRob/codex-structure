---
name: session-memory-sync
description: Automatically capture context at session end and restore at session start. Makes every conversation smarter by preserving decisions, blockers, and work-in-progress across sessions.
tools: []
requires:
  env: []
---

# Session Memory Sync

Automatic context persistence across agent sessions via lifecycle hooks.

## When to Use

- At the START of every session (restore context)
- At the END of every session (save context)
- When a session is about to be compacted (preserve key context)

## Session Start Protocol

On session start, load and present:

1. **Active Plan** — Check for `memory/ACTIVE_PLAN.md` or equivalent. If exists, summarize current phase and next steps.
2. **Recent Findings** — Check for `memory/FINDINGS.md`. Surface any blockers or discoveries from last session.
3. **Pending Follow-ups** — Check task system for items due today or overdue.
4. **User Context** — Load user profile/preferences from memory store.

Present as a brief status (3-5 lines max):
```
Resuming context: [project/feature name]
- Last session: [what was accomplished]
- Next up: [immediate next step]
- Blockers: [any, or "none"]
- Due today: [count] items
```

## Session End Protocol

Before session ends, capture:

1. **Decisions Made** — Any architectural, design, or business decisions
2. **Work Completed** — Files changed, features added, bugs fixed
3. **Blockers Discovered** — Issues that couldn't be resolved this session
4. **Next Steps** — What should happen next session
5. **Lessons Learned** — Gotchas, workarounds, or patterns discovered

Save to persistent memory store (file-based or database).

## Pre-Compact Protocol

When context window is about to be compressed:

1. Extract all TODO items and their status
2. Save current file edit locations
3. Preserve any error messages being debugged
4. Note the current phase of any active plan

## Memory Format

```yaml
session_id: "YYYY-MM-DD-HHMMSS"
project: "project-name"
decisions:
  - "Chose X over Y because Z"
completed:
  - "Implemented feature A"
  - "Fixed bug in B"
blockers:
  - "Waiting on API key for service C"
next_steps:
  - "Write tests for feature A"
  - "Deploy to staging"
findings:
  - "Library X has a bug with Y — use workaround Z"
```

## Integration

- **Claude Code**: Implement via `SessionStart` and `PreCompact` hooks in `settings.json`
- **Rafi Assistant**: Implement via heartbeat system + memory service
- **Codex**: Implement via `~/Documents/CODEX.md` plus launcher/bootstrap instructions that restore session context at startup
- **Antigravity**: Implement via `.agent/rules/` session rules
