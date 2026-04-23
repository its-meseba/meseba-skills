---
name: blog-from-history
description: Turn months of Claude Code session history into a small set of categorized long-form blog-ready essays using two waves of parallel Opus subagents and an enforced name denylist. Use this whenever the user wants to mine their own AI-assisted work history for blog content, write a "year in review" or professional-approach series, distill hundreds of MB of JSONL logs into publishable essays, repurpose session work as thought leadership, or generate cohesive writing from fragmented development activity across multiple projects. Also use when the user says they want to "write about what I've been doing", "turn my Claude Code history into content", "extract my professional approach", or similar — even if they don't say the word "blog".
---

# blog-from-history

Transform a personal Claude Code session-history corpus (typically hundreds of MB across multiple profiles and dozens of projects) into ≤5 categorized long-form blog essays, each ~5,000–8,000 words, with all product and company names stripped so the output reads as a *professional approach* rather than a product catalog.

## Why this skill exists

A developer accumulates enormous amounts of work context inside Claude Code — hundreds of session transcripts, thousands of prompts, dozens of projects. That context is almost always wasted as a writing source because:

1. **The corpus is too big** to fit in one context window.
2. **It's brand-saturated** — raw transcripts name specific products, companies, and internal ticket IDs that aren't publishable as-is.
3. **It's fragmented** — sessions cluster by project, not by theme, so the professional throughlines are invisible without cross-cutting synthesis.

This skill solves all three at once: parallel subagents each get their own 1M context window to mine a domain slice, a middle synthesis pass collapses slices into ≤5 themes, and a second parallel wave drafts full essays with a strict denylist that forces every passage into methodology-framing.

## When to use

Trigger when the user:
- Wants to write a blog series from their own work
- Asks to "turn my history into essays" / "distill what I've been doing"
- Wants a year-in-review, professional-approach summary, or thought-leadership series
- Needs to repurpose fragmented session work as cohesive writing
- Has weeks+ of Claude Code activity and wants to extract professional material from it

Do NOT trigger for: single-topic blog drafts with no personal-history component, generic blog outlining without a history corpus, short-form social content.

## Prerequisites

- **Claude Code** with subagent support (`Agent` tool) — hard requirement
- **Opus 4.7 access** with 1M context — strongly preferred for both waves (1M is the headroom that keeps each agent from flooding out)
- **ctx_execute** (context-mode MCP) or equivalent sandbox — for processing large JSONL files without flooding main context
- **Python 3.9+** on the runtime for the verification scripts
- A Claude Code session-history corpus on disk at `~/.claude/`, `~/.claude-work/`, `~/.claude-personal/`, or `~/.claude-shared/projects/` (any or all)

## The 5-phase workflow

### Phase 0 — Map the terrain & collect the denylist

Before any agent runs, you need to know the shape of the corpus and what names to strip.

**0a. Map the corpus.** Run `scripts/map_history.sh` from this skill's directory. It prints profile sizes, JSONL session file counts, per-project activity, and which projects have `memory/` subdirectories. Use `ctx_execute` to run it so its output doesn't flood context — only print a distilled summary back.

**0b. Cluster projects into 4–6 domain slices.** Read the per-project breakdown and group similar projects into slices. The slicing dimension is *audience* or *product family*, not *technology*. Typical slice patterns:
- Main work product (mobile/backend)
- Work product (web/data/internal tools)
- Side-project portfolio
- Tooling / meta / agent-infrastructure
- Personal / knowledge-work / cross-cutting

4–6 slices work best. Fewer than 4 = agents get overloaded. More than 6 = synthesis becomes harder.

**0c. Collect the denylist.** Ask the user explicitly: *"Before I spawn agents, I need your denylist — the product names, company names, internal codenames, ticket-ID prefixes, PR numbers (if they identify a repo), and branded skill/repo names you do NOT want in the output."* Record these verbatim. Do not try to auto-extract; inferring brand names creates false positives on common English words.

