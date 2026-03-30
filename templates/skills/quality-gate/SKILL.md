---
name: quality-gate
description: Run a release-quality gate before commit, PR, merge, or deploy. Use when code changes are hard to reverse or touch tests, infrastructure, data models, auth, billing, APIs, or shared workflows. Produces a ship, hold, or conditional decision with evidence.
tools: []
requires:
  env: []
---

# Quality Gate

Evidence-first release review that decides whether a change is ready to ship.

## When to Use

- Before commit on risky or cross-cutting changes
- Before opening or merging a PR
- Before deploys, migrations, or operational changes
- After large refactors or bug fixes with unclear blast radius

## Skip When

- WIP spikes that will not be shared or merged
- Notes-only changes with no runnable behavior

## Gate Steps

### 1. Summarize the change

- What changed?
- Why did it change?
- What is the blast radius?

### 2. Check correctness

- Are requirements met?
- Are edge cases handled?
- Are defaults safe?

### 3. Check validation evidence

- What tests were run?
- What lint, type, or static checks were run?
- What manual verification was performed?

If no validation was run, say so explicitly.

### 4. Check operational readiness

- Docs, runbooks, or usage notes updated?
- Config changes captured?
- Rollback path available?

### 5. Check risk areas

- Security-sensitive paths reviewed?
- Performance or resource regressions considered?
- User-visible failure modes acceptable?

## Decision States

- **Ship** — evidence is sufficient and risks are acceptable
- **Conditional** — mostly ready, but requires named follow-ups
- **Hold** — not ready; must fix blockers first

## Output Template

Provide:

1. **Decision**
2. **Evidence reviewed**
3. **Blockers**
4. **Follow-ups**
5. **Rollback / recovery note**

## Good Companion Skills

- `security-audit` for exposed or sensitive flows
- `consensus-review` for high-stakes actions
- `pair-programming` for iterative implementation before the gate
