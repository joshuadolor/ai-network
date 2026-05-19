---
name: local-image-gen
description: Request images from ComfyUI on KUBB (Tailscale). Health check and generate via API workflow. Drafts only until Joshua approves publish.
user-invocable: true
---

# Local image generation (KUBB ComfyUI)

Images are generated on **KUBB** (AI server), **not** on this VPS. ComfyUI is **never** at `localhost` or `127.0.0.1` from Felix’s perspective.

## Canonical URL (use this)

**`http://100.86.160.110:8188`** — KUBB over Tailscale (also in `workspace/docs/comfyui-workflow.md`).

Do **not** use `http://localhost:8188`, `127.0.0.1`, or `host.docker.internal` unless Joshua explicitly says ComfyUI was moved to the VPS.

## Environment

Set on the gateway host in `~/.openclaw/.env` (scripts load this automatically; you must **not** paste `.env` in chat):

- `COMFYUI_BASE_URL=http://100.86.160.110:8188`
- `COMFYUI_WORKFLOW_API=/home/deploy/.openclaw/comfyui-workflow-api.json`  
  If missing, run: `bash ~/AINetwork/setup/vps-openclaw/scripts/install-comfyui-workflow.sh ~/AINetwork`

## How to run (always use scripts)

Do **not** hand-write `curl` to ComfyUI. Do **not** open ComfyUI in the browser on localhost.

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
