# Setup — three machines

Your stack uses **three different computers**. Guides are split so you only open the folder for the machine you are sitting at.

| Where | Folder | Role |
|--------|--------|------|
| **KUBB OCTO (Ubuntu + Ollama)** | [ai-server/](ai-server/README.md) | Wipe Windows, install Ubuntu, Ollama, models, optional image tools |
| **Hostinger VPS — apps** | [vps-apps/](vps-apps/README.md) | Docker, Open WebUI pointing at home Ollama |
| **Hostinger VPS — OpenClaw only** | [vps-openclaw/](vps-openclaw/README.md) | OpenClaw install, memory, dreaming, security |
| **All machines** | [network-tailscale/](network-tailscale/README.md) | Tailscale on every node so they can talk privately |

```text
Browser ──► VPS-apps (Open WebUI) ──► Tailscale ──► AI server (Ollama)
                                            ▲
Discord ──► VPS-openclaw ───────────────────┘ (uses Ollama for embeddings + optional LLM)
```

**Typical first-time path**

1. Finish **[ai-server/](ai-server/README.md)** through Ollama + at least one model.
2. Do **[network-tailscale/](network-tailscale/README.md)** on **all three** machines.
3. Finish **[vps-apps/](vps-apps/README.md)** (Docker → Open WebUI → security).
4. Finish **[vps-openclaw/](vps-openclaw/README.md)** (install → memory → dreaming → security).

**Keeping commands accurate:** [DOCUMENTATION-SOURCES.md](DOCUMENTATION-SOURCES.md) (official links + Context7). *Last doc sweep: 2026-05-01.*
