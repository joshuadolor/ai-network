---
name: local-image-gen
description: Request images from Joshua's local ComfyUI or diffusion stack on KUBB (Tailscale). Use for thumbnails, concepts, social drafts — not production deploys without approval.
user-invocable: true
---

# Local image generation (KUBB)

Images are generated on the **AI server**, not the OpenClaw VPS. The VPS only triggers or checks status over Tailscale.

## Environment

- `COMFYUI_BASE_URL` — e.g. `http://100.x.x.x:8188` (KUBB Tailscale IP, ComfyUI default port).
- Optional: `COMFYUI_WORKFLOW` — name of a saved API workflow on the server (Joshua configures on KUBB).

Never read `~/.openclaw/.env` in chat. Use process env only.

## Health check (exec)

    python3 {baseDir}/scripts/comfyui_health.py

If unreachable, tell Joshua: ComfyUI must be running on KUBB and `COMFYUI_BASE_URL` set in gateway `.env`.

## Workflow

1. Confirm **prompt**, **aspect ratio**, and **purpose** (draft vs publish).
2. Run health check.
3. If Joshua has a **fixed API workflow** on ComfyUI, follow the prompt template documented in `workspace/docs/comfyui-workflow.md` (create that file on first successful setup).
4. Otherwise: guide Joshua to export a simple text-to-image API workflow on KUBB, or use browser on a local-only UI if Tailscale exposes it (rare).
5. Deliver: attach image in Discord if size allows, or save under `workspace/docs/images/` and give the path.
6. **Publishing** social posts or client assets requires explicit **approved** from Joshua.

## Fallback

If ComfyUI is down but **Ollama** has a vision/generation model Joshua enabled, say so and do not fake an image — offer text-only concept or wait.

## Setup reference

Repo: `setup/ai-server/05-image-video/README.md` (SDXL / diffusers on KUBB).
