# Codex Global Setup Prompts

These prompts and templates recreate a **Codex-native** environment on a new machine. Legacy Claude-specific operational assumptions have been removed.

## What this repo now contains

| File | Purpose |
|---|---|
| `01-core-config-watcher.md` | Create `~/.codex/watcher/`, Windows and Unix watcher launchers, `~/.codex/alerts.jsonl`, `~/Documents/CODEX.md`, and `~/Documents/.mcp.json` |
| `02-memory-files.md` | Recreate project memory files under `~/.codex/memories/projects/<slug>/` |
| `03-design-skill.md` | Entry point for the portable skill library; installs `design` and links to the other skill-pack prompts |
| `04-csv-data-instructions.md` | Transfer the design CSV data files into `~/.codex/skills/design/data/` |
| `05-aios-workflow-skills.md` | Install the AIOS workflow skill pack under `~/.codex/skills/` |
| `06-engineering-quality-skills.md` | Install the engineering and quality skill pack under `~/.codex/skills/` |
| `07-productivity-skills.md` | Install the productivity skill pack under `~/.codex/skills/` |
| `templates/launcher/` | Install wrapper scripts that inject `~/Documents/CODEX.md` into every new Codex session |
| `templates/` | Source-of-truth files to copy from instead of giant inline markdown blobs |
| `templates/agents/` | 7 portable agent playbooks for Codex-style coordination, implementation, review, and validation |
| `templates/docs/WORKLOG.md` | Standard project worklog template for plans, to-dos, mistakes, fixes, and handoff notes |
| `templates/docs/AGENT-PLAYBOOKS.md` | Overview of the portable agent playbooks and how they map onto Codex roles |
| `templates/skills/` | 13 portable skills — design + AIOS workflow + engineering/quality + productivity skills (see below) |

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

### Engineering & Quality Skills

| Skill | Purpose |
|-------|---------|
| `security-audit` | Structured security review for exposed, sensitive, or untrusted-input changes |
| `quality-gate` | Evidence-based ship/hold gate before commit, merge, or deploy |
| `pair-programming` | Driver/navigator, TDD, debug, and refactor workflows for iterative coding |
| `skill-builder` | Standard pattern for creating new reusable AIOS skills |

### Productivity Skills (executive assistant capabilities)

| Skill | Purpose |
|-------|---------|
| `inbox-triage` | Email urgency categorization + draft replies |
| `smart-scheduling` | Deep-work protection, conflict detection, reschedule suggestions |
| `follow-up-tracker` | Waiting-on ledger with due dates and overdue surfacing |
| `delegation-tracker` | Assign and track work across people with accountability |

## Portable Agent Playbooks

| Playbook | Purpose |
|-------|---------|
| `coordinator` | Owns planning, delegation, integration, and final delivery |
| `planner` | Breaks complex work into executable phases and acceptance criteria |
| `researcher` | Runs focused investigations and returns evidence |
| `implementer` | Makes bounded code/content changes in a defined scope |
| `reviewer` | Performs independent bug/risk/regression review |
| `tester` | Reproduces, validates, and retests behavior |
| `production-validator` | Performs final readiness review for high-stakes changes |

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
5. Use `05-aios-workflow-skills.md`
6. Use `06-engineering-quality-skills.md`
7. Use `07-productivity-skills.md`

## Post-setup checklist

- [ ] use `~/.codex/watcher/start.ps1` on Windows or `~/.codex/watcher/start.sh` on macOS/Linux
- [ ] `chmod +x ~/.codex/watcher/*.sh ~/.codex/watcher/server.py ~/.codex/watcher/append_event.py`
- [ ] copy memory files into `~/.codex/memories/projects/<slug>/`
- [ ] add your API keys to `~/Documents/.mcp.json`
- [ ] transfer CSV data files into `~/.codex/skills/design/data/`
- [ ] launch Codex through `~/.codex/launcher/start-codex.(ps1|sh)` so `~/Documents/CODEX.md` is injected at session start
- [ ] create a repo-local `WORKLOG.md` from `templates/docs/WORKLOG.md` and keep it updated during work

## Repo structure

```text
templates/
├── agents/
│   ├── coordinator.md
│   ├── implementer.md
│   ├── planner.md
│   ├── production-validator.md
│   ├── researcher.md
│   ├── reviewer.md
│   └── tester.md
├── config/mcp.json
├── docs/
│   ├── AGENT-PLAYBOOKS.md
│   ├── CODEX.md
│   └── WORKLOG.md
├── launcher/
│   ├── start-codex.ps1
│   └── start-codex.sh
├── memory/*.md
├── skills/
│   ├── design/SKILL.md
│   ├── sparc-workflow/SKILL.md
│   ├── model-router/SKILL.md
│   ├── consensus-review/SKILL.md
│   ├── security-audit/SKILL.md
│   ├── quality-gate/SKILL.md
│   ├── pair-programming/SKILL.md
│   ├── skill-builder/SKILL.md
│   ├── session-memory-sync/SKILL.md
│   ├── inbox-triage/SKILL.md
│   ├── smart-scheduling/SKILL.md
│   ├── follow-up-tracker/SKILL.md
│   └── delegation-tracker/SKILL.md
└── watcher/
    ├── append_event.py
    ├── dashboard.html
    ├── server.py
    ├── start.ps1
    ├── start.sh
    ├── stop.ps1
    └── stop.sh
```
