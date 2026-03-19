---
name: ship-wreck-check
description: Use when you've finished implementing changes and need a final brutal quality review before considering work done. Use this after completing a feature, bugfix, or refactor — before committing or creating PRs. Also use when the user says things like "review this", "is this ready", "final check", "check my work", "quality check", "ship it", or "are we good". This skill should trigger whenever implementation work is complete and needs honest self-assessment, even if the user doesn't explicitly ask for it.
---

# Ship-Wreck Check

You wrote the code — now tear it apart like a senior engineer reviewing a junior's PR. No hand-waving, no "it should be fine", no skipping steps. The name says it all: catch the wreck before it ships.

## Core Principle

**You are not allowed to be nice to yourself.** Every change you made is suspect until proven otherwise. The goal is catching problems NOW — not discovering them in production.

## The Review Process

```dot
digraph ship_wreck_check {
  rankdir=TB;
  node [shape=box];

  gather [label="1. Gather all changed files\n(uncommitted + unpushed + branch diff)" shape=ellipse];
  discover [label="2. Discover project quality commands\n(package.json, CLAUDE.md, Makefile, CI)"];
  run_commands [label="3. Run ALL quality commands\n(build, lint, typecheck, tests)"];
  commands_pass [label="All pass?" shape=diamond];
  fix_commands [label="Fix failures\nthen restart"];
  intent [label="4. Intent verification\n(find spec/plan, verify against code)"];
  plan_found [label="Plan found?" shape=diamond];
  verify_intent [label="Dispatch spec-reviewer:\ncheck code against spec"];
  no_plan [label="Set flag:\nintent check skipped"];
  deep_review [label="5. Deep review: read each changed file\n+ related files + project context\n(informed by spec if available)"];
  simplify [label="6. Invoke code-simplifier agent\non changed files"];
  issues [label="Issues found?" shape=diamond];
  report [label="7. Report with file:line refs\nBLOCKER / WARNING / SUGGESTION\n+ intent gaps + red warning if no plan"];
  fix [label="Fix issues"];
  rerun [label="Re-run from step 3"];
  clean [label="Ship it" shape=ellipse];

  gather -> discover -> run_commands -> commands_pass;
  commands_pass -> fix_commands [label="no"];
  commands_pass -> intent [label="yes"];
  fix_commands -> run_commands;
  intent -> plan_found;
  plan_found -> verify_intent [label="yes"];
  plan_found -> no_plan [label="no"];
  verify_intent -> deep_review;
  no_plan -> deep_review;
  deep_review -> simplify -> issues;
  issues -> report [label="yes"];
  issues -> clean [label="no"];
  report -> fix -> rerun -> run_commands;
}
```

### Step 1: Gather Your Changes

Get the full picture of what changed. Changes can live in multiple places — check ALL of them:

```bash
# Uncommitted changes (staged + unstaged)
git diff HEAD --name-only

# If working tree is clean, check unpushed commits
# (user may have already committed but not pushed)
git log --name-only --oneline origin/$(git branch --show-current)..HEAD

# If both are empty, check the main branch diff
# (user may be on a feature branch with all changes committed)
git diff --name-only main...HEAD
```

The key insight: "check my work" doesn't always mean uncommitted changes. The user might have committed already, or be on a feature branch. Cast a wide net — find ALL the changes that are part of the current work, wherever they live.

Only review files that are part of the current work — but read surrounding context and related files to understand impact.

### Step 2: Discover Project Quality Commands

Before reviewing a single line, find every quality check the project defines. Scan these locations:

- **package.json** → `scripts` section (`quality`, `lint`, `build`, `type-check`, `test`, `test:run`, `format:check`)
- **CLAUDE.md / README.md** → documented commands, "before committing" sections, quality check instructions
- **Makefile** → `check`, `lint`, `test`, `build` targets
- **pyproject.toml** → pytest, mypy, ruff, black configs
- **Cargo.toml** → `cargo clippy`, `cargo test`
- **CI config** (`.github/workflows/`, `.gitlab-ci.yml`) → whatever CI runs, you run too

Read these files. If they say "run X before committing", run X.

### Step 3: Run ALL Quality Commands

Run every command you discovered. If any fail, fix the failures before proceeding to the code review. There is zero point reviewing code that doesn't build or pass lint.

### Step 4: Intent Verification — Does the Code Match the Plan?

Before reviewing code quality, check whether the implementation matches its original intent. This step connects the code back to the spec/plan that motivated it.

#### Finding the Plan

Search these locations for spec/plan documents:

- `docs/superpowers/specs/` — design specs from brainstorming
- `docs/plans/` — implementation plans
- `docs/superpowers/plans/` — plans from the superpowers workflow

**Matching strategy (in order):**

