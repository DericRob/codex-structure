# Platform Migration Notes

Goal: rebuild an assistant product's capabilities inside another agent platform using native patterns such as skills, rules, and workflows.

Key mapping:

- Thinking frameworks map well to instructions-only skills
- Ecosystem integrations map naturally to skills plus scripts
- Messaging, voice, trading execution, and some persistence patterns need custom work

Important difference:

An IDE agent is not a messaging bot, so channel abstractions do not transfer directly.
