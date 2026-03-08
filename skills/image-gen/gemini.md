---
name: image-gen:gemini
description: Generate images using Google Gemini (API + Web backends). Use when user specifically wants Gemini for image generation, or when generating game assets with the web backend.
---

# Image Gen — Gemini Backend

Uses Google's Gemini for image generation via two sub-backends:
- **Web** (recommended): Uses `gemini-webapi` with browser cookies. No rate limits with Pro subscription.
- **API** (fallback): Uses `google-genai` with API key. Free tier has daily limits.

## Script

```bash
python3 <skill-path>/scripts/generate_gemini.py \
  --prompt "Your prompt" \
  --output ./output/image.png \
  --backend web \
  --delay 0
```

### Arguments
- `--prompt` (required): Image generation prompt
- `--output` (required): Output file path
- `--backend`: `web` (default) or `api`
- `--delay`: Seconds to wait before starting (for staggering parallel requests)
- `--aspect`: Aspect ratio (API only)
- `--input`: Input image for editing (API only)
- `--timeout`: Max seconds (default: 120)

### Output (JSON on stdout)
```json
{"status": "success", "output_path": "/path/to/image.png", "duration_seconds": 24.7, "backend": "web"}
```

### Credentials needed
- `__Secure-1PSID` and `__Secure-1PSIDTS` for web backend
- `gemini_api_key` for API backend

### Batch limits
- **Web**: Max 5 parallel subagents
- **API**: Max 1-2 parallel due to rate limits
