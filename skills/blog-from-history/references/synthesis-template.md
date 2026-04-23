# Phase 3 — Synthesis Template

After all research agents return, collapse their findings into `BLOG-CATEGORIES.md`. This phase is done by the orchestrator (you), not a subagent — synthesis needs judgment about what's distinct, what's overlapping, and what collapses cleanly.

## Step 1 — Extract compact bullets from each research file

Run this Python snippet via `ctx_execute`. It reads each `0N-*.md`, pulls sections 2 / 3 / 4 / 5 / 6 / 7, and compacts each bullet to ~280 chars. Target: all N findings fit into one context window.

```python
import re, os, glob

ROOT = "{{BLOG_RESEARCH_DIR}}"  # e.g. "/Users/foo/project/blog-research"

def extract_section(text, title_rxs):
    parts = re.split(r"^(##\s+.*)$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i+1] if i+1 < len(parts) else ""
        for rx in title_rxs:
            if re.search(rx, header, re.I):
                return header, body
    return None, None

def compact_bullets(body, max_n=12, max_chars=280):
    bullets = re.findall(r"^(?:\d+\.|\-|\*)\s+(.+?)(?=\n\n|\n(?:\d+\.|\-|\*)\s+|\Z)",
                          body, flags=re.M|re.S)
    out = []
    for b in bullets[:max_n]:
        b = re.sub(r"\s+", " ", b.strip())
        if len(b) > max_chars:
            b = b[:max_chars] + "…"
        out.append(b)
    return out

for fname in sorted(os.listdir(ROOT)):
    if not re.match(r"^\d+-.*\.md$", fname): continue
    with open(os.path.join(ROOT, fname)) as f:
        text = f.read()
    print("\n" + "="*60)
    print(f"### {fname}")
    print("="*60)
    for label, patterns in [
        ("ACCOMPLISHMENTS", [r"Professional accomplishments", r"outcomes"]),
        ("TECH",            [r"Technical work", r"Hooks.*harness", r"orchestration"]),
        ("DECISIONS",       [r"Decisions.*trade-offs"]),
        ("PATTERNS",        [r"Tooling.*skills.*patterns"]),
        ("STORIES",         [r"Stories worth blogging"]),
        ("TIMELINE",        [r"Timeline anchors"]),
    ]:
        h, body = extract_section(text, patterns)
        if not body: continue
        bullets = compact_bullets(body, max_n=10)
        print(f"\n[{label}]")
        for i, b in enumerate(bullets, 1):
            print(f"  {i}. {b}")
```

## Step 2 — Cluster the compacted bullets into ≤5 categories

Read all the compacted output. Look for **themes across slices**, not within a single slice. The categories almost never map 1:1 to slices — a slice might contribute to 2 categories, or two slices might collapse into one.

### Clustering dimensions that work

Pick one of:
- **Audience** (external users / internal team / yourself) — this is the default and usually works.
- **Problem type** (shipping features / building infrastructure / building systems).
- **Lifecycle stage** (zero-to-one / growth / maturity / retirement).

### Rules

1. **≤5 is hard cap.** If you have 6 candidates, collapse the weakest two.
2. **No category should be a single slice.** If you find yourself writing "Category 3: what Slice C did", you're categorizing lazily. Re-read.
3. **Every category must have a thesis title, not a taxonomy label.** Not "Mobile Work" — but "Shipping subscription-mobile features that move the revenue curve."
4. **Each category should pull evidence from at least 2 slices.** Cross-slice evidence is what makes a category real. If one category pulls only from Slice A, it's probably a slice masquerading as a theme.

## Step 3 — Write `BLOG-CATEGORIES.md`

Use `assets/BLOG-CATEGORIES.md.template` as the starting structure. For each of the ≤5 categories, write:

### Required structure per category

```markdown
## N. [Thesis title — methodology-framed, NOT product-framed]

**Who it's for:** [audience tag — 1 line]
**The thread:** [1-sentence statement of the professional approach this category expresses]

**Approach evidence (from agents {{X}} + {{Y}}):**
- [5–10 bullets, each referencing a SPECIFIC decision, pattern, or outcome from the research files]
- [Stack / framework names ARE fine; product names are NOT]
- [Each bullet should be standalone — a reader should understand the point without needing the source file]

**Draft post titles (methodology-first):**
1. [Title 1]
2. [Title 2]
...
(6–10 titles per category)
```

### Title craft

Methodology-first titles sound like theses, not table-of-contents entries:
- BAD: "Working with Flutter"
- GOOD: "Why I ship referral rewards as $0 promo products, not custom billing logic"
- BAD: "Analytics dashboard features"
- GOOD: "Vertical-slice shipping: every analytics feature through all six layers in one PR"

Titles should state a position. If a title would fit on any generic tech blog, it's too flat.

## Step 4 — Append cross-category and gaps sections

After the 5 categories, add:

```markdown
## Cross-category posts

[Stories that span 2+ categories — often your highest-leverage posts because they thread the whole stack together]

- **"[Title]"** — [1-line description + which categories it spans]

## What's NOT in these categories (intentional exclusions)

[Data sources you skipped, corpora you didn't mine, work that doesn't fit — be honest]

## Next actions

[Which category to write first, highest immediate reach, optional follow-ups]
```

## Step 5 — Verify denylist clean

```bash
python3 scripts/verify_denylist.py BLOG-CATEGORIES.md .denylist.txt
```

Expect 0 word-bounded hits. If any appear, rewrite those passages before spawning Wave 2.

## Why this synthesis shape works

- **≤5 cap** forces real synthesis — 10 categories is a taxonomy, 5 is a series.
- **Cross-slice evidence** requirement prevents you from writing 5 category labels that are just slice labels.
- **Thesis titles** force you to pick a *position*, which is what makes a category worth reading about.
- **Denylist-clean before Wave 2** prevents branded phrasing from leaking into the essay-agent prompts and propagating downstream.

## Common synthesis mistakes

- Writing categories that mirror the slice names 1:1 — you haven't synthesized, you've relabeled.
- Including evidence bullets that reference specific ticket IDs, PR numbers, or feature flag names — these either need to be anonymized or removed.
- Draft titles that could fit any tech blog (generic "How I use X" patterns). Aim for titles that only *you* could write.
- Writing 7 categories because you "can't decide which to cut." Cut anyway. The cap is the synthesis.
