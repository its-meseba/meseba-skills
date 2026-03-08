---
name: frame-forge
description: >
  Automated image story chain creator for social media reels and storytelling.
  Creates sequences of 2×2 grid panels (4 scenes per panel) from a topic and reference image,
  maintaining character consistency throughout. Use this skill whenever the user wants to create
  visual stories, image sequences for reels, panel-based storytelling, scene chains, or
  storyboard-style content. Triggers on /frame-forge, /frame-forge:image:with-text,
  /frame-forge:image:without-text, /frame-forge:video. Also triggers when the user mentions
  "story panels", "reel images", "scene sequence", "visual story", or "image chain".
---

# Frame Forge

Create consistent, chain-based visual stories as 2×2 grid panels for social media reels.

## Concept

Each **panel** is a square 1:1 image containing **4 scenes** arranged in a 2×2 grid:
- **Top-left** → Scene 1 (first chronologically)
- **Top-right** → Scene 2
- **Bottom-left** → Scene 3
- **Bottom-right** → Scene 4

The user provides a **panel count** (N). Total scenes = N × 4. The story arc spans all panels continuously.

## Sub-commands

| Command | Mode | Description |
|---------|------|-------------|
| `/frame-forge` | Default (`image:with-text`) | Panels with narrator text overlays |
| `/frame-forge:image:with-text` | With text | Panels with narrator text overlays |
| `/frame-forge:image:without-text` | Without text | Panels without text, pure visual storytelling |
| `/frame-forge:video` | Video | Compile all panels into a video with transitions |

## Required Inputs

1. **Topic** — The story theme/premise (e.g., "a cat who becomes a software engineer")
2. **Reference image** — Path to a base image used for character consistency. Analyze this image thoroughly before generating — extract character features, art style, color palette, and mood.
3. **Panel count** (N) — Number of output panels. Each panel = 4 scenes, so N panels = 4N total story beats.

## Workflow

### Phase 1: Analyze Reference Image

Read the reference image. Extract and document:
- **Character details**: physical features, clothing, accessories, expressions, proportions
- **Art style**: illustration style, line weight, color palette, rendering technique
- **Mood/tone**: lighting, atmosphere, visual language

Build a **character prompt block** — a reusable prompt fragment that describes the character(s) consistently. This block goes into every scene prompt to maintain visual continuity.

### Phase 2: Plan the Story

Given the topic and N panels (4N scenes total), plan the complete story arc:

1. Write a one-paragraph story synopsis
2. Break into N panel groups, each with 4 scene beats
3. For each scene, write:
   - A brief scene description (what happens)
   - The emotional beat (tension, humor, resolution, etc.)
   - Key visual elements unique to this scene
   - **[with-text mode only]** A short narrator text (1-2 lines max)

Story planning rules:
- The story must flow naturally across panels — panel N's scene 4 connects to panel N+1's scene 1
- Vary scene compositions: close-ups, wide shots, action shots, reaction shots
- Build narrative tension — don't peak too early
- Make it relatable, fun, and professional
- **Never repeat narrator text** across scenes. Each narrator line is unique and advances the story. No "Meanwhile..." or "And so..." appearing twice. No recycling the same joke or observation.
- Keep narrator text concise — it's overlaid on the image, so it must be readable at small sizes

### Phase 3: Generate Scene Images

Use the `image-gen` skill to generate each scene. Default backend: **Gemini** (web backend).

For each scene, construct a prompt that includes:
1. The character prompt block (from Phase 1)
2. The scene-specific description
3. Style consistency instructions
4. Composition guidance — "this image will be placed in the [position] quadrant of a 2×2 grid"

**Orchestration strategy:**
- Spawn parallel agents for generation — one agent per scene or per panel depending on backend limits
- For Gemini web: max 5 parallel agents, stagger by 2 seconds
- Group scenes by panel — generate all 4 scenes of a panel together for maximum consistency
- If credentials are expired for the web backend, stop and tell the user to update credentials

