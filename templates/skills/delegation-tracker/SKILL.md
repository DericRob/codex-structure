# Delegation Tracker

Delegate tasks to people and track accountability — assignee, due date, priority, status updates.

## When to Use

- User says "assign this to...", "delegate to...", "have X do Y"
- User asks "what have I delegated?", "who's working on what?"
- Morning briefing — surface overdue delegations
- User needs to update delegation status or add notes

## Behavior

1. **Track assignments** — Record assignee, description, due date, and priority
2. **Surface overdue** — During briefing, flag delegations past their due date
3. **Status workflow** — assigned → in_progress → completed (or overdue if past due)
4. **Priority levels** — high, medium, low — used for sorting and alerting
5. **Notes trail** — Each update can include notes for accountability record

## Data Model

Each delegation tracks:
- **Assignee** — who is doing the work
- **Description** — what needs to be done
- **Due date** — when it's expected
- **Priority** — high, medium, low
- **Status** — assigned, in_progress, completed, overdue
- **Notes** — context and updates
- **Created at** — when the delegation was made
