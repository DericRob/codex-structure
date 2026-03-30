# Inbox Triage & Draft Replies

AI-powered email triage — categorize by urgency, surface action items, and draft context-aware replies.

## When to Use

- User says "check my email", "what's urgent", "anything important?"
- Morning briefing / heartbeat check
- User says "draft a reply to..." or "respond to..."
- User asks for email summary or inbox status

## How It Works

### Triage Categories

1. **Urgent** — Needs response within hours. Signals: named deadlines, escalation language ("ASAP", "critical", "blocker"), C-suite senders, reply-all chains with your name.
2. **Action Needed** — Requires a response or task, but not time-critical. Signals: questions directed at user, approval requests, meeting invites, document reviews.
3. **FYI** — Informational, no action needed. Signals: CC'd emails, status updates, team announcements, automated reports.
4. **Low Priority** — Newsletters, promotions, notifications. Signals: unsubscribe links, bulk senders, CATEGORY_PROMOTIONS label.

### Draft Reply Behavior

- Match the sender's formality level
- Reference specific points from the email thread
- Keep replies concise (3-5 sentences default)
- Never commit to meetings/deadlines without user confirmation
- Always present draft for user approval before sending

## Important

- ALWAYS show the user the triage results before taking any action
- NEVER auto-send replies — always get user confirmation
- For emails marked urgent, proactively mention them even if user didn't ask
- Draft replies are for review only — never auto-send
