---
name: intel:gather
description: "Deep research and data gathering for a tracked entity. Usage: /intel:gather [entity-name]"
argument-hint: "[entity-name]"
---

<objective>
Run a deep intel gathering pass on a specific entity. Updates all dossier files with fresh data using parallel sub-agents.
</objective>

<process>
1. **Resolve entity** — Match `$ARGUMENTS` against `~/.claude-shared/intel/REGISTRY.md`. If no match, check if it's a new entity and offer to initialize it first. If no argument, ask which entity.

2. **Read current state** — Read all files in `~/.claude-shared/intel/{slug}/` to know what you already have and what's missing or stale.

3. **Spawn parallel research agents** — Launch 3 background agents simultaneously:

   **Agent 1 — Company & Product:**
   ```
   Research {entity}: company background, founding story, team size,
   funding, product features, pricing tiers, recent changes, roadmap
   (if public). Update:
   - ~/.claude-shared/intel/{slug}/ABOUT.md
   - ~/.claude-shared/intel/{slug}/PRODUCT.md
   Format: bullet points, sourced where possible.
   ```

   **Agent 2 — Technical:**
   ```
   Research {entity}: tech stack, architecture (if known), API capabilities,
   integrations, SDKs, developer experience, known limitations.
   Update: ~/.claude-shared/intel/{slug}/TECH.md
   Format: bullet points, sourced where possible.
   ```

   **Agent 3 — Market & Competitive:**
   ```
   Research {entity}: market position, key competitors, differentiators,
   user sentiment, known pain points, recent news or pivots.
   Append findings to: ~/.claude-shared/intel/{slug}/NOTES.md
   under a [YYYY-MM-DD] Market Research header.
   ```

   All three use `run_in_background: true`.

4. **Update INDEX.md** — Set `Last Updated` to today's date.

5. **Update REGISTRY.md** — Update the `Last Updated` column.

6. **Confirm** — `Gathering intel on {entity}. 3 research agents running in background.`
</process>
