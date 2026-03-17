# Security Audit — All Projects (2026-02-19)

Credential rotation remained a critical cross-project action item.

Highlighted exposures included:

- cloud service credentials committed to source control
- database and admin credentials exposed in application config
- third-party API keys present in deploy or app code
- production payment credentials hardcoded in code

Priority actions included credential rotation, auth restoration, HTTPS enforcement, rate limiting, and git history cleanup where secrets were committed.
