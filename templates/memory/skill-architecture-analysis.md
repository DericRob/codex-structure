# Skill Architecture Analysis

Key architectural note:

Folder-based skills with `SKILL.md`, plus optional `scripts/`, `references/`, and `assets/`, are a better long-term pattern than a single monolithic skill file.

Three-level progressive disclosure is valuable:

1. metadata
2. skill body
3. bundled resources loaded only when needed
