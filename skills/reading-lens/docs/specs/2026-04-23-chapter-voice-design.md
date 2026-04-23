# Reading Lens — Chapter-Voice & Parallel Generation Redesign

**Date:** 2026-04-23
**Status:** Approved design, ready for implementation plan
**Author:** Semih Babacan (via brainstorming session with Claude Code)
**Scope:** The reading-lens skill's per-chapter pre-read brief and post-read synthesis output. Book-level `0. General.md` stays as-is.

---

## 1. Context & problem

The reading-lens skill currently produces per-chapter briefs and syntheses that feel shallow and generic. After running it on *The Mom Test* (32 chapters), the reader identified three concrete issues:

1. **The writing doesn't flow.** It reads like a book-reviewer's outline: clipped bullets, noun-stacked phrases, em-dash pileups, academic register. The user calls this "friction."
2. **The output isn't grounded in the actual chapter text.** Watch-For bullets and Key Terms feel paraphrased from general understanding rather than anchored to specific phrases and metaphors from the chapter.
3. **Per-lens angles collapse to one-liners.** The PM/CEO/Entrepreneur lenses often get combined or reduced to a single generic sentence, losing the role-specific depth that makes the tool valuable.

A reference example (screenshot from another reading tool the user shared) shows the target quality bar: a one-line author-voice thesis, phrase-anchored Watch-For bullets, crisp term→definition pairs, open philosophical Questions to Hold, and visually-distinct per-lens angles with 3–5 sentence paragraphs each.

The fix is **voice + depth + workflow discipline + parallel execution**. The output needs to read as if the author sat down to write it for the reader — both before the chapter and after. Generation needs to anchor to extracted verbatim material. Execution needs to dispatch parallel subagents so a 32-chapter book doesn't serialize through the main agent.

## 2. Goals

- **Author voice throughout.** Pre-read = author warming you up before the chapter. Post-read = author reflecting with you after. First-person. Warm. Flowing. Complexity where earned, not performative.
- **Channel the author's character.** Fitzpatrick reads different from Kahneman reads different from Taleb. The generator detects each book's voice register from extracted samples and writes in that register.
- **Ground every bullet in the text.** Close-reading extraction pass is mandatory before generation. Watch-For bullets cite verbatim phrases/metaphors. Key Terms use the author's own vocabulary. Nothing is invented.
- **Full per-lens depth.** PM/CEO/Entrepreneur each get their own 3–5 sentence paragraph, directly addressed, Monday-morning specific.
- **Readable flow.** Drop em-dash pileups. Drop noun stacks. Let prose breathe. Tables/checkboxes/callouts chosen to serve understanding, not template consistency.
- **Parallel execution.** Setup generation runs across subagents so 32 chapters don't block serially in the main agent.
- **Language support.** Default English. User can override per-book ("do it in Turkish"). Stored in book frontmatter.

## 3. Non-goals

- **No format revolution.** The existing bold-label section format (`**Watch for**`, `**Key terms**`, etc.) stays. The divider + ✍️ emoji around My notes stays. The `> [!info]` post-read callout stays. The `0. General.md` book overview stays as-is.
- **No new top-level sections.** Don't add a separate "What I'm doing in this chapter" heading. The author-voice opener is a flowing paragraph under the one-liner, not a new section.
- **Don't change the sub-command surface.** `/reading-lens:setup`, `/reading-lens:brief`, `/reading-lens:synthesize`, `/reading-lens:overview-redo`, `/reading-lens:lenses`, `/reading-lens:to-notion`, `/reading-lens:help` all keep their names and behavior.
- **Don't change parsing.** `scripts/parse_epub.py` stays as-is.

## 4. Design — writing voice

Every section of every brief and synthesis is written as the author speaking directly to the reader.

- **Pre-read framing:** *"Before you dive in, here's what I'm doing in this chapter…"*
- **Post-read framing:** *"Now that you've made it through — here's what I hoped landed, and here's where I'd give ground to a sharp critic."*

