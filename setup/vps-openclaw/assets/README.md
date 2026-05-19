# OpenClaw VPS assets

## `comfyui-workflow-api.example.json`

Starter **ComfyUI API-format** txt2img graph (SDXL-sized latent, `sd_xl_base_1.0.safetensors`).

Installed to `~/.openclaw/comfyui-workflow-api.json` by:

```bash
bash setup/vps-openclaw/scripts/install-comfyui-workflow.sh
# or: update-vps-openclaw.sh (creates if missing)
```

### If generation fails on KUBB

1. On KUBB, list checkpoints in ComfyUI or:

   ```bash
   ls ~/ComfyUI/models/checkpoints/   # path may vary
   ```

2. Edit `ckpt_name` in `~/.openclaw/comfyui-workflow-api.json` to match a file you have.

**Better (recommended):** In ComfyUI on KUBB, build a working graph → **Save (API Format)** → replace `~/.openclaw/comfyui-workflow-api.json` entirely.

```bash
# From laptop
scp KUBB:~/path/to/your-api.json deploy@OPENCLAW_VPS:~/.openclaw/comfyui-workflow-api.json
chmod 600 ~/.openclaw/comfyui-workflow-api.json
```

Felix patches **CLIPTextEncode** (positive/negative) and **KSampler** `seed` via `comfyui_generate.py`.
