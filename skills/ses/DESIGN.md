# ses — v1 Design

> **Frozen design doc, 2026-05-01.** This file records the original design decisions so future edits can either honor them or knowingly deviate. Not loaded at activation — read only when restructuring the skill.

## Purpose

Personal-writing skill for Semih Babacan (semih@joyolabs.com). Captures his voice and structural taste so any document, report, blog post, or Notion page produced on his behalf reads like him instead of generic AI prose. Multi-language (English + Turkish v1, others added on demand). Modes for output type (`report` + `blog` v1).

The problem the skill solves: by default I produce prose with telltale AI markers — "comprehensive", "leverage", "robust", em-dashes-where-Semih-would-use-a-period, paragraph shapes that don't match how he actually writes. Each fresh session has to relearn his preferences from scratch. `ses` persists those preferences.

## Out of scope (v1)

- Source code, code comments, commit messages, log output — those have their own conventions and don't benefit from `ses`.
- Multi-author writing — `ses` is a single-author skill (Semih). Other team members would need their own skill instance.
- Auto-applying voice to text-not-meant-to-be-prose — captions on charts, table cells, JSON.

## Why these naming + structure choices

- **Name `ses`**: Turkish for *voice / tone / sound*. Three letters, distinctive, multilingual proof-of-concept baked into the name. Picked over `my-mouth`, `kalem` (Turkish for *pen*), `scribe`, `as-semih`, `longhand`, `house-style`, `semih-says`.

- **Two-level disclosure** (SKILL.md → voice/* + modes/*): activation loads only the thin index; voice and mode files load on demand. Avoids dumping unrelated rules into context. Matches the `joyo-data-analyst` learnings-map pattern.

- **Per-language voice files**: voice features differ enough between English and Turkish (idiom, particle use, sentence rhythm, register markers) that mixing them in one file would cause cross-contamination during drafting.

- **Per-mode structure files**: report and blog share voice but differ structurally — reports want toggles + methodology locks + scope-labels; blogs want hooks + narrative arcs + CTAs. Same voice, different bones.

- **`examples/<lang>/` for raw samples + `scripts/extract-voice.md` for the extraction prompt**: this is the feedback loop. Semih shares samples → script extracts features → features get appended to `voice/<lang>.md` via `Edit`. Examples stay on disk so future runs can re-extract or audit.

- **Lives in `meseba-skills`, NOT JoyoLabs team repo**: this is personal voice, not team knowledge. Sync via `sync-skills.sh`.

## Loading rules (verbatim from SKILL.md)

| Trigger | Files loaded |
|---|---|
| Skill activation | `SKILL.md` only |
| Output language detected | `voice/<lang>.md` |
| Output mode decided | `modes/<mode>.md` |
| Sample doc shared | `scripts/extract-voice.md` |

## Always-on rules

1. Detect target language first.
2. Load matching mode.
3. Run `humanizer` skill on the final draft.
4. Edit files in place — no `.bak` siblings.
5. Voice file is a guide, not a costume.

## v1 ships with

- `voice/en.md` populated with patterns observed in the originating session (em-dash for inline asides, lowercase casual register, "okay" as discourse marker, no AI-cliché vocabulary, etc.).
- `voice/tr.md` as a stub — first Turkish use will trigger sample collection.
- `modes/report.md` populated with rules already established (Notion toggles for methodology/extra-info; scope-labels per chapter; methodology lock at top; humanizer required).
- `modes/blog.md` as a stub.

## Future modes likely to be added

In rough order of likelihood:
- `email` — long-form email, especially to investors / partners.
- `exec-brief` — short C-level summary doc.
- `slack-message` — substantive Slack post (not one-liner).
- `release-note` — App Store / changelog copy.
- `slide` — slide-deck text (titles, bullets, speaker notes).

These don't ship in v1 — they get added when the first real instance shows up.

## Future languages likely to be added

- `tr` (Turkish) — already stubbed, first sample triggers population.
- `de`, `es`, `fr` — only if Semih ever drafts in those.

## Maintenance discipline

- Voice files grow as samples are processed. Soft cap ~150 lines per language file before pruning low-signal entries.
- Mode files stay small (<100 lines). Anything bigger means the mode is doing too much.
- `extract-voice.md` is a prompt template — should not exceed one screen. If extraction logic gets complex, factor into multiple sub-templates.
