---
name: no-brainer:brief
description: Prepare to communicate a topic to executives or C-level colleagues. Reads Linear issue context (including related/blocking issues and activity), generates an executive summary, and provides talking points with the main narrative flow. Use when the user says "brief me", "help me explain this", "I need to present this", "prepare me for a meeting", "how do I explain this to my CEO/CTO", or needs to communicate a technical or product topic to leadership clearly.
argument-hint: "[Linear issue ID/URL or topic to explain]"
---
<objective>
Help the user communicate a topic to executive/C-level colleagues. Generate an executive summary enriched with Linear context, then provide a structured talking flow so the user walks into the conversation prepared — leading with the macro, not drowning in micro.
</objective>

<context>
Input: $ARGUMENTS (if empty, ask "What topic do you need to explain? Share a Linear issue or describe the situation.")
</context>

<process>
1. **Gather context from Linear.** This is what makes brief different from summary — it pulls in the bigger picture:
   - Fetch the main issue via Linear MCP (`get_issue` with `includeRelations: true`)
   - Fetch comments/activity on the issue (`list_comments`) — these often contain the real decisions and data
   - **Analyze images from comments:** Comments often contain charts, screenshots, and data visualizations. When image URLs are present in comments (markdown `![...](<url>)` format):
     1. Use `WebFetch` on each image URL immediately (signed URLs expire in ~5 minutes) — this downloads to a local temp file
     2. Use `Read` on the downloaded file path (returned in the WebFetch output) to visually analyze the image
     3. Extract key data points, trends, and insights from charts/graphs to strengthen the summary with real numbers
     4. **Fetch all images in parallel** — call `WebFetch` on all image URLs in the same turn to beat URL expiration
   - **Parallel subagents for multi-issue context:** When there are blocking/related issues or multiple issues to analyze:
     - Spawn an **"issue-context-gatherer"** subagent per related issue — each reads the issue, its comments, and downloads/analyzes any images
     - Spawn an **"image-analyzer"** subagent when there are 3+ images to process — it fetches all URLs via WebFetch, reads the downloaded files, and returns a summary of visual insights
     - Spawn a **"cycle-scanner"** subagent to list open issues in the same project/cycle and return titles + status for the "related work in flight" section
     - Run all subagents in parallel to minimize wait time
   - Only go deep (full description + comments) on issues that are directly relevant to the narrative

2. **Build the executive summary** using the standard no-brainer format:

```markdown
# Executive Summary

1. **Problem:** [One sentence — what's broken or missing]
2. **Solution:** [One sentence — the approach or path forward]
3. **Impact:** [One sentence — what changes when this is done]

**Context**

[One paragraph max. Include relevant links, related issues, dependencies, or prior decisions that an executive would want to know. Reference related Linear issues by ID when relevant.]

---
```

3. **Provide talking points.** After the executive summary, add a section that helps the user navigate the conversation:

```markdown
## Talking Flow

**Lead with:** [The one sentence that frames the entire conversation — this is what you say first]

**If they ask "why now?":** [Why this is urgent or timely — data point or business trigger]

**If they ask "what's the risk?":** [What happens if we don't do this, or what could go wrong]

**If they ask "what do you need?":** [The specific ask — resources, approval, time, decision]

**Related work in flight:**
- [ISSUE-ID] Issue title — [one-line relevance to this topic]
- [ISSUE-ID] Issue title — [one-line relevance]
```

4. **Present everything** to the user in the conversation.

5. **Generate an HTML briefing page** and save it to `/tmp/brief-<ISSUE-ID>.html` (e.g., `/tmp/brief-JOY-1510.html`). Then open it with `open /tmp/brief-<ISSUE-ID>.html`.

   The HTML must be a single self-contained file — no external dependencies. Design it as a polished, readable briefing document:

   **Visual Design Requirements:**
   - **Light theme** with a clean white/off-white background (`#FAFAFA` or similar)
   - **High contrast** — dark text (`#1A1A1A`) on light backgrounds, never gray-on-gray
   - **System font stack** — `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
   - **Comfortable reading width** — max `720px`, centered, with generous padding
   - **Clear visual hierarchy** — the 3-point summary should be the dominant element, scannable in 5 seconds

   **Structure:**
   - **Header:** Issue ID as a subtle label, issue title as the main heading
   - **Executive Summary section:** The 3 points (Problem, Solution, Impact) in a visually distinct card or panel with a subtle left border accent (use a calm blue like `#2563EB`)
   - **Context section:** If present, below the summary in a lighter, secondary style
   - **Talking Flow section:** Each talking point as its own card/block — the trigger question (`"If they ask..."`) as a bold label, the answer below. Use subtle background differentiation between cards
   - **Related Work section:** Clean list with issue IDs as monospace badges

   **Typography:**
   - Title: `1.75rem`, bold, `#1A1A1A`
   - Section headers: `1.1rem`, semibold, `#374151`
   - Body text: `1rem`, `#1A1A1A`, line-height `1.7`
   - Labels/badges: `0.8rem`, uppercase, letter-spaced, `#6B7280`

   **Key principle:** This is a document someone glances at on their phone before walking into a meeting. Every section should be instantly scannable. Use whitespace generously — breathing room between sections. No clutter.

## Principles

- **Macro first, always.** The executive doesn't care about implementation details. They care about: what's the problem, what are we doing, what changes.
- **Anticipate questions.** Executives ask "why now?", "what's the risk?", and "what do you need from me?" — have answers ready.
- **Use data when available.** Pull numbers from issue comments/activity. "CVR drops 40%" beats "it's not performing well."
- **Connect to the bigger picture.** Show how this relates to other work in flight. Executives think in portfolio, not individual tasks.
- **Keep the "lead with" sentence short enough to say in one breath.** If you can't, it's too complex — simplify.

## Quality Checks
- Each summary point is ONE sentence
- Talking flow answers the 3 questions executives always ask
- Related work section only includes genuinely relevant issues (not everything in the backlog)
- The "lead with" sentence passes the elevator test — you could say it between floors
</process>
