# Security Audit — All Projects (2026-02-19)

Credential rotation remained a critical cross-project action item.

Highlighted exposures included:

- IntentionAI: SMTP, MongoDB, admin and Cloudflare keys
- SistersPromise: MongoDB, JWT, Square, reCAPTCHA, SMTP, Google Cloud key
- Arabis: Google Cloud key, Twilio, FTP/SSH, Vercel token
- Glomall: Braintree production credentials hardcoded in code

Priority actions included credential rotation, auth restoration, HTTPS enforcement, rate limiting, and git history cleanup where secrets were committed.
