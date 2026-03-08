---
name: founderbrain-openclaw
description: Bootstrap a FounderBrain OpenClaw workspace with 9 core strategic skills, skill router, founder system prompt, and memory layer templates. Use when the user asks to initialize or rebuild a founder-style AI agent stack quickly and safely in a new workspace.
---

# FounderBrain OpenClaw

Install FounderBrain templates into a target workspace.

## Steps

1. Ask for target workspace path.
2. Run `scripts/install_templates.sh <target>`.
3. Confirm these paths exist in the target:
- `skills/`
- `router/skill_router.py`
- `prompts/founder_agent_prompt.md`
- `memory/*.json`
- `agent/IDENTITY.md`, `agent/TOOLS.md`, `agent/MEMORY.md`

## Safety

- Always back up existing destination paths before overwrite.
- Never write outside the user-provided target path.
