---
name: mini-decade
description: "MiniDecade goal achievement and mastery tracking system for Obsidian. Manages long-term learning plans, tracks progress against goals, researches resources, and suggests next actions. Use whenever the user mentions goals, achievements, learning paths, curriculum, quarterly plans, progress reviews, field mastery, MiniDecade, 'what should I work on', 'how am I progressing', 'find resources for', 'update my plan', 'review my quarter', or any long-term skill development topic. Also trigger when setting weekly goals (connects to daily-brain skill), when the user asks to review their trajectory, or when they want to start learning something new. Even casual mentions like 'I want to get better at X' or 'what's next for my AI engineering path' should trigger this skill."
---

# MiniDecade — 3-Year Mastery System

You manage the user's MiniDecade system — a 156-week (3-year) mastery framework organized into 12 quarters. Each week produces a "brick" (a shipped artifact). The weekly cadence is: **Mon Plan, Tue-Thu Build, Fri Ship, Sat-Sun Reflect**. The system lives in their Obsidian vault and connects to the daily-brain skill for daily logging.

## Vault Location

```
/Users/mehmetsemihbabacan/dev/brain/
```

## Vault Structure

```
Work/Mine/MiniDecade/
  0. What is MiniDecade/              # Methodology docs (read-only reference)
  [Field Name]/                        # e.g., "AI Engineering"
    0. Plan.md                         # Living plan — THE core document
    Resources/                         # Books, articles, courses, videos
      [Resource Name].md
    Progress/                          # Weekly/monthly progress snapshots
      YYYY-MM-DD.md
    Artifacts/                         # Links to shipped work
      [Artifact Name].md
    Tools/                             # Field-specific tools and integrations
```

### Existing Fields (vault paths)

- AI Engineering → `Work/Mine/MiniDecade/AI Engineering/`
- Context Engineering → `Work/Mine/MiniDecade/Context Engineering/`
- Backend Engineering → `Work/Mine/MiniDecade/Backend Engineering/`
- SaaS Product → `Work/Mine/MiniDecade/SaaS Product/`
- Entrepreneurship → `Work/Mine/MiniDecade/Entrepreneurship/`
- Languages → `Work/Mine/MiniDecade/Languages/`
- Personal Growth → `Work/Mine/MiniDecade/Personal Growth/`

New fields are created as the user develops them (use `/mini-decade:new-field`).

## Plan.md Template

The living plan is THE core document for each field. Always read it before making changes.

```markdown
# [Field Name] — MiniDecade Plan

## Declaration
**Field Type:** Primary / Secondary
**Started:** YYYY-MM-DD
**Target Mastery:** [What "done" looks like]

## Current Quarter (Q[N] YYYY)
**Focus:** [Specific focus for this 12-week season]
**Capstone:** [What I'll ship by end of quarter]

### Weekly Objectives
| Week | Objective | Artifact | Status |
|------|-----------|----------|--------|
| 1    | ...       | ...      | ...    |

## Milestones
- [ ] Milestone 1: [Description] — Target: [Date]

## Skills Map
| Skill | Current Level | Target Level | Gap |
|-------|--------------|-------------|-----|

## Resources Queue
- [ ] [Book/Course/Article] — Priority: High/Med/Low

## Evidence Log
| Date | Artifact | Type | Link | Metrics | Lesson |
|------|----------|------|------|---------|--------|

## Quarterly Reviews
### Q[N] YYYY Review
**Wins:** ...
**Failures:** ...
**Next bets:** ...
```

### Status Emojis

Use these consistently across all plans:
- `⬜` — Not started
- `🟡` — In progress
- `✅` — Done
- `❌` — Dropped

## Core Operations

### A) Creating a New Field

When the user says "I want to start learning X" or "add X as a MiniDecade field":

1. **Interview the user** — Ask about:
   - Current background/experience level in this field
   - How many hours per week they can dedicate
   - What "mastery" looks like to them (the 3-year target)
   - What they want to ship by end of this quarter (12-week capstone)

2. **Create the folder structure:**
```bash
FIELD_PATH="/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/[Field Name]"
mkdir -p "$FIELD_PATH/Resources"
mkdir -p "$FIELD_PATH/Progress"
mkdir -p "$FIELD_PATH/Artifacts"
mkdir -p "$FIELD_PATH/Tools"
```

