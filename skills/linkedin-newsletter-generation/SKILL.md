---
name: linkedin-newsletter-generation
description: Generate high-quality LinkedIn newsletters and posts. Created by Nazım (4 Kallavi Turks). Uses Claude Opus 4.6, generates 1 long post + 1 image, also adds to personal blog.
---

# LinkedIn Newsletter Generation

**Created by Nazım** — 4 Kallavi Turks

A skill for generating polished, analytically rigorous LinkedIn content with strict quality gates.

## Key Differences from Standard LinkedIn Generation

- **Model**: Claude Opus 4.6 only (via OpenRouter: anthropic/claude-opus-4.6)
- **Output**: 1 long post (not 5 variations)
- **Images**: 1 image (not 3)
- **Blog Integration**: Automatically adds to personal blog (personal-blog-semih)

---

## When to Use

- Generate a LinkedIn newsletter post on any topic
- Create analytical, Paul Graham-style long-form content
- Build content that demonstrates structured thinking

---

## Rules Files (All Required)

This skill uses the following rule files (embedded):

1. **Structural Exclusions** — What NOT to write about
2. **Evidence Bank** — Decision contexts and constraints
3. **Language & Reasoning Constitution** — How reasoning is expressed
4. **LinkedIn Operating Principles** — Content standards
5. **Personal Analytical Playbook** — Risk posture and stage-based analysis
6. **Language & Expression Rules** — Sentence-level rules
7. **Paul Graham Exception Layer** — Style overrides when requested
8. **Image Generation Rules** — How to create visuals
9. **Blog Integration** — How to add posts to personal blog
10. **Reference Writers Modules** — Calibration framework for intellectual rigor
11. **Rewrite Instructions** — Concept → Accessible essay transformation
12. **Series Recommendations Rule** — For series posts, create recommendations.md
13. **Styling** — Visual guidelines for images
14. **Writing Style** — Paul Graham writing techniques

---

## Phase 1: Topic Qualification

Before generating, verify the topic passes these gates:

**Gate 1: Evidence** — Topic must connect to:
- A Decision Context (C1-C7) from Evidence Bank
- An Observed Constraint (K1-K6)
- A Recurrent Failure Mode (F1-F5)

**Gate 2: Exclusion** — Reject if topic:
- Relies on personal experience, motivation, generic advice
- Makes universal claims without localization
- Substitutes narrative for mechanism
- States preferences without trade-offs
- Calls outcomes/predictions
- Fetishizes tools/frameworks
- Over-claims confidence

**Gate 3: Confidence** — B1/B2 domains = structural analysis only. B3 = silence.

**Gate 4: Style** — If "Paul Graham Style" requested, apply the exception layer.

---

## Phase 2: Pre-Generation Setup

1. **Select Primary Category** (from reference writers):
   - A: Behavioral Econ, B: Microecon, C: Game Theory, D: Macroecon
   - E: Institutional, F: Dev Econ, G: Uncertainty, H: Strategy
   - I: M&A, J: Market, K: Finance, PG: Paul Graham

2. **Identify Trade-Off**:
   - Capital/Optionality, Speed/Reversibility, Efficiency/Resilience
   - Scale/Control, Precision/Robustness, Local/System
   - Info/Action, Incentive/Autonomy

3. **Determine Risk Posture**:
   - Early (Downside-first)
   - Mid (Option-value)
   - Later (Asymmetry-seeking)

---

## Phase 3: Generation (Claude Opus 4.6)

**Model**: `anthropic/claude-opus-4.6` via OpenRouter

Generate **1 long post** (not 5). Apply:

### Structural Template

1. **Observation** — A concrete pattern, mistake, or tension
2. **Underlying Mechanism** — Incentives, constraints, or assumptions
3. **Implication** — How this should change decision-making
4. **Clean Stop** — End without CTA, question, or summary

### Writing Style

- Use Paul Graham style language (plain, direct, counter-intuitive)
- No "I" for authority — use only for framing
- Static verbs, precise nouns
- No em-dashes, lists, or motivational tone
- Trade-offs must be explicit

---

## Phase 4: Image Generation

Generate **1 image** following:

1. **Ideation**: Identify 1 object/metaphor strongly associated with topic
2. **Styling**: Navy blue dominant (#1a365d), stylized, geometric, wireframe or glass-morphism
3. **Requirements**: Abstract/geometric, no humans/text, premium/intellectual feel
4. **Output**: Save to `posts/[topic-slug]/images/1.png`

---

## Phase 5: Blog Integration

After generating the LinkedIn post, add to personal blog:

1. **Create MDX**: `personal-blog-semih/app/(post)/2026/[slug]/page.mdx`
2. **Register in posts.json**: Add entry to `personal-blog-semih/app/posts.json`
3. **Update llms.txt**: Add URL to `personal-blog-semih/public/llms.txt`

See `personal-blog-semih/docs/integration/integration.md` for full details.

---

## Output Structure

```
posts/[topic-slug]/
├── version-long.md        # The 1 long post
└── images/
    └── 1.png              # Generated image
```

---

## Quality Gate (Final Check)

Before finalizing:
- [ ] Decision context explicit?
- [ ] Constraints named?
- [ ] Trade-off exposed?
- [ ] Risk posture appropriate?
- [ ] Abstraction localized?
- [ ] No prescription?
- [ ] Would a consultant/investor respect this?
- [ ] Is it interesting without my name?

If any fails, regenerate.

---

## Usage

```
Generate a LinkedIn newsletter about [TOPIC] in Paul Graham style.
```

```
Create a long-form LinkedIn post about [TOPIC] about capital allocation under scarcity.
```

---

## Publishing to LinkedIn

After generating, use the HTML Editor to format for LinkedIn:

**URL:** `http://bore.pub:50223/posts/newsletter-editor.html`

Features:
- Markdown editor with live preview
- "Copy for LinkedIn" button
- "Load Sample" with example

**Workflow:**
1. Generate newsletter content
2. Paste into the HTML editor
3. Edit/preview
4. Copy for LinkedIn
5. Paste to LinkedIn

---

## Example Output

**Latest generated newsletter: "The Identity Crisis of AI Agents" (March 6, 2026)**

Sample structure:

```
# The Observation

Most companies right now are worried about the wrong AI problem.

They're debating prompt engineering techniques, model selection, fine-tuning strategies. Meanwhile, something much more fundamental is broken, and almost nobody is talking about it.

Every AI agent accessing your systems today is, for all practical purposes, an unmanaged employee. No badge. No audit trail. No boundaries.

---

## The Underlying Mechanism

The reason this is happening is architectural. Our entire identity infrastructure was built for two types of principals: humans and services. AI agents are neither.

An agent isn't a human. It doesn't respond to MFA prompts. But it's also not a traditional service. It's autonomous.

---

## The Implication

Here's the thing that should make every product and engineering leader uncomfortable: the agent deployment problem is going to get worse by an order of magnitude before anyone's governance catches up.

---

## The Clean Stop

The agentic era doesn't need better models. It needs better infrastructure. Agent identity is the unsexy, foundational layer that determines whether enterprise AI deployment is a transformation or a catastrophe.
```

Format: *Observation* → *Underlying Mechanism* → *Implication* → *Clean Stop*
