# VPS — Docker

## Upstream reference

Ubuntu package install is convenient; for the latest **Docker Engine** steps (official repo, rootless, etc.), use [docs.docker.com/engine/install/ubuntu](https://docs.docker.com/engine/install/ubuntu).

## Where to install

| Machine | Need Docker? |
|---------|----------------|
| **This VPS** (apps — Open WebUI) | **Yes** — Open WebUI runs as a container here. |
| **OpenClaw VPS** | Only if you chose Hostinger's Docker template (Option B) — handled by hPanel. |
| **AI server (KUBB)** | Optional — Ollama runs natively. Install only if you want other containerized services here. |

## Install (Ubuntu)

```bash
sudo apt install -y docker.io docker-compose-plugin docker-buildx-plugin 2>/dev/null || true
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker "$USER"
```

Log out and back in (or reboot) so the `docker` group applies.

## Verification

```bash
docker run --rm hello-world
```

- [ ] Hello World runs without permission errors (after re-login).

## Next

- **AI server (Ollama):** [../../ai-server/03-ollama/README.md](../../ai-server/03-ollama/README.md)
- **This VPS** (after Ollama is reachable over Tailscale): [../02-open-webui/README.md](../02-open-webui/README.md)
- **OpenClaw VPS:** [../../vps-openclaw/README.md](../../vps-openclaw/README.md)
