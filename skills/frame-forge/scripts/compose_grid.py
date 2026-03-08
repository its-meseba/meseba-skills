#!/usr/bin/env python3
"""
Frame Forge — Grid Composer
Composes 4 scene images into a single 2×2 grid panel.
Optionally overlays narrator text on each scene.
"""

import argparse
import json
import sys
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_MISSING_DEPS = 1
EXIT_MISSING_IMAGES = 2
EXIT_COMPOSITION_FAILED = 3

DEFAULT_SIZE = 2048
DEFAULT_GAP = 4
DEFAULT_TEXT_POSITION = "bottom"
TEXT_BG_OPACITY = 180
TEXT_PADDING_RATIO = 0.03
FONT_SIZE_RATIO = 0.035
MIN_FONT_SIZE = 16
MAX_FONT_SIZE = 48
SCENE_COUNT = 4
GRID_COLS = 2
GRID_ROWS = 2


def load_dependencies():
    """Import Pillow and return modules."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        print(json.dumps({
            "status": "error",
            "error": "Missing dependency: pip install Pillow"
        }))
        sys.exit(EXIT_MISSING_DEPS)


def calculate_font_size(cell_size, font_size_override=None):
    """Calculate appropriate font size based on cell dimensions."""
    if font_size_override:
        return font_size_override
    calculated = int(cell_size * FONT_SIZE_RATIO)
    return max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, calculated))


def load_font(font_size):
    """Load a font, falling back to default if needed."""
    _, _, ImageFont = load_dependencies()

    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]

    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, font_size)
            except (OSError, IOError):
                continue

    return ImageFont.load_default()


def draw_text_overlay(draw, cell_img, text, position, font, cell_size):
    """Draw text overlay with semi-transparent background on a cell image."""
    Image, ImageDraw, _ = load_dependencies()

    padding = int(cell_size * TEXT_PADDING_RATIO)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    bg_height = text_height + padding * 3

    if position == "bottom":
        bg_y = cell_size - bg_height
    else:
        bg_y = 0

    overlay = Image.new("RGBA", (cell_size, cell_size), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    overlay_draw.rectangle(
        [(0, bg_y), (cell_size, bg_y + bg_height)],
        fill=(0, 0, 0, TEXT_BG_OPACITY)
    )

    text_x = (cell_size - text_width) // 2
    text_y = bg_y + padding

    overlay_draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    cell_rgba = cell_img.convert("RGBA")
    composited = Image.alpha_composite(cell_rgba, overlay)
    return composited.convert("RGB")


def compose_grid(image_paths, output_path, size, gap, mode, texts,
                 font_size_override, text_position):
    """Compose 4 images into a 2×2 grid with optional text overlays."""
    Image, ImageDraw, _ = load_dependencies()

    for i, path in enumerate(image_paths):
        if not Path(path).exists():
            print(json.dumps({
                "status": "error",
                "error": f"Scene image not found: {path} (scene {i + 1})"
            }))
            sys.exit(EXIT_MISSING_IMAGES)

    cell_size = (size - gap) // GRID_COLS
    actual_size = cell_size * GRID_COLS + gap

    canvas = Image.new("RGB", (actual_size, actual_size), (20, 20, 20))

    font_size = calculate_font_size(cell_size, font_size_override)
    font = load_font(font_size) if mode == "with-text" else None

    positions = [
        (0, 0),                          # top-left: scene 1
        (cell_size + gap, 0),            # top-right: scene 2
        (0, cell_size + gap),            # bottom-left: scene 3
        (cell_size + gap, cell_size + gap),  # bottom-right: scene 4
    ]

    for i in range(SCENE_COUNT):
        img = Image.open(image_paths[i])
        img = img.resize((cell_size, cell_size), Image.LANCZOS)

        if mode == "with-text" and texts and i < len(texts) and texts[i]:
            draw = ImageDraw.Draw(img)
            img = draw_text_overlay(draw, img, texts[i], text_position,
                                    font, cell_size)

        canvas.paste(img, positions[i])

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, "PNG", quality=95)

    print(json.dumps({
        "status": "success",
        "output_path": str(output_path),
        "size": actual_size,
        "cell_size": cell_size,
        "mode": mode,
        "scenes": len(image_paths)
    }))


def main():
    parser = argparse.ArgumentParser(description="Frame Forge Grid Composer")
    parser.add_argument("--images", nargs=SCENE_COUNT, required=True,
                        help="4 scene image paths (top-left, top-right, bottom-left, bottom-right)")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE,
                        help=f"Output image size in pixels (default: {DEFAULT_SIZE})")
    parser.add_argument("--gap", type=int, default=DEFAULT_GAP,
                        help=f"Gap between scenes in pixels (default: {DEFAULT_GAP})")
    parser.add_argument("--mode", choices=["with-text", "without-text"],
                        default="with-text", help="Text overlay mode")
    parser.add_argument("--texts", nargs=SCENE_COUNT, default=None,
                        help="4 narrator texts, one per scene")
    parser.add_argument("--font-size", type=int, default=None,
                        help="Font size override (auto-calculated if not set)")
    parser.add_argument("--text-position", choices=["bottom", "top"],
                        default=DEFAULT_TEXT_POSITION,
                        help=f"Text overlay position (default: {DEFAULT_TEXT_POSITION})")
    args = parser.parse_args()

    if args.mode == "with-text" and not args.texts:
        print(json.dumps({
            "status": "error",
            "error": "Text mode requires --texts with 4 narrator texts"
        }))
        sys.exit(EXIT_COMPOSITION_FAILED)

    compose_grid(
        image_paths=args.images,
        output_path=args.output,
        size=args.size,
        gap=args.gap,
        mode=args.mode,
        texts=args.texts,
        font_size_override=args.font_size,
        text_position=args.text_position
    )


if __name__ == "__main__":
    main()
