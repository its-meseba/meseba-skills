#!/usr/bin/env python3
"""
Frame Forge — HTML Viewer Generator
Creates an interactive HTML page showing all story panels vertically
with copy and download buttons for each panel.
"""

import argparse
import base64
import json
import sys
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_NO_PANELS = 1

VIEWER_TITLE_DEFAULT = "Frame Forge Story"


def encode_image_base64(image_path):
    """Encode an image file to base64 data URI."""
    data = Path(image_path).read_bytes()
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def load_story_data(input_dir):
    """Load story.json if it exists."""
    story_path = Path(input_dir) / "story.json"
    if story_path.exists():
        try:
            return json.loads(story_path.read_text())
        except json.JSONDecodeError:
            return None
    return None


def generate_panel_html(panel_number, image_data_uri, story_data):
    """Generate HTML for a single panel card."""
    panel_texts = ""
    if story_data and "panels" in story_data:
        panels = story_data["panels"]
        if panel_number <= len(panels):
            panel_info = panels[panel_number - 1]
            scenes = panel_info.get("scenes", [])
            if scenes:
                text_items = []
                for i, scene in enumerate(scenes):
                    text = scene.get("narrator_text", scene.get("description", ""))
                    if text:
                        text_items.append(
                            f'<span class="scene-label">Scene {i + 1}:</span> {text}'
                        )
                if text_items:
                    panel_texts = '<div class="panel-texts">' + \
                        "<br>".join(text_items) + "</div>"

    return f"""
    <div class="panel-card" id="panel-{panel_number}">
      <div class="panel-header">
        <h2>Panel {panel_number}</h2>
        <div class="panel-actions">
          <button class="btn btn-copy" onclick="copyImage('img-{panel_number}')"
                  title="Copy image to clipboard">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
            Copy
          </button>
          <a class="btn btn-download" href="{image_data_uri}"
             download="panel-{panel_number}.png" title="Download image">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            Download
          </a>
        </div>
      </div>
      <img id="img-{panel_number}" src="{image_data_uri}" alt="Panel {panel_number}"
           class="panel-image" loading="lazy"/>
      {panel_texts}
    </div>
    """


def generate_viewer_html(input_dir, title, panel_count):
    """Generate the complete HTML viewer."""
    panels_html_parts = []

    for i in range(1, panel_count + 1):
        image_path = Path(input_dir) / f"{i}.png"
        if not image_path.exists():
            print(json.dumps({
                "status": "error",
                "error": f"Panel image not found: {image_path}"
            }))
            sys.exit(EXIT_NO_PANELS)

        image_data_uri = encode_image_base64(image_path)
        story_data = load_story_data(input_dir)
        panels_html_parts.append(
            generate_panel_html(i, image_data_uri, story_data)
        )

    panels_html = "\n".join(panels_html_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #0a0a0a;
    color: #e0e0e0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 2rem;
    max-width: 900px;
    margin: 0 auto;
  }}

  h1 {{
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
    color: #fff;
  }}

  .subtitle {{
    text-align: center;
    color: #888;
    margin-bottom: 2rem;
    font-size: 0.9rem;
  }}

  .panel-card {{
    background: #1a1a1a;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2rem;
    border: 1px solid #2a2a2a;
    transition: border-color 0.2s;
  }}

  .panel-card:hover {{
    border-color: #444;
  }}

  .panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.2rem;
    border-bottom: 1px solid #2a2a2a;
  }}

  .panel-header h2 {{
    font-size: 1rem;
    color: #ccc;
    font-weight: 500;
  }}

  .panel-actions {{
    display: flex;
    gap: 0.5rem;
  }}

  .btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    font-size: 0.8rem;
    cursor: pointer;
    border: 1px solid #333;
    background: #222;
    color: #ccc;
    text-decoration: none;
    transition: all 0.15s;
  }}

  .btn:hover {{
    background: #333;
    color: #fff;
    border-color: #555;
  }}

  .btn-copy.copied {{
    background: #1a3a1a;
    border-color: #2d5a2d;
    color: #6fcf6f;
  }}

  .panel-image {{
    width: 100%;
    display: block;
  }}

  .panel-texts {{
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    line-height: 1.6;
    color: #aaa;
    border-top: 1px solid #2a2a2a;
  }}

  .scene-label {{
    color: #888;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .toast {{
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    background: #333;
    color: #fff;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-size: 0.85rem;
    opacity: 0;
    transition: all 0.3s ease;
    z-index: 1000;
    pointer-events: none;
  }}

  .toast.show {{
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }}
</style>
</head>
<body>
  <h1>{title}</h1>
  <p class="subtitle">{panel_count} panels &middot; {panel_count * 4} scenes</p>

  {panels_html}

  <div class="toast" id="toast">Copied to clipboard!</div>

  <script>
    async function copyImage(imgId) {{
      const img = document.getElementById(imgId);
      const btn = img.closest('.panel-card').querySelector('.btn-copy');

      try {{
        const response = await fetch(img.src);
        const blob = await response.blob();
        await navigator.clipboard.write([
          new ClipboardItem({{ 'image/png': blob }})
        ]);

        btn.classList.add('copied');
        btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12"/>
        </svg> Copied!`;

        showToast('Copied to clipboard!');

        setTimeout(() => {{
          btn.classList.remove('copied');
          btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg> Copy`;
        }}, 2000);
      }} catch (err) {{
        showToast('Copy failed — try downloading instead');
      }}
    }}

    function showToast(message) {{
      const toast = document.getElementById('toast');
      toast.textContent = message;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2000);
    }}
  </script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Frame Forge Viewer Generator")
    parser.add_argument("--input-dir", required=True,
                        help="Directory containing numbered panel images")
    parser.add_argument("--title", default=VIEWER_TITLE_DEFAULT,
                        help="Story title for the viewer")
    parser.add_argument("--panel-count", type=int, required=True,
                        help="Number of panels to include")
    args = parser.parse_args()

    html = generate_viewer_html(args.input_dir, args.title, args.panel_count)

    output_path = Path(args.input_dir) / "viewer.html"
    output_path.write_text(html)

    print(json.dumps({
        "status": "success",
        "output_path": str(output_path),
        "panel_count": args.panel_count,
        "total_scenes": args.panel_count * 4
    }))


if __name__ == "__main__":
    main()
