# Tailscale (both machines)

Use this **once the AI server and VPS each have Linux + internet**. Tailscale is what lets the **VPS** reach **Ollama on the AI server** without exposing Ollama to the public internet.

## Upstream references

- One-line install: [tailscale.com/download/linux](https://tailscale.com/download/linux)
- Full Linux install doc: [tailscale.com/docs/install/linux](https://tailscale.com/docs/install/linux)

## Goal

Every node you care about joins the **same tailnet**:

- Your laptop/phone → **apps VPS:3000** (Open WebUI).
- **Apps VPS** → **AI server:11434** (Ollama) and **:8188** (ComfyUI) over Tailscale IPs.
- **OpenClaw VPS** → **AI server:11434** (embeddings / LLM) and **:8188** (ComfyUI for Felix).

## On each Linux machine (AI server + apps VPS + OpenClaw VPS)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Complete browser login when prompted (do this on **both** the AI server and the VPS).

## Get IPv4 addresses

**On each machine:**

```bash
tailscale ip -4
```

Save:

- **AI server** Tailscale IP — e.g. `100.86.160.110` for Ollama `:11434` and ComfyUI `:8188`. Used by Open WebUI `OLLAMA_BASE_URL` / `COMFYUI_BASE_URL` ([../vps-apps/02-open-webui/README.md](../vps-apps/02-open-webui/README.md)) and OpenClaw `~/.openclaw/.env` ([../vps-openclaw/skills/local-image-gen/](../vps-openclaw/skills/local-image-gen/)).
- **Apps VPS** Tailscale IP — to reach Open WebUI privately at `http://<APPS_VPS_TAILSCALE_IP>:3000`.
- **OpenClaw VPS** Tailscale IP — to reach the OpenClaw dashboard / SSH privately.

## ACLs (recommended later)

In the Tailscale admin console you can restrict which nodes can reach which ports. Start permissive; tighten after everything works.

## Verification

- [ ] AI server, apps VPS, and OpenClaw VPS all show **Connected** in the Tailscale admin console.
- [ ] After [Ollama listens on the LAN/Tailnet](../ai-server/03-ollama/README.md) (`OLLAMA_HOST`), from **each** VPS:  
  `curl -s http://<AI_SERVER_TAILSCALE_IP>:11434/api/tags` returns JSON.
- [ ] (optional) [ComfyUI on KUBB](../ai-server/05-comfyui/README.md):  
  `curl -s http://<AI_SERVER_TAILSCALE_IP>:8188/system_stats` returns JSON.

## What to run next

| Machine | Next step in this repo |
|---------|-------------------------|
| **AI server** | [../ai-server/03-ollama/README.md](../ai-server/03-ollama/README.md) (if not finished) → [../ai-server/04-models/README.md](../ai-server/04-models/README.md) |
| **Apps VPS** | [../vps-apps/01-docker/README.md](../vps-apps/01-docker/README.md) (if needed) → [../vps-apps/02-open-webui/README.md](../vps-apps/02-open-webui/README.md) |
| **OpenClaw VPS** | [../vps-openclaw/01-install/README.md](../vps-openclaw/01-install/README.md) → memory → dreaming → security |
