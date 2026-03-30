# Agent Playbooks

These are **portable playbooks**, not a runtime-specific agent registry.

Use them to standardize how AIOS-style work is delegated and reviewed across Codex-native environments.

## Why This Exists

Richer agent systems often mix good role definitions with tool-specific orchestration. This repo keeps the role definitions while staying portable.

## Codex Mapping

| Playbook | Best Codex Mapping | Main Job |
|---|---|---|
| `coordinator` | main agent / `default` | Own plan, delegation, integration, and final answer |
| `planner` | main agent / `default` | Break work into steps, dependencies, and exit criteria |
| `researcher` | `explorer` | Answer focused questions with evidence |
| `implementer` | `worker` | Make bounded code or content changes |
| `reviewer` | `worker` or main-agent review pass | Find bugs, risk, and missing evidence |
| `tester` | `worker` | Reproduce, validate, and retest |
| `production-validator` | `worker` | Final release-readiness check |

## Recommended Flow

1. `coordinator` owns the task
2. `planner` defines the next executable steps
3. `researcher` answers blocked questions
4. `implementer` makes the change
5. `tester` validates it
6. `reviewer` inspects risk and regressions
7. `production-validator` signs off on readiness when stakes are high

## Companion Skills

These playbooks work best with:

- `sparc-workflow`
- `consensus-review`
- `security-audit`
- `quality-gate`
- `session-memory-sync`
