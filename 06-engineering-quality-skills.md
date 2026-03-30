# Prompt 06 — Engineering & Quality Skills

Install the engineering-focused Codex skills under `~/.codex/skills/`.

## Destination

```text
~/.codex/skills/
├── security-audit/
│   └── SKILL.md
├── quality-gate/
│   └── SKILL.md
├── pair-programming/
│   └── SKILL.md
└── skill-builder/
    └── SKILL.md
```

## Source templates

Copy these repo files to the matching destination paths:

| Repo file | Destination | What the skill is used for |
|---|---|---|
| `templates/skills/security-audit/SKILL.md` | `~/.codex/skills/security-audit/SKILL.md` | Reviewing auth, input handling, file operations, subprocesses, secrets, and exposed services for security risk |
| `templates/skills/quality-gate/SKILL.md` | `~/.codex/skills/quality-gate/SKILL.md` | Running an evidence-based ship / hold decision before commit, merge, or deploy |
| `templates/skills/pair-programming/SKILL.md` | `~/.codex/skills/pair-programming/SKILL.md` | Driver/navigator, TDD, debug, and refactor workflows for iterative coding sessions |
| `templates/skills/skill-builder/SKILL.md` | `~/.codex/skills/skill-builder/SKILL.md` | Creating or refining reusable AIOS skills with strong trigger metadata and lean structure |

## Notes

- Use `security-audit` and `quality-gate` together on high-risk changes.
- `pair-programming` is best for active implementation sessions; `quality-gate` is best after the diff exists.
- `skill-builder` is for maintaining the skill library itself.

## Skill descriptions

### `security-audit`

Use this skill for changes that touch untrusted input, authentication, authorization, secrets, external integrations, file handling, subprocesses, or exposed services. It provides a structured review for security weaknesses before code is merged or shipped.

### `quality-gate`

Use this skill when a change needs an explicit release-readiness decision. It gathers validation evidence and produces a clear ship, conditional, or hold outcome based on testing, correctness, operational readiness, and risk.

### `pair-programming`

Use this skill during active implementation when tight feedback loops help. It supports driver/navigator, TDD, debugging, refactoring, and review-oriented coding sessions so work progresses in smaller, verified steps.

### `skill-builder`

Use this skill when creating or cleaning up reusable AIOS skills. It helps keep skill names, descriptions, triggers, structure, and optional references/scripts consistent across the repo.
