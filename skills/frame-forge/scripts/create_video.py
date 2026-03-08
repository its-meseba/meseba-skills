#!/usr/bin/env python3
"""
Frame Forge — Video Creator
Compiles numbered panel images into a video with transitions using ffmpeg.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_NO_FFMPEG = 1
EXIT_NO_PANELS = 2
EXIT_VIDEO_FAILED = 3

DEFAULT_DURATION = 3
DEFAULT_TRANSITION = "fade"
TRANSITION_DURATION = 0.5
DEFAULT_FPS = 30
OUTPUT_CODEC = "libx264"
PIXEL_FORMAT = "yuv420p"


def check_ffmpeg():
    """Verify ffmpeg is installed."""
    if not shutil.which("ffmpeg"):
        print(json.dumps({
            "status": "error",
            "error": "ffmpeg not found. Install with: brew install ffmpeg"
        }))
        sys.exit(EXIT_NO_FFMPEG)


def build_no_transition_command(input_dir, output_path, panel_count,
                                duration, music_path):
    """Build ffmpeg command for simple slideshow without transitions."""
    concat_file = Path(tempfile.mktemp(suffix=".txt"))
    lines = []
    for i in range(1, panel_count + 1):
        img_path = Path(input_dir) / f"{i}.png"
        lines.append(f"file '{img_path}'")
        lines.append(f"duration {duration}")

    last_img = Path(input_dir) / f"{panel_count}.png"
    lines.append(f"file '{last_img}'")
    concat_file.write_text("\n".join(lines))

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
    ]

    if music_path:
        cmd.extend(["-i", music_path, "-shortest"])

    cmd.extend([
        "-vf", f"scale=trunc(iw/2)*2:trunc(ih/2)*2,fps={DEFAULT_FPS}",
        "-c:v", OUTPUT_CODEC,
        "-pix_fmt", PIXEL_FORMAT,
        "-movflags", "+faststart",
        str(output_path)
    ])

    return cmd, concat_file


def build_fade_transition_command(input_dir, output_path, panel_count,
                                  duration, music_path):
    """Build ffmpeg command with fade transitions between panels."""
    inputs = []
    filter_parts = []

    for i in range(1, panel_count + 1):
        img_path = Path(input_dir) / f"{i}.png"
        inputs.extend(["-loop", "1", "-t", str(duration), "-i", str(img_path)])

    for i in range(panel_count):
        filter_parts.append(
            f"[{i}:v]scale=trunc(iw/2)*2:trunc(ih/2)*2,"
            f"fps={DEFAULT_FPS},format=yuva420p,"
            f"setpts=PTS-STARTPTS[v{i}]"
        )

    if panel_count == 1:
        filter_complex = f"[0:v]scale=trunc(iw/2)*2:trunc(ih/2)*2," \
                         f"fps={DEFAULT_FPS}[outv]"
    else:
        xfade_parts = ["; ".join(filter_parts)]
        prev = "v0"
        for i in range(1, panel_count):
            offset = i * duration - TRANSITION_DURATION * i
            out_label = f"xf{i}" if i < panel_count - 1 else "outv"
            xfade_parts.append(
                f"[{prev}][v{i}]xfade=transition=fade:"
                f"duration={TRANSITION_DURATION}:offset={offset:.1f}[{out_label}]"
            )
            prev = out_label

        filter_complex = "; ".join(xfade_parts)

    cmd = ["ffmpeg", "-y"]
    cmd.extend(inputs)

    if music_path:
        cmd.extend(["-i", music_path, "-shortest"])

    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", OUTPUT_CODEC,
        "-pix_fmt", PIXEL_FORMAT,
        "-movflags", "+faststart",
        str(output_path)
    ])

    return cmd, None


def create_video(input_dir, output_path, panel_count, duration,
                 transition, music_path):
    """Create video from panel images."""
    check_ffmpeg()

    for i in range(1, panel_count + 1):
        img_path = Path(input_dir) / f"{i}.png"
        if not img_path.exists():
            print(json.dumps({
                "status": "error",
                "error": f"Panel image not found: {img_path}"
            }))
            sys.exit(EXIT_NO_PANELS)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    concat_file = None

    if transition == "none" or transition == "slide":
        cmd, concat_file = build_no_transition_command(
            input_dir, output_path, panel_count, duration, music_path
        )
    else:
        cmd, concat_file = build_fade_transition_command(
            input_dir, output_path, panel_count, duration, music_path
        )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            print(json.dumps({
                "status": "error",
                "error": f"ffmpeg failed: {result.stderr[:500]}"
            }))
            sys.exit(EXIT_VIDEO_FAILED)

        total_duration = panel_count * duration
        if transition == "fade":
            total_duration -= TRANSITION_DURATION * (panel_count - 1)

        print(json.dumps({
            "status": "success",
            "output_path": str(output_path),
            "panel_count": panel_count,
            "duration_seconds": round(total_duration, 1),
            "transition": transition
        }))

    except subprocess.TimeoutExpired:
        print(json.dumps({
            "status": "error",
            "error": "ffmpeg timed out after 300 seconds"
        }))
        sys.exit(EXIT_VIDEO_FAILED)
    finally:
        if concat_file and Path(concat_file).exists():
            Path(concat_file).unlink()


def main():
    parser = argparse.ArgumentParser(description="Frame Forge Video Creator")
    parser.add_argument("--input-dir", required=True,
                        help="Directory containing numbered panel images")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--panel-count", type=int, required=True,
                        help="Number of panels")
    parser.add_argument("--duration", type=float, default=DEFAULT_DURATION,
                        help=f"Seconds per panel (default: {DEFAULT_DURATION})")
    parser.add_argument("--transition", choices=["fade", "slide", "none"],
                        default=DEFAULT_TRANSITION,
                        help=f"Transition type (default: {DEFAULT_TRANSITION})")
    parser.add_argument("--music", default=None,
                        help="Background music path or 'none'")
    args = parser.parse_args()

    music_path = args.music if args.music and args.music != "none" else None

    create_video(
        input_dir=args.input_dir,
        output_path=args.output,
        panel_count=args.panel_count,
        duration=args.duration,
        transition=args.transition,
        music_path=music_path
    )


if __name__ == "__main__":
    main()
