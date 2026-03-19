---
name: intel:initiate
description: Scan current context for products/companies being discussed, ask which to track, create dossier structure, and run initial research to populate files.
---

<objective>
Detect products/companies in the current conversation context, confirm with the user which ones to track, create their intel dossier, and populate it with initial research.
</objective>

<process>
1. **Scan context** — Look at the current conversation, open files, project name, CLAUDE.md, package.json, and any other signals. Extract every product, company, service, or platform mentioned or implied.

2. **Present candidates** — Show the user a compact list:
   ```
   Detected in context:
   - Linear (project management) — mentioned in issues
   - Stripe (payments) — imported in codebase
   - Vercel (deployment) — in package.json
   Track all? Or pick: [numbers]
   ```

3. **For each confirmed entity, create the dossier:**

   a. Generate the slug (lowercase, hyphenated)

   b. Create directory: `~/.claude-shared/intel/{slug}/`

   c. Create INDEX.md with the template from SKILL.md, filled with what you already know

   d. Create empty ABOUT.md, PRODUCT.md, TECH.md, NOTES.md with just a `# {Section}` header

   e. Add entry to `~/.claude-shared/intel/REGISTRY.md` (create if missing)

4. **Run initial research** — For each entity, spawn a background Agent:
   ```
   Research {entity}: company overview, product features, pricing model,
   tech stack (if known), key differentiators. Write findings directly to:
   - ~/.claude-shared/intel/{slug}/ABOUT.md
   - ~/.claude-shared/intel/{slug}/PRODUCT.md
   - ~/.claude-shared/intel/{slug}/TECH.md
   Keep it compact — bullet points, no prose. Every line must be a fact.
   ```
   Use `run_in_background: true` so the user isn't blocked.

5. **Confirm** — One line: `Initialized {N} entities. Research running in background.`

6. **Log** — Add a timestamped entry to each entity's NOTES.md:
   ```
   [YYYY-MM-DD] Initialized tracking. Source: session context.
   ```
</process>
