---
name: image-gen:update
description: Update existing image generation credentials (Gemini cookies, API keys, Replicate token).
---

# Image Gen — Update Credentials

## Steps

### 1. Read current credentials

```bash
cat ~/.config/image-gen/credentials.json 2>/dev/null
```

If none exist, redirect to `/image-gen:init`.

### 2. Show masked values and ask what to update

> Current credentials:
> - **Gemini API Key**: `AIza...F49A`
> - **1PSID**: `g.a000...0076`
> - **1PSIDTS**: `sidts-...XEAA`
> - **Replicate Token**: `r8_0R...XydV`
>
> Which to update? (gemini-cookies / gemini-api / replicate / all)

### 3. Update and save

Read existing, update changed fields, write back with chmod 600.
