#!/usr/bin/env python3
"""
Replicate Image Generator — Single image generation script.
Used by Claude subagents for parallel batch generation.
Outputs JSON to stdout for easy parsing.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

CREDENTIALS_PATH = Path.home() / ".config" / "image-gen" / "credentials.json"
LEGACY_CREDENTIALS_PATH = Path.home() / ".config" / "gemini-imagegen" / "credentials.json"
DEFAULT_MODEL = "google/nano-banana"

EXIT_SUCCESS = 0
EXIT_NO_CREDENTIALS = 1
EXIT_GENERATION_FAILED = 2
EXIT_MISSING_DEPS = 3


def load_replicate_token():
    """Load Replicate API token from credentials file or environment."""
    env_token = os.environ.get("REPLICATE_API_TOKEN")
    if env_token:
        return env_token

    for creds_path in [CREDENTIALS_PATH, LEGACY_CREDENTIALS_PATH]:
        if creds_path.exists():
            try:
                creds = json.loads(creds_path.read_text())
                token = creds.get("replicate_api_token")
                if token:
                    return token
            except json.JSONDecodeError:
                continue

    return None


def output_result(status, output_path=None, duration_seconds=None,
                  model=None, error=None):
    """Print JSON result to stdout."""
    result = {"status": status, "backend": "replicate"}
    if output_path:
        result["output_path"] = str(output_path)
    if duration_seconds is not None:
        result["duration_seconds"] = round(duration_seconds, 1)
    if model:
        result["model"] = model
    if error:
        result["error"] = error
    print(json.dumps(result))


def generate(prompt, output_path, model, image_inputs=None, timeout=300):
    """Generate image using Replicate API."""
    try:
        import replicate
    except ImportError:
        output_result("error", error="Missing dependency: pip install replicate")
        sys.exit(EXIT_MISSING_DEPS)

    token = load_replicate_token()
    if not token:
        output_result("error", error="No Replicate API token. Run /image-gen:init")
        sys.exit(EXIT_NO_CREDENTIALS)

    os.environ["REPLICATE_API_TOKEN"] = token

    input_params = {"prompt": prompt}
    if image_inputs:
        input_params["image_input"] = image_inputs

    start = time.time()
    try:
        output = replicate.run(model, input=input_params)
    except Exception as e:
        output_result("error", model=model, error=str(e),
                      duration_seconds=time.time() - start)
        sys.exit(EXIT_GENERATION_FAILED)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        # output can be a FileOutput, list, or URL string
        if hasattr(output, 'read'):
            image_data = output.read()
        elif isinstance(output, list) and len(output) > 0:
            item = output[0]
            if hasattr(item, 'read'):
                image_data = item.read()
            else:
                import httpx
                response = httpx.get(str(item))
                image_data = response.content
        elif isinstance(output, str):
            import httpx
            response = httpx.get(output)
            image_data = response.content
        else:
            # Try treating as bytes-like or FileOutput
            image_data = bytes(output)

        Path(output_path).write_bytes(image_data)
        output_result("success", output_path=output_path,
                      duration_seconds=time.time() - start, model=model)

    except Exception as e:
        output_result("error", model=model, error=f"Failed to save image: {e}",
                      duration_seconds=time.time() - start)
        sys.exit(EXIT_GENERATION_FAILED)


def main():
    parser = argparse.ArgumentParser(description="Replicate Image Generator")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Replicate model (default: {DEFAULT_MODEL})")
    parser.add_argument("--delay", type=float, default=0,
                        help="Seconds to wait before starting (for staggering)")
    parser.add_argument("--image-input", nargs="*", default=None,
                        help="Input image URLs for style transfer/editing")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Max seconds to wait (default: 300)")
    args = parser.parse_args()

    if args.delay > 0:
        time.sleep(args.delay)

    generate(args.prompt, args.output, args.model, args.image_input, args.timeout)


if __name__ == "__main__":
    main()
