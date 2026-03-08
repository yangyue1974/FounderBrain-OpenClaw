# Founder Agent Skill System Spec

## Skill map

- industry signals -> decision_radar
- macro trends -> trend_distiller
- opportunities -> opportunity_scanner
- product ideas -> idea_forge
- product evaluation -> product_killer
- founder decisions -> founder_mode
- personal reflection -> personal_os
- music discovery -> taste_curator
- ambiguous/deep thinking -> second_brain

## Router behavior

1. Respect explicit slash command aliases.
2. Otherwise score all skills with keyword + heuristic rules.
3. Select best match.
4. If confidence is low, fallback to `second_brain`.
5. Keep selected skill internal (not exposed to end user).

## Response behavior

- Strategic, concise, analytical
- Structured output when useful
- No generic filler

## Memory layer

Files:
- `memory/insights.json`
- `memory/experiments.json`
- `memory/preferences.json`
- `memory/models.json`
- `memory/model_history.json`

Write memory only for:
- strong beliefs
- concrete experiment outcomes
- stable preferences
- durable strategic models

## Optional APIs

- `POST /v1/memory/compress`
- `POST /v1/memory/belief_update`

Use these to compress insights into models and update models with new evidence.
