---
name: little-paws
description: >
  Daily story generation for Little Paws Instagram Reels. Creates 4-frame (1 panel) or 8-frame (2 panel) 
  cute couple cat stories for Instagram. Uses frame-forge skill. Triggers daily at 8pm or via "/little-paws" command.
  Topics: cozy-morning, work-hard-play-hard, love-is-all-around.
---

# Little Paws - Daily Story Generator

Generate cute couple cat stories for Instagram Reels using the frame-forge skill.

## ⚠️ MANDATORY CHARACTER CONTEXT

**ALWAYS include this context in every image generation:**

### Character Structure
- **Male (Boy)** = Bigger/larger cat
- **Female (Girl)** = Smaller/cuter cat

### Male Character (Bigger)
- **Physical:** Larger, bigger build, slightly wider than tall, very round head that almost merges with body, thick fluffy tail
- **Eyes:** Large circular dark brown eyes with multiple white highlights (one large + one small dot)
- **Expression:** Loving, brave, intelligent, smart, very able. Slightly curious/neutral eyebrows
- **Accessories:** Dark brown collar with small gray/silver beads and teardrop-shaped GREEN PENDANT
- **Fur:** Fluffy white, short irregular black strokes for texture, tufts at ears/cheeks/chest/tail

### Female Character (Smaller)  
- **Physical:** Smaller, extremely round/chubby body (like plush toy), cute tiny stubby limbs
- **Eyes:** Very large emerald-green eyes with multi-highlight style, long subtle upper lashes
- **Expression:** Compassionate, loving, always caring, helping, understanding, supporting. Gets angry/complains because of love. Stronger blush on cheeks.
- **Accessories:** Beaded necklace (string of small gray/silver beads), sometimes holding a fish/toy
- **Fur:** White fluffy, slightly denser around cheeks for squishiness

### Art Style (ALWAYS FOLLOW)
- Kawaii/chibi cartoon style
- Thick consistent black outlines, slightly varied for hand-drawn feel
- Flat solid colors with minimal shading
- Multi-highlight eyes (one large round white highlight + smaller dot) for glossy doll-like look
- Short fur strokes around edges, ears, chest, tail for fluffiness
- Small blush marks under eyes
- Heart motifs for affection

### Color Palette
- Fur: Pure white #FFFFFF
- Outlines: Black #000000
- Inner ear/Blush: Soft pink ~#FF9AA2 / #FFC1CC
- Male eyes: Dark brown ~#4B2E2A
- Female eyes: Emerald green ~#1E8F6B
- Male collar: Dark brown ~#4B3621
- Pendant: Deep teal/green ~#0D8A5F
- Beads: Silver/gray ~#BDBDBD

## Reference Images

**Location:** `skills/little-paws/reference/`

- `story1.jpg` - Male (big with green pendant) + Female (small with fish)
- `story2.jpg` - Caregiver vs overworked dynamic (same characters)

## Main Story Topics (3)

### 1. Cozy Morning (cozy-morning)
The couple wakes up together, has breakfast, starts the day with love.

### 2. Work Hard, Play Hard (work-hard-play-hard)
Male works too hard, female takes care of him with love.

### 3. Love Is All Around (love-is-all-around)
Simple cute moments showing their love through actions.

## Commands

| Command | Description |
|---------|-------------|
| `/little-paws` | Generate today's story (1 panel = 4 frames) |
| `/little-paws:2` | Generate with 2 panels (8 frames) |
| `/little-paws:topic` | Generate specific topic |

## IMPORTANT: Image Generation with Text

**ALWAYS include narrator text in the image generation prompts!**

When generating each scene:
1. Include the scene's narrator text as part of the scene description
2. The text should be visually represented in the scene (floating text, speech bubble, or overlay)

Example prompt structure:
```
[Character block - male with brown eyes + green pendant, female with green eyes + beads]

Scene: [Scene description]
Text shown: "[Narrator text for this scene]"
Style: Kawaii chibi cartoon, thick black outlines, flat colors
[Other details]
```

## Output

Save to: `skills/little-paws/output/<date>/`
- `1.png` - Panel 1
- `2.png` - Panel 2 (if 2 panels)
- `story.mp4` - Video
- `viewer.html` - Interactive viewer
- `caption.txt` - Instagram caption

## Instagram Caption Template

```
🐾 Little Paws: [Title]

[Story one-liner]

#LittlePaws #CuteCats #Kawaii #CatCouple #ChibiCats #CatComic #Webtoon #DailyComic #CatLovers #FluffyCats #KawaiiArt #CatStory #PetComic #CuteArt
```

## Daily Automation (8pm)

Cron job runs daily at 8pm UTC to generate story automatically.
