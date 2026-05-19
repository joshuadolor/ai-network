---
name: local-image-gen
description: Request images from ComfyUI on KUBB (Tailscale). Health check and generate via API workflow. Drafts only until Joshua approves publish.
user-invocable: true
---

# Local image generation (KUBB ComfyUI)

Images are generated on the **AI server** (`100.86.160.110:8188` over Tailscale — confirm with Joshua if IP changed). The OpenClaw VPS triggers ComfyUI; it does not run GPU work locally.

## Environment

- `COMFYUI_BASE_URL` — e.g. `http://100.86.160.110:8188`
- `COMFYUI_WORKFLOW_API` — absolute path to **Save (API Format)** JSON from ComfyUI on KUBB

Never read `~/.openclaw/.env` in chat. Use process env only.

Setup: repo `setup/ai-server/05-comfyui/README.md` and `workspace/docs/comfyui-workflow.md`.

## Health check (exec)

    python3 {baseDir}/scripts/comfyui_health.py

## Generate image (exec)

Requires `COMFYUI_WORKFLOW_API` file on the VPS.

    python3 {baseDir}/scripts/comfyui_generate.py \
      --prompt "description here" \
      --out workspace/docs/images/YYYY-MM-DD-slug.png

Optional negative prompt: `--negative "blurry, watermark"`.

On success, script prints JSON with `path`. Attach or upload to Discord if size allows; always give the path in the **completion report**.

## Workflow

1. Confirm **prompt**, **aspect ratio**, and **purpose** (draft vs publish).
2. Run **health check**; if fail, stop and report (ComfyUI down or wrong URL).
3. Run **comfyui_generate.py** with a clear `--out` under `workspace/docs/images/`.
4. **Publishing** social posts or client assets requires explicit **approved** from Joshua.

## Fallback

If `COMFYUI_WORKFLOW_API` is missing, tell Joshua to export API workflow from ComfyUI (see `05-comfyui/README.md`) — do not fake an image.

## Open WebUI

Joshua can also generate images in the browser via Open WebUI on the apps VPS (same `COMFYUI_BASE_URL`).
