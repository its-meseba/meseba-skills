---
name: image-gen:init
description: First-time setup for image generation credentials (Gemini + Replicate).
---

# Image Gen — Init

Set up credentials for all image generation backends.

## Steps

### 1. Check existing credentials

```bash
cat ~/.config/image-gen/credentials.json 2>/dev/null
cat ~/.config/gemini-imagegen/credentials.json 2>/dev/null
```

If credentials exist, show masked values and ask if user wants to overwrite.

### 2. Ask for credentials

> I need credentials for the image generation backends. You can set up one or all:
>
> **Replicate** (recommended — most reliable):
> - API token from https://replicate.com/account/api-tokens
>
> **Gemini Web** (free with Pro subscription):
> - `__Secure-1PSID` and `__Secure-1PSIDTS` cookies from https://gemini.google.com
> - (F12 → Application → Cookies)
>
> **Gemini API** (free tier, limited):
> - API key from https://aistudio.google.com/apikey

### 3. Save credentials

Write to `~/.config/image-gen/credentials.json` with chmod 600.

### 4. Migrate legacy credentials

If `~/.config/gemini-imagegen/credentials.json` exists, merge values into the new file.
