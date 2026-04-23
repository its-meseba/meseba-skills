# Wave 2 — Essay Agent Prompt Template

Use this template verbatim for each of the ≤5 essay agents dispatched in Phase 4. One agent per category from `BLOG-CATEGORIES.md`. All agents launched in a **single assistant turn**.

## Critical design rule (same as Wave 1)

**The denylist MUST be inlined verbatim into every agent's prompt.** Duplicate it. Every agent.

## Template (copy and fill)

```
You are writing a long-form first-person essay for {{USER_NAME}}'s blog.

## The essay you are writing

**Category {{N}}: {{CATEGORY_TITLE}}**

{{ORDINAL}} of a 5-part series on their professional approach. Audience: {{AUDIENCE_TAG_FROM_CATEGORY}}. It describes HOW they {{ONE_SENTENCE_APPROACH_STATEMENT}} — not WHAT they shipped (no product catalog).

## Absolute constraint: no product, company, or codename references

Do NOT name any of these (even in passing, even as "at X I…"):
{{DENYLIST_INLINED_VERBATIM}}

Tool / framework / SDK / service names ARE fine — those are technology, not products. Examples of terms that stay in: {{ALLOWLIST_EXAMPLES_OR_LEAVE_BLANK}}. Also fine: generic referents like "the app I work on", "the internal dashboard I build", "my indie-app portfolio".

Skill names that describe a FUNCTION are fine (e.g. "my daily-brain skill", "my reading-lens skill"). Skill names that identify a BRAND or public repo are NOT (e.g. "my meseba-skills repo" — use "my public skill repo" instead).

**Before you save, grep your own text for every name in the denylist. If any match survives (word-bounded), rewrite that passage.**

## Your sources (read these first)

1. **Category framing:** `{{PATH_TO_BLOG_CATEGORIES_MD}}` — read the section for Category {{N}} carefully. That's the spine of your essay.
2. **Deep evidence:** `{{PATH_TO_PRIMARY_RESEARCH_FILE}}` — use the Read tool. This has the raw receipts.
3. **Supporting evidence (skim):** {{PATHS_TO_SECONDARY_FILES}}

The receipts in those files DO contain product/company names. Your job is to extract the PATTERNS and DECISIONS, leaving the brand context behind.

## Essay structure (target {{MIN_WORDS}}–{{MAX_WORDS}} words)

Write as a flowing essay, NOT a listicle.

{{10_TO_14_SECTION_OUTLINE_WITH_WORD_TARGETS_AND_CONTENT_GUIDANCE}}

Each section has:
- A guiding sub-thesis
- A word target
- Explicit content guidance (what to cover, what specifics to extract from research)
- An ending one-line takeaway

## Voice & craft

- First person ("I"), confident, grounded, specific. Not "we at <company>".
- Short paragraphs. Strong verbs. Show, don't tell.
- Include at least {{N}} concrete code-level or config artifacts (snippets under 15 lines each).
- Include at least 2 pull quotes — standalone one-liners that capture the thesis and could be lifted for social.
- 2–4 `>` callout blocks with steal-this templates.
- End each major section with a one-line takeaway.

## Output

Write to `{{OUTPUT_PATH}}/essays/category-{{N}}-{{slug}}.md` (create `essays/` subdir if needed).

Reply with just: file path + word count + **confirmation that your denylist grep (word-bounded) returned zero real-name matches**.
```

## Per-category outline examples

The outline section is the heart of the prompt. Below are tested shapes for the 5 typical categories that emerge from Claude Code histories. Adapt these to the actual categories in `BLOG-CATEGORIES.md`.

### Subscription-mobile monetization (~5000–7000 words)

```
1. Cold open (200–400 words) — arresting opener, single sharp claim.
2. Why subscription-mobile is different — SDK landscape, receipts-are-truth boundary. (400–600)
3. The flag-then-experiment arc — flag with escape hatches, then Bayesian experiment once signal matters. (700–900)
4. Subscription-infra SDKs over custom billing logic — $0 promo products, native code-redemption sheet. (500–700)
5. The telemetry audit — validate the LAST HOP; checklist. (700–900)
6. App-lifecycle fallbacks for unreliable SDK streams — e.g. app-resume re-fetch. (400–600)
7. Event coverage as a product metric — threading metadata through feedback paths. (400–600)
8. Lifecycle email as empathy-copy-on-top-of-orchestration. (500–700)
9. Ops-readiness is part of shipping — internal playbooks. (300–500)
10. Audit channels honestly — push-program template. (400–600)
11. Closing thesis (200–400) — reinforcement + series link.
```

