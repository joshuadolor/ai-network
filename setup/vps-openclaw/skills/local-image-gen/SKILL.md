---
name: local-image-gen
description: Generate images via ComfyUI on KUBB (Tailscale). Canonical tools in setup/ai-server/05-image-video/local. Drafts only until Joshua approves publish.
user-invocable: true
---

# Local image generation (KUBB ComfyUI)

**Canonical source (read if confused):** `~/AINetwork/setup/ai-server/05-image-video/local/README.md`

Images run on **KUBB**, not this VPS. **Never** `localhost:8188` or `127.0.0.1`.

## Environment (`~/.openclaw/.env` — scripts load; do not paste in chat)

| Variable | Example | Required |
|----------|---------|----------|
| `COMFYUI_BASE_URL` | `http://100.86.160.110:8188` | yes |
| `COMFYUI_CHECKPOINT` | from `comfyui_list_models.py` | no (auto-picks first) |
| `COMFYUI_WORKFLOW` | path to exported API JSON | no (built-in graph used) |
| `COMFYUI_WORKFLOW_API` | legacy path on VPS | no |

Also: `setup/ai-server/05-image-video/scripts/start_comfyui.sh` on KUBB.

## Commands (always `exec` — skill `scripts/` synced from `05-image-video/local`)

Working directory for imports: run from skill scripts dir or use full paths below.

### 1. Health

    python3 {baseDir}/scripts/comfyui_health.py

### 2. List checkpoints (if generate fails on model name)

    python3 {baseDir}/scripts/comfyui_list_models.py

### 3. Generate (built-in workflow — preferred)

Positional **prompt** (not `--prompt`). Save under workspace:

    python3 {baseDir}/scripts/comfyui_generate.py \
      "your description here" \
      --output workspace/docs/images/YYYY-MM-DD-slug.png \
      --json

Optional: `--negative "..."`, `--checkpoint exact_name.safetensors`, `-W 1024 -H 1024`, `--steps 20`, `--cfg 7`

### 4. Custom exported workflow (optional)

    python3 {baseDir}/scripts/comfyui_generate.py \
      "prompt" \
      --workflow ~/AINetwork/setup/ai-server/05-image-video/local/workflows/txt2img_api.json \
      --output workspace/docs/images/out.png \
      --json

Or set `COMFYUI_WORKFLOW` in `.env` to that path.

## Workflow for Felix

1. Confirm prompt + draft vs publish (publish needs Joshua **approved**).
2. Start **ralph-loop** if generation may take >2 min.
3. `comfyui_health.py` → fail fast with clear error if KUBB down.
4. `comfyui_list_models.py` if checkpoint errors.
5. `comfyui_generate.py` with `--json` → read `path` in output → share in Discord + completion report.
6. Do **not** `curl` ComfyUI by hand. Do **not** open ComfyUI in browser on localhost.

## Proceed behavior (strict)

If Joshua says **"do it" / "proceed" / "go"**:

- Run the command immediately (do not restate the same command repeatedly).
- If a precheck is needed, run it once then immediately run generate.
- If command fails, show the exact error and next fix.

Correct generate path includes `scripts/`:

`python3 ~/.openclaw/workspace/skills/local-image-gen/scripts/comfyui_generate.py ...`

## If something is missing

Search repo: `grep -ri comfyui ~/AINetwork/setup/ai-server/05-image-video/local`

See `workspace/docs/comfyui-workflow.md` and `PROJECT-LOOKUP.md`.

## Open WebUI

Same `COMFYUI_BASE_URL` on apps VPS — `setup/vps-apps/02-open-webui/`.
