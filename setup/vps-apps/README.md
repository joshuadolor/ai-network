# VPS — Apps (Open WebUI + future apps)

This is the **first** Hostinger VPS — runs **Open WebUI** (the chat UI for your private LLM) and any other application containers. It does **not** run OpenClaw; OpenClaw lives on its own VPS ([../vps-openclaw/README.md](../vps-openclaw/README.md)).

## Order

| Step | Folder | What |
|------|--------|------|
| 0 | [../network-tailscale/README.md](../network-tailscale/README.md) | Install Tailscale on this VPS (and on the AI server if not done) |
| 1 | [01-docker](01-docker/README.md) | Docker Engine |
| 2 | [02-open-webui](02-open-webui/README.md) | Open WebUI container → Ollama on the AI server |
| 3 | [03-security](03-security/README.md) | Firewall habits, Open WebUI users |

**Prereq:** from this VPS, `curl` to `http://<AI_SERVER_TAILSCALE_IP>:11434/api/tags` must work (Ollama + Tailscale + `OLLAMA_HOST` on the AI server).

Doc hygiene: [../DOCUMENTATION-SOURCES.md](../DOCUMENTATION-SOURCES.md)