### Internal analytics with LLM layer (~5000–7500 words)

```
1. Cold open — "internal analytics products get built twice…" (200–400)
2. Vertical-slice shipping across all layers — types → SQL → endpoint → hook → chart → tab. (700–900)
3. Competitive intelligence vs user analytics — small multiples, URL-param state sharing. (700–1000)
4. Clean data at the storage boundary, not in the UI. (400–600)
5. Ad-network ingestion without rate-limit shutoffs. (700–900)
6. One LLM call, multiple fields — single-call multi-field JSON vs fragile chains. (500–700)
7. Rating-conditional prompt design for reply generation. (900–1200)
8. Research sprints against real ticket IDs — numbers worth publishing. (500–700)
9. Replacing a paid SaaS with a weekend-built in-house clone. (600–800)
10. Reviewing intent, not code. (400–600)
11. Closing thesis. (200–400)
```

### Multi-app indie portfolio (~5000–7500 words)

```
1. Cold open — "the playbook is the product." (200–400)
2. One-planning-session SDK stack install. (500–700)
3. Retrospectives as artifacts — lessons library. (900–1200)
4. ASO as a parallelizable AI pipeline. (700–900)
5. Strategy lives in onboarding. (600–800)
6. Design-system migrations as single sessions. (700–900)
7. Strict concurrency traps captured as memory. (500–700)
8. Dev-environment silent fails, hunted explicitly. (400–600)
9. UI-framework gotchas captured as rules. (400–600)
10. Single commits at end of plan. (400–600)
11. Unfakeable accountability — pick the metric your user can't cheat. (400–600)
12. Closing thesis. (200–400)
```

### Engineering with AI agents (~6000–8500 words — longest category)

```
1. Cold open — "the harness is a product." (300–500)
2. Skills as the unit of composition. (900–1200)
3. LLM as permission firewall. (900–1200)
4. Context-monitor as IPC hook. (600–800)
5. Parallel fan-out as a skill design pattern. (700–900)
6. An agent swarm that talks through state files. (800–1000)
7. Three-profile symlink architecture. (700–900)
8. MCP integrations: reach as a multiplier. (500–700)
9. Rust-backed command rewriter / token-savings hooks. (400–600)
10. Sound cues as agent lifecycle signals. (400–600)
11. Post-implementation self-review as a slash command. (400–600)
12. Executive-summary as a skill. (400–600)
13. Closing thesis. (300–500)
```

### Personal systems / knowledge work (~4500–7000 words)

```
1. Cold open — concrete stat ("I sent 10,162 prompts across three profiles in 84 days"). (300–500)
2. The cadence data is the post. (500–700)
3. Desktop for thinking, Code for doing. (700–900)
4. Structured daily logger beats freeform journal. (700–900)
5. 156-week bricks — 3-year mastery framework. (800–1000)
6. A Teacher persona for every field. (700–900)
7. Reading as structured analysis. (600–900)
8. One ritual per context. (500–700)
9. Three profiles = three mental modes. (600–800)
10. Publishing your skill library as a forcing function. (400–600)
11. Closing thesis — personal systems compound. (300–500)
```

## Word targets by category

| Category archetype | Min | Max | Why |
|---|---|---|---|
| Subscription-mobile monetization | 4500 | 7000 | Thesis-driven, avoid listicle temptation |
| Internal analytics + LLM | 5000 | 7500 | More concrete artifacts per section |
| Indie portfolio | 5000 | 7500 | Many discrete lessons, moderate per-lesson depth |
| AI agent engineering | 6000 | 8500 | Richest raw material, most artifacts to show |
| Personal systems | 4500 | 7000 | Reflective tone, less code-dense |

## Common essay-agent pitfalls

- **Listicle drift.** Agents default to "10 things I learned" structure. Your outline explicitly prescribes section word targets — follow them, not bullet counts.
- **Evidence-without-position.** An essay that lists what the user did without claiming a position is a CV, not a blog post. Each section should have a sub-thesis, not just a topic.
- **Over-citation of research files.** Don't have the agent quote back the research file. The research file is evidence; the essay is argument.
- **Brand leakage on skill / repo names.** Functional skill names are fine; brand skill names are not. Example: `daily-brain` (function) = OK, `meseba-skills repo` (brand) = not OK.
- **Self-verification skipped.** Require the agent to grep its own output word-bounded before reporting done. Saves a round-trip.