Also ask: *"Any specific brand-adjacent terms that ARE allowed?"* — usually framework names (Flutter, PostHog, BigQuery) and generic words (app, dashboard, bot) stay in; verify.

Save the denylist to `<output-dir>/.denylist.txt`, one term per line.

### Phase 1 — Build the research shared filesystem

Create a dedicated output directory (default: `<cwd>/blog-research/`). Scaffold:

```
blog-research/
├── INDEX.md            (from assets/INDEX.md.template — fill in source table + agent assignments)
├── _TEMPLATE.md        (from assets/_TEMPLATE.md — each research agent copies this)
└── .denylist.txt       (from Phase 0)
```

Use `assets/INDEX.md.template` as the base. Fill in the placeholders:
- `{{DATE}}` → today's date
- `{{CORPUS_SIZES}}` → the table from `map_history.sh`
- `{{AGENT_ASSIGNMENTS}}` → the 4–6 domain slices from 0b, with filenames like `01-<slice-name>.md`

### Phase 2 — Wave 1: parallel research agents

Dispatch one Opus subagent per domain slice **in a single tool-use turn**. All agents run in parallel, each with Opus 4.7 1M context.

Use the template at `references/research-agent-template.md`. For each agent, fill in:
- **Scope** — the exact list of project directory paths to read
- **Output file** — dedicated markdown file (e.g. `01-<slice-name>.md`)
- **Denylist** — the full list from Phase 0, inlined verbatim (NOT a file reference — each agent lives in its own context and cannot see files outside its prompt)
- **Method notes** — the "use ctx_execute, do not Read jsonl directly" instruction

**Why one message with N tool calls:** parallel dispatch is essential. Sequential spawning triples wall-clock time and wastes the 1M-per-agent budget. Send all N `Agent` calls in a single assistant turn.

**Background or foreground?** Foreground if you want progress indicators between returns. Background (`run_in_background: true`) if you want to start the user conversation again while agents work; you'll get task-notification events as each completes.

Each research agent writes its own findings file. When all N complete, Phase 3 begins.

### Phase 3 — Synthesis into ≤5 categories

After every research agent has returned:

**3a. Extract compact bullets from each research file.** Use `ctx_execute` with a Python script that reads each `0N-*.md`, extracts sections 2 (Accomplishments), 3 (Technical Work), 6 (Stories), and 7 (Timeline), and compacts each bullet to ~280 chars. This fits all findings into one context window for synthesis. See `references/synthesis-template.md` for the extractor snippet.

**3b. Produce `BLOG-CATEGORIES.md`** from the compacted bullets. The cap is **≤5 categories**. This is a deliberate constraint — fewer than 5 often collapses too aggressively, more than 5 fragments the narrative. Aim for 5.

Category shape: each category should have
- A thesis title (methodology-framed, NOT product-framed — e.g. "Shipping subscription-mobile features that move the revenue curve", NOT "Shipping [Product X]")
- A *"Who it's for"* audience tag
- 5–10 approach-evidence bullets (distilled from the research files)
- 6–10 draft blog-post titles

**3c. Verify the synthesis doc is denylist-clean.** Run `scripts/verify_denylist.py <path-to-BLOG-CATEGORIES.md> <path-to-.denylist.txt>`. If any word-bounded hits appear, rewrite those passages before continuing.

See `references/synthesis-template.md` for the full BLOG-CATEGORIES.md structure.

### Phase 4 — Wave 2: parallel long-form essay agents

One Opus agent per category (so up to 5 agents), **again dispatched in a single tool-use turn**.

Use the template at `references/essay-agent-template.md`. Each essay agent receives:
- The full denylist (inlined — NOT a file ref)
- A pointer to `BLOG-CATEGORIES.md` for category framing
- A pointer to the specific research file(s) the category draws from
- Strict craft constraints:
  - Target 4,500–8,500 words (Cat 4 / tooling-meta categories tend to go longer)
  - 10–14 sections with clear thesis arc
  - ≥3 concrete technical artifacts (snippets <15 lines each)
  - ≥2 pull quotes (standalone one-liners)
  - 2–4 callout blocks (steal-this templates)
  - Section-ending takeaways
  - First-person voice
  - **Self-verification** — agent must grep its own output against the denylist before reporting done