**Scene prompt template:**
```
[Character prompt block]

Scene: [scene description]
Style: [art style from reference analysis]. Maintain exact same character design, proportions, and color palette.
Composition: [close-up / medium shot / wide shot / etc.]. This scene occupies the [top-left / top-right / bottom-left / bottom-right] quadrant of a story panel.
Mood: [emotional beat]
Background: [scene-specific environment details]

Generate as a single clean illustration, no text, no borders, no panels within the image.
```

### Phase 4: Compose Grid Panels

After generating all 4 scenes for a panel, compose them into a single 2×2 grid image using the compose script:

```bash
python3 <skill-path>/scripts/compose_grid.py \
  --images scene1.png scene2.png scene3.png scene4.png \
  --output panel.png \
  --size 2048 \
  --gap 4 \
  --mode with-text \
  --texts "Text 1" "Text 2" "Text 3" "Text 4"
```

Arguments:
- `--images`: 4 image paths in order (top-left, top-right, bottom-left, bottom-right)
- `--output`: Output path for the composed grid
- `--size`: Output image size in pixels (square, default 2048)
- `--gap`: Gap between scenes in pixels (default 4)
- `--mode`: `with-text` or `without-text` (default: `with-text`)
- `--texts`: 4 narrator texts, one per scene (required if mode is `with-text`)
- `--font-size`: Font size for narrator text (default: auto-calculated based on image size)
- `--text-position`: Where to place text: `bottom`, `top` (default: `bottom`)

### Phase 5: Create Viewer & Save

Save all panels to `unsynced-data/frame-forge/<session-id>/`:
- `1.png`, `2.png`, ..., `N.png` — the composed panel images
- `story.json` — the full story plan with all scene descriptions and texts
- `viewer.html` — the interactive HTML viewer

Generate the viewer:
```bash
python3 <skill-path>/scripts/generate_viewer.py \
  --input-dir unsynced-data/frame-forge/<session-id>/ \
  --title "Story Title" \
  --panel-count N
```

The viewer shows:
- All panels vertically, numbered 1 to N
- A copy button on each panel (copies image to clipboard)
- A download button on each panel
- Story text alongside each panel (if with-text mode)
- Clean, modern, dark-themed design optimized for reviewing story flow

### Phase 6: Video (only for /frame-forge:video)

After panels are created, compile into a video:
```bash
python3 <skill-path>/scripts/create_video.py \
  --input-dir unsynced-data/frame-forge/<session-id>/ \
  --output unsynced-data/frame-forge/<session-id>/story.mp4 \
  --panel-count N \
  --duration 3 \
  --transition fade \
  --music none
```

Arguments:
- `--duration`: Seconds per panel (default: 3)
- `--transition`: Transition type between panels: `fade`, `slide`, `none` (default: `fade`)
- `--music`: Background music path or `none`

Requires ffmpeg (`brew install ffmpeg` on macOS).

## Output Structure

```
unsynced-data/frame-forge/<session-id>/
├── scenes/           # Individual scene images (before composition)
│   ├── panel-1-scene-1.png
│   ├── panel-1-scene-2.png
│   └── ...
├── 1.png             # Composed panel 1
├── 2.png             # Composed panel 2
├── ...
├── N.png             # Composed panel N
├── story.json        # Story plan and metadata
├── viewer.html       # Interactive HTML viewer
└── story.mp4         # Video (only in video mode)
```

## Important Notes

- `unsynced-data/` must be in `.gitignore` — this directory is not synced with GitHub
- Session ID format: `YYYYMMDD-HHMMSS-<topic-slug>` (e.g., `20260308-143022-cat-engineer`)
- Always analyze the reference image before generating — do not skip this step
- If Gemini web credentials are expired, tell the user: "Gemini web credentials have expired. Please update them with `/image-gen:update`"
- This skill works with both Claude Code and OpenClaw. In OpenClaw, use the available tool-calling mechanisms to execute scripts and spawn agents.

## OpenClaw Compatibility

When running in OpenClaw (or any Claude-compatible environment that is not Claude Code):
- Use the environment's native tool-calling for script execution
- Agent spawning may not be available — in that case, generate scenes sequentially
- The compose_grid.py, generate_viewer.py, and create_video.py scripts are standalone Python and work anywhere with Python 3.8+ and Pillow installed
- Ensure `pip install Pillow` is available in the environment
