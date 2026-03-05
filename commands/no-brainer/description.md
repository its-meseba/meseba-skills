---
name: no-brainer:description
description: Generate an executive summary and update a Linear issue description with it. Use when starting a task — takes the issue content, distills it to Problem/Solution/Impact, and prepends it to the Linear issue description. Trigger when user says "update this issue", "add summary to issue", shares a Linear issue and wants it clarified, or is about to start working on an issue and wants the description cleaned up.
argument-hint: "[paste issue content or Linear issue ID/URL]"
---
<objective>
Generate a concise executive summary from the provided input and update the Linear issue description — prepending the summary at the top with existing content below.
</objective>

<context>
Input: $ARGUMENTS (if empty, ask "Which issue? Paste the content or share the Linear issue ID/URL.")
</context>

<process>
1. **Parse the input.** Determine if the user provided:
   - Raw text/content → use it directly for summarization
   - A Linear issue ID or URL → fetch the issue via Linear MCP tools first
   - Also fetch issue comments/activity for additional context
   - **Analyze images from comments:** When image URLs are present (markdown `![...](<url>)` format), use `WebFetch` on each URL immediately (signed URLs expire in ~5 min) — then `Read` the downloaded file path to visually analyze charts/screenshots and extract data points for the summary

2. **Read the input carefully.** Understand the full picture before summarizing.

3. **Identify the macro.** Ask yourself:
   - "If I had 10 seconds to explain this to a CEO, what would I say?" → Problem
   - "What are we doing about it?" → Solution
   - "Why should anyone care?" → Impact

4. **Write the summary** in this exact format:

```markdown
# Executive Summary

1. **Problem:** [One sentence — what's broken or missing]
2. **Solution:** [One sentence — the approach or path forward]
3. **Impact:** [One sentence — what changes when this is done]

**Context**

[One paragraph max. Supplementary only — the 3 points above must stand on their own.]

---
```

Formatting rules:
- `# Executive Summary` is always an H1 header
- Problem, Solution, Impact are a numbered ordered list (1. 2. 3.) with bold labels
- No divider before Context — it flows naturally after the 3 points
- Divider (`---`) goes AFTER Context, before any remaining content below
- Context section is optional — only include when genuinely useful. If no context, no divider either

5. **Present the summary** to the user for confirmation before updating.

6. **Update the Linear issue:**
   - Fetch the current issue description via Linear MCP (`get_issue`)
   - Prepend the executive summary at the top
   - The `---` divider after Context separates the summary from previous content
   - Update the issue via Linear MCP (`save_issue`)
   - Confirm: "Updated [ISSUE-ID]: [issue title]"

## Quality Checks
- Each point is ONE sentence. No compound sentences with semicolons. No "and also."
- Problem states what's broken — not symptoms, not history
- Solution states the approach — not implementation details, not a task list
- Impact states what changes — in measurable or observable terms
- Always show the summary before updating — never update blind
</process>