3. **Generate `0. Plan.md`** using the template above, filled with:
   - Declaration from interview answers
   - Quarterly plan with 12 weekly objectives
   - Initial skills map based on current vs target level
   - First milestones

4. **Research initial resources** using WebSearch:
   - Find 5-10 relevant books, courses, articles, videos
   - Prefer free/open resources first
   - Save each to `Resources/[Resource Name].md` (see Resource format below)
   - Populate the Resources Queue in Plan.md

5. **Create first weekly goals** and push to the daily-brain weekly Goals.md:
   - Use the daily-brain skill's Goals.md format
   - Group goals under the new field name

### B) Updating Plans

When the user completes work, logs learnings (via daily-brain), or reports progress:

1. **Read the relevant field's `0. Plan.md`** — always read before writing
2. **Update weekly objective status** — change ⬜ to 🟡 or ✅ as appropriate
3. **Add to Evidence Log** if an artifact was shipped — include date, type, link, metrics, lesson
4. **Adjust upcoming weeks** if behind or ahead of schedule — keep the plan realistic
5. **Suggest next actions** — what should the user focus on next based on their plan state

### C) Research and Context

When the user asks to find resources or when setting up a new field:

1. **Use WebSearch** to find relevant books, courses, articles, YouTube videos
2. **Save structured notes** to `Resources/[Resource Name].md`:

```markdown
# [Resource Title]

**Author/Source:** [Name]
**URL:** [Link]
**Type:** Book / Course / Article / Video / Tool
**Relevance:** [Why this matters for the field]
**Key Topics:** [Comma-separated list]
**Estimated Time:** [Hours to complete]
**Priority:** High / Med / Low
**Status:** ⬜ Not started

## Notes
[User's notes added as they consume the resource]
```

3. **Update Resources Queue** in the field's Plan.md

### D) Weekly Review

When the user asks "how am I doing" or at the end of the week (Friday-Sunday):

1. **Read daily-brain entries** tagged with this field:
```bash
obsidian-cli search-content "[Field Name]"
```
Also check the current week's daily files directly:
```bash
# Calculate current week folder path
MM_YYYY=$(date "+%m-%Y")
# Determine week number (day 1-7 = Week 1, 8-14 = Week 2, etc.)
```

2. **Read current week's objectives** from the field's Plan.md

3. **Generate summary:**
   - Completed vs planned objectives
   - Lessons learned (extracted from daily entries)
   - Blockers identified
   - Artifacts shipped this week

4. **Suggest adjustments** for next week based on what happened

5. **Save review** to `Progress/YYYY-MM-DD.md`:

```markdown
# [Field Name] — Week [N] Review (YYYY-MM-DD)

## Planned vs Actual
| Objective | Status | Notes |
|-----------|--------|-------|

## Lessons Learned
- ...

## Artifacts Shipped
- ...

## Blockers
- ...

## Next Week Adjustments
- ...
```

### E) Quarterly Review

At the end of each 12-week season:

1. **Aggregate all weekly reviews** from `Progress/` for this quarter
2. **Assess against quarterly goals:**
   - Was the capstone shipped?
   - How much of the skills gap was closed?
   - How many evidence log entries were added?
   - Which milestones were hit/missed?
3. **Draft quarterly review** and append to the Quarterly Reviews section of Plan.md
4. **Propose next quarter's plan:**
   - New focus area
   - New capstone project
   - Updated weekly objectives
   - Adjusted milestones
5. **Ask the user to confirm or adjust** before writing the next quarter

### F) Suggestions Engine

Based on plan state, proactively suggest actions when relevant:

- **Missing artifact:** "You haven't shipped an artifact for [Field] this week yet -- Friday is ship day."
- **Approaching milestone:** "Your [Milestone] is due in 2 weeks -- here's what's left."
- **Learning connections:** "Based on your learning about X, you might want to explore Y."
- **Public building:** "Consider posting about [recent learning] for your weekly public building."
- **Stale field:** "You haven't logged anything for [Field] in 2 weeks -- want to review the plan?"
- **Resource completion:** "You finished [Resource] -- time to update your skills map."

Only suggest when the user is interacting with MiniDecade or asks "what should I work on." Do not spam suggestions unprompted during unrelated tasks.

## Connecting with Daily Brain

The daily-brain skill handles daily logging. MiniDecade connects to it as follows:

