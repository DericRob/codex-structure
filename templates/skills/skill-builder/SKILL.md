---
name: skill-builder
description: Create or refine reusable AIOS skills with clear trigger metadata, concise instructions, and optional scripts, references, or assets. Use when adding a new skill or cleaning up an existing one.
tools: []
requires:
  env: []
---

# Skill Builder

Use this when authoring portable skills for the AIOS repo.

## Goal

Create skills that are:

- easy to trigger
- short enough to load cheaply
- specific enough to be reliable
- extensible with scripts, references, or assets when needed

## Required Layout

```text
templates/skills/<skill-name>/
└── SKILL.md
```

Optional:

- `scripts/` for deterministic helpers
- `references/` for docs loaded only when needed
- `assets/` for output resources

## Frontmatter Rules

Every `SKILL.md` should include:

```yaml
---
name: skill-name
description: What the skill does and when it should be used.
---
```

The description should name both:

1. the job the skill performs
2. the situations that should trigger it

## Body Structure

Keep the body concise and prefer this shape:

1. short purpose
2. when to use
3. when to skip
4. core workflow
5. expected output or decision format
6. companion skills if relevant

## Authoring Rules

- Prefer one strong workflow over many weak options
- Do not repeat generic model knowledge
- Put bulky details in `references/`, not the main file
- Add scripts only when deterministic execution helps
- Avoid extra docs inside the skill folder

## Validation Checklist

Before shipping a skill, verify:

- the name is short and hyphenated
- the description is trigger-friendly
- the instructions fit the repo style
- the workflow is reusable across projects
- the skill does not duplicate another AIOS skill unnecessarily

## Existing Patterns To Reuse

Strong existing examples in this repo:

- `sparc-workflow`
- `consensus-review`
- `session-memory-sync`
- `security-audit`
- `quality-gate`
