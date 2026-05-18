# AI server (KUBB OCTO)

Everything here runs on the **physical workstation** where you install **Ubuntu** and **Ollama**. Nothing in this folder assumes your Hostinger VPS.

## Order

| Step | Folder | What |
|------|--------|------|
| 1 | [00-before-you-install](00-before-you-install/CHECKLIST.md) | Backup, USB, wipe Windows |
| 2 | [01-ubuntu](01-ubuntu/README.md) | Install Ubuntu only |
| 3 | [02-base-system](02-base-system/README.md) | Updates, `git`, bootstrap script |
| 4 | [03-ollama](03-ollama/README.md) | Ollama install, `OLLAMA_HOST`, GPU |
| 5 | [04-models](04-models/README.md) | Model pulls |
| 6 | (optional) [05-image-video](05-image-video/README.md) | SDXL / AnimateDiff in a venv |
| 7 | [06-security](06-security/README.md) | UFW, SSH, Ollama not on the public WAN |

**Networking:** when this box is online and you are ready to pair it with the VPSes, follow **[../network-tailscale/README.md](../network-tailscale/README.md)** on **all** machines (AI server + apps VPS + OpenClaw VPS).

**VPS work** lives in two folders — **not** on this machine unless you choose optional Docker here:

- Apps VPS (Open WebUI): **[../vps-apps/README.md](../vps-apps/README.md)**
- OpenClaw VPS (gateway, memory, dreaming): **[../vps-openclaw/README.md](../vps-openclaw/README.md)**

Doc hygiene: [../DOCUMENTATION-SOURCES.md](../DOCUMENTATION-SOURCES.md)
