# Modes — Output Type Picker

Each mode adds structural rules on top of the shared voice file. Voice answers "how does Semih sound?"; mode answers "how is *this kind of doc* shaped?".

| Mode | File | Use for | Status |
|---|---|---|---|
| `report` | `report.md` | analysis docs, audit findings, Notion data reports, anything with chapters / methodology / numbers | populated v1 |
| `blog` | `blog.md` | blog posts, public-facing essays, long-form thought pieces | stub — needs first sample |

## How to pick a mode

1. **Destination tells you** most of the time. Notion page with chapters → `report`. Public blog → `blog`. Slack #general post → ask Semih (might be a TBD `slack-message` mode).
2. **If destination is unclear**, ask: "Is this a report (numbers + analysis + recommendations) or a blog (narrative + opinion + reader hook)?"
3. **If a doc legitimately straddles two modes** (e.g. "blog post about a data finding") → load both files, then prefer report-mode for the data sections and blog-mode for the framing/hook.

## Adding a new mode

Create `modes/<mode>.md` with these sections (skip the ones that don't apply):

```markdown
# Mode — <Name>

## When to use
## Required structure
## Optional sections
## Formatting rules (length, blocks, links)
## Always-on
## What to avoid
```

Then add a row to the table above. New modes ship as stubs and get populated as Semih writes the first real instance — same pattern as voice files.
