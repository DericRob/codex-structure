# Zero Trust for Agentic AI

Core principles to apply across projects:

1. Verify before trust.
2. Grant least privilege, only when needed.
3. Assume breach.
4. Track non-human identities and credentials carefully.
5. Validate inputs and outputs at every boundary.
6. Keep immutable audit logs for sensitive actions.
7. Protect secrets from source code, logs, and responses.
8. Keep human override and kill-switch paths available.

Implementation checklist:

- No hardcoded secrets
- Validated external inputs
- Rate limiting on sensitive flows
- Restrictive CORS and security headers
- Prompt-injection awareness for tool-using systems
- Output filtering to avoid accidental disclosure
