# Follow-Up Tracker

Track who owes what by when. Manage a waiting-on ledger with due dates, auto-surface overdue items.

## When to Use

- User says "remind me to follow up with...", "I'm waiting on..."
- After sending an email that expects a reply
- After a meeting with action items assigned to others
- Morning briefing — surface overdue follow-ups
- User asks "what am I waiting on?", "who owes me?"

## Behavior

1. **Auto-suggest** — After user sends an email, ask "Want me to track a follow-up for this?"
2. **Morning surface** — During briefing, list overdue and due-today items
3. **Nudge ready** — When a follow-up is overdue, offer to draft a nudge email
4. **Complete on signal** — If an email arrives from the tracked contact about the tracked subject, suggest marking it complete

## Data Model

Each follow-up tracks:
- **Contact** — who you're waiting on
- **Subject** — what you're waiting for
- **Due date** — when it's expected
- **Status** — pending, completed
- **Notes** — optional context
- **Outcome** — what happened (when completed)
