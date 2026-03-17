# Security Hardening Status (2026-02-19)

## Mandatory rules

1. No embedded credentials
2. Validate all inputs
3. Rate limit sensitive operations
4. Apply security headers
5. Use constant-time comparison for secrets
6. Keep sensitive data out of responses
7. Keep sensitive data out of logs
8. Fail closed when auth config is missing
9. Prefer battle-tested libraries
10. Keep CORS restrictive

## Status

Committed fixes were recorded for Glomall, Arabis, SistersPromise, and IntentionAI.

Manual work still pending:

- rotate credentials
- clean git history where needed
- install secret scanning hooks consistently