1. **Branch name keywords** — Extract meaningful words from the current branch name (e.g., `fix/user-reviews-page-updates` → "user", "reviews", "page", "updates") and match against plan filenames and their contents.
2. **Changed file context** — Look at the changed files from Step 1. What domain do they touch? (e.g., changes in `src/components/reviews/` suggest a reviews-related plan). Match plan contents against these domains.
3. **Multiple plans** — The implementation may span multiple plans. If changed files clearly map to different plans, include ALL matching plans.
4. **Ambiguity** — If you find multiple candidate plans and can't confidently determine which ones apply, show the candidates to the user and ask them to confirm:
   > "I found these plans that might relate to your changes:
   > 1. `docs/plans/2026-03-04-review-duplicates-and-freshness-fix.md`
   > 2. `docs/superpowers/specs/2026-03-03-table-keyboard-navigation-scroll.md`
   > Which ones apply to this work? (or 'none')"

#### Verifying Against the Plan

If one or more plans are found, dispatch a **spec-reviewer** analysis. This is a skeptical review — read the actual code, don't trust summaries:

1. Read each matched plan/spec fully — extract acceptance criteria, requirements, constraints, and scope boundaries
2. Read each changed file fully — understand what was actually built
3. Compare implementation against spec:
   - **INTENT_MATCH** — Implementation fulfills the spec requirement
   - **INTENT_GAP** — Spec required something that the implementation doesn't deliver
   - **OVER_BUILT** — Implementation includes functionality not in the spec (scope creep)
   - **SPEC_AMBIGUITY** — Spec was unclear and implementation made an assumption worth flagging

Report intent findings with the same `file:line` format:

```
[INTENT_GAP] docs/plans/2026-03-04-review-fix.md requirement: "deduplicate reviews by user+date"
  → Not implemented in src/services/review-service.ts — no deduplication logic found

[OVER_BUILT] src/components/reviews/ReviewCard.tsx:45 - Added animation on hover
  → Not in spec. Intentional enhancement or scope creep?

[INTENT_MATCH] src/utils/reviews/freshness.ts - Freshness calculation matches spec criteria ✓
```

#### If No Plan Is Found

If no matching plan/spec is found in any of the search locations:

1. **Set a flag** — `intentCheckSkipped = true`
2. **Continue to Step 5** — proceed with the normal code review
3. **In Step 7 (Report)** — append a prominent red warning (see Step 7)

Do NOT block the review because a plan is missing. The code review is still valuable on its own.

### Step 5: Deep Review — Understand What You Changed

This is the heart of the review. For every changed file, truly understand it — don't skim.

**If a spec/plan was found in Step 4**, use it as your lens — you know what the code is supposed to do, so read with purpose. Flag anything that contradicts the spec or seems unrelated to it.

**Read each changed file fully.** Then read the files that depend on it and the files it depends on. Understand the ripple effects. Use Grep and Glob to find callers, importers, and related code.

#### Production Safety

- **Will this break callers?** Trace every function/component you modified. Who calls it? Did you change a return type, parameter order, or default value that callers rely on?
- **Error handling** — Proper handling for new code paths? Not generic `catch(e) { console.log(e) }` — specific, actionable errors with proper propagation.
- **Edge cases** — What happens with null, undefined, empty arrays, empty strings, zero, negative numbers? Concurrent access?
- **Resource cleanup** — Any new listeners, intervals, subscriptions, connections? Are they cleaned up on unmount/disconnect/error?
- **Environment differences** — Will this work in production? Different configs, missing env vars, different data volumes, different permissions?

#### Code Quality

- **Duplications** — Did you write something that already exists in the codebase? Search for similar function names and patterns. BUT: only flag as duplication if you are CERTAIN after reading both implementations fully. Similar-looking code that handles different edge cases or types is NOT duplication. When in doubt, it's not a duplication.
- **God files** — Did any file grow beyond ~300 lines or handle multiple unrelated concerns? Split it.
- **Separation of concerns** — Business logic mixed with UI? Data fetching in components? Validation inside handlers? Each file/function does ONE thing.
- **Dead code** — Unused imports, variables, functions, commented-out blocks? Remove them.
- **Magic values** — Hardcoded strings, numbers, URLs that should be constants or config?
- **Naming** — Do new names follow existing project conventions? Are they descriptive and consistent?

#### File & Folder Structure

- **New files in the right place?** Follow the project's existing directory conventions.
- **Consistent patterns** — Same export style, hook patterns, error handling approach as neighboring files?
- **File size** — New file already large? Probably needs splitting.

### Step 6: Invoke the Code-Simplifier Agent

After your manual review, dispatch the `code-simplifier` agent (available as the `simplify` skill) on the changed files. It provides a focused second pair of eyes on:

- Unnecessary complexity and nesting
- Redundant code paths that can be consolidated
- Variable/function names that could be clearer
- Overly clever one-liners that hurt readability
- Inconsistencies with project coding standards
- Over-engineering (abstractions nobody asked for, factory patterns where functions suffice)

The code-simplifier focuses on recently modified code by default — exactly what we need. Incorporate its findings into your report.

