# Wave 1 — Research Agent Prompt Template

Use this template verbatim for each of the N research agents dispatched in Phase 2. One agent per domain slice. All agents launched in a **single assistant turn** (multiple `Agent` tool calls in one message) so they run in parallel.

## Critical design rule

**The denylist MUST be inlined verbatim into every agent's prompt.** Subagents live in isolated contexts — they cannot see files outside their prompt, cannot read other agents' outputs, cannot inherit constraints from the orchestrator. Duplicate the full denylist into each agent call. This is not redundancy; it's the only enforcement mechanism you have.

## Template (copy and fill)

```
You are Agent {{LETTER}} of a {{N}}-agent parallel research team. Your job: extract the user's professional accomplishments from their Claude Code session history so they can write blog posts about their work.

## Your scope: {{SLICE_NAME}}

Read session logs and memory files from these project directories:
{{LIST_OF_ABSOLUTE_PATHS}}

Also check for a `memory/` subdir inside any of those — memory files are pre-distilled facts.

## Data format
Each project dir contains `.jsonl` session files (one JSON object per line, with role/content structure — user messages, assistant messages with tool calls, tool results). May also contain `memory/` with markdown files.

## Method (CRITICAL — conserve context)
DO NOT read `.jsonl` files directly with the Read tool. They are huge and will flood your context. Use `ctx_execute` (context-mode MCP) or equivalent sandbox to process them, returning only summaries.

Recommended per-project pipeline:
1. `ls` the project dir via ctx_execute — count jsonl files, sort by mtime.
2. For each jsonl, extract ONLY user messages (`o["type"] == "user"` and content is a string, not a tool result). Take first 10–15 per session — they reveal the user's INTENT for that session.
3. Also extract assistant messages containing outcome phrases: "## Summary", "I've", "I built", "I shipped", "I deployed", "I added", "I fixed", "Done".
4. Read all markdown files in any `memory/` subdir in full — those are distilled facts.

Sandbox snippet to adapt per project:
```python
import json, os, glob
root = "{{PROJECT_PATH}}"
for f in sorted(glob.glob(f"{root}/*.jsonl"), key=os.path.getmtime):
    msgs = []
    with open(f, errors='ignore') as fh:
        for line in fh:
            try: o = json.loads(line)
            except: continue
            if o.get("type") == "user":
                c = o.get("message",{}).get("content")
                if isinstance(c, str) and len(c) < 2000:
                    msgs.append(c[:400])
                if len(msgs) >= 12: break
    if msgs:
        print(f"=== {os.path.basename(f)} mtime={os.path.getmtime(f)} ===")
        for m in msgs[:12]: print(f"- {m[:200]}")
```

Keep your final answer focused — you're extracting BLOG MATERIAL, not a full history log.

## Denylist (strip these from your output)

Do not mention any of these product/company/codenames in your findings (skill names by function are fine):
{{INLINED_DENYLIST_FULL_VERBATIM}}

Before writing, note the names to strip, and use generic framings:
- "a subscription SaaS I ship for" instead of "{{PRODUCT_X}}"
- "the internal dashboard I build" instead of "{{INTERNAL_TOOL_Y}}"
- "my indie-app portfolio" instead of "{{SIDE_PROJECT_BRAND}}"

## Output

Write ONE file: `{{OUTPUT_PATH}}/{{0N}}-{{slice-name}}.md`

Use this exact structure:

```
# Agent {{LETTER}} — {{SLICE_NAME}}
> Date: {{TODAY}}

## 1. Projects touched
> For each project: one-line what-it-is, what was built, rough date range (from file mtimes). No brand names — use generic referents.

## 2. Professional accomplishments (user-facing outcomes)
> Shipped features, systems made live, experiments run, measurable wins. Lead each bullet with the outcome, not the activity.

## 3. Technical work delivered
> Systems designed, integrations wired, migrations executed, architectures chosen. Stack / framework names ARE fine; product names are NOT.

## 4. Decisions & trade-offs
> Non-obvious calls — what was considered, what was chosen, what was rejected and why. Blog gold.

## 5. Tooling, skills & patterns demonstrated
> Things that would appear on a "how I work" / "lessons learned" post.

## 6. Stories worth blogging
> Specific incidents, debugging sagas, refactors, "aha" moments. Detailed enough to draft a post from each bullet.

## 7. Timeline anchors
> Chronological list: `YYYY-MM-DD — [what happened]`.

## 8. Data gaps / caveats
> What you could NOT determine from the logs.
```

Each section should be rich with SPECIFIC facts — NOT generic. Extract proper nouns that are tools/SDKs/frameworks (those are fine). Strip proper nouns that are product/company names.

Target length: 800–2000 words of distilled content. Don't pad. Write so the final section (stories) has enough detail that a blog post could be drafted from each bullet.

Report back with: file path + one-sentence summary of what you found + confirmation that the denylist returned zero hits in your output.
```

## Variations for specific slice types

### Meta-engineering / tooling slice
If the slice is about the user's own Claude Code toolkit (skills, hooks, agent patterns), add to the template:

```
## Also read
- `~/.claude-shared/skills/` — every subdir is a skill. List them, skim the SKILL.md header of each custom-authored one.
- `~/.claude-shared/agents/` if present
- `~/.claude-shared/settings.json` — scan hooks, commands, env vars
- `~/.claude-shared/hooks/` if present
- `~/Library/Application Support/Claude/claude_desktop_config.json` — list MCP integrations
```

### Personal / cross-cutting slice
If the slice is about working cadence and cross-cutting patterns, add:

```
## Also analyze
- `~/.claude*/history.jsonl` — one-line-per-prompt logs. Process via ctx_execute; bucket by keyword.
- Active days vs total days; hour-of-day and weekday distribution; per-project activity share.
```

## Why this template works

- **Denylist inlined per-agent** — enforcement must travel in the prompt, not in a file.
- **Sandbox-first processing** — prevents context flooding on multi-GB jsonl dirs.
- **Fixed output structure** — makes the synthesis phase mechanical; predictable bullet locations.
- **First 10–15 user messages per session** — that's where intent lives; assistant responses are where outcomes live.
- **Section-numbered headers** — lets the synthesis extractor find sections by number even if the agent rewords slightly.
