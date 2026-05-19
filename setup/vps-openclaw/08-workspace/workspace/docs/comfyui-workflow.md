# ComfyUI workflow (Felix / OpenClaw)

## Server

- **KUBB Tailscale IP:** `100.86.160.110` (verify with `tailscale ip -4` on KUBB if this drifts)
- **Base URL:** `http://100.86.160.110:8188`
- **Health:** `curl -s http://100.86.160.110:8188/system_stats`

## API workflow file on OpenClaw VPS

Set in `~/.openclaw/.env`:

```bash
COMFYUI_BASE_URL=http://100.86.160.110:8188
COMFYUI_WORKFLOW_API=/home/deploy/.openclaw/comfyui-workflow-api.json
```

Export from ComfyUI on KUBB: **Save (API Format)** → copy to the path above.

## Generate (exec)

```bash
python3 {baseDir}/scripts/comfyui_generate.py \
  --prompt "your description" \
  --out workspace/docs/images/YYYY-MM-DD-slug.png
```

Save deliverables under `workspace/docs/images/`. Draft only until Joshua **approved** publish.

## Open WebUI

Same ComfyUI URL in apps VPS `open-webui.env` — see repo `setup/vps-apps/02-open-webui/`.
