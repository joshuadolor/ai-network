# AI server — security & habits

## References

- Ollama exposure: [docs.ollama.com/faq](https://docs.ollama.com/faq)

## Checklist (this machine)

- [ ] **Do not** port-forward Ollama (`11434`) from your home router to the public internet.
- [ ] Set `OLLAMA_HOST=0.0.0.0:11434` only together with a sane plan (Tailscale + optional UFW on `tailscale0`). See [../03-ollama/README.md](../03-ollama/README.md).
- [ ] `sudo ufw status` reviewed if UFW is enabled.
- [ ] SSH: prefer keys; disable password auth when you are comfortable (`/etc/ssh/sshd_config`).
- [ ] Avoid loading **72B + 33B** at the same time unless you know RAM headroom (`ollama ps`).
- [ ] `sudo apt update && sudo apt upgrade -y` on a schedule you like.

## VPS / Open WebUI users

Account creation for the **chat UI** happens on the apps VPS: [../../vps-apps/03-security/README.md](../../vps-apps/03-security/README.md).

## Done on the AI server?

- Apps VPS (Open WebUI): [../../vps-apps/README.md](../../vps-apps/README.md)
- OpenClaw VPS (gateway, memory, dreaming): [../../vps-openclaw/README.md](../../vps-openclaw/README.md)
