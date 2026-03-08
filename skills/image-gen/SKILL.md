---
name: image-gen
description: Generate images using multiple AI backends (Gemini, Replicate) with parallel batch support. Use when the user wants to generate one or more images, create game assets, illustrations, or batch-produce images. Triggers on any image generation request, or when the user invokes /image-gen. Also triggers for /image-gen:gemini, /image-gen:replicate, /image-gen:init, /image-gen:update.
---

# Image Gen

Multi-backend image generation skill with parallel batch support via Claude subagents.

## Backends

| Backend | Script | Best For | Rate Limits |
|---------|--------|----------|-------------|
| **Gemini Web** | `scripts/generate_gemini.py --backend web` | High quality, no rate limits with Pro sub | Requires fresh cookies |
| **Gemini API** | `scripts/generate_gemini.py --backend api` | Quick generations | Free tier limited |
| **Replicate** | `scripts/generate_replicate.py` | Reliable, paid per-use, many models | Pay-per-use, generous |

## Credentials

All credentials stored at `~/.config/image-gen/credentials.json` (chmod 600):

```json
{
  "gemini_api_key": "AIza...",
  "__Secure-1PSID": "g.a000...",
  "__Secure-1PSIDTS": "sidts-...",
  "replicate_api_token": "r8_..."
}
```

Legacy path `~/.config/gemini-imagegen/credentials.json` is also checked as fallback.

### Check credentials before generating:
```bash
cat ~/.config/image-gen/credentials.json 2>/dev/null
```

If missing, tell the user to run `/image-gen:init`.

## Sub-commands

| Command | Purpose |
|---------|---------|
| `/image-gen` | Generate images (auto-selects best backend, or specify) |
| `/image-gen:gemini` | Generate using Gemini specifically |
| `/image-gen:replicate` | Generate using Replicate specifically |
| `/image-gen:init` | First-time credential setup for all backends |
| `/image-gen:update` | Update specific credentials |

## Generating Images

### Single image

**Gemini:**
```bash
python3 <skill-path>/scripts/generate_gemini.py \
  --prompt "A cyberpunk cat" \
  --output ./output/cat.png \
  --backend web
```

**Replicate:**
```bash
python3 <skill-path>/scripts/generate_replicate.py \
  --prompt "A cyberpunk cat" \
  --output ./output/cat.png
```

### Batch generation (parallel subagents)

For multiple images, spawn **Claude subagents** — each generates one image independently:

1. **Split work across subagents** — one image per agent
2. **Stagger starts** — 2-second delay offset per agent
3. **Max 5 parallel** for Gemini web, unlimited for Replicate
4. **For 10+ images**, batch in waves of 5

Subagent prompt template:
```
Generate a single image using the image generation script.
Run: python3 <skill-path>/scripts/<script>.py --prompt '<prompt>' --output '<path>' --delay <N>
Report: output path, success/fail, duration.
```

### Backend selection

- **Default: Replicate** — most reliable, no cookie expiry issues
- **Gemini Web** — free with Pro subscription, but cookies expire
- **Gemini API** — free tier has strict daily limits

### Result reporting

After all subagents complete, compile a summary:

```
| # | Prompt | Output | Status | Time |
|---|--------|--------|--------|------|
| 1 | ... | ./output/x.png | Success | 24.7s |

**Total: X/Y succeeded, Z failed**
**Output directory: ./output/**
```
