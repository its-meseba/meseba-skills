#!/usr/bin/env python3
"""
Little Paws Daily Story Generator
Generates 4-frame or 8-frame stories for Instagram Reels
With proper character context and narrator text in images
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

# Paths
SKILL_DIR = Path("/root/.openclaw/workspace/kallavi-turk-skills/skills/little-paws")
OUTPUT_DIR = SKILL_DIR / "output"
REFERENCE_DIR = SKILL_DIR / "reference"

# Character prompt block - ALWAYS USE THIS
CHARACTER_PROMPT = """Two chibi-style white cats in kawaii cartoon style.

MALE CHARACTER (bigger, left):
- Larger, bigger build, slightly wider than tall, very round head
- Large circular dark brown eyes with multiple white highlights
- Dark brown collar with teardrop-shaped GREEN pendant
- Loving, brave, intelligent, smart, very able expression
- Fluffy white fur with short black strokes, thick black outlines
- Thick fluffy tail

FEMALE CHARACTER (smaller, right):  
- Smaller, extremely round/chubby like plush toy, tiny stubby limbs
- Very large emerald-green eyes with multi-highlight style
- Beaded necklace (small gray/silver beads)
- Compassionate, loving, always caring, sometimes angry from love
- Stronger blush on cheeks, pink inner ears
- White fluffy fur, thick black outlines

ART STYLE (ALWAYS FOLLOW):
- Kawaii chibi cartoon, thick consistent black outlines
- Flat solid colors with minimal shading
- Multi-highlight eyes (large round white highlight + smaller dot)
- Short fur strokes for fluffiness
- Small blush marks under eyes, heart motifs for affection

COLOR: Pure white fur #FFFFFF, black outlines #000000"""

# Story topics with narrator text embedded
TOPICS = {
    "cozy-morning": {
        "title": "Cozy Morning",
        "synopsis": "A sweet morning routine where the couple starts their day with love.",
        "scenes": [
            {
                "description": "Morning light streams through window. Both cats wake up stretchily, male cat yawns, female rubs eyes.",
                "text": "Good morning, my love 💕"
            },
            {
                "description": "Female cat prepares breakfast on tiny plates, male cat watches sleepily from bed.",
                "text": "Breakfast time!"
            },
            {
                "description": "They eat together, heads bumping affectionately, tails wagging, hearts appearing.",
                "text": "*head bump*"
            },
            {
                "description": "Male escorts female to door, they hug goodbye, pink hearts float around them.",
                "text": "Have a great day!"
            }
        ]
    },
    "work-hard-play-hard": {
        "title": "Work Hard, Play Hard",
        "synopsis": "Male works too hard, female takes care of him with love.",
        "scenes": [
            {
                "description": "Male cat at laptop, fur messy, tired eyes with dark circles, working hard. Female watches with concern.",
                "text": "You've been working so hard..."
            },
            {
                "description": "Female brings coffee/snacks to male, both look at each other with love, female pouts slightly.",
                "text": "Take a break, please?"
            },
            {
                "description": "Male collapses on desk exhausted, papers scattered, eyes half-closed. Female looks worried.",
                "text": "*exhausted sigh*"
            },
            {
                "description": "Female wraps blanket around male, pets his head gently, pink hearts float above, cozy atmosphere.",
                "text": "I'll take care of you 💕"
            }
        ]
    },
    "love-is-all-around": {
        "title": "Love Is All Around",
        "synopsis": "Small everyday moments showing their love through actions.",
        "scenes": [
            {
                "description": "Reading together on couch, heads touching, male holds book, female points at pages.",
                "text": "Reading together 📚"
            },
            {
                "description": "Female finds pretty flower, gives it to male with big eyes, male touched.",
                "text": "For you 🌸"
            },
            {
                "description": "Playing with yarn ball, chasing each other, female pretends to catch, male laughs.",
                "text": "Tag! You're it!"
            },
            {
                "description": "Curled up together sleeping peacefully, tails intertwined, tiny hearts above.",
                "text": "Goodnight, my love 💤"
            }
        ]
    }
}

def generate_story(topic_key: str = None, panels: int = 1):
    """Generate a Little Paws story with proper prompts"""
    
    # Select topic
    if not topic_key:
        day_of_year = datetime.now().timetuple().tm_yday
        topics = list(TOPICS.keys())
        topic_key = topics[day_of_year % len(topics)]
    
    topic = TOPICS[topic_key]
    
    # Create output directory for today
    today = datetime.now().strftime("%Y-%m-%d")
    output_subdir = OUTPUT_DIR / today
    output_subdir.mkdir(parents=True, exist_ok=True)
    
    scenes_dir = output_subdir / "scenes"
    scenes_dir.mkdir(exist_ok=True)
    
    print(f"Generating {topic['title']} story ({panels} panel(s))")
    print(f"Output: {output_subdir}")
    
    # Generate image prompts for each scene
    image_prompts = []
    for i, scene in enumerate(topic["scenes"], 1):
        prompt = f"""{CHARACTER_PROMPT}

Scene: {scene['description']}
Text shown: "{scene['text']}" (display this text as floating text or in speech bubble in the image)
Style: Kawaii chibi cartoon, thick black outlines, flat solid colors, cute and heartwarming
Composition: Scene {i} of 4 - will be placed in {['top-left', 'top-right', 'bottom-left', 'bottom-right'][i-1]} quadrant of 2x2 grid
Background: Simple, cozy, pastel colored to match the mood
Emotion: {topic['title']}"""
        image_prompts.append({
            "scene_num": i,
            "text": scene["text"],
            "description": scene["description"],
            "prompt": prompt
        })
    
    # Save story plan with prompts
    story_plan = {
        "date": today,
        "topic": topic_key,
        "title": topic["title"],
        "synopsis": topic["synopsis"],
        "panels": panels,
        "character_context": CHARACTER_PROMPT,
        "scenes": image_prompts,
        "created_at": datetime.now().isoformat()
    }
    
    with open(output_subdir / "story.json", "w") as f:
        json.dump(story_plan, f, indent=2)
    
    # Generate caption
    caption = generate_caption(topic["title"], topic["synopsis"])
    with open(output_subdir / "caption.txt", "w") as f:
        f.write(caption)
    
    print(f"\n📝 Instagram Caption:\n{caption}")
    print(f"\n🎨 Generated {len(image_prompts)} scene prompts")
    for i, sp in enumerate(image_prompts, 1):
        print(f"  Scene {i}: {sp['text']}")
    
    print(f"\n✅ Story saved to {output_subdir}")
    print(f"📝 Caption saved")
    
    return output_subdir, topic, image_prompts

def generate_caption(title: str, synopsis: str) -> str:
    """Generate Instagram caption with hashtags"""
    caption = f"""🐾 Little Paws: {title}

{synopsis}

#LittlePaws #CuteCats #Kawaii #CatCouple #ChibiCats #CatComic #Webtoon #DailyComic #CatLovers #FluffyCats #KawaiiArt #CatStory #PetComic #CuteArt #CatCartoon #FelineArt #KawaiiCats #CatLover #DailyComics #Webcomic"""
    return caption

if __name__ == "__main__":
    import sys
    
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    panels = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    output, topic_data, prompts = generate_story(topic, panels)
    print(f"\n🎬 Use these prompts with image-gen to create scenes")
    print(f"📺 Then create video with 9:16 ratio, 2.5s per frame")