First person. Contractions OK. No em-dash pileups (one em-dash per paragraph max; prefer sentence breaks). Plain English when plain English lands harder. Complexity only when the idea earns it.

**One explicit voice break:** the Contrarian Take section in the post-read synthesis briefly leaves author voice to let a critic speak, then returns: *"A sharp reader will push back here, and they'd be right about X. I'd give ground on that — here's where my argument stretches further than my evidence can carry…"*

**Author-character channeling** is load-bearing and book-specific. The generator identifies the author's register during the close-reading pass (Section 7) and carries it into every section. Examples of what this looks like in practice:

| Author | Register samples to channel |
|---|---|
| Rob Fitzpatrick (*The Mom Test*) | Self-effacing, colloquial ("cool," "awesome," "doomed," "gold dust"), anecdote-driven, "I was doing it wrong for three years" |
| Daniel Kahneman (*Thinking, Fast and Slow*) | Precise, measured, academic, "my colleague Amos and I," careful self-questioning |
| Nassim Taleb (*Antifragile*) | Polemical, erudite, multilingual vocabulary, sardonic asides, "IYI" |
| Atul Gawande (*The Checklist Manifesto*) | Warm, physician-reflective, patient case studies, careful moral framing |

The generator must not impose a single house style. Each book should feel genuinely different.

## 5. Design — pre-read brief structure

Existing bold-label format, Obsidian-rendered. One section added: a 1–2 paragraph author-voice opener under the one-liner.

**Notation in this template:** `[...]` marks a placeholder to be filled during generation. Placeholder descriptions use plain text — the rendered output is plain prose, *not* italic, unless an explicit `*…*` is shown in the template literally.

```markdown
**Pre-read brief**

> [Author-voice one-line thesis — their own framing, not a
> summary of what the chapter covers]

[Paragraph 1: 2–3 sentences. Author's voice. A personal opener,
"here's where I'm about to take you." Introduces the chapter's
concerns in the author's register. Plain prose, not italic.]

[Paragraph 2: 2–4 sentences. More explanatory. Gives the reader
enough context to understand what they're about to encounter.
Places the chapter in the book's arc without becoming a meta-
commentary. Example: "I made the asymmetric-risk argument back in
Chapter 3 — this chapter builds on that by showing you the three
species of bad data I keep seeing…"]

**Watch for**
- [Phrase-anchored bullet, 1–3 sentences, author voice. Cites a
  specific word, metaphor, anecdote, or moment from the chapter
  text. "When I drop the bulldozer metaphor in a bit, I mean
  something very specific — the entrepreneur who asks 'do you
  think this is a good idea?' and treats the nod they get as
  data."]
- [3–5 bullets total. Each grounded in extracted verbatim
  material.]

**Key terms**
- **Term** — Author-voice definition, 1–2 sentences. The
  author's own working vocabulary. No academic paraphrase.
- [3–6 term→definition pairs total.]

**Questions to hold**
- [ ] Open philosophical question the chapter raises, framed as
  the author asking the reader to wrestle with it.
- [ ] [3–5 questions total. Checkboxes preserved. Not personal-
  action questions — the chapter's unresolved tensions.]

**Per-lens angles**

*Product Manager.* [3–5 sentences, flowing prose. First person.
Directly addressed. Names what this chapter asks of the PM
specifically. Enough depth that a PM nods in recognition. Not a
bullet disguised as a paragraph.]

*CEO.* [Same depth. Same flow. The ask of the CEO specifically.]

*Entrepreneur.* [Same depth. Same flow. The ask of the
entrepreneur specifically.]
```

### Flexibility rules

- If the chapter's content is **structurally a comparison** (two conversation patterns, two failure modes, before/after dialogues), the generator may render Watch For or Key Terms as a **2-column markdown table** instead of a bulleted list.
- If the chapter has a **sequential process**, Watch For may become a numbered list.
- **Per-lens angles never collapse** — always three separate paragraphs, always in the listed lens order, even if two lenses share overlap.

### What stays unchanged

