# AIOS Overview Slides

## Slide 1 - What This AIOS Is

**Title:** AIOS: Codex-Native Workstation Operations

- A Codex-native workstation bootstrap repo.
- A local watcher and alerting system for Codex session activity.
- A packaging format for memory, MCP config, startup prompts, and skills.
- An operational control layer for a developer machine.

**Speaker note:** Start by defining the current project precisely so people do not confuse it with a full agent kernel.

## Slide 2 - What It Is Not

**Title:** Important Boundary Conditions

- Not a scheduler for multiple agents.
- Not a kernel that exposes syscall-style agent services.
- Not a general-purpose LLM runtime.
- Not an execution substrate for many agent frameworks.

**Speaker note:** This slide prevents overclaiming and sets up the case for an `AIOSx` follow-on.

## Slide 3 - Why It Matters

**Title:** Practical Benefits Today

- Standardizes the local AI workspace across machines and teams.
- Makes Codex sessions observable through the watcher dashboard and alerts.
- Preserves working context with memory files and startup instructions.
- Reduces setup time when rebuilding a machine or onboarding a new developer.
- Keeps the stack local-first, which is useful when teams need tighter control over data and execution.

**Speaker note:** After defining the system and its limits, show the concrete operational value it already provides.

## Slide 4 - What The Watcher Adds

**Title:** Watcher Value

- Tracks Codex session activity from local session logs in near real time.
- Surfaces tool usage, blocked actions, alerts, and activity patterns in a dashboard.
- Helps identify risky behavior such as permission failures, excessive shell usage, or suspicious file access patterns.
- Gives teams a concrete way to review how AI tooling is being used without relying on manual recollection.

**Speaker note:** The watcher is the operational visibility layer that makes this usable in controlled environments.

## Slide 5 - CDC Developer Use Cases

**Title:** Likely High-Value Tasks at CDC

- Accelerating internal tool development for data pipelines, reporting utilities, and analyst workflows.
- Assisting with documentation updates, SOP generation, and config-heavy engineering tasks.
- Supporting code review and debugging on local projects where traceability matters.
- Rebuilding standardized environments for contractors, new hires, or rotating teams.
- Monitoring AI-assisted development patterns in teams that need stronger governance and auditability.

**Speaker note:** Focus on engineering productivity, reproducibility, and oversight in regulated or mission-sensitive work.
