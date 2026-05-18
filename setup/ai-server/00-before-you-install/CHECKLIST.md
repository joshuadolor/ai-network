# Before you install Ubuntu (read once)

## Decisions

- [ ] You are **removing Windows** and installing **Ubuntu only** on the KUBB.
- [ ] You have a **VPS** (or will get one) for Open WebUI.
- [ ] You will use **Tailscale** so the VPS reaches Ollama on the KUBB without exposing Ollama to the public internet.

## Backup from Windows (last chance)

Export anything you need:

- [ ] Personal files (Documents, Pictures, etc.) to external drive or cloud you trust.
- [ ] Browser bookmarks / password vault (already in a vault is ideal).
- [ ] Windows / OEM license note (optional; you will not need it for Ubuntu).
- [ ] Any BitLocker recovery keys if the disk was encrypted (save before wipe).

## Hardware prep

- [ ] **8 GB+ USB** stick for the Ubuntu installer.
- [ ] Download **Ubuntu 24.04 LTS** desktop ISO from [ubuntu.com](https://ubuntu.com/download/desktop) (recommended for newer AMD Ryzen AI / firmware; 22.04 LTS is OK if 24.04 causes issues).
- [ ] Flash with **balenaEtcher** (or `dd` if you know how).
- [ ] Note: **Secure Boot** — Ubuntu installer usually handles it; if install fails, check BIOS for Secure Boot / CSM settings per motherboard docs.

## Network

- [ ] Ethernet cable ready (simplest for first boot and large model pulls).
- [ ] Wi‑Fi SSID and password if you will use wireless.

## Accounts (have them ready)

- [ ] Tailscale account (Google/Microsoft/GitHub sign-in).
- [ ] VPS SSH access and sudo.
- [ ] Optional: domain or static workflow for VPS IP (not required if you use IP:port).

When done, go to [../01-ubuntu/README.md](../01-ubuntu/README.md).

For **ongoing accuracy** of commands (Ollama, Open WebUI, Tailscale, OpenClaw), see [../../DOCUMENTATION-SOURCES.md](../../DOCUMENTATION-SOURCES.md).
