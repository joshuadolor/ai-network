---
name: local-image-gen
description: Generate images via ComfyUI on KUBB (Tailscale). Use generate_image.sh for Discord requests. Never claim started without exec output.
user-invocable: true
---

# Local image generation (KUBB ComfyUI)

Images run on **KUBB** (`COMFYUI_BASE_URL`, e.g. `http://100.86.160.110:8188`). **Never** `localhost`.

## Hard rules (read first)

1. **Never** say "initiated", "in progress", "shortly", or "check in a moment" **without** running `exec` in the **same turn**.
2. If Joshua asks for an image → **run** `generate_image.sh` immediately (one message max before exec: "Generating on KUBB…").
3. After `exec`, reply with **real** result from JSON (`ok`, `path`, or `error`). Attach/send the file path in Discord if your tools allow.
4. Wrong CLI flags break generation:
   - Prompt is **positional** (first argument), not `--prompt`
   - Output flag is **`--output` or `-o`**, not a made-up path
5. Script path must include **`scripts/`**:
   - `~/.openclaw/workspace/skills/local-image-gen/scripts/generate_image.sh`

## One-shot command (preferred for Discord)

    bash {baseDir}/scripts/generate_image.sh "a cat playing basketball"

Optional explicit output path:

    bash {baseDir}/scripts/generate_image.sh "a cat playing basketball" \
      /home/deploy/.openclaw/workspace/docs/images/cat-basketball.png

Parse stdout JSON. On success, tell Joshua the **`path`** and share the image. On failure, paste the **exact error** and run `comfyui_list_models.py` if checkpoint-related.

## Manual steps (if debugging)

    python3 {baseDir}/scripts/comfyui_health.py
    python3 {baseDir}/scripts/comfyui_list_models.py
    python3 {baseDir}/scripts/comfyui_generate.py "prompt here" \
      --output workspace/docs/images/out.png --json

## Env (`~/.openclaw/.env`, scripts load it)

- `COMFYUI_BASE_URL=http://100.86.160.110:8188`
- Optional: `COMFYUI_CHECKPOINT`, `COMFYUI_WORKFLOW`

Repo reference: `~/AINetwork/setup/ai-server/05-image-video/local/README.md`

## Long runs

If generation may exceed ~2 minutes, start **ralph-loop** and still run `generate_image.sh` in the same session — do not defer to "later".