### Step 7: Report Findings

Be specific and actionable. For each issue, cite the exact location:

```
[BLOCKER] src/hooks/useFilter.ts:42 - Missing null check on filterState.dates
  → Add guard: if (!filterState.dates) return defaultRange;

[WARNING] src/components/FilterPanel.tsx:118 - Inline magic number 86400000
  → Extract to constant: const MS_PER_DAY = 86400000;

[SUGGESTION] src/utils/dateUtils.ts:23 - Duplicates logic in src/utils/common/formatDate.ts:15
  → Reuse existing formatDate() instead of reimplementing
```

Severity levels:
- **BLOCKER** — Will break production or existing functionality. Must fix before shipping.
- **WARNING** — Code smell, convention violation, potential issue. Should fix.
- **SUGGESTION** — Could be better but not harmful. Nice to have.

**If `intentCheckSkipped` is true** (no plan was found in Step 4), append the following red warning at the end of the report. This must be visually prominent:

> **🔴 WARNING: No spec/plan found — intent verification was skipped.**
> Could not verify whether the implementation matches the original intent.
> Consider creating plans via `/brainstorming` → `/writing-plans` for future work to enable full verification.

### Step 8: Fix and Re-verify

After fixing, re-run from Step 3. The cycle ends when:
- All quality commands pass
- No BLOCKERs or WARNINGs remain
- No INTENT_GAPs remain (if a plan was found)
- The code-simplifier has no further findings
- You can honestly say: "I'd approve this PR if someone else wrote it"

## Red Flags — Be Honest With Yourself

If you catch yourself thinking any of these, STOP:

| Thought | Reality |
|---------|---------|
| "This is good enough" | Good enough for whom? Check every item. |
| "It works, so it's fine" | Working code can still be bad code. Review quality. |
| "I'll clean it up later" | Later never comes. Clean it now. |
| "It's just a small change" | Small changes cause production outages. Review it. |
| "The tests pass" | Tests only catch what they test. Review what they don't. |
| "I already reviewed while writing" | Building mode ≠ review mode. Different mindset. |
| "This file was already messy" | Don't add to the mess. Leave it better. |
| "I'm sure this isn't a duplication" | Did you actually search? Grep for it. |

## The Brutal Honesty Test

Before declaring "ship it", answer honestly:

1. If a senior engineer reviewed this PR tomorrow, would they approve without comments?
2. If this change caused a production incident, could you defend every line?
3. Did you actually READ every line of your diff, or did you skim?
4. Did you run every quality command the project defines?
5. Did you check what the project's CLAUDE.md or README says to run before committing?

## Commands

| Command | Purpose |
|---------|---------|
| `/ship-wreck-check` | Run the full quality review on your changes |
| `/ship-wreck-check:help` | Show help — what Ship-Wreck Check does and how to use it |

## Help (`/ship-wreck-check:help`)

When this sub-command is invoked, present the following to the user:

---

### Ship-Wreck Check

A brutal, honest quality review of your code changes — the kind a senior engineer would give a junior's PR. Catches wrecks before they ship.

#### The 8-Step Process

| Step | What happens |
|------|-------------|
| 1. **Gather changes** | Finds all changed files (uncommitted, unpushed, and branch diff) |
| 2. **Discover quality commands** | Scans package.json, CLAUDE.md, Makefile, CI config for lint/build/test commands |
| 3. **Run all quality commands** | Executes every discovered command — build, lint, typecheck, tests |
| 4. **Intent verification** | Finds matching spec/plan docs, verifies implementation matches original intent |
| 5. **Deep review** | Reads every changed file + related files, checks for production safety, code quality, structure (informed by spec) |
| 6. **Code simplifier** | Invokes the code-simplifier agent for a second pair of eyes |
| 7. **Report findings** | Reports issues with exact `file:line` references, severity levels, and intent gaps |
| 8. **Fix and re-verify** | Fixes issues and re-runs from step 3 until clean |

#### Severity Levels

| Level | Meaning |
|-------|---------|
| **BLOCKER** | Will break production. Must fix before shipping. |
| **WARNING** | Code smell or convention violation. Should fix. |
| **SUGGESTION** | Could be better but not harmful. Nice to have. |

#### Usage

```
/ship-wreck-check
```

Also triggers on: "review this", "is this ready", "final check", "check my work", "quality check", "are we good".

#### What it checks

- **Intent compliance** — matches implementation against spec/plan from superpowers workflow (INTENT_MATCH/INTENT_GAP/OVER_BUILT)
- **Production safety** — broken callers, error handling, edge cases, resource cleanup, environment differences
- **Code quality** — duplications, god files, separation of concerns, dead code, magic values, naming
- **File structure** — new files in the right place, consistent patterns, file size

#### When to use

After completing a feature, bugfix, or refactor — before committing or creating PRs. Run it whenever implementation work is complete and needs honest self-assessment.
