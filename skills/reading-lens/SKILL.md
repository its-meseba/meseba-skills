---
name: reading-lens
description: Active-reading scaffolding for nonfiction books (EPUB). Parses an EPUB, generates a structured book analysis in the user's Obsidian vault at Read/{Book Name} ({Author})/, with 0. General.md as the book-level overview and one numbered markdown file per chapter containing pre-read brief, the user's own notes section, and post-read synthesis — all through configurable role lenses (e.g. PM, CEO, Entrepreneur). Six sub-skills — `reading-lens:setup` loads an EPUB with lens selection, `reading-lens:brief` generates a pre-read brief for a chapter, `reading-lens:synthesize` generates a post-read synthesis, `reading-lens:overview-redo` regenerates 0. General.md, `reading-lens:lenses` manages global lens presets, `reading-lens:to-notion` mirrors the book to Notion via MCP. Use whenever the user wants deep, structured book analysis, says "analyze this book", "read this book", "reading lens", "book analysis", "pre-read brief", "chapter synthesis", or references an EPUB path. Prefer this skill for any book-study workflow — even when the user doesn't say its name.
---

# Reading Lens

Active-reading scaffolding for nonfiction books. Given an EPUB, produce a structured set of markdown files in the user's Obsidian vault: book-level overview (`0. General.md`), per-chapter pre-read briefs (what to watch for), and per-chapter post-read syntheses (what it meant + contrarian takes + actionable experiments). The user takes their own notes in each chapter file — this skill is scaffolding, never a replacement for the user's own thinking.

## Why This Exists

Reading nonfiction passively leaks most of its value. This skill pre-frames each chapter so the reader knows what to watch for, then produces a synthesis with per-lens takeaways, a contrarian take (what the book overclaims), and concrete experiments worth running. Everything lands in Obsidian, wikilinked, so the vault accumulates into durable knowledge.

## Model & Thinking

- **Default model: Opus 4.7** (`claude-opus-4-7`). This skill does qualitative analysis — use the strongest reasoning model available. Check with `/model`, switch if needed.
- **Use extended thinking** (`<think>` / ultrathinking) for three steps specifically: (1) generating `0. General.md`, (2) generating a post-read synthesis, (3) generating a contrarian take. The quality bar is high — platitudes are a failure mode.

## Sub-commands

| Command | Purpose |
|---------|---------|
| `/reading-lens:setup <epub-path>` | Parse EPUB, resolve lenses, create book folder, generate `0. General.md`, AND generate pre-read briefs + post-read syntheses for every chapter |
| `/reading-lens:brief <N>` | Generate pre-read brief for chapter N (before reading) |
| `/reading-lens:synthesize <N>` | Generate post-read synthesis for chapter N (after reading) |
| `/reading-lens:overview-redo` | Regenerate `0. General.md` for the current book (lenses preserved) |
| `/reading-lens:lenses [action]` | Manage global lens presets: list / add / edit / remove |
| `/reading-lens:to-notion` | Mirror the current book to Notion via Notion MCP |
| `/reading-lens:help` | Show usage |

If the user's intent clearly matches a sub-command but they didn't type the exact syntax, run the matching sub-command. Don't stall on syntax pedantry.

## Configuration

Global settings live in `{SKILL_DIR}/config.yaml`. On first use, verify `vault_path` is set to a real directory — if it still says `/path/to/your/obsidian/vault`, abort and tell the user to edit it.

Config fields:
- `vault_path` — absolute path to the Obsidian vault (required)
- `books_folder` — subfolder name (default `Reads`)
- `global_lenses` — list of `{role, interests}` objects
- `notion_parent_url` — optional, for `:to-notion`

## Vault Structure

```
{vault_path}/{books_folder}/{Book Name} ({Author})/
├── 0. General.md                 # Book-level overview (the "orientation" file)
├── 1. {chapter 1 title}.md       # Chapter notes: brief | my notes | synthesis
├── 2. {chapter 2 title}.md
└── n. {chapter n title}.md
```

