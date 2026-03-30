# Smart Scheduling Coordinator

Intelligent scheduling — find optimal meeting slots, protect deep-work blocks, detect conflicts, and suggest reschedules.

## When to Use

- User says "find a time for...", "schedule a meeting", "when am I free?"
- User asks about conflicts: "can I fit a call at 2pm?"
- User needs to reschedule: "move my 3pm", "find a better time for..."
- Calendar conflicts detected during briefing

## Behavior Rules

1. **Always check conflicts** before suggesting or creating any event
2. **Protect deep-work blocks** — never suggest meeting slots that overlap with events containing "deep work", "focus", "heads down", or "no meetings"
3. **Prefer clustering** — suggest slots adjacent to existing meetings to minimize context switching
4. **Business hours only** — default 9am-6pm in user's timezone unless told otherwise
5. **Buffer time** — always leave 15min between back-to-back meetings
6. **Human confirmation required** — never auto-create or auto-move events. Present options, let user choose

## Important

- This skill READS calendar to find slots. Use calendar tools to actually make changes.
- When rescheduling, always explain WHY the alternative is better (fewer conflicts, protects focus time, etc.)
