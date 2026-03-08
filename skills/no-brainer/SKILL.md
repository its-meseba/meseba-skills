---
name: no-brainer
description: Boil down any input into a 3-point executive summary (Problem, Solution, Impact) plus optional Context. Three sub-skills — `no-brainer:summary` presents the summary, `no-brainer:description` updates a Linear issue with it, `no-brainer:brief` prepares you to communicate a topic to executives with full Linear context. Use when the user shares something verbose and wants the core takeaway distilled, says "summarize", "break this down", "tldr", "executive summary", "brief me", or pastes a wall of text needing clarity.
---

# No-Brainer

Turn any input into a crystal-clear executive summary. Three points, no fluff.

## Why This Exists

People drown in details. Whether it's a Linear issue, a meeting recap, or a Slack thread — the actual point gets buried. This skill forces macro clarity: what's broken, how to fix it, and what changes when you do.

## The Format

Every summary follows this exact structure:

```markdown
# Executive Summary

1. **Problem:** [One sentence — what's broken or missing]
2. **Solution:** [One sentence — the approach or path forward]
3. **Impact:** [One sentence — what changes when this is done]

**Context**

[One paragraph max. Include relevant links, prior decisions, or technical constraints. Supplementary — the 3 points above must stand on their own.]

---
```

Formatting rules:
- `# Executive Summary` is always an H1 header
- Problem, Solution, Impact are a numbered ordered list (1. 2. 3.) with bold labels
- No divider before Context — it flows naturally after the 3 points
- Divider (`---`) goes AFTER Context, before any remaining content below
- Context section is optional — only include when genuinely useful

## How to Write Each Point

### Problem
State what's broken, missing, or blocking — not symptoms, not history. One sentence.
- Bad: "Users have been complaining about the checkout flow and we've seen a 12% drop in conversions over the last quarter"
- Good: "Checkout abandonment is 40% because the payment step requires 6 form fields"

### Solution
State the approach — not implementation details, not a task list. One sentence.
- Bad: "We need to create a new React component that integrates with Stripe's v3 API and handles card tokenization"
- Good: "Reduce payment to a single-step card input with Stripe's hosted checkout"

### Impact
State what changes — in measurable or observable terms. One sentence.
- Bad: "This will improve the user experience and make things better"
- Good: "Recover ~15% of abandoned checkouts, estimated $50K/month in recovered revenue"

## Core Process

1. **Read the input carefully.** Understand the full picture before summarizing.
2. **Identify the macro.** "If I had 10 seconds to explain this to a CEO, what would I say?" — Problem. "What are we doing about it?" — Solution. "Why should anyone care?" — Impact.
3. **Write the 3 points.** Each a single sentence. No compound sentences. One idea per line.
4. **Decide on Context.** Genuinely useful background? Add it. Otherwise skip.

## Sub-Skills

| Command | Purpose |
|---------|---------|
| `/no-brainer:summary` | Just present the executive summary — no Linear updates |
| `/no-brainer:description` | Generate summary + update Linear issue description |
| `/no-brainer:brief` | Full executive communication prep — reads Linear context, gives talking points |
| `/no-brainer:help` | Show help — what No-Brainer does and how to use it |

## Help (`/no-brainer:help`)

When this sub-command is invoked, present the following to the user:

---

### No-Brainer

Distills any input into a 3-point executive summary: **Problem, Solution, Impact** — plus optional Context. Feed it a wall of text, get back the core takeaway.

#### The Format

Every summary follows this structure:

```
1. Problem:   [One sentence — what's broken or missing]
2. Solution:  [One sentence — the approach or path forward]
3. Impact:    [One sentence — what changes when this is done]

Context: [One paragraph max — links, prior decisions, constraints. Optional.]
```

#### Commands

| Command | What it does |
|---------|-------------|
| `/no-brainer` or `/no-brainer:summary` | Present the executive summary only |
| `/no-brainer:description` | Generate summary + update a Linear issue description with it |
| `/no-brainer:brief` | Full executive communication prep — reads Linear context, gives talking points for presenting to leadership |

#### When to use

Say "summarize this", "tldr", "break this down", "executive summary", or just paste a wall of text. Works on meeting recaps, Slack threads, Linear issues, technical writeups — anything verbose that needs the core point extracted.

#### What it's NOT

- Not a detailed analysis tool — it distills, not expands
- Not a project plan — it clarifies "what" and "why", not "how in 47 steps"
- Not a meeting notes formatter — it extracts the core point, not a chronological recap

## What This Skill is NOT

- Not a detailed analysis tool — it distills, not expands
- Not a project plan — it clarifies "what" and "why", not "how in 47 steps"
- Not a meeting notes formatter — it extracts the core point, not a chronological recap
