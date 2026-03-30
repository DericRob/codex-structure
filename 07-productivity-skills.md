# Prompt 07 — Productivity Skills

Install the productivity-oriented Codex skills under `~/.codex/skills/`.

## Destination

```text
~/.codex/skills/
├── inbox-triage/
│   └── SKILL.md
├── smart-scheduling/
│   └── SKILL.md
├── follow-up-tracker/
│   └── SKILL.md
└── delegation-tracker/
    └── SKILL.md
```

## Source templates

Copy these repo files to the matching destination paths:

| Repo file | Destination | What the skill is used for |
|---|---|---|
| `templates/skills/inbox-triage/SKILL.md` | `~/.codex/skills/inbox-triage/SKILL.md` | Categorizing email by urgency, surfacing action items, and drafting replies |
| `templates/skills/smart-scheduling/SKILL.md` | `~/.codex/skills/smart-scheduling/SKILL.md` | Finding meeting slots, protecting focus time, and suggesting better scheduling options |
| `templates/skills/follow-up-tracker/SKILL.md` | `~/.codex/skills/follow-up-tracker/SKILL.md` | Tracking who owes what by when and surfacing overdue follow-ups |
| `templates/skills/delegation-tracker/SKILL.md` | `~/.codex/skills/delegation-tracker/SKILL.md` | Recording delegated work, due dates, and status updates across people |

## Notes

- These skills describe behavior and decision logic; actual email or calendar actions still require the right tools and permissions.
- `follow-up-tracker` and `delegation-tracker` work well with a recurring daily review workflow.

## Skill descriptions

### `inbox-triage`

Use this skill when reviewing email, identifying urgent items, or drafting replies. It helps separate urgent mail from informational mail and turns the inbox into an actionable queue instead of a raw message list.

### `smart-scheduling`

Use this skill when finding times for meetings, checking for conflicts, or improving a calendar plan. It is designed to protect focus time, reduce context switching, and suggest better scheduling alternatives.

### `follow-up-tracker`

Use this skill when you are waiting on someone else to respond or deliver something. It keeps a ledger of pending follow-ups, due dates, and overdue items so commitments do not disappear into email or meeting notes.

### `delegation-tracker`

Use this skill when assigning work to other people and needing accountability. It tracks the assignee, due date, status, and notes so delegated work remains visible until it is completed.
