# VPS — security & users

## Scope

This file is for the **apps VPS** (Open WebUI). OpenClaw security lives on its own VPS: [../../vps-openclaw/04-security/README.md](../../vps-openclaw/04-security/README.md).

## References

- Open WebUI: [docs.openwebui.com](https://docs.openwebui.com/)

## Principles

- Prefer reaching **Open WebUI** via **Tailscale** (`http://<VPS_TAILSCALE_IP>:3000`) instead of a wide-open public port.
- If you use a **public IP + port 3000**, use Hostinger’s firewall and restrict sources when possible.

## Open WebUI users

- [ ] **First login** on Open WebUI = admin account (you).
- [ ] **Admin panel → Users** — add your wife (or others) with appropriate roles.
- [ ] Strong passwords (or enterprise SSO later if you add it).

## Ongoing

- [ ] Keep the VPS updated: `sudo apt update && sudo apt upgrade -y` on a schedule.
- [ ] AI server habits (RAM, Ollama): [../../ai-server/06-security/README.md](../../ai-server/06-security/README.md)

## Next

OpenClaw lives on its own VPS now → [../../vps-openclaw/README.md](../../vps-openclaw/README.md).
