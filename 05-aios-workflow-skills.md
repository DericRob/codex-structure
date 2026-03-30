# Prompt 05 — AIOS Workflow Skills

Install the AIOS workflow-oriented Codex skills under `~/.codex/skills/`.

## Destination

```text
~/.codex/skills/
├── sparc-workflow/
│   └── SKILL.md
├── model-router/
│   └── SKILL.md
├── consensus-review/
│   └── SKILL.md
└── session-memory-sync/
    └── SKILL.md
```

## Source templates

Copy these repo files to the matching destination paths:

| Repo file | Destination | What the skill is used for |
|---|---|---|
| `templates/skills/sparc-workflow/SKILL.md` | `~/.codex/skills/sparc-workflow/SKILL.md` | Structured execution of complex work: specification, pseudocode, architecture, refinement, and completion |
| `templates/skills/model-router/SKILL.md` | `~/.codex/skills/model-router/SKILL.md` | Choosing the cheapest capable model tier for a task without sacrificing quality |
| `templates/skills/consensus-review/SKILL.md` | `~/.codex/skills/consensus-review/SKILL.md` | Multi-pass review and voting before risky commits, communications, or deploys |
| `templates/skills/session-memory-sync/SKILL.md` | `~/.codex/skills/session-memory-sync/SKILL.md` | Capturing and restoring project context between sessions so work picks up cleanly |

## Notes

- These skills are platform-agnostic workflow helpers for Codex-native work.
- Create the destination directories before copying the files.
- `session-memory-sync` works best when the repo or project also keeps a current `WORKLOG.md` or equivalent memory files.

## Skill descriptions

### `sparc-workflow`

Use this skill when work is large enough to need deliberate structure before implementation. It helps break complex requests into specification, pseudocode, architecture, refinement, and completion so the agent does not jump straight into coding without a plan.

### `model-router`

Use this skill when a system can choose among multiple LLM tiers and cost matters. It helps classify a task by complexity and route it to the cheapest model that is still capable of doing the work well.

### `consensus-review`

Use this skill before high-stakes actions such as risky commits, external communications, or deploys. It forces multiple review passes and a clear pass/fail decision instead of relying on a single unchecked answer.

### `session-memory-sync`

Use this skill when work spans multiple sessions and losing context is expensive. It helps capture active plans, recent findings, blockers, and next steps so future sessions resume quickly and consistently.
