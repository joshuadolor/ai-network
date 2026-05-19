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

## API workflow on OpenClaw VPS (required for Felix)

**Missing file?** On the OpenClaw VPS:

```bash
cd ~/AINetwork && git pull
bash setup/vps-openclaw/scripts/install-comfyui-workflow.sh ~/AINetwork
# creates ~/.openclaw/comfyui-workflow-api.json from repo starter template
```

Or full sync: `bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork --restart`

### Replace with your real graph (recommended after first test)

1. Build a working **text-to-image** graph in ComfyUI on KUBB.
2. **Save (API Format)** → copy to the VPS:

```bash
scp KUBB:~/path/to/your-api.json deploy@OPENCLAW_VPS:~/.openclaw/comfyui-workflow-api.json
chmod 600 ~/.openclaw/comfyui-workflow-api.json
```

3. `~/.openclaw/.env` should include:

```bash
COMFYUI_BASE_URL=http://100.86.160.110:8188
COMFYUI_WORKFLOW_API=/home/deploy/.openclaw/comfyui-workflow-api.json
```

5. Optional for Open WebUI: paste the same JSON in **Admin → Settings → Images** or set `COMFYUI_WORKFLOW` in `open-webui.env` (see [../../vps-apps/02-open-webui/README.md](../../vps-apps/02-open-webui/README.md)).

## Why Felix must not use localhost

ComfyUI runs on **KUBB**. The OpenClaw VPS only has Tailscale access. If Felix uses `http://127.0.0.1:8188`, nothing is listening there.

Felix is told **not** to read `~/.openclaw/.env` in chat (secrets). Without reading `workspace/docs/comfyui-workflow.md` or using the skill scripts, models often default to “ComfyUI = localhost:8188” from training data. **Fix:** always `exec` the skill scripts (they load `.env` and reject localhost).

Ensure the **gateway** loads `.env` on restart:

```bash
set -a && source ~/.openclaw/.env && set +a
openclaw gateway restart
```

Or add `EnvironmentFile=/home/deploy/.openclaw/.env` to the `openclaw-gateway` systemd user unit if your install supports it.

## Test generation (OpenClaw VPS)

Canonical tools: [../05-image-video/local/README.md](../05-image-video/local/README.md)

```bash
cd ~/AINetwork/setup/ai-server/05-image-video/local
export COMFYUI_BASE_URL=http://100.86.160.110:8188   # or: source ~/.openclaw/.env

python3 comfyui_health.py
python3 comfyui_list_models.py
python3 comfyui_generate.py "a grey tabby cat CEO, minimalist poster" -o /tmp/test.png --json
```

After `update-vps-openclaw.sh`, the same scripts live under `~/.openclaw/workspace/skills/local-image-gen/scripts/`.

## Upstream

- [Open WebUI — ComfyUI](https://docs.openwebui.com/features/image-generation/comfyui/)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

## Next

- Apps VPS: [../../vps-apps/02-open-webui/README.md](../../vps-apps/02-open-webui/README.md)
- OpenClaw skill: [../../vps-openclaw/skills/local-image-gen/](../../vps-openclaw/skills/local-image-gen/SKILL.md)
