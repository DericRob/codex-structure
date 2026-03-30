# Presentation Notes

## Purpose

This file captures decisions made while building the AIOS demo presentation so future edits do not lose structure, tone, or asset choices.

## Current Presentation Files

- Main presenter-facing deck: `AIOS-DEMO-PRESENTATION-V2.html`
- Earlier draft deck: `AIOS-DEMO-PRESENTATION.html`
- Watcher screenshot asset: `watcherPageImage.png`
- AIOSx architecture image used in the comparison slide: `AIOSx_diagram.png`

## Presentation Positioning

- Present `AIOS` as a practical, Codex-native workstation operations layer.
- Do not present `AIOS` as a full AI operating system.
- Present `AIOSx` as the broader future architecture for control plane, tracing, replay, analytics, and runtime-kernel ideas.
- Keep the distinction between `AIOS` and `AIOSx` explicit to avoid overclaiming.

## Tone And Audience

- The presenter-facing deck should sound like the speaker is addressing the audience directly, not like notes to the presenter.
- Avoid "speaker note" labels in the visible slide content.
- Use simple executive-friendly framing with technical specificity where useful.
- Keep language suitable for an internal AI department or leadership-technical mixed audience.

## Slide Decisions To Preserve

### Navigation

- The fixed arrows in `AIOS-DEMO-PRESENTATION-V2.html` should move one slide at a time.
- Do not revert to top-of-page or bottom-of-page jump links.

### Slide 1

- Keep the first slide visual style and general structure. It was specifically liked and used as a quality bar for the rest of the deck.

### Slide 3

- Keep Slide 3 unchanged unless there is a strong reason to revise it. It was explicitly approved.

### Five Key Features Slide

- Title should remain `Five Key Features`.
- Each feature should point to repo files or code locations rather than staying purely conceptual.

### Use Cases Slide

- The closing sentence should remain:
  `If we want teams to use AI productively without losing operational discipline, AIOS is a lightweight but credible starting point.`
- Frame the slide as `business problem -> AIOS use case -> business outcome`.
- Keep the examples AIOS-only:
  - workstation setup
  - watcher visibility
  - startup instruction injection
  - memory and worklog continuity
  - shared MCP and tool configuration

### Watcher Slides

- Keep one slide that explains watcher widgets in short audience-facing descriptions.
- Keep one separate screenshot slide immediately after it.
- The screenshot slide should use `watcherPageImage.png` and fit the image inside the slide without distortion.

### AIOS / AIOSx Comparison Slide

- Title should remain `About AIOS and AIOSx`.
- Keep the `AIOS` and `AIOSx` boxes visually close together.
- Keep the AIOSx reference image to the right using `AIOSx_diagram.png`.
- Preserve the lower cards:
  - `Emphasis`
  - `Big Note`
- The `Big Note` text should remain:
  `AIOS is not a full "AI Operating System." It is better described as a disciplined local operational layer.`

### Install Slide

- Keep installation commands on their own slide before `Bottom Line`.
- Keep the clone block above the Windows and macOS/Linux install blocks.
- Keep only the repository URL clickable, not the words `git clone`.
- Use the cleaner card-based layout with whitespace instead of comment-heavy command dumps.
- Keep the repo-path to installed-path mapping as a visual copy map.

### Bottom Line Slide

- Keep it as a true close, not a setup slide.
- Keep the contact block with:
  - `Questions? Contact me:`
  - `Deric Robinson`
  - `lwx3@cdc.gov`
  - `404.639.6022`

### References Slide

- Use external references only.
- Do not include local repo files as references on that slide.
- Current framing sentence:
  `Outside sources most closely aligned with the basis for this project: the public AIOS ecosystem, the AIOS papers, and observability/evaluation guidance for agent systems.`

## Current External References In The Deck

- `https://github.com/agiresearch/AIOS`
- `https://github.com/agiresearch/Cerebrum`
- `https://github.com/agiresearch`
- `https://arxiv.org/abs/2403.16971`
- `https://arxiv.org/abs/2312.03815`
- `https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/`
- `https://danielmiessler.com/`

## Demo Guidance

- If asked whether AIOS is running on the machine, verify the watcher health endpoint instead of assuming from installed files.
- In this environment, the watcher responded successfully at:
  - `http://127.0.0.1:9999/api/health`
- A prior issue occurred where the watcher started but `watcher.pid` could not be refreshed due to file permission denial. This did not prevent the watcher from running, but it could affect stop/restart scripts.

## Talking Points To Reuse

- `Zero trust` should be described as an operating posture, not a claim of full enterprise Zero Trust architecture.
- Good phrasing:
  - AIOS applies a zero-trust mindset to AI-assisted development on the workstation.
  - It assumes AI actions should be observable, reviewable, and not implicitly trusted.
- For blocked actions:
  - In AIOS, blocked actions are inferred from permission or sandbox failures seen in session logs.
  - In AIOSx, policy-driven blocking is a stronger future/control-plane model.

## Watcher Widget Explanations To Reuse

- Tool Usage: summarizes which tools the AI is relying on most.
- Security Alerts: the watcher triage layer for risky or abnormal behavior.
- Recent Events: the latest normalized session activity.
- Activity Timeline: event volume over time.
- Sessions: how many unique sessions have been observed.
- Agents / Session Detail: maps higher-level metrics back to concrete session context.

## Recommended Starting Files For Future Presentation Work

- `PRESENTATION-NOTES.md`
- `AIOS-DEMO-PRESENTATION-V2.html`
- `WORKLOG.md`
- `AIOSx-PLAN.md`
- `AIOSx-ARCHITECTURE-BRIEF.md`
- For use-case edits, start from AIOS business outcomes first and then connect AIOSx only as future direction if needed.
