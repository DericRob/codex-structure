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
- `project-rafi-business-goal.md`
- `zero-trust-agentic-ai.md`
- `rafi-docker-headless.md`
- `rafi-multi-tenant-platform.md`
- `security-audit-2026-02-19.md`
- `security-hardening-status.md`
- `antigravity-rafi-migration.md`
- `design-advisor-skill.md`
- `superpowers-parry-install.md` *(historical notes only; no install step required)*
- `vibe-coding-improvements.md`
- `claude-skills-analysis.md` *(historical analysis; may be renamed later)*
- `reminder-electric-bill-april-2026.md`

## Required cleanup after copy

Update memory text anywhere it still says:

- `~/.claude/...`
- `CLAUDE.md`
- `Claude Code`
- Claude-only slash commands or plugin references

Those files are being preserved for durable project knowledge, not as operational instructions.
