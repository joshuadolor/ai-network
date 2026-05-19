# ComfyUI — Felix quick reference

**Full docs:** `~/AINetwork/setup/ai-server/05-image-video/local/README.md`

## KUBB (not this VPS)

| Item | Value |
|------|--------|
| Tailscale IP | `100.86.160.110` (verify on KUBB: `tailscale ip -4`) |
| Base URL | `http://100.86.160.110:8188` |
| Health | `python3 …/comfyui_health.py` (skill **local-image-gen**) |

## `~/.openclaw/.env`

```bash
COMFYUI_BASE_URL=http://100.86.160.110:8188
# optional:
# COMFYUI_CHECKPOINT=your_model.safetensors
# COMFYUI_WORKFLOW=/home/deploy/AINetwork/setup/ai-server/05-image-video/local/workflows/txt2img_api.json
```

Scripts load `.env` automatically (`comfyui_env.py`). Felix must **not** paste `.env` in Discord.

## Generate (Felix — skill scripts)

```bash
cd ~/.openclaw/workspace/skills/local-image-gen/scripts

python3 comfyui_health.py
python3 comfyui_list_models.py

python3 comfyui_generate.py \
  "grey tabby cat CEO, poster style" \
  --output ~/.openclaw/workspace/docs/images/test.png \
  --json
```

**Built-in graph** — no `comfyui-workflow-api.json` required if checkpoints exist on KUBB.

Optional legacy file: `~/.openclaw/comfyui-workflow-api.json` from `install-comfyui-workflow.sh`.

## Repo paths

| What | Path |
|------|------|
| Canonical Python tools | `setup/ai-server/05-image-video/local/` |
| Start ComfyUI on KUBB | `setup/ai-server/05-image-video/scripts/start_comfyui.sh` |
| Reference API JSON | `setup/ai-server/05-image-video/local/workflows/txt2img_api.json` |
| OpenClaw skill (VPS copy) | `workspace/skills/local-image-gen/` |

## Open WebUI

`setup/vps-apps/02-open-webui/open-webui.env.example` — same `COMFYUI_BASE_URL`.
