# AI server — ComfyUI (KUBB)

ComfyUI runs on **this machine** (KUBB). Open WebUI (apps VPS) and OpenClaw (OpenClaw VPS) reach it over **Tailscale** on port **8188**.

## Verified (Joshua)

From **apps VPS** and/or **OpenClaw VPS**:

```bash
curl -s http://100.86.160.110:8188/system_stats
```

Replace the IP with `tailscale ip -4` on KUBB if it ever changes.

## On KUBB — listen on the tailnet

- Start ComfyUI with **`--listen 0.0.0.0`** (or bind to the Tailscale interface).
- **Do not** port-forward **8188** on your home router.
- UFW (if enabled), allow **8188/tcp on `tailscale0` only** (same pattern as Ollama `11434`):

```bash
sudo ufw allow in on tailscale0 to any port 8188 proto tcp
```

## Export an API workflow (required for automation)

1. Build a simple **text-to-image** graph in ComfyUI (checkpoint + CLIP encode + KSampler + VAE decode + Save Image).
2. **Save (API Format)** → `~/comfyui-workflows/txt2img-api.json` on KUBB.
3. Copy the same file to the OpenClaw VPS for Felix:

```bash
# From laptop, example:
scp KUBB:~/comfyui-workflows/txt2img-api.json deploy@OPENCLAW_VPS:~/.openclaw/comfyui-workflow-api.json
chmod 600 ~/.openclaw/comfyui-workflow-api.json
```

4. Set on OpenClaw VPS `~/.openclaw/.env`:

```bash
COMFYUI_BASE_URL=http://100.86.160.110:8188
COMFYUI_WORKFLOW_API=/home/deploy/.openclaw/comfyui-workflow-api.json
```

5. Optional for Open WebUI: paste the same JSON in **Admin → Settings → Images** or set `COMFYUI_WORKFLOW` in `open-webui.env` (see [../../vps-apps/02-open-webui/README.md](../../vps-apps/02-open-webui/README.md)).

## Test generation (OpenClaw VPS)

```bash
source ~/.openclaw/.env
python3 ~/AINetwork/setup/vps-openclaw/skills/local-image-gen/scripts/comfyui_health.py
python3 ~/AINetwork/setup/vps-openclaw/skills/local-image-gen/scripts/comfyui_generate.py \
  --prompt "a grey tabby cat CEO, minimalist poster" \
  --out /tmp/test-comfyui.png
```

## Upstream

- [Open WebUI — ComfyUI](https://docs.openwebui.com/features/image-generation/comfyui/)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

## Next

- Apps VPS: [../../vps-apps/02-open-webui/README.md](../../vps-apps/02-open-webui/README.md)
- OpenClaw skill: [../../vps-openclaw/skills/local-image-gen/](../../vps-openclaw/skills/local-image-gen/SKILL.md)
