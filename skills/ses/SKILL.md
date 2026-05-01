---
name: ses
description: Personal writing voice and structural taste for Semih Babacan (semih@joyolabs.com). Use whenever drafting a document, report, blog post, Notion page, executive summary, release note, longer Slack message, email, or any prose meant to read as Semih's own words rather than generic AI output. Trigger on phrases like "write a report", "draft a doc", "put this on Notion", "write a blog post", "write up the analysis", "make this into a Notion page", or any task where Semih's voice should appear in prose. Activates whenever the requester is Semih and the output is prose for another human to read — even when not explicitly asked. Skip for source code, code comments, commit messages, and raw query/log output.
---

# ses — Semih's writing voice

`ses` is Turkish for *voice / tone / sound*. This skill keeps Semih's writing tastes — vocabulary, rhythm, structural preferences, per-language idiom — in one place so any document I produce on his behalf reads like him, not like generic AI prose.

## When this skill activates

Activate when **all** of:
- The requester is Semih (or the conversation is in his account).
- The output will be **prose meant to be read by another human** — a Notion page, a report, a blog post, an exec brief, a longer Slack message, an email, a release note.
- The output is NOT source code, NOT a commit message, NOT raw query/data output, NOT a CLI invocation.

If the output mixes prose and code (e.g. a tutorial blog post with snippets), `ses` applies to the prose around the snippets, not the snippets themselves.

## What loads when (progressive disclosure)

The body you're reading now is the only thing loaded on activation. Sub-files load on demand so the skill doesn't dump irrelevant rules into context.

| Trigger | Files to read |
|---|---|
| Skill activation (you're reading this) | `SKILL.md` only |
| Output language detected | `voice/<lang>.md` (English → `voice/en.md`, Turkish → `voice/tr.md`) |
| Output mode decided | `modes/<mode>.md` (report → `modes/report.md`, blog → `modes/blog.md`) |
| Semih shares a new sample doc to learn from | `scripts/extract-voice.md` then append findings to `voice/<lang>.md` |

Picker logic for language and mode is in `voice/_index.md` and `modes/_index.md` — read those if the right file isn't obvious.

## Hard rules (always on)

1. **Detect target language first.** Look at recent messages and the topic. English → load `voice/en.md`. Turkish → load `voice/tr.md`. If signals are mixed, ask Semih which language to draft in before writing any prose. Detecting wrong burns time on a draft Semih has to throw away.

2. **Load the matching mode.** Reports use Notion toggles, methodology locks, scope-labels per chapter — that lives in `modes/report.md`. Blogs have their own rules. Drafting without the mode file produces structurally-wrong output even if the voice is right.

3. **Run humanizer at the end.** After producing the draft, invoke the `humanizer` skill on the output to scrub residual AI-cliché vocabulary. Humanizer is a polish pass on top of voice, not a replacement for it.

4. **Edit files in place.** When Semih says "save this rule," use the `Edit` tool to amend the right file. Never create `.bak` siblings (per global `NO_INCREMENTAL_BACKUP_FILES` rule).

5. **The skill is a guide, not a costume.** Don't parrot Semih's literal phrases from the voice file. Use the file to *constrain choices* (vocabulary tics, sentence shapes, structural moves) — the actual writing still has to come from understanding the topic, and Semih still has to recognize the result as his own thinking.

## Updating the skill mid-conversation

- **"Save this as a rule"** → append a line to the right file via `Edit`. Voice-related (vocabulary, rhythm, idiom) goes in `voice/<lang>.md`. Structural (always-include sections, formatting choices, output destination conventions) goes in `modes/<mode>.md` or, if it applies across all modes, in this `SKILL.md`.

- **Adding a new mode** (e.g. `email`, `exec-brief`) → create `modes/<mode>.md` with that mode's structural rules + add a row to `modes/_index.md`. v1 ships with `report` and `blog`.

- **Adding a new language** (e.g. `de`, `es`) → create `voice/<lang>.md` (initially a stub) + add a row to `voice/_index.md`. Don't draft in a stubbed language — first ask Semih to share at least one sample doc, run `scripts/extract-voice.md` against it, and only then draft in that language.

- **Learning from a sample doc Semih just shared** → run the prompt template at `scripts/extract-voice.md` against the sample, then append the extracted features to `voice/<lang>.md`.

## Repo and sync

`ses` lives in the `meseba-skills` private repo (Semih's personal backup). Sync edits with:

```bash
bash ~/.claude-shared/scripts/sync-skills.sh
```

`ses` does NOT belong in the JoyoLabs team repo — that's for `joyo-*` skills only. Don't run `sync-joyo-skills.sh` from this skill's directory.
