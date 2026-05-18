# OpenClaw — install on the Hostinger VPS

## Official documentation (use these if anything here drifts)

- Repo doc hygiene + **Context7**: [../../DOCUMENTATION-SOURCES.md](../../DOCUMENTATION-SOURCES.md)
- [Install overview](https://docs.openclaw.ai/install)
- [**Hostinger** (1-Click + VPS via hPanel)](https://docs.openclaw.ai/install/hostinger)
- [Linux server / generic VPS](https://docs.openclaw.ai/vps)
- [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)
- [Gateway remote access](https://docs.openclaw.ai/gateway/remote)
- [Channels](https://docs.openclaw.ai/channels) — your channel will be **[Discord](https://docs.openclaw.ai/channels/discord)** (see [`05-discord-channel/`](../05-discord-channel/README.md))
- [Security](https://docs.openclaw.ai/gateway/security)
- **Doc index for agents:** [docs.openclaw.ai/llms.txt](https://docs.openclaw.ai/llms.txt) (see “Fast access to Markdown docs” below)

## Fast access to Markdown docs — `llms.txt`

The convention you wanted is **`llms.txt`**: a curated **Markdown index** (often at `/llms.txt`) so agents fetch a small table of contents instead of crawling whole sites. Spec: [llmstxt.org](https://www.llmstxt.org/).

OpenClaw exposes its index at **[https://docs.openclaw.ai/llms.txt](https://docs.openclaw.ai/llms.txt)**. Point any skill/tool that fetches docs at this index first, then it follows only the linked `.md` pages it actually needs.

If you also want **semantic search across Markdown** (your repos, an Obsidian vault, etc.), that is **RAG** — not `llms.txt`. The next folder ([../02-memory/README.md](../02-memory/README.md)) covers that path with OpenClaw's memory plugins.

---

## Choose how you run it on this VPS

### Option A — Managed 1-Click OpenClaw (simplest)

1. From the [Hostinger OpenClaw page](https://www.hostinger.com/openclaw) pick a **Managed OpenClaw** plan and complete checkout.
2. Hostinger handles infrastructure, Docker, and updates.
3. In the wizard:
   - **Channel:** skip the bundled Telegram/WhatsApp setup. **Discord is the only supported channel for this stack** — you will wire it up in [`05-discord-channel/`](../05-discord-channel/README.md).
   - **Model provider:** **do not** pick the bundled credits, Anthropic, OpenAI, Gemini, or xAI. This stack uses **local Ollama only** on your KUBB OCTO AI server. If the wizard requires a provider before continuing, pick **Ollama** and point `baseUrl` at `http://<AI_SERVER_TAILSCALE_IP>:11434` (no `/v1`) with `apiKey: "ollama-local"`. If Ollama isn't an option in the managed wizard, pick anything to get past the screen, then immediately overwrite the provider config in [`06-agents-teams/`](../06-agents-teams/README.md).
4. Click **Finish** → open the **OpenClaw dashboard** from **OpenClaw Overview** in **hPanel**. Then continue with Discord setup.

**Verify after Discord pairing:** DM your bot — "Hi" should be answered.

### Option B — Hostinger VPS with the OpenClaw Docker template (hPanel-managed)

1. From the same flow choose an **OpenClaw on VPS** plan and complete checkout.
2. Once provisioned, fill the config in hPanel:
   - **Gateway token** — save it.
   - **Channel fields:** leave **Telegram/WhatsApp/Slack/iMessage/Signal** fields blank — Discord is the only channel for this stack ([`05-discord-channel/`](../05-discord-channel/README.md)).
   - **Model provider:** leave any **Anthropic / OpenAI / Gemini / xAI / OpenRouter / MiniMax** key fields blank. You'll set `models.providers.ollama.baseUrl` to `http://<AI_SERVER_TAILSCALE_IP>:11434` in [`06-agents-teams/`](../06-agents-teams/README.md). No paid AI keys needed.
3. Click **Deploy**. Use **Docker Manager** in hPanel for logs / restart / **Update** (pulls latest image).

**Troubleshooting (from the official Hostinger doc):**

- Dashboard slow → wait, check Docker Manager logs.
- Container restart loop → logs usually point at missing tokens / API keys.
- Discord pairing trouble → see [`05-discord-channel/`](../05-discord-channel/README.md) and [official Discord channel doc](https://docs.openclaw.ai/channels/discord).

### Option C — Plain Ubuntu KVM + official Linux installer

Use this when you bought a generic KVM VPS without the OpenClaw template — full SSH control, matches the [Linux server / VPS](https://docs.openclaw.ai/vps) guide.

1. **SSH in** (`ssh user@YOUR_VPS_IP`).
2. **Harden SSH** before exposing services — see [../04-security/README.md](../04-security/README.md) and [Linux server — Harden admin access first](https://docs.openclaw.ai/vps).
3. **Install OpenClaw** (the script installs Node if needed):

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Non-interactive first pass (optional):

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

4. **Onboard + systemd user daemon** (typical for servers).

> **During the wizard:** pick **Ollama** as the model provider (point at `http://<AI_SERVER_TAILSCALE_IP>:11434`, `apiKey: "ollama-local"`). When asked for a channel, pick **Discord** or **Skip for now** — never Telegram/WhatsApp/Slack/iMessage/Signal. Use the [Setup Wizard Cheat Sheet prompt](../07-prompts/README.md#2-setup-wizard-cheat-sheet) to get answer-by-answer guidance.

```bash
openclaw onboard --install-daemon
```

5. **Verify:**

```bash
openclaw --version
openclaw doctor
openclaw gateway status
```

6. Optional small-VPS tuning (from [Linux server docs](https://docs.openclaw.ai/vps)) — faster cold starts:

```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

For systemd overrides on the gateway unit, follow the **systemd tuning checklist** on the same page (`systemctl --user edit openclaw-gateway.service`).

**Alternative installs:** [`install-cli.sh`](https://docs.openclaw.ai/install/installer#install-clish), `npm install -g openclaw@latest`, or [Docker](https://docs.openclaw.ai/install/docker) — all linked from [Install](https://docs.openclaw.ai/install).

## Next

[../02-memory/README.md](../02-memory/README.md) → dreaming → security → **[../05-discord-channel/README.md](../05-discord-channel/README.md)** to wire up the Discord bot → **[../08-workspace/README.md](../08-workspace/README.md)** for `SOUL.md`, `AGENTS.md`, and `USER.md` on the VPS.
