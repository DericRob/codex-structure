# Prompt 03 — Codex Skills Overview + Design Skill

Use this prompt as the entry point for the repo's portable Codex skills.

It installs the global `design` skill directly and points to the follow-on skill packs for workflow, engineering, and productivity.

## Destination

```text
~/.codex/skills/
├── design/
│   ├── SKILL.md
│   └── data/
├── sparc-workflow/
├── model-router/
├── consensus-review/
├── session-memory-sync/
├── security-audit/
├── quality-gate/
├── pair-programming/
├── skill-builder/
├── inbox-triage/
├── smart-scheduling/
├── follow-up-tracker/
└── delegation-tracker/
```

## Skill packs in this repo

| Prompt file | Skills covered | What they are used for |
|---|---|---|
| `03-design-skill.md` | `design` | Industry-specific UI/UX guidance backed by local CSV data |
| `05-aios-workflow-skills.md` | `sparc-workflow`, `model-router`, `consensus-review`, `session-memory-sync` | Complex-task planning, model routing, multi-pass review, and session continuity |
| `06-engineering-quality-skills.md` | `security-audit`, `quality-gate`, `pair-programming`, `skill-builder` | Security review, release readiness, coding collaboration, and skill authoring |
| `07-productivity-skills.md` | `inbox-triage`, `smart-scheduling`, `follow-up-tracker`, `delegation-tracker` | Executive-assistant style email, scheduling, follow-up, and delegation workflows |

Each of the follow-on prompt files includes per-skill descriptions so the installer can see not just what to copy, but when each skill should be used.

## Design skill source template

Copy:

| Repo file | Destination |
|---|---|
| `templates/skills/design/SKILL.md` | `~/.codex/skills/design/SKILL.md` |

Then create the `data/` directory. Prompt 04 covers the CSV transfer.

## Design skill usage

Use the `design` skill for:

- UI direction before building
- industry-specific palettes and component guidance
- typography and layout choices
- dashboard or product UX recommendations

## Notes

- This is a Codex skill, not a Claude slash command.
- Invoke it using Codex skill selection or whenever the task clearly matches design guidance work.
- The skill expects the CSV data files to live under `~/.codex/skills/design/data/`.
- Use Prompts 05, 06, and 07 to install the other portable skill packs in this repo.
