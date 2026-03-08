# FounderBrain-OpenClaw

Open-source starter kit for building a Founder Thinking Agent on OpenClaw.

## What is included

- 9 cognitive skills (`skills/*.md`)
- Intent router (`router/skill_router.py`)
- Founder system prompt (`prompts/founder_agent_prompt.md`)
- Memory layer skeleton (`memory/*.json`)
- Agent core docs (`agent/IDENTITY.md`, `agent/TOOLS.md`, `agent/MEMORY.md`)
- Safe installer and uninstaller scripts (`scripts/install.sh`, `scripts/uninstall.sh`)

## Design goals

- Auto-route natural language to the right skill
- Keep skills invisible to end users
- Support slash-command override (`/think`, `/kill`, etc.)
- Persist high-signal founder memory
- Keep installation isolated and reversible

## Quick start

```bash
git clone https://github.com/yangyue1974/FounderBrain-OpenClaw.git
cd FounderBrain-OpenClaw
bash scripts/install.sh /path/to/your/workspace
```

Example:

```bash
bash scripts/install.sh ~/Documents/Hoozi-Founder
```

This copies templates into the target workspace:

- `skills/`
- `router/`
- `prompts/`
- `memory/`
- `agent/`

If destination files already exist, installer creates backups under:

- `.founder-kit-backup/<timestamp>/...`

## Uninstall

```bash
bash scripts/uninstall.sh /path/to/your/workspace
```

This removes installed files listed in `.founder-kit/installed_paths.txt`.
Backups are not deleted automatically.

## OpenClaw integration notes

1. Point your agent workspace to the installed target directory.
2. Load `prompts/founder_agent_prompt.md` as your system prompt.
3. Wire `router/skill_router.py` into your message handling pipeline.
4. Log routing decisions: user message, selected skill, reason.
5. Add low-confidence fallback to `second_brain`.
6. Keep memory writes limited to high-signal entries.

## Safety

- This repo does not auto-modify `~/.openclaw` or running LaunchAgents.
- Installation is file-level only and target-path scoped.

## License

MIT