- Bold-label sections (`**Watch for**` etc.) — no H3 headers, no section emojis
- `> …` blockquote for the one-liner
- `*italic*` role names in per-lens angles
- `- [ ]` checkbox format for Questions to Hold
- The `---` divider + `## ✍️ My notes` pattern after the brief (skill-wide, not changed here)

## 6. Design — post-read synthesis structure

Same voice principles. Same bold-label format.

```markdown
**Post-read synthesis**

> [!info] Generated at setup — no reader notes yet
> [existing callout, unchanged]

> [Author-voice one-line core idea — the sentence they'd want
> to survive this chapter]

[Paragraph 1: 2–3 sentences in author voice. Reflecting on what
you just read together. Plain prose, not italic. Example: "Now that
you've made it through — here's what I most hoped landed, and here's
why I built the chapter this way."]

[Paragraph 2 (optional, chapter-dependent): 2–3 more sentences.
Where the chapter fits in the book's running argument now that it's
done its work. Plain prose.]

**Key takeaways**
- [Substantial bullet, 1–2 sentences per bullet, author voice.
  4–6 total. No clipped labels.]
- [End with a mental-model-naming sentence: "The model I hope you
  walk away with: false positives are asymmetric bets against
  your own runway."]

**Per-lens takeaways**

*Product Manager.* [3–5 sentences, flowing, directly addressed.
Monday-morning specific — what changes in the PM's week because
of this chapter. Author voice.]

*CEO.* [Same depth.]

*Entrepreneur.* [Same depth.]

**Contrarian take**

[2–3 paragraphs. Voice break: the critic speaks first. "A sharp
reader will push back here, and they'd be right about X —" then
the specific pushback, concrete and biting. Then back to author
voice, graciously: "I'd give ground on that. This is where my
argument stretches further than my evidence can carry…"]

**Actionable experiments**
- [Concrete experiment, 1–2 sentences, author voice. 2–3 total.]

**Connections**
- **[Other book / framework]** — [1-sentence link in author voice.
  "*Lean Startup* (Ries) — he wrote the learning-loop theory; I'm
  writing the script for what to say inside the loop."]
- [3–5 connections total.]

**Flashcards**
- **Q:** [Sharp question]
  **A:** [Under 30 words]
- [3–5 pairs.]
```

## 7. Design — close-reading extraction discipline

**Required workflow step.** Before filling any pre-read or post-read template, the generator runs an internal extraction pass against the chapter text. The extraction output stays internal (not written to the chapter file) — it's the scratchpad the generator reasons over.

### The extraction pass (per chapter)

1. **Thesis** — the one sentence from the chapter that, reduced to ~25 words, survives. Verbatim or close paraphrase.
2. **Anchor phrases** — 8–12 verbatim phrases, metaphors, vivid images, canonical examples. Specific words the author uses (bulldozer, toothbrush, fragile, gold dust, doomed, earlyvangelist, etc.). Every Watch-For bullet must attach to one.
3. **Terms the author actively defines** — 4–8 terms with the author's own working definition. Pulled from the text. Not invented.
4. **Author-voice register** — 2–3 sentences characterizing the author's voice in this chapter (can refine across chapters). Colloquial / academic / polemical / warm / etc. Specific turns of phrase. This register drives every section's voice.
5. **Structural role** — 1–2 sentences on what this chapter does in the book's argument. "It's the 'why rigor matters' beat before the rules in Ch 4."

### Enforcement

The SKILL.md workflow step for `:brief N` and `:synthesize N` explicitly reads:

> **Before filling the template: complete the close-reading extraction (thesis, 8–12 anchor phrases, 4–8 defined terms, voice register, structural role). Do not proceed to template filling until extraction is complete. Each bullet, term, and per-lens paragraph must be traceable to extracted material.**

This converts the extraction from "guidance" to "hard discipline."

## 8. Design — execution model (parallel, non-blocking)

The main performance bottleneck in the current setup flow is **serial generation** in the main agent's context. For a 32-chapter book, that means 32 × (extraction + generation) blocking in one thread.

**Fix:** fan out across subagents using Claude Code's native `Task` tool. The close-reading extraction lives *inside* each subagent, so parallelism is free.

