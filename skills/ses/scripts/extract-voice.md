# Prompt template — Extract voice features from a Semih sample

Run this when Semih shares a document, blog post, Slack message, email, or any prose he wrote himself, and asks (or implicitly needs) the voice file to learn from it.

## Step 1 — Determine the language

Read the sample. Identify the primary language. If mixed, ask Semih which language's voice file should absorb the features.

## Step 2 — Save the raw sample

Save the original text under `examples/<lang>/<short-slug>-<YYYY-MM-DD>.md`. This is the audit trail — future runs can re-extract or sanity-check against it. Don't paraphrase or clean up the sample; save it verbatim.

## Step 3 — Extract features into these buckets

Read the sample looking specifically for:

| Bucket | What to look for |
|---|---|
| **Vocabulary** | Words used unusually often (e.g., "okay", "hey", "nope"). Words that should appear but don't (AI-cliché vocabulary like "leverage" — its absence is itself a feature). Domain terms that stay untranslated. |
| **Sentence shapes** | Average sentence length. Where em-dashes appear. Lead-in phrases (`X: Y` patterns). When paragraphs break. |
| **Punctuation / case** | Lowercase mid-sentence? Comma-thousand numbers? Percentage formatting? Emoji policy? |
| **Discourse markers** | The "spoken-on-page" tics: openers ("okay,", "hey,"), confirmations ("yep", "nope"), transitions ("so,", "well,"). |
| **Argumentation tics** | How does he disagree? How does he concede? How does he caveat? Does he number claims or hedge them? |
| **What's NOT there** | AI-cliché vocabulary, closing flourishes, meta-narration ("Let me break this down"), unnecessary hedging — note their absence as features. |
| **Structural moves** | Does he state findings before unpacking, or vice versa? Where do caveats land — in parens, em-dashes, or separate sentences? |

## Step 4 — Append findings to `voice/<lang>.md`

Use the `Edit` tool. For each feature, append a line in the existing format:

```markdown
- **<feature>** <description with concrete example from the sample>. *Why:* <why this matters / what failure mode it prevents>.
```

Do NOT overwrite existing patterns — append. If a new finding contradicts an existing one, append the new one and ask Semih which to keep.

Place new entries in the right section (Vocabulary / Sentence shapes / Punctuation and case / Discourse markers / Argumentation tics / What to avoid / Structural prose moves). If a new bucket is needed, add it at the bottom with the same heading pattern.

## Step 5 — Show Semih what changed

Tell him:
- Where the raw sample was saved (`examples/<lang>/...`).
- Which features were extracted (count + 2-3 examples).
- Which voice file was updated.
- Sync to `meseba-skills` repo (`bash ~/.claude-shared/scripts/sync-skills.sh`) — mention this; don't auto-run unless he says yes.

## Discipline

- **Concrete > abstract.** "Uses 'okay' as opener" beats "Uses casual openers." The voice file gets queried mid-draft; concrete patterns are easier to apply than abstract principles.
- **Pair every rule with a *why*.** If you can't articulate the failure mode, the rule is probably noise.
- **One sample → 5–10 features max.** Don't over-extract; you'll dilute the signal. Pick the patterns that show up *consistently* in the sample, not one-off quirks.
- **Multilingual hygiene.** If the sample is Turkish, append to `voice/tr.md` ONLY — don't bleed Turkish features into `voice/en.md`. Cross-language transfer is a separate discipline.
