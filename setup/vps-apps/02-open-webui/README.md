# VPS — Open WebUI (Docker)

## Upstream references

- Docker install + **`OLLAMA_BASE_URL`** when Ollama is on another host: [Open WebUI README — Quick Start with Docker](https://github.com/open-webui/open-webui#quick-start-with-docker-) (raw: [README on main](https://raw.githubusercontent.com/open-webui/open-webui/main/README.md))
- Connection issues: [docs.openwebui.com — Troubleshooting](https://docs.openwebui.com/troubleshooting/)

## Goal

Docker container on the **VPS** uses your **KUBB** Ollama over Tailscale (same idea as upstream’s **“Ollama on a Different Server”** example; use `http://` + your Tailscale IP is fine on the tailnet).

## Prereqs

- [ ] Docker installed on this VPS ([../01-docker/README.md](../01-docker/README.md)).
- [ ] Tailscale on **VPS and AI server** ([../../network-tailscale/README.md](../../network-tailscale/README.md)).
- [ ] `curl` from VPS to `http://<KUBB_TAILSCALE_IP>:11434/api/tags` works.

## Configure and run

1. Copy the example env and edit the IP:

```bash
cp open-webui.env.example open-webui.env
nano open-webui.env   # set OLLAMA_BASE_URL to http://<AI_SERVER_TAILSCALE_IP>:11434
```

2. Run the helper script **on the VPS** (copy this folder or the whole `setup` directory to the VPS):

```bash
chmod +x run-open-webui.sh
./run-open-webui.sh
```

Or run Docker manually (replace `100.x.x.x`):

```bash
docker rm -f open-webui 2>/dev/null || true
docker run -d \
  -p 3000:8080 \
  -e OLLAMA_BASE_URL="http://100.x.x.x:11434" \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

The **`-v open-webui:/app/backend/data`** volume is required upstream so the database persists ([Open WebUI README](https://github.com/open-webui/open-webui#quick-start-with-docker-)).

## Open in browser

`http://<VPS_TAILSCALE_IP>:3000` or `http://<VPS_PUBLIC_IP>:3000` depending how you route (prefer Tailscale-only access if you can).

## First user

The **first account** created in Open WebUI is the admin — create yours, then add your wife under **Admin → Users**.

## Verification

- [ ] Web UI loads.
- [ ] Chat completes using a model that exists on the **AI server** (`ollama list` there).

## Files in this folder

| File | Purpose |
|------|---------|
| `open-webui.env.example` | Template for `OLLAMA_BASE_URL` |
| `run-open-webui.sh` | Starts container with env file |

## Next

[../03-security/README.md](../03-security/README.md)
