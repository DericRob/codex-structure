# CODEX.md

This file provides workspace guidance for Codex and other coding agents when working from this Documents directory.

## Directory Overview

This is a personal Documents folder containing multiple independent projects, business files, and media. It is not a single repository. Navigate to the relevant project directory before doing work.

## Active Software Projects

Each active project should keep its own local notes, memory, or agent guidance. Read those before making changes.

| Project | Path | Stack | Description |
|---------|------|-------|-------------|
| **Rafi Assistant** | `Rafi/rafi_assistant/` | Python, FastAPI, Docker | AI personal assistant with Telegram/WhatsApp channels, 11 skills, 25+ tools, 4 LLM providers. |
| **Rafi Deploy** | `Rafi/rafi_deploy/` | Python CLI | Onboarding/deployment tooling for Rafi instances |
| **Sister's Promise** | `SistersPromise/` | Express.js + React Native | E-commerce skincare platform |
| **Arabis** | `Arabis/` | Next.js, TypeScript | Web app with Twilio SMS |
| **IntentionAI** | `IntentionAI/intention-ai/` | Next.js, TypeScript | Web platform |
| **Glomall** | `Glomall/Glomall_APKs/Glomall_Server-master/` | PHP, Android | E-commerce marketplace |

## Cross-Project Notes

- Never run two polling instances of the same bot/integration at once.
- Each project manages its own secrets in ignored config files.
- Treat security review as part of implementation, not a follow-up task.
