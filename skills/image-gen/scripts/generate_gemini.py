#!/usr/bin/env python3
"""
Gemini Image Generator — Single image generation script.
Used by Claude subagents for parallel batch generation.
Outputs JSON to stdout for easy parsing.
"""

import argparse
import asyncio
import json
import os
import sys
import time
from io import BytesIO
from pathlib import Path

CREDENTIALS_PATH = Path.home() / ".config" / "image-gen" / "credentials.json"
LEGACY_CREDENTIALS_PATH = Path.home() / ".config" / "gemini-imagegen" / "credentials.json"
LEGACY_COOKIE_PATH = Path.home() / ".config" / "gemini-imagegen" / "cookies.json"
DEFAULT_MODEL = "gemini-2.5-flash-image"

EXIT_SUCCESS = 0
EXIT_NO_CREDENTIALS = 1
EXIT_GENERATION_FAILED = 2
EXIT_RATE_LIMITED = 3
EXIT_MISSING_DEPS = 4


def load_credentials():
    """Load credentials from the unified credentials file, falling back to legacy."""
    creds = {}

    if CREDENTIALS_PATH.exists():
        try:
            creds = json.loads(CREDENTIALS_PATH.read_text())
        except json.JSONDecodeError:
            pass

    if not creds.get("__Secure-1PSID") and LEGACY_CREDENTIALS_PATH.exists():
        try:
            legacy = json.loads(LEGACY_CREDENTIALS_PATH.read_text())
            creds.setdefault("__Secure-1PSID", legacy.get("__Secure-1PSID", ""))
            creds.setdefault("__Secure-1PSIDTS", legacy.get("__Secure-1PSIDTS", ""))
            if not creds.get("gemini_api_key"):
                creds.setdefault("gemini_api_key", legacy.get("gemini_api_key", ""))
        except json.JSONDecodeError:
            pass

    if not creds.get("__Secure-1PSID") and LEGACY_COOKIE_PATH.exists():
        try:
            legacy = json.loads(LEGACY_COOKIE_PATH.read_text())
            creds.setdefault("__Secure-1PSID", legacy.get("__Secure-1PSID", ""))
            creds.setdefault("__Secure-1PSIDTS", legacy.get("__Secure-1PSIDTS", ""))
        except json.JSONDecodeError:
            pass

    if not creds.get("gemini_api_key"):
        env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if env_key:
            creds["gemini_api_key"] = env_key

    return creds


def output_result(status, output_path=None, width=None, height=None,
                  duration_seconds=None, backend=None, error=None):
    """Print JSON result to stdout."""
    result = {"status": status}
    if output_path:
        result["output_path"] = str(output_path)
    if width and height:
        result["width"] = width
        result["height"] = height
    if duration_seconds is not None:
        result["duration_seconds"] = round(duration_seconds, 1)
    if backend:
        result["backend"] = backend
    if error:
        result["error"] = error
    print(json.dumps(result))


def generate_via_api(prompt, output_path, creds, aspect_ratio=None, input_image=None):
    """Generate image using the official Gemini API."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        output_result("error", error="Missing dependency: pip install google-genai Pillow")
        sys.exit(EXIT_MISSING_DEPS)

    api_key = creds.get("gemini_api_key")
    if not api_key:
        output_result("error", error="No API key found. Run /gemini-image-generator:init")
        sys.exit(EXIT_NO_CREDENTIALS)

    client = genai.Client(api_key=api_key)

    contents = []
    if input_image:
        from PIL import Image as PILImage
        contents.append(PILImage.open(input_image))
    contents.append(prompt)

    config_kwargs = {"response_modalities": ["TEXT", "IMAGE"]}
    if aspect_ratio:
        config_kwargs["image_config"] = types.ImageConfig(aspect_ratio=aspect_ratio)
    config = types.GenerateContentConfig(**config_kwargs)

    start = time.time()
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL, contents=contents, config=config
        )
    except Exception as e:
        error_str = str(e)
        if "429" in error_str:
            output_result("rate_limited", backend="api",
                          error="Rate limit hit. Use --backend web instead.",
                          duration_seconds=time.time() - start)
            sys.exit(EXIT_RATE_LIMITED)
        output_result("error", backend="api", error=error_str,
                      duration_seconds=time.time() - start)
        sys.exit(EXIT_GENERATION_FAILED)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    for part in response.parts:
        if part.inline_data:
            from PIL import Image as PILImage
            image = PILImage.open(BytesIO(part.inline_data.data))
            image.save(output_path)
            output_result("success", output_path=output_path,
                          width=image.size[0], height=image.size[1],
                          duration_seconds=time.time() - start, backend="api")
            return

    output_result("error", backend="api", error="No image in response",
                  duration_seconds=time.time() - start)
    sys.exit(EXIT_GENERATION_FAILED)


def generate_via_web(prompt, output_path, creds, timeout=120):
    """Generate image using the Gemini web interface (gemini-webapi)."""
    try:
        from gemini_webapi import GeminiClient
    except ImportError:
        output_result("error", error="Missing dependency: pip install gemini-webapi Pillow")
        sys.exit(EXIT_MISSING_DEPS)

    psid = creds.get("__Secure-1PSID", "")
    psidts = creds.get("__Secure-1PSIDTS", "")
    if not psid:
        output_result("error", error="No 1PSID cookie. Run /gemini-image-generator:init")
        sys.exit(EXIT_NO_CREDENTIALS)

    async def _run():
        client = GeminiClient(psid, psidts)
        await client.init(timeout=timeout)
        return await client.generate_content(f"Generate an image: {prompt}")

    start = time.time()
    try:
        response = asyncio.run(_run())
    except Exception as e:
        output_result("error", backend="web", error=str(e),
                      duration_seconds=time.time() - start)
        sys.exit(EXIT_GENERATION_FAILED)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if response.images:
        for i, image in enumerate(response.images):
            if i == 0:
                save_path = output_path
            else:
                p = Path(output_path)
                save_path = str(p.parent / f"{p.stem}_{i}{p.suffix}")
            asyncio.run(image.save(
                path=str(Path(save_path).parent),
                filename=Path(save_path).name
            ))

        output_result("success", output_path=output_path,
                      duration_seconds=time.time() - start, backend="web")
        return

    output_result("error", backend="web", error="No image in response",
                  duration_seconds=time.time() - start)
    sys.exit(EXIT_GENERATION_FAILED)


def main():
    parser = argparse.ArgumentParser(description="Gemini Image Generator")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--backend", choices=["api", "web"], default="web",
                        help="Generation backend (default: web)")
    parser.add_argument("--delay", type=float, default=0,
                        help="Seconds to wait before starting (for staggering)")
    parser.add_argument("--aspect", default=None, help="Aspect ratio (API only)")
    parser.add_argument("--input", default=None, help="Input image for editing (API only)")
    parser.add_argument("--timeout", type=int, default=120,
                        help="Max seconds to wait (default: 120)")
    args = parser.parse_args()

    if args.delay > 0:
        time.sleep(args.delay)

    creds = load_credentials()

    if args.backend == "web":
        generate_via_web(args.prompt, args.output, creds, args.timeout)
    else:
        generate_via_api(args.prompt, args.output, creds, args.aspect, args.input)


if __name__ == "__main__":
    main()
