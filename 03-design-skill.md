# Prompt 03 — Codex Design Skill

Install the global `design` skill under Codex skills.

## Destination

```text
~/.codex/skills/design/
├── SKILL.md
└── data/
```

## Source template

Copy:

| Repo file | Destination |
|---|---|
| `templates/skills/design/SKILL.md` | `~/.codex/skills/design/SKILL.md` |

Then create the `data/` directory. Prompt 04 covers the CSV transfer.

## Notes

- This is a Codex skill, not a Claude slash command.
- Invoke it using Codex skill selection or whenever the task clearly matches design guidance work.
- The skill expects the CSV data files to live under `~/.codex/skills/design/data/`.