### Setup flow (revised)

1. **Parse EPUB** — `scripts/parse_epub.py`, single call.
2. **Generate `0. General.md`** — in the main agent. Extracts book-level author voice register, thesis, lens framing. These become **shared subagent context**.
3. **Create chapter stubs** — programmatic script, fast.
4. **Dispatch parallel subagents** — single message with N `Task` tool calls (4–8 subagents for a 32-chapter book, batched 4–8 chapters per subagent). Each subagent receives:
   - Its assigned chapter texts (inline, or via file paths)
   - Book-level author voice register (from step 2)
   - Book thesis and frozen lens list
   - Full pre-read / post-read templates
   - Close-reading extraction discipline as instruction
   - Direct write mandate — subagent writes the completed brief + synthesis straight into the chapter file
5. **Wait for all subagents**, verify file structure, report.

### Superpowers skills invoked internally

- `superpowers:dispatching-parallel-agents` — codifies the fan-out pattern (independent tasks, no shared state, parallel `Task` calls in a single message).
- `superpowers:subagent-driven-development` — used when the user later runs a multi-chapter `:synthesize` upgrade across read chapters.

These are invoked by the reading-lens skill internally. The user doesn't see them.

### Non-setup commands

- `:brief N` and `:synthesize N` for a single chapter stay in the main agent (no parallelism needed for N=1).
- `:overview-redo` stays in the main agent.

### Performance expectation

For a 32-chapter book, the setup time drops roughly 4–8× relative to the current serial flow. The exact multiplier depends on how many subagents can run concurrently and chapter size variance.

## 9. Design — language support

### Default

English.

### Per-book override

During `/reading-lens:setup`, if the user's invocation message is in a non-English language, or if they include an explicit directive like *"do it in Turkish"* / *"yap bunu Türkçe"*, the skill:

1. Sets `language: <code>` in the book's `0. General.md` frontmatter (ISO 639-1: `en`, `tr`, `de`, etc.)
2. Generates all output (`0. General.md`, every chapter brief and synthesis) in that language
3. Author-voice channeling is preserved across the target language — Fitzpatrick in Turkish still reads like Fitzpatrick, not like generic Turkish prose

### Per-command consistency

`:brief N`, `:synthesize N`, `:overview-redo`: the skill reads the `language` field from `0. General.md` frontmatter and produces output in that language. The user doesn't need to re-specify per command.

### Language override mid-book

If the user wants to change a book's language after setup, they'd use `/reading-lens:overview-redo` (which they can already do) — the redo honors a new language directive if present, otherwise preserves the existing frontmatter value.

## 10. Design — linking mechanism

Three linkage types, inside existing sections. No new top-level sections.

### 10.1. Cross-chapter wikilinks

When a chapter builds on an earlier one, the brief/synthesis includes inline Obsidian wikilinks:

> *"I made the asymmetric-risk argument back in [[3. Talking to customers is hard|Chapter 3]] — if you skipped that, it's worth re-reading before this one."*

