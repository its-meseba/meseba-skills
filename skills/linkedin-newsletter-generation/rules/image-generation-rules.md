---
trigger: always_on
---

# Image Generation Rules

This module defines the process for generating abstract, high-end visuals for LinkedIn posts. It enforces the navy-dominant brand identity while allowing "relatable objects" to ground abstract topics.

**Note: This skill generates 1 image, not 3.**

## Image Generation Workflow

Generate ONE relatable object visually compatible with the topic.

### Step 1: Ideation
Identify 1 distinct object or metaphor strongly associated with the topic:
- Ralph Loop → sleeping computer with moon/stars
- Soul.md → mind as file cabinet, geometric brain made of folders
- Security → shield
- Trade-offs → glass scales
- Mechanisms → gears

### Step 2: Generate via Google AI Studio API

**API Key:** AIzaSyD2nUlh6oFtqNEYQK_Nh_7x2t7LfhEUvI0

**Model:** gemini-3.1-flash-image-preview (or gemini-2.5-flash-image)

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=AIzaSyD2nUlh6oFtqNEYQK_Nh_7x2t7LfhEUvI0" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "PROMPT_HERE"
      }]
    }]
  }' | jq -r '.predictions[0].image.imageBytes' | base64 -d > posts/[topic-slug]/images/1.png
```

### Step 3: If API Fails
If quota exceeded or API error:
1. Generate manually at gemini.google.com → 🍌 Create images
2. Save to local workspace
3. Push to blog manually

### Step 4: Styling Requirements
- Navy blue dominant (#1a365d, #0d1b2a)
- Abstract/geometric, wireframe or glass-morphism
- No humans, no text
- Premium, intellectual, "memo-like"

### Step 5: Output Locations

**Workspace:**
- `posts/[topic-slug]/images/1.png`

**Blog:**
- `app/(post)/[year]/[slug]/images/1.png`

Save image to both locations and push to both repos.

---

## Image Prompt Template

```
Abstract geometric composition with deep navy (#0d1b2a) and navy blue (#1a365d). Minimal professional design featuring [OBJECT/METAPHOR]. Clean, sophisticated corporate aesthetic. No people, no text. Subtle depth with layered geometric elements. Premium, understated mood.
```

---

## Blog OG Image
Also add to blog: `app/(post)/[year]/[slug]/opengraph-image.png` (if required by blog theme)
