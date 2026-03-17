# Prompt 02 — Codex Memory Files

Recreate project memory files under Codex global memory.

## Destination format

```text
~/.codex/memories/projects/<project-slug>/
```

Example for a Documents-root workspace:

```text
~/.codex/memories/projects/-Users-drob-Documents/
```

Use the slug that matches the target machine's project root.

## Source templates

Copy every markdown file from:

```text
templates/memory/
```

into:

```text
~/.codex/memories/projects/<project-slug>/
```

That includes:

- `MEMORY.md`
- `user-profile.md`
- `feedback-communication-style.md`
- `zero-trust-agentic-ai.md`
- `docker-headless-environment-notes.md`
- `security-audit-2026-02-19.md`
- `security-hardening-status.md`
- `design-advisor-skill.md`
- `vibe-coding-improvements.md`
- `skill-architecture-analysis.md`

## Notes

These memory templates are intentionally public-safe examples. Keep any real personal notes, reminders, account details, or machine-specific context in private local files rather than the public template set.
