---
name: sparc-workflow
description: Structured workflow for complex tasks — Specification, Pseudocode, Architecture, Refinement, Completion. Forces disciplined decomposition before implementation.
tools: []
requires:
  env: []
---

# SPARC Workflow Orchestrator

A structured methodology for tackling complex tasks. Use this whenever a task involves multiple steps, architectural decisions, or cross-cutting concerns.

## When to Use

- Building a new feature or system
- Refactoring existing architecture
- Planning a migration or integration
- Any task that would take more than 30 minutes of implementation

## The SPARC Phases

### 1. Specification (S)
Define WHAT needs to be built. Not HOW.

- **Inputs**: What data/context does this need?
- **Outputs**: What should exist when done?
- **Constraints**: Performance, security, compatibility requirements
- **Acceptance criteria**: How do we know it's done?

Deliverable: A clear, testable spec (3-10 bullet points).

### 2. Pseudocode (P)
Sketch the logic in plain language or pseudocode.

- Walk through the happy path step by step
- Identify edge cases and error paths
- Note where external dependencies are needed
- Keep it language-agnostic

Deliverable: Pseudocode that a junior developer could follow.

### 3. Architecture (A)
Decide HOW to structure the solution.

- Which files to create or modify (exact paths)
- Data flow between components
- Interface contracts (function signatures, API shapes)
- Dependencies and their justification

Deliverable: File list with responsibilities + interface contracts.

### 4. Refinement (R)
Review and improve before coding.

- Does this over-engineer? Remove unnecessary abstractions.
- Does this under-engineer? Add missing error handling at boundaries.
- Security review: input validation, auth, secrets handling
- Test strategy: what tests prove this works?

Deliverable: Revised architecture + test plan.

### 5. Completion (C)
Implement, test, and verify.

- Write failing tests first (TDD)
- Implement minimal code to pass tests
- Run full test suite
- Commit with descriptive message
- Verify in context (does it integrate correctly?)

Deliverable: Working, tested, committed code.

## Rules

- Never skip phases. Each phase is a checkpoint.
- Spec and Pseudocode phases produce NO code files.
- Architecture phase produces NO implementation code, only structure.
- Refinement catches over-engineering BEFORE you write code.
- Completion follows TDD strictly.

## Anti-Patterns

- Jumping straight to Completion (cowboy coding)
- Spending too long in Specification (analysis paralysis) — timebox to 5 minutes
- Skipping Refinement (the phase that catches 80% of design mistakes)
- Gold-plating in Architecture (YAGNI — only what's needed now)