Obsidian renders them clickable. This works for both pre-read (forward/back references) and post-read (synthesis tying chapter to book's larger argument).

### 10.2. Author-voiced Connections

The existing Connections section stays, but each connection becomes a **1-sentence author-voiced link** rather than a dry "see also":

> *"*Lean Startup* (Ries) — he wrote the learning-loop theory; I'm writing the script for what to say inside the loop."*

### 10.3. Mental-model naming

The last bullet of Key Takeaways (post-read only) explicitly names the mental model the chapter builds, as a takeaway sentence:

> *"The model I hope you walk away with: false positives are asymmetric bets against your own runway."*

This helps the reader name what they learned so it sticks. Not a new section — a conventional closing line inside Key Takeaways.

## 11. Migration

### Changes to `SKILL.md`

- **Section "Pre-read Brief — fills `## Pre-read brief`"** — rewrite the template to match Section 5 of this spec (author-voice opener paragraphs, deeper bullets, full-paragraph per-lens angles).
- **Section "Post-read Synthesis — fills `## Post-read synthesis`"** — rewrite to match Section 6 (author-voice reflection paragraphs, mental-model-naming closer in Key Takeaways, Contrarian Take voice-break pattern).
- **New section before templates: "Writing voice"** — 3–4 paragraphs describing the author-voice principle, character channeling, and voice-break rules. Referenced from each template.
- **New section: "Close-reading extraction discipline"** — codifies Section 7 as a required workflow step in `:brief` and `:synthesize`.
- **Workflow Step "Generate pre-read briefs for every chapter"** (currently setup step 11) — replace the inline serial generation with a **parallel subagent dispatch** subsection. Document the fan-out pattern. Reference `superpowers:dispatching-parallel-agents`.
- **Workflow Step "Generate post-read syntheses for every chapter"** (currently setup step 12) — same treatment.
- **Config schema** — add `language` to the book-level frontmatter spec (documented in the `0. General.md` template section).
- **Quality Rules** — tighten the existing rules. The "No generic MBA platitudes" rule stays. Add: "Every Watch-For bullet must cite a specific phrase from the chapter text." Add: "Per-lens angles never collapse — always three distinct paragraphs in the declared lens order."

### Backward compatibility

Existing chapter files produced by the old skill (e.g., *The Mom Test* setup from earlier today) remain valid. The user can re-run `:overview-redo` on an old book to regenerate `0. General.md` with the new voice, and `:brief N` / `:synthesize N` per chapter to upgrade individual chapters. A bulk upgrade command is *not* in scope for this spec — the user can script it themselves if needed.

### No changes to

- `scripts/parse_epub.py` — untouched
- `config.yaml` — untouched
- Filename sanitization rules — untouched
- Update-Don't-Delete safety behavior — untouched
- Sub-command names and arguments — untouched

## 12. Testing / validation

### Quality gate — re-run on *The Mom Test*

After implementation:

1. Delete one existing chapter file (e.g., `3. Talking to customers is hard.md`) preserving only the `## ✍️ My notes` section.
2. Run `/reading-lens:brief 3` to regenerate the pre-read.
3. Run `/reading-lens:synthesize 3` to regenerate the post-read.
4. Compare against the reference screenshot the user shared and against the old output:
   - Does the pre-read read as if Fitzpatrick sat down to write it?
   - Are Watch-For bullets anchored to specific phrases from the chapter?
   - Do PM / CEO / Entrepreneur each have a full 3–5 sentence paragraph?
   - Does the prose flow — no em-dash pileups, no clipped labels?
   - Does the post-read's Contrarian Take break voice gracefully and return?

### Parallel dispatch smoke test

Run `/reading-lens:setup` on a short-to-medium book (10–15 chapters) and time the total setup duration. Compare against the old serial flow on a book of comparable length. Target: ≥3× speedup.

### Language override test

Run `/reading-lens:setup /path/to/book.epub` with an explicit *"do it in Turkish"* directive in the setup message. Verify:
- `0. General.md` frontmatter has `language: tr`
- All chapter briefs and syntheses are in Turkish
- The author's voice register is preserved in Turkish (not generic)
- Re-running `:brief N` on an existing chapter continues in Turkish without re-specifying

### Per-lens regression test

Pick three chapters from different books (if any other book is set up) and verify that per-lens angles are never collapsed into a single line — always three distinct paragraphs.

## 13. Deferred / out of scope

- **Bulk upgrade command** for existing books generated under the old skill. The user can re-run `:brief` / `:synthesize` per chapter manually or script it.
- **Automatic cross-chapter wikilink detection** — the generator uses wikilinks when the author explicitly references back ("as I said in Chapter 3"). Detecting *implicit* connections across chapters is a future enhancement.
- **Per-sentence citations** in Watch-For bullets (linking to exact paragraph in the EPUB). Out of scope — the generator cites phrases, not line numbers.
- **User-customizable templates** (letting the user edit the pre-read / post-read shape). The current spec is opinionated on structure. A future version could allow template overrides via `config.yaml`.
- **Non-EPUB sources** (PDFs, web articles) — stays scoped to EPUB input.
