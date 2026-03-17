# Auto Memory

## Priority Project

- Project-specific implementation notes are stored in the companion memory files in this folder
- See `docker-headless-environment-notes.md` for Docker and headless-environment pitfalls
- Config loader merges env vars via `_ENV_OVERRIDES`; clear them in unit tests that run alongside dotenv-loading integration tests
- MCP server note: stdio transport should use synchronous stdout writes instead of async write-pipe assumptions

## User Profile

- See `user-profile.md` for the user background, role, business goals, and experience level
- See `feedback-communication-style.md` for communication rules

## User Preferences

- Always scan downloaded code for malware or suspicious behavior before use
- Apply zero-trust thinking to all agentic tooling and generated code
- Treat security-first development as mandatory for every feature and fix

## Security Audit Status

- See `security-audit-2026-02-19.md` for audit findings across projects
- See `security-hardening-status.md` for committed fixes and manual follow-up items

## Design Advisor Skill

- See `design-advisor-skill.md` for the global design workflow and data-backed recommendation system
- CSV placeholders are installed locally and should be replaced with transferred data files

## Other Notes

- See `superpowers-parry-install.md` for optional tooling setup notes
- See `vibe-coding-improvements.md` and `skill-architecture-analysis.md` for workflow and skill architecture guidance
- See `reminder-electric-bill-april-2026.md` for the dated reminder record
