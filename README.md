# Codex Global Setup Prompts

These prompts and templates recreate a **Codex-native** environment on a new machine. Legacy Claude-specific operational assumptions have been removed.

## What this repo now contains

| File | Purpose |
|---|---|
| `01-core-config-watcher.md` | Create `~/.codex/watcher/`, `~/.codex/alerts.jsonl`, `~/Documents/CODEX.md`, and `~/Documents/.mcp.json` |
| `02-memory-files.md` | Recreate project memory files under `~/.codex/memories/projects/<slug>/` |
| `03-design-skill.md` | Recreate the global `design` skill under `~/.codex/skills/design/` |
| `04-csv-data-instructions.md` | Transfer the design CSV data files into `~/.codex/skills/design/data/` |
| `templates/launcher/` | Install wrapper scripts that inject `~/Documents/CODEX.md` into every new Codex session |
| `templates/` | Source-of-truth files to copy from instead of giant inline markdown blobs |
| `templates/skills/` | 9 portable skills — design + AIOS workflow + productivity skills (see below) |

## Skills

### Design & UI Skill

| Skill | Purpose |
|-------|---------|
| `design` | Industry-specific UI/UX recommendations backed by local CSV data |

### AIOS Portable Skills (platform-agnostic workflow skills)

| Skill | Purpose |
|-------|---------|
| `sparc-workflow` | Structured methodology: Spec → Pseudocode → Architecture → Refine → Complete |
| `model-router` | Cost-optimal LLM routing by task complexity (fast/balanced/heavy tiers) |
| `consensus-review` | Multi-pass voting quality gate before high-stakes actions |
| `session-memory-sync` | Auto-capture/restore context across sessions via lifecycle hooks |

### Productivity Skills (executive assistant capabilities)

| Skill | Purpose |
|-------|---------|
| `inbox-triage` | Email urgency categorization + draft replies |
| `smart-scheduling` | Deep-work protection, conflict detection, reschedule suggestions |
| `follow-up-tracker` | Waiting-on ledger with due dates and overdue surfacing |
| `delegation-tracker` | Assign and track work across people with accountability |

## Key changes from the old Claude version

- `~/.claude/...` → `~/.codex/...`
- removed Claude hook events and `CLAUDE_*` env vars
- removed Claude slash commands and plugin-marketplace instructions
- removed Superpowers and Parry setup steps
- converted project instructions to generic Codex workspace notes
- kept the watcher, design skill, MCP config, and memory content

## Recommended setup order

1. Use `01-core-config-watcher.md`
2. Use `02-memory-files.md`
3. Use `03-design-skill.md`
4. Use `04-csv-data-instructions.md`

## Post-setup checklist

- [ ] `chmod +x ~/.codex/watcher/*.sh ~/.codex/watcher/server.py ~/.codex/watcher/append_event.py`
- [ ] copy memory files into `~/.codex/memories/projects/<slug>/`
- [ ] add your API keys to `~/Documents/.mcp.json`
- [ ] transfer CSV data files into `~/.codex/skills/design/data/`
- [ ] start watcher with `~/.codex/watcher/start.sh`
- [ ] launch Codex through `~/.codex/launcher/start-codex.(ps1|sh)` so `~/Documents/CODEX.md` is injected at session start

## Repo structure

```text
templates/
├── config/mcp.json
├── docs/CODEX.md
├── launcher/
│   ├── start-codex.ps1
│   └── start-codex.sh
├── memory/*.md
├── skills/
│   ├── design/SKILL.md
│   ├── sparc-workflow/SKILL.md
│   ├── model-router/SKILL.md
│   ├── consensus-review/SKILL.md
│   ├── session-memory-sync/SKILL.md
│   ├── inbox-triage/SKILL.md
│   ├── smart-scheduling/SKILL.md
│   ├── follow-up-tracker/SKILL.md
│   └── delegation-tracker/SKILL.md
└── watcher/
    ├── append_event.py
    ├── dashboard.html
    ├── server.py
    ├── start.sh
    └── stop.sh
```
