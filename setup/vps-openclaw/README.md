# VPS — OpenClaw (dedicated)

This Hostinger VPS is **only for OpenClaw**: gateway, **Discord** channel, memory, dreaming. It does **not** run Open WebUI — that lives on the apps VPS ([../vps-apps/README.md](../vps-apps/README.md)).

## Order

| Step | Folder | What |
|------|--------|------|
| 0 | [../network-tailscale/README.md](../network-tailscale/README.md) | Tailscale on this VPS (so it can reach the AI server's Ollama for embeddings, optional but recommended) |
| 1 | [01-install](01-install/README.md) | OpenClaw install: Hostinger 1-Click, Hostinger VPS Docker, or plain Ubuntu |
| 2 | [02-memory](02-memory/README.md) | Memory plugins (builtin / LanceDB / wiki) — Markdown + Ollama embeddings |
| 3 | [03-dreaming](03-dreaming/README.md) | Background memory consolidation (`dreaming.enabled`) |
| 4 | [04-security](04-security/README.md) | SSH hardening, gateway exposure, secrets |
| 5 | [05-discord-channel](05-discord-channel/README.md) | Discord bot, intents, pairing, optional guild workspace |
| 6 | [06-agents-teams](06-agents-teams/README.md) | DLR Web Solutions LLC: Felix 🐈 Marcus 😼 Nyx 🐈‍⬛ Byte 🐾 — local Ollama only, no paid AI |
| 7 | [07-prompts](07-prompts/README.md) | Ready-to-use prompt library: hardware selector, setup wizard, Mission Control, self-improvement, security audit |
| 8 | [08-workspace](08-workspace/README.md) | Where `SOUL.md`, `AGENTS.md`, `USER.md`, `MEMORY.md` live on the VPS (`~/.openclaw/workspace/`) |

**Reference gateway config (Felix + compaction + browser + email):** [openclaw.json.example](openclaw.json.example) and [.env.example](.env.example). Bundled skills: [skills/](skills/) (research, image, crypto watch, UX, proactive, email) — synced by `update-vps-openclaw.sh`.

**Felix workspace** = [javiConsu/felix-workspace](https://github.com/javiConsu/felix-workspace) (CEO tone, cron discipline, production lock) + [Tina Huang](https://www.youtube.com/watch?v=oOCN30ulVyo) patterns (memory logging, multi-agent/cron hygiene), adapted for **Ollama on KUBB + OpenClaw VPS + Discord**.

**Update on VPS:** `bash setup/vps-openclaw/scripts/update-vps-openclaw.sh` (see `--help`). Templates: [08-workspace/workspace/](08-workspace/workspace/).

**Lead → site trial** (businesses without websites → HTML → ngrok): [reference/lead-site-trial-workflow.md](reference/lead-site-trial-workflow.md) · skill [lead-site-pipeline](skills/lead-site-pipeline/).

**Tina Huang prompts ([video](https://www.youtube.com/watch?v=oOCN30ulVyo), [Google Doc](https://docs.google.com/document/d/1cJPzi3j0WioG-PzTZ5eQR7HxzEETLlr2zHRtYvIsUq0/edit)):** full export + Felix versions in [reference/tina-huang-openclaw-prompts/](reference/tina-huang-openclaw-prompts/).

## Why a separate VPS

- **Isolation:** OpenClaw runs background skills/cron; keep it away from your chat UI users.
- **RAM headroom:** the gateway + plugins consume meaningful memory; less contention with Open WebUI.
- **Blast radius:** a compromised app on the apps VPS does not get your OpenClaw secrets.

## Connecting the dots

OpenClaw's **LLM calls** go to **your Ollama** on the AI server through Tailscale. Set the Ollama provider `baseUrl` to `http://<AI_SERVER_TAILSCALE_IP>:11434` ([providers/ollama](https://docs.openclaw.ai/providers/ollama)).

For the DLR multi-agent setup, see [06-agents-teams](06-agents-teams/README.md) — all agents use local models, no external API keys required.

Doc hygiene + Context7: [../DOCUMENTATION-SOURCES.md](../DOCUMENTATION-SOURCES.md)
