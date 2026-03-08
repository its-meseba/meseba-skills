---
name: image-gen:replicate
description: Generate images using Replicate API with models like google/nano-banana. Reliable pay-per-use backend with no cookie expiry issues. Use when the user wants reliable image generation or specifically asks for Replicate.
---

# Image Gen — Replicate Backend

Uses Replicate's API for image generation. Pay-per-use, reliable, no cookie management needed.

## Script

```bash
python3 <skill-path>/scripts/generate_replicate.py \
  --prompt "Your prompt" \
  --output ./output/image.png \
  --delay 0
```

### Arguments
- `--prompt` (required): Image generation prompt
- `--output` (required): Output file path
- `--model`: Replicate model (default: `google/nano-banana`)
- `--delay`: Seconds to wait before starting (for staggering)
- `--image-input`: One or more input image URLs for style transfer / editing
- `--timeout`: Max seconds (default: 300)

### Output (JSON on stdout)
```json
{"status": "success", "output_path": "/path/to/image.png", "duration_seconds": 15.2, "backend": "replicate", "model": "google/nano-banana"}
```

### Credentials needed
- `replicate_api_token` in credentials file, or `REPLICATE_API_TOKEN` env var

### Batch limits
- Replicate handles concurrency well — up to 10 parallel subagents is fine
- Pay-per-use so no free tier quota issues

### Available models
- `google/nano-banana` (default) — fast, high quality
- Can use any Replicate image model by passing `--model owner/name`