**Filename rules.** For both the book folder and chapter filenames, sanitize thus:
- Replace `:` with ` - ` (space-hyphen-space) — preserves readability in titles like `Start: A Parable` → `Start - A Parable`
- Remove `/ \ * ? " < > |`
- Collapse multiple spaces to one, trim leading/trailing whitespace
- Do NOT slugify — preserve capitalization and spaces (this is Obsidian, not URLs)

**Examples.**
- Book `The Lean Startup` by `Eric Ries` → folder `The Lean Startup (Eric Ries)`
- Chapter `Start: A Parable` → file `1. Start - A Parable.md`
- Chapter `What/When/How` → file `3. WhatWhenHow.md` (slashes removed)

## Lens Selection Flow

Executed at the start of every `/reading-lens:setup` after EPUB parsing.

1. Read `global_lenses` from `config.yaml`.
2. If the list is empty: tell the user "No global lenses configured yet. What lenses should I use for this book?" Ask for `role + interests` pairs. Offer to save them globally after the user defines them.
3. If the list is non-empty: present the globals and ask:

   > You have {N} global lenses:
   >   1. {Role 1} — {interests}
   >   2. {Role 2} — {interests}
   >   ...
   >
   > For **{Book Title}**, do you want to:
   >   (a) Use all global lenses
   >   (b) Choose a subset of globals
   >   (c) Define new lenses just for this book (ignoring globals)
   >   (d) Combine a subset of globals + new book-specific lenses

4. Based on the answer, resolve the final lens set. Confirm back to the user before proceeding: "Using these lenses for this book: [list]. Continue?"
5. Store chosen lenses in the book's `0. General.md` frontmatter under `lenses:`. These become the book's frozen lens set — they override globals for this book going forward. Changing globals later does not rewrite this book.

## Update-Don't-Delete Safety

Before writing any file, check if it already exists. Never overwrite silently. Specific rules:

**On `:setup` when the book folder already exists:**

1. List what's there: `0. General.md`, which chapter files, and for each chapter file read the frontmatter to report `brief_generated` and `synthesis_generated` state.
2. Present status and ask:
   > Book already exists at `{path}`. Current state:
   >   - 0. General.md  [generated {date}]
   >   - 1. {title}     [✓ brief, ✓ synthesis]
   >   - 2. {title}     [✓ brief, — no synthesis]
   >   - 3. {title}     [— untouched]
   >
   > What would you like to do?
   >   (a) Skip — leave everything as-is
   >   (b) Fill missing pieces only (generate briefs/syntheses for chapters that lack them)
   >   (c) Regenerate `0. General.md` only (keeps per-book lenses + chapter files)
   >   (d) Add chapters that aren't in the vault yet (EPUB may have more than the folder)
   >   (e) Review and decide file-by-file

