---
name: intel:automate
description: "Enable continuous background intel tracking by adding a directive to the user's global CLAUDE.md. Makes every session intel-aware so observations are captured automatically."
---

<objective>
Add a compact, non-intrusive directive to the user's global CLAUDE.md that tells Claude to passively track intel during all sessions.
</objective>

<process>
1. **Read the user's global CLAUDE.md** at `~/.claude-shared/CLAUDE.md`.

2. **Check if intel automation is already present** — search for `INTEL_AUTOMATION` or `intel/` references. If already there, say `Intel automation is already active.` and stop.

3. **Read REGISTRY.md** to get the list of currently tracked entities.

4. **Append this block** to the end of the global CLAUDE.md:

```markdown

---

## INTEL_AUTOMATION

When you notice information about any of these tracked entities flowing through a session — pricing, features, API details, limitations, team changes, user complaints — silently append a timestamped bullet to `~/.claude-shared/intel/{entity-slug}/NOTES.md`. No announcement, no interruption. Use a background agent if needed.

Tracked entities are listed in `~/.claude-shared/intel/REGISTRY.md`. Check it at session start if the user's work involves competitors or product analysis.

If you encounter a product/company that seems like the user would want to track but isn't in the registry, mention it once: `"Want me to track {entity}? /intel:initiate"`

Available commands: `/intel:initiate`, `/intel:gather [entity]`, `/intel:list`, `/intel:automate`
```

5. **Confirm** — `Intel automation added to global CLAUDE.md. All future sessions will passively track intel for registered entities.`
</process>
