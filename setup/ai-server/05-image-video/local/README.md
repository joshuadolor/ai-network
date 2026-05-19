# ComfyUI local API tools

Scripts to health-check, list models, and **generate images** against ComfyUI on KUBB (or any host) over HTTP.

Used by the OpenClaw **local-image-gen** skill on the VPS (`COMFYUI_BASE_URL` → KUBB Tailscale IP).

## Prerequisites

1. ComfyUI running on KUBB (`start_comfyui.sh`), listening on `0.0.0.0:8188`.
2. At least one **checkpoint** in your data folder, e.g.  
   `Documents/ComfyUI/models/checkpoints/*.safetensors`
3. Environment:
   - `COMFYUI_BASE_URL` — e.g. `http://100.86.160.110:8188`
   - Optional: `COMFYUI_CHECKPOINT` — exact filename from `comfyui_list_models.py`

On the **OpenClaw VPS**, set `COMFYUI_BASE_URL` in `~/.openclaw/.env` and restart the gateway.

## Scripts

| Script | Purpose |
|--------|---------|
| `comfyui_health.py` | Ping `/system_stats` |
| `comfyui_list_models.py` | List checkpoint filenames |
| `comfyui_generate.py` | Queue txt2img, wait, download PNG |
| `comfyui_client.py` | Shared library (import only) |
| `workflows/txt2img_api.json` | Reference graph; optional `--workflow` |

## Examples

From this directory (VPS or Git Bash):

```bash
export COMFYUI_BASE_URL=http://100.86.160.110:8188

python3 comfyui_health.py
python3 comfyui_list_models.py
python3 comfyui_generate.py "a cat wearing a space helmet, studio photo" --width 1024 --height 1024
python3 comfyui_generate.py "sunset over mountains" -o /tmp/out.png --json
```

Custom exported workflow (from ComfyUI → Save API format):

```bash
export COMFYUI_WORKFLOW=/path/to/my_api.json
python3 comfyui_generate.py "your prompt"
```

## Env vars

| Variable | Default | Meaning |
|----------|---------|---------|
| `COMFYUI_BASE_URL` | (required) | ComfyUI HTTP base URL |
| `COMFYUI_CHECKPOINT` | first listed | Checkpoint filename |
| `COMFYUI_WORKFLOW` | built-in graph | Path to API JSON |
| `COMFYUI_OUTPUT_DIR` | `./comfyui_outputs` | Download directory |
| `COMFYUI_WIDTH` / `HEIGHT` | `1024` | Latent size |
| `COMFYUI_STEPS` | `20` | Sampling steps |
| `COMFYUI_CFG` | `7.0` | CFG scale |
| `COMFYUI_TIMEOUT` | `600` | Wait timeout (seconds) |

## Agent (OpenClaw / Felix)

**This folder is canonical.** Felix must read this README when doing image work — do not guess URLs or CLI flags.

On the OpenClaw VPS:

1. Repo path: `~/AINetwork/setup/ai-server/05-image-video/local/`
2. After `git pull`, run `bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork` — copies these scripts into `~/.openclaw/workspace/skills/local-image-gen/scripts/` (keeps VPS-only `comfyui_env.py`).
3. Skill: `setup/vps-openclaw/skills/local-image-gen/SKILL.md`
4. Workspace cheat sheet: `~/.openclaw/workspace/docs/comfyui-workflow.md`

**Felix command shape:** positional prompt, not `--prompt`:

```bash
python3 ~/.openclaw/workspace/skills/local-image-gen/scripts/comfyui_generate.py \
  "description" --output ~/.openclaw/workspace/docs/images/out.png --json
```

Use **ralph-loop** for long image batches. Never `localhost:8188` from the VPS.