Each agent writes to `essays/category-N-<slug>.md`.

### Phase 5 — Cross-essay verification

Even though each agent self-checked, run a **consolidated denylist sweep** across all 5 essays from the orchestrator side. Agents can miss things.

```bash
python3 scripts/verify_denylist.py essays/*.md .denylist.txt --word-bounded
```

Expect 0 hits. If any appear, the grep will print file + line + context; edit those passages manually (do NOT re-spawn an agent for a 3-word fix).

Also run:
```bash
wc -w essays/*.md          # confirm word-count targets met
grep -c '^## ' essays/*.md # confirm section structure
```

### Delivery

Final tree:

```
blog-research/
├── INDEX.md
├── _TEMPLATE.md
├── .denylist.txt
├── BLOG-CATEGORIES.md              (the ≤5 category synthesis)
├── 01-<slice-1>.md                 (research findings, wave 1)
├── 02-<slice-2>.md
├── ...
└── essays/
    ├── category-1-<slug>.md        (long-form essay, wave 2)
    ├── category-2-<slug>.md
    ├── ...
    └── category-5-<slug>.md
```

Report back to user: total word count, files written, denylist clean confirmation, suggested first essay to publish.

## Trade-offs & gotchas

- **Opus 1M is expensive.** A full 2-wave run with 10 total Opus agents burns serious tokens. If budget is a concern, the research wave can use Sonnet at much lower cost (quality dips noticeably but is still workable); the essay wave needs Opus for voice quality.
- **The denylist must be human-provided.** Tempting to auto-extract brand names from the corpus itself, but you'll hit false positives on words like "note", "plan", "dashboard" if those happen to be product names. Ask the user.
- **≤5 is not "try for 5."** It's a real constraint. If the material only supports 3 categories, write 3. If it naturally wants 7, force-collapse to 5 — the collapsing *is* the synthesis.
- **Skill names that describe function are NOT brand names.** In the denylist, distinguish `daily-brain` (a function name — fine) from `meseba-skills` (a brand name — denied).
- **Product directories in Claude Desktop LevelDB are protobuf-locked.** A naive `strings` extraction yields draft fragments, not chat titles. Don't promise Desktop coverage; focus on Claude Code.
- **The 2-wave-parallel pattern is the moat.** A single-pass agent trying to read the whole corpus AND write 5 essays will fail on context budget. Resist the temptation to collapse waves.

## References

- `references/research-agent-template.md` — full prompt template for Wave 1 research agents (fill-in-the-blanks)
- `references/synthesis-template.md` — structure and writing rules for `BLOG-CATEGORIES.md`
- `references/essay-agent-template.md` — full prompt template for Wave 2 essay agents
- `scripts/map_history.sh` — corpus mapping / terrain scan
- `scripts/verify_denylist.py` — word-bounded cross-file denylist sweep
- `scripts/extract_user_messages.py` — sandbox-safe JSONL user-message extractor (embeddable in any agent's ctx_execute block)
- `assets/INDEX.md.template` — master TOC scaffold for the research directory
- `assets/_TEMPLATE.md` — per-agent research-findings section template
- `assets/BLOG-CATEGORIES.md.template` — synthesis document scaffold

## One-paragraph summary for triggering

A developer with a rich Claude Code history is sitting on publishable material they can't easily extract. This skill runs a two-wave parallel-Opus pipeline against the JSONL corpus — research agents scoped by domain slice write shared findings files, a synthesis pass collapses into ≤5 methodology-framed categories with a user-provided name denylist, essay agents write long-form blog drafts with strict craft constraints and self-verification, and a final cross-file sweep confirms the corpus is brand-clean. Output: 5 publishable essays totaling ~30,000 words, grounded in real session evidence but reading as professional approach rather than product catalog.
