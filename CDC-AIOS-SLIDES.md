# AIOS Overview Slides

## Slide 1 - What AIOS Is

**Title:** AIOS: A Practical Operating Layer for Codex-Based Development

- AIOS gives developers a repeatable local setup for Codex work.
- It packages the watcher, launcher, memory files, MCP config, and project templates into one reproducible system.
- The result is less setup drift, faster onboarding, and better visibility into how AI-assisted work is actually happening.

**Speaker note:** Position AIOS as infrastructure for reliable AI-assisted engineering, not just a prompt collection.

## Slide 2 - Why It Matters

**Title:** Core Benefits

- Standardizes the local AI workspace across machines and teams.
- Makes Codex sessions observable through the watcher dashboard and alerts.
- Preserves working context with memory files and startup instructions.
- Reduces setup time when rebuilding a machine or onboarding a new developer.
- Keeps the stack local-first, which is useful when teams need tighter control over data and execution.

**Speaker note:** Emphasize consistency, observability, and lower operational friction.

## Slide 3 - What The Watcher Adds

**Title:** Watcher Value

- Tracks Codex session activity from local session logs in near real time.
- Surfaces tool usage, blocked actions, alerts, and activity patterns in a dashboard.
- Helps identify risky behavior such as permission failures, excessive shell usage, or suspicious file access patterns.
- Gives teams a concrete way to review how AI tooling is being used without relying on manual recollection.

**Speaker note:** The watcher is the operational visibility layer for the rest of AIOS.

## Slide 4 - CDC Developer Use Cases

**Title:** Likely High-Value Tasks at CDC

- Accelerating internal tool development for data pipelines, reporting utilities, and analyst workflows.
- Assisting with documentation updates, SOP generation, and config-heavy engineering tasks.
- Supporting code review and debugging on local projects where traceability matters.
- Rebuilding standardized environments for contractors, new hires, or rotating teams.
- Monitoring AI-assisted development patterns in teams that need stronger governance and auditability.

**Speaker note:** Focus on engineering productivity, reproducibility, and oversight in regulated or mission-sensitive work.

## Slide 5 - Recommended Adoption Path

**Title:** How To Use AIOS Safely

- Start with a small pilot team using the standardized launcher and watcher setup.
- Use the watcher to understand normal AI-assisted work patterns before expanding usage.
- Treat memory files and startup docs as controlled operational context, not ad hoc notes.
- Add project-specific guidance incrementally instead of over-customizing the base system.
- Use AIOS as a local engineering copilot platform with clear boundaries, visibility, and repeatable workflows.

**Speaker note:** Recommend phased adoption with operational discipline rather than broad uncontrolled rollout.
