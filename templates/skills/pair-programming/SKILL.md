---
name: pair-programming
description: Structured AI pair programming with driver/navigator, TDD, review, debug, and refactor modes. Use when building features, debugging tricky issues, or wanting tighter feedback loops while coding.
tools: []
requires:
  env: []
---

# Pair Programming

Run coding sessions as an explicit collaboration loop instead of a one-shot implementation.

## When to Use

- New feature work with several small decisions
- Bug hunts where hypotheses need fast iteration
- Refactors that benefit from frequent check-ins
- TDD or code-review-first workflows

## Modes

- **Driver / Navigator** — one side writes, the other critiques and steers
- **TDD** — write failing test, implement, then refactor
- **Debug** — isolate, instrument, reproduce, fix, verify
- **Refactor** — preserve behavior while improving structure
- **Review** — inspect code first, then patch only after agreement

## Session Loop

### 1. Frame the task

- state the goal
- define constraints
- choose a mode

### 2. Make a micro-plan

Work in small steps that can be validated quickly.

### 3. Implement one step

- keep the diff bounded
- narrate assumptions
- avoid hidden scope creep

### 4. Checkpoint

After each step:

- what changed?
- what was verified?
- what remains risky?

### 5. Swap or continue

If momentum drops or uncertainty rises, switch modes or roles.

## Rules

- Prefer small diffs over heroic rewrites
- Keep validation close to each change
- Say when you are guessing
- Pause for `security-audit` or `quality-gate` on risky changes

## Output

End each session with:

1. current state
2. tests or checks run
3. open risks
4. recommended next step
