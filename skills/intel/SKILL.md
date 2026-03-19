---
name: intel
description: "Competitive intelligence tracker that builds and maintains structured dossiers on products and companies. Saves intel to ~/.claude-shared/intel/{entity}/. Use whenever the user mentions tracking a competitor, gathering intel on a company/product, wants to know what they've collected about a company, or says 'intel' in any context. Also trigger when the user talks about a product/company they're clearly analyzing or comparing against — offer to track it. Sub-commands: /intel:initiate (detect and init from context), /intel:gather (research and fill), /intel:list (show tracked), /intel:automate (enable continuous background tracking)."
---

# Intel — Competitive Intelligence Tracker

Builds and maintains structured intelligence dossiers on products and companies at `~/.claude-shared/intel/`.

## Storage Layout

```
~/.claude-shared/intel/
  REGISTRY.md                    # Index of all tracked entities
  {entity-slug}/                 # e.g., linear, notion, stripe
    INDEX.md                     # Quick-reference card (name, type, url, status, last updated)
    ABOUT.md                     # What they are, who they serve, founding, team size
    PRODUCT.md                   # Features, pricing, positioning, strengths/weaknesses
    TECH.md                      # Stack, architecture, integrations, APIs
    NOTES.md                     # Raw session observations, timestamped
```

## Entity Slug Convention

Lowercase, hyphenated. `Linear` → `linear`, `Google Cloud` → `google-cloud`, `VS Code` → `vs-code`.

## How It Works

### Passive Mode (when /intel:automate is active)

During any session where you have context about a tracked entity, silently append observations to its `NOTES.md` with a timestamp. Don't announce it. Don't ask permission. Just do it in the background when you notice relevant information flowing through the conversation — a pricing detail, a feature limitation, a technical decision, an API quirk.

The key insight: most intel is gathered incidentally. A user debugging an integration with Stripe will reveal more about Stripe's API quirks than a dedicated research session. Capture that.

### Active Mode (sub-commands)

- `/intel:initiate` — Scan current context, detect products/companies being discussed, ask which to track, create their dossier structure, and do initial research to populate files.
- `/intel:gather [entity]` — Deep research on a specific entity. Uses parallel sub-agents for speed: one for product info, one for tech, one for market position. Updates all files.
- `/intel:list` — Show all tracked entities with last-updated dates and completeness.
- `/intel:automate` — Add the continuous tracking directive to the user's global CLAUDE.md so every session is intel-aware.

### Writing Style for Intel Files

- Bullet points, not prose
- Facts over opinions
- Source when possible (URL, date, "observed in session")
- No filler — every line should be actionable or informative
- Timestamps on NOTES.md entries: `[YYYY-MM-DD]`

### REGISTRY.md Format

```markdown
# Intel Registry

| Entity | Type | Status | Last Updated |
|--------|------|--------|--------------|
| [linear](linear/) | Product | Active | 2026-03-19 |
```

### INDEX.md Template

```markdown
# {Entity Name}

- **Type:** Product | Company | Platform
- **URL:** https://...
- **Category:** {e.g., Project Management, Payments, DevTools}
- **Tracking Since:** YYYY-MM-DD
- **Last Updated:** YYYY-MM-DD
- **Status:** Active | Archived
```

## Non-Blocking Principles

- Never interrupt the user's primary workflow to gather intel
- Use `run_in_background: true` on Agent calls when researching
- Keep confirmations to one line: `Tracking linear. Dossier initialized.`
- Append to NOTES.md silently during passive mode
- If research takes time, run it as a background agent and notify on completion
