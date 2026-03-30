---
name: security-audit
description: Review code, workflows, and operational changes for security issues before shipping. Use for auth, tokens, APIs, file operations, subprocesses, secrets, user data, payments, external integrations, watcher/server changes, or anything exposed to untrusted input.
tools: []
requires:
  env: []
---

# Security Audit

Structured security review for changes that could expose data, systems, or operator control.

## When to Use

- New endpoints, APIs, dashboards, or automation surfaces
- Auth, tokens, sessions, permissions, billing, or user-data flows
- File I/O, uploads, archive handling, path construction, or symlink-sensitive logic
- Shell commands, subprocesses, eval-like behavior, or tool execution
- Logging, tracing, alerts, or error handling that might leak secrets
- External integrations, webhooks, network fetches, or proxy behavior

## Skip When

- Pure copy changes with no behavioral impact
- Static docs or presentation-only edits
- Styling-only changes with no new data or execution path

## Review Checklist

### 1. Exposure map

- What new surface is reachable?
- Who can trigger it?
- What trust boundary does it cross?

### 2. Input handling

- Validate and normalize all external input
- Reject unexpected types, shapes, sizes, and encodings
- Avoid command, template, and query injection paths

### 3. Auth and authorization

- Confirm least-privilege behavior
- Check role/ownership enforcement
- Ensure sensitive actions require explicit authorization

### 4. Filesystem and process safety

- Prevent path traversal and symlink abuse
- Avoid unsafe temp-file or archive extraction behavior
- Constrain subprocess arguments and working directories

### 5. Secrets and logging

- Do not log tokens, keys, passwords, cookies, or raw personal data
- Keep stack traces and debug output out of production-facing paths
- Sanitize error messages returned to callers

### 6. Abuse resistance

- Add rate limits or friction for sensitive flows
- Bound retries, fan-out, and resource usage
- Fail closed when policy or validation is uncertain

### 7. Production hardening

- Prefer restrictive defaults for CORS, access, and debug modes
- Ensure safe host/port binding and local-only assumptions are explicit
- Confirm rollout or rollback steps exist for risky changes

## Output Format

Return findings grouped by severity:

- **Critical** — must fix before ship
- **High** — fix before merge unless explicitly accepted
- **Medium** — track and schedule
- **Low** — hygiene improvement

Always include:

1. affected file or flow
2. exploit or failure mode
3. recommended fix
4. residual risk if left unchanged

## Good Companion Skills

- Use `quality-gate` before commit or deploy
- Use `consensus-review` for high-stakes external actions
- Use `sparc-workflow` when the change needs redesign, not just review
