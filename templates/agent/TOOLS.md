# Founder Agent Tooling

Internal capabilities:
- Skill routing via router/skill_router.py
- Skill modules in skills/*.md
- Prompt frame in prompts/founder_agent_prompt.md
- Persistent memory in memory/*.json

Execution policy:
- Slash commands like /think or /kill can force a route.
- Natural language should auto-route.
- Log: original message, selected skill, routing reason.
