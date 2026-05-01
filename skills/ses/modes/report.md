# Mode — Report

Use when drafting an analysis doc, a written report, a Notion data report, or anything structured around a question + evidence + answer + actions. Voice rules from `voice/<lang>.md` apply on top.

This file is about *writing*. Domain-specific rules (data reconciliation, query verification, source-of-truth checks for analytics work) live in the relevant domain skill (e.g. `joyo-data-analyst` for JoyoLabs data) — not here.

## When to use

- Notion pages titled with a date + topic ("May 1 — Top 20 Country Pricings").
- Multi-section docs that combine framing + evidence + interpretation + recommendations.
- Any prose deliverable where another person needs to read, understand the question, see the evidence, and walk away with an action.

If the doc is mostly narrative + opinion without evidence/recommendations → use `blog.md` instead.

## Required structure (narrative arc)

Every report follows this arc — **General → Specific → General + Action**. Lets the reader skim or deep-read at their preference, and lets the conclusion bind back to the question the intro asked.

1. **TL;DR** — at the very top, before anything else. 3–5 sentences max. Executive-level summary written as a *pitch*, not a recap: scope (what's being analyzed + time window if relevant) + what we did (one phrase) + what we found (the punchy result with the headline number) + what's next (one line). The reader should leave the TL;DR knowing the story AND wanting to read on for the proof. If they only read the TL;DR, they still got the answer.

2. **Introduction** *(general)* — what we're looking at and why it matters now. Scope: time window, audience/segment, key variables. Brief framing of how the report will answer the question. Stay declarative — describe what the report does, not how the writing of it went.

3. **Development** *(specific)* — the chapters / sections / tables / evidence. Each section opens with the bottom-line finding before the supporting data (voice rule: bottom line first). Caveats inside parens or em-dashes, not as standalone "Note:" paragraphs.

4. **Conclusion** *(general — harder than intro)* — synthesize the development findings back into the question the introduction asked. Quantify the answer in one or two sentences with real numbers. Optional: name the contradictions or open questions the development surfaced. Don't just recap section headers — close the loop.

5. **Next steps** *(action)* — recommendations sized by effort (small / medium / large) + expected payoff. Recommendations without sizing get ignored.

## Formatting rules

- **Notion toggle blocks** for methodology details / extended context / "for the curious" / appendix-style content. Top-level reading flow stays clean; readers expand toggles only if they want depth.
- **Table-first for data**, prose-second. Don't restate every cell in prose — call out the rows that move the story.
- **Currency** with `$` prefix and comma-separated thousands: `$308,684`. **Percentages** with one decimal: `13.85%`. **Counts** with comma-separated thousands: `9,374`.
- **Scope labels on every total** when sections cover different audiences/segments/slices. A row that says `Total | $308,684` two paragraphs after `Total | $354,880` with no scope label is a defect — readers will conflate them.

## Always-on

- **Reports are published artifacts, not work logs.** Anything about how the report was made — corrections, methodology pivots, dead ends, "we initially found X but rebuilt to Y" — does NOT go inside the report body. The published version reflects the final framing only, declaratively.
- **Run `humanizer` after the draft.** No exceptions. (Voice rule + mode rule.)
- **TL;DR is non-optional.** Even short reports have one. If the doc is too short to justify a TL;DR, it isn't a report — it's a Slack message.
- **Conclusion ties back to Introduction.** The conclusion's job is to answer the question the intro raised, with the evidence the development supplied. Not a bullet-list recap.
- **Prose figures must match adjacent tables** to 0-decimal tolerance. When a draft updates a table, scan the prose around it and reconcile.

## What to avoid

- **Correction-narration anywhere in the report.** No "earlier we used X but rebuilt to Y", "post-audit", "after the rebuild", "this section was rebuilt because". The published report has no past tense about its own production. If the work pivoted mid-investigation, the report only reflects the final framing.
- **Section titles that flag the writing process.** "Post-audit lock", "Rebuilt section", "Corrected version" — name the section by what it contains, not by what happened to it.
- **TL;DR longer than 5 sentences.** If it can't fit, the doc is two reports. Split or tighten the framing.
- **TL;DR that recaps instead of pitches.** The opening should make the reader want to read on. State the punchy result with the headline number; let the body deliver the proof.
- **Bullet-list conclusion that restates section headers.** The conclusion is writing, not a recap.
- **Open-ended recommendations** without effort/payoff sizing. They get ignored.
- **Closing flourishes** ("In conclusion...", "I hope this helps", "Let me know if questions"). The doc ends when the next-steps end.
- **Unnamed scope.** When a doc covers different audiences/segments/slices in different sections, every total figure must name its slice. One unlabeled total in a multi-slice doc is a defect.

## Notion-specific (when destination is a Notion page)

- Title is the same as the page title — don't repeat it as an H1 inside the body.
- Use Notion's native toggle blocks (`▶`) for methodology details / extended context — NOT markdown details/summary tags.
- Use Notion callouts (with emoji like 📐, 📌, ⚠️) for framing notes that benefit from visual separation from the prose.
- Use Notion's database/table block for actual data tables (not markdown tables) so they're sortable/filterable.
- Use Notion's column layout for side-by-side comparisons (current state vs proposed state).
- Quote-block for the TL;DR at the very top so it visually reads as the headline.