- **Field tags:** daily-brain tags entries with `[Field Name]` in square brackets (e.g., `[AI Engineering]`). MiniDecade reads these tags to track progress.
- **Weekly Goals.md:** Lives in the daily-brain folder structure (`Daily Tracking/MM-YYYY/Week N/Goals.md`). MiniDecade populates field-specific goals there.
- **Evidence Log:** When daily-brain captures a shipped artifact, MiniDecade pulls it into the field's Evidence Log.
- **Progress extraction:** Weekly reviews pull tagged entries from daily notes to assess progress.

Do NOT duplicate daily-brain functionality. Use daily-brain for daily logging, use MiniDecade for planning, tracking, and reviewing.

## Tools Integration

### HabitAdd (app.habitadd.com)

The user's habit tracking app. Read `references/habitadd-api.md` for the full API reference.

**What the agent can do:**
- **Read habits and streaks** — Pull completion data for progress reports
- **Log entries** — Record habit completions when user reports them
- **Create habits** — Set up new daily habits from MiniDecade weekly plans
- **Get analytics** — Streak, completion rate, and trend data for reviews

**When to use HabitAdd:**
- Setting up a new MiniDecade field → Create corresponding daily habits
- Weekly review → Pull this week's completion data for all field-related habits
- User reports completing a habit → Log via API
- Monthly/quarterly progress report → Include streak and completion rate data
- User asks "how consistent am I with X" → Pull analytics

**Configuration:**
Store API key at: `Work/Mine/MiniDecade/0. What is MiniDecade/Tools/.habitadd-config.json`

To call the API from Claude Code, use curl:
```bash
curl -X POST "https://us-central1-habits-x.cloudfunctions.net/agentGetHabits" \
  -H "Content-Type: application/json" \
  -d '{"data": {"apiKey": "KEY_FROM_CONFIG"}}'
```

## Quick Reference: obsidian-cli Commands

```bash
# Print a note
obsidian-cli print "note name"

# Search content across vault
obsidian-cli search-content "search term"

# Create a note
obsidian-cli create "path/to/note" --content "content here"

# Open (brings to focus in Obsidian)
obsidian-cli open "note name"

# Append to existing note
obsidian-cli open "note name" --append "content to append"
```

If `obsidian-cli` fails for nested paths, fall back to direct file operations:
```bash
mkdir -p "/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/[Field Name]/Resources"
```
Then write/append to `.md` files directly.

## Commands

These sub-commands can be invoked explicitly for specific operations:

| Command | Purpose |
|---------|---------|
| `/mini-decade:new-field` | Create a new mastery field (interview → structure → plan → resources → goals) |
| `/mini-decade:plan` | Write or update a field's quarterly plan |
| `/mini-decade:review` | Weekly or quarterly review (auto-detects based on date) |
| `/mini-decade:research` | Find and save resources for a field |
| `/mini-decade:progress` | Cross-field dashboard + "what should I work on?" suggestions |
| `/mini-decade:habits` | Sync HabitAdd data, create habits from plan, pull analytics |

Cross-references:
- `/mini-decade:new-field` → ends with `/daily-brain:goals` to set weekly goals
- `/mini-decade:review` → reads daily-brain entries tagged with `[Field Name]`
- `/mini-decade:habits` → uses HabitAdd API reference at `references/habitadd-api.md`
- `/daily-brain:morning` → reads MiniDecade plan state for daily briefing
- `/daily-brain:goals` → reads Plan.md files for field-level goal mapping

## Important Behaviors

- **Always read Plan.md first** — before suggesting changes, updating status, or proposing new objectives, read the current state of the plan
- **Keep plans realistic** — do not over-schedule; if the user has 5 hours/week for a field, plan accordingly
- **Respect the cadence** — Mon Plan, Tue-Thu Build, Fri Ship, Sat-Sun Reflect; suggest actions that match the current day
- **Preserve the user's voice** — plans and reviews should sound like the user wrote them, not corporate boilerplate
- **Free resources first** — when suggesting resources, prefer free/open materials before paid ones
- **One field at a time** — when updating or reviewing, focus on one field unless the user asks for a cross-field overview
- **Always get the real date** — use `date` command, never guess or use stale values
- **Confirm before major changes** — quarterly plan rewrites, dropping milestones, or restructuring objectives require user confirmation
- **Track everything in the vault** — no state lives outside Obsidian; everything is in markdown files the user owns
