---
name: intel:list
description: Show all tracked entities with status, last updated, and completeness indicator.
---

<objective>
Display a compact overview of all tracked intel entities.
</objective>

<process>
1. **Read REGISTRY.md** at `~/.claude-shared/intel/REGISTRY.md`. If it doesn't exist, say `No entities tracked yet. Use /intel:initiate to start.`

2. **For each entity**, check file completeness:
   - Read each file (INDEX.md, ABOUT.md, PRODUCT.md, TECH.md, NOTES.md)
   - Score: Empty (just header) = missing, Has content = present
   - Completeness = filled files / 5

3. **Display as table:**
   ```
   # Tracked Intel

   | Entity | Type | Last Updated | Completeness |
   |--------|------|--------------|--------------|
   | linear | Product | 2026-03-19 | 4/5 |
   | stripe | Platform | 2026-03-15 | 5/5 |
   ```

4. **Suggest actions** if any entity has low completeness:
   `stripe has gaps — run /intel:gather stripe to fill in.`
</process>
