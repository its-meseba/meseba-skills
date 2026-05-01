# Voice — Language Picker

Pick the file based on the **output** language, not the input language. If Semih asks (in English) for a Turkish blog post, load `tr.md`. If he asks (in Turkish) for an English report, load `en.md`.

| Output language | File | Status |
|---|---|---|
| English | `en.md` | populated v1 |
| Turkish | `tr.md` | stub — needs first sample |

## How to detect output language

In rough priority order:

1. **Explicit instruction** — Semih says "write this in Turkish" / "draft in English". Use that.
2. **Destination signal** — Notion page title is in one language, target audience is named ("write to the team" → English; "müşteriye yazıyorum" → Turkish). Use that.
3. **Topic content** — domain terms in one language (App Store, ROAS, ARPU → likely English; "pazarlama bütçesi", "abonelik" → likely Turkish).
4. **If still ambiguous** → ask Semih before drafting. Don't guess — drafting in the wrong language wastes a full pass.

## Adding a new language

Create `voice/<lang>.md` as a stub:

```markdown
# Voice — <Language Name>

> Stub. Awaiting first sample. Run `../scripts/extract-voice.md` against a real Semih document in this language to populate.
```

Then add a row to the table above. Do NOT draft in a stubbed language — ask Semih for at least one sample first.
