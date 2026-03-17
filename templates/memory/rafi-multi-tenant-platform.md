---
name: rafi-multi-tenant-platform
description: Architecture and status of the Rafi multi-tenant platform
type: project
---

Rafi multi-tenant platform work added:

- `rafi_platform`: FastAPI control plane for tenant signup, billing, provisioning, and A2A registry concerns
- `rafi_portal`: Next.js portal for pricing, signup, and customer dashboard flows
- `rafi_assistant`: gained platform config, A2A support, and multi-tenant routing support

Pricing snapshot:

- Starter: `$49/mo`
- Pro: `$149/mo`
- Business: `$299/mo`

Status snapshot:

- Platform code largely complete
- Remaining work depends on Stripe product setup, platform Supabase provisioning, and a few dependency/runtime follow-ups