3. Never delete files. Never overwrite `## ✍️ My notes` sections (the user's own writing).

**On `:brief N` or `:synthesize N` when the section is already filled:**

- Show the user the current content of `## Pre-read brief` (or `## Post-read synthesis`), say when it was generated, and ask: "Overwrite, keep, or append?" Default to "keep" on any ambiguous response.
- If the user chooses "append", add the new version under a `### Re-generated {ISO-date}` subheader so both versions are preserved.

**On `:overview-redo`:**

- Show current `0. General.md` summary (first paragraph + lens list). Ask: "Regenerate `0. General.md`? Per-book lenses will be preserved. Overwrite? (y/n)". Only proceed on explicit yes.

## Workflow

### `/reading-lens:setup <epub-path>`

1. **Validate.** Check the path exists and ends in `.epub`. Abort with a clear error if not.
2. **Read config.** Load `config.yaml` from the skill directory. If `vault_path` is the default placeholder or not a directory, abort with: "Edit `{SKILL_DIR}/config.yaml` first — set `vault_path`."
3. **Parse EPUB.** Run `python3 {SKILL_DIR}/scripts/parse_epub.py <epub-path>` and capture JSON. On error, surface stderr to the user.
4. **Build book folder path.** `{vault_path}/{books_folder}/{Book Name} ({Author})/`. Sanitize as per filename rules.
5. **Check for existing book.** If the folder exists, run the Update-Don't-Delete flow above.
6. **Resolve lenses.** Run the Lens Selection Flow above.
7. **Create folder + cache.** Create the book folder. Save parsed EPUB JSON to `{SKILL_DIR}/.cache/{book-folder-name}.json` for fast re-use by `:brief` and `:synthesize`.
8. **Generate `0. General.md`.** Use extended thinking. Source material: title, author, TOC (all chapter titles in order), and sample text (first 6000 chars of chapter 1 + first 6000 chars of chapter 2). Fill the **Book Overview Template** below.
9. **Create chapter stubs.** For each chapter, write a file with frontmatter + the three empty section headers (Pre-read brief, My notes, Post-read synthesis). Include `synthesis_has_notes: false` in the frontmatter.
10. **Warn the user about duration.** Print: "Generating pre-read briefs + post-read syntheses for all {N} chapters. This uses Opus extended thinking for each chapter and will take roughly {N}–{N*2} minutes. Syntheses are generated WITHOUT your reading notes (you haven't read yet) — after you read a chapter and take notes in `## ✍️ My notes`, re-run `/reading-lens:synthesize <N>` to upgrade that chapter's synthesis with your framing." Do not block on a confirmation — proceed.
11. **Generate pre-read briefs for every chapter.** Iterate N = 1..chapters. For each N, run the `:brief N` workflow inline (steps 2–6 of the brief workflow) using the cached EPUB JSON. After each write, update the chapter file's frontmatter: `brief_generated: <ISO-date>`, `status: briefed`.
12. **Generate post-read syntheses for every chapter.** Iterate N = 1..chapters. For each N, run the `:synthesize N` workflow inline with one variation: since `## ✍️ My notes` is empty, do NOT fabricate user-note references. Produce the synthesis from chapter text + book lenses only. After writing, update frontmatter: `synthesis_generated: <ISO-date>`, `synthesis_has_notes: false`, `status: synthesized`. Prepend this callout block to the `## Post-read synthesis` body, before the template output:

    ```
    > [!info] Generated at setup — no reader notes yet
    > This synthesis was generated from chapter text only, before you read the chapter. After you read and take notes in `## ✍️ My notes`, re-run `/reading-lens:synthesize {N}` to produce a notes-aware upgrade.
    ```

13. **Report.** Tell the user: book title, author, N chapters parsed, briefs generated, syntheses generated (all flagged `synthesis_has_notes: false`), full folder path. Recommend: "Start with chapter 1. After each chapter, fill `## ✍️ My notes` then re-run `/reading-lens:synthesize N` to upgrade that chapter's synthesis."

### `/reading-lens:brief <N>`

1. **Resolve current book.** Find the most recently modified `0. General.md` under `{vault_path}/{books_folder}/`. If multiple books have been touched recently, ask which one.
2. **Load chapter N.** Read cached EPUB JSON from `{SKILL_DIR}/.cache/`. If missing, tell the user to run `:setup` again.
3. **Check for existing brief.** If `## Pre-read brief` in the chapter file already has content, run the overwrite flow.
4. **Generate brief.** Using the chapter text (truncate to 40000 chars if longer) and the book's per-book lenses (from `0. General.md` frontmatter), produce the **Pre-read Brief** matching the template below.
5. **Write.** Replace the content under `## Pre-read brief` (or append per user choice). Update frontmatter: `brief_generated: <ISO-date>`, `status: briefed`.
6. **Report.** Print a 3-line summary and the path to the chapter file.

### `/reading-lens:synthesize <N>`

1. **Resolve current book.** Same as `:brief`.
2. **Load chapter N text** and read the user's content from `## ✍️ My notes` section if present.
3. **Check for existing synthesis.** If `## Post-read synthesis` is filled:
   - If frontmatter says `synthesis_has_notes: false` AND the user has written real content under `## ✍️ My notes` (more than just the placeholder `*(take your notes...)*`), offer a notes-aware upgrade: "Current synthesis was generated at setup from chapter text only. You've since written notes — upgrade the synthesis to weave them in? (y/n)". On yes: overwrite the synthesis, remove the setup `> [!info]` callout, set `synthesis_has_notes: true`, regenerate using notes.
   - Otherwise, run the standard overwrite flow (keep/overwrite/append).
4. **Generate synthesis.** USE EXTENDED THINKING. If `## ✍️ My notes` has real content, reference it ("you noted X — this connects to..."). Produce the **Post-read Synthesis** matching the template below.
5. **Write.** Replace the content under `## Post-read synthesis`. Update frontmatter: `synthesis_generated: <ISO-date>`, `synthesis_has_notes: <true if notes were used, else false>`, `status: synthesized`.
6. **Report.** Print a 3-line summary + flashcard count + path + whether this was a notes-aware generation.

### `/reading-lens:overview-redo`

1. Resolve current book.
2. Run overwrite flow for `0. General.md`.
3. Preserve existing per-book lenses (from current frontmatter).
4. Use extended thinking. Regenerate the overview with the same source material as setup (TOC + sample from first two chapters).
5. Write, report.

### `/reading-lens:lenses [action]`

Manage `global_lenses` in `config.yaml`.

- `/reading-lens:lenses` or `/reading-lens:lenses list` → print current globals
- `/reading-lens:lenses add` → prompt for `role` + `interests`, append to config
- `/reading-lens:lenses edit <role>` → show current values, prompt for new
- `/reading-lens:lenses remove <role>` → confirm, then remove
- `/reading-lens:lenses reset` → confirm, replace with built-in defaults (PM / CEO / Entrepreneur)

Edit `config.yaml` in place. Preserve comments and formatting.

### `/reading-lens:to-notion`

1. Confirm Notion MCP is connected. If not, tell the user to enable it in settings.
2. Resolve current book.
3. Use `notion_parent_url` from config, or ask the user for the parent page.
4. Create a parent page from `0. General.md` (strip Obsidian wikilinks, convert to plain references).
5. Create one subpage per chapter file.
6. Report Notion URLs.

### `/reading-lens:help`

Print the sub-commands table, vault structure, where to edit config, how to manage lenses, and model recommendation (Opus 4.7).

## Templates

### Book Overview — content for `0. General.md`

```markdown
---
type: book
title: "{title}"
author: "{author}"
source_epub: "{absolute-epub-path}"
status: reading
started: {YYYY-MM-DD}
chapters: {N}
lenses:
  - role: "{Role 1}"
    interests: "{interests}"
  - role: "{Role 2}"
    interests: "{interests}"
tags: [book, reading-lens]
---

# {title}
*by {author}*

> **{one-liner — 1 sentence on what this book is really about, not the marketing blurb}**

## Thesis

{2–3 sentences: the core argument the book is making}

## Why it matters to a builder

{2–3 sentences: why a reader with the configured lenses should read this specifically}

## Key terms this book teaches

- **{term}** — {working definition under 20 words}
- ... (6–10 items)

## Focus prompts — hold these while reading

- [ ] {active-reading question to hold across the whole book}
- ... (4–6 items, checkboxes)

## Per-lens learning

### {Role 1}
{1–2 sentences: what this reader, in this role, stands to gain from this book specifically — not generic "will learn about strategy"}

### {Role 2}
...

(one H3 per lens)

## Converses with

- {other book, framework, or resource} — {1 sentence on the link}
- ... (3–5 items)

## Chapters

- [[1. {chapter 1 title}|1. {chapter 1 title}]]
- [[2. {chapter 2 title}|2. {chapter 2 title}]]
- ...
```

### Chapter Stub (written at setup, sections filled later)

```markdown
---
type: chapter
book: "[[0. General|{book-title}]]"
chapter_number: {N}
chapter_title: "{title}"
word_count: {wc}
status: unread
brief_generated: null
synthesis_generated: null
synthesis_has_notes: false
tags: [chapter, reading-lens]
---

# {N}. {chapter_title}

## Pre-read brief

*(run `/reading-lens:brief {N}` before reading)*

---

## ✍️ My notes

*(take your notes here while reading — this section is never overwritten by the skill)*

---

## Post-read synthesis

*(run `/reading-lens:synthesize {N}` after reading)*
```

### Pre-read Brief — fills `## Pre-read brief`

```markdown
> **{one-liner — what this chapter is about, 1 sentence}**

**Watch for**
- {specific thing to notice while reading}
- ... (3–5 items)

**Key terms**
- **{term}** — {definition under 20 words}
- ... (3–6 items)

**Questions to hold**
- [ ] {active-reading question}
- ... (3–5 items, checkboxes)

**Per-lens angles**

*{Role 1}.* {1–2 sentences: what to specifically attend to through this lens}

*{Role 2}.* ...
```

### Post-read Synthesis — fills `## Post-read synthesis`

```markdown
> **{core idea — 1 crisp sentence, no hedging}**

**Key takeaways**
- {concrete takeaway with substance}
- ... (4–6 items)

**Per-lens takeaways**

*{Role 1}.* {2–3 sentences of role-specific learnings the reader could act on tomorrow}

*{Role 2}.* ...

**Contrarian take**

{2–3 sentences. What does this chapter overclaim, ignore, or get wrong? Be direct — not hedged. This is the most important section — the reader must read critically, not reverentially. If the chapter is genuinely solid, say what it UNDER-claims or what a smart critic would still push back on.}

**Actionable experiments**
- {concrete experiment a builder could run this quarter}
- ... (2–3 items)

**Connections**
- {other book/idea/framework this chapter links to} — {the link, 1 sentence}
- ... (2–4 items)

**Flashcards**
- **Q:** {question}
  **A:** {answer under 30 words}
- ... (3–5 items)
```

## Quality Rules

Book analysis is important — these rules are not optional:

- **No generic MBA platitudes.** Bad: "focus on customers." Good: "Ries argues the unit of progress is the validated learning cycle — not revenue, users, or ship velocity." Every takeaway must be specific enough that a reader who skipped the chapter could still lose the argument against one who read it.
- **Lens takeaways must be role-specific.** If a PM takeaway would read identically as a CEO takeaway, both are wrong. Rewrite until they diverge.
- **Contrarian takes must bite.** "Some readers might disagree" is not a contrarian take. Name the specific claim and say why it's wrong, overstated, or incomplete. This is where the skill earns its keep.
- **Actionable experiments must fit a small startup.** Not "hire a data science team" — "add an event to track X in the existing analytics for Y feature, run for 2 weeks, compare to the Z cohort."
- **Never pretend to know what you don't.** If the chapter text is thin or the topic is outside your confidence, say so in-line rather than fabricating.
- **Respect the user's notes.** Never modify `## ✍️ My notes`. When generating synthesis, read it and weave its content in — the reader's own framing is data.
- **Never delete files.** Ever. When in doubt, ask.
- **Ask before overwriting.** Every regeneration is a deliberate choice, confirmed by the user.

## What This Skill Is NOT

- Not a reading app — reading happens in your EPUB reader of choice.
- Not a summary generator — it's scaffolding around the user's own active reading.
- Not a research agent — it works on one EPUB at a time. Don't web-search unless verifying a specific proper noun.
- Not a general note-taker — other skills (e.g., `no-brainer`) handle general summarization.

## Help Output (`/reading-lens:help`)

When this sub-command is invoked, present:

---

### Reading Lens

Active-reading scaffolding for nonfiction books. Parses an EPUB → generates a structured book analysis in your Obsidian vault.

#### Where things go

`{vault_path}/{books_folder}/{Book Name} ({Author})/`
- `0. General.md` — book overview
- `1. {chapter title}.md` ... `n. {chapter title}.md` — chapter files (brief | your notes | synthesis)

#### Commands

| Command | What it does |
|---------|-------------|
| `/reading-lens:setup <epub-path>` | Start a new book: parse EPUB, choose lenses, generate overview, plus pre-read briefs + post-read syntheses for every chapter |
| `/reading-lens:brief <N>` | Generate pre-read brief for chapter N |
| `/reading-lens:synthesize <N>` | Generate post-read synthesis for chapter N |
| `/reading-lens:overview-redo` | Regenerate `0. General.md` for the current book |
| `/reading-lens:lenses [action]` | Manage global lens presets (list / add / edit / remove / reset) |
| `/reading-lens:to-notion` | Mirror the current book to Notion |

#### Recommended

Use Opus 4.7. Check with `/model`.

#### Setup

Edit `config.yaml` in the skill folder — set `vault_path` and (optionally) edit `global_lenses`.
