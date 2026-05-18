# Keeping these guides current

This folder is **procedural** (your architecture + copy-paste). **Behavior and flags** change upstream. Treat the links below as the source of truth and refresh this repo when those docs change.

## Context7 MCP (recommended in Cursor)

Context7 pulls **current** library docs into the agent instead of relying on training data.

**Status today:** `.cursor/mcp.json` exists but Cursor must be **restarted** for the agent to see the Context7 server. After restart, confirm by asking: `use context7 to list libraries for /openclaw/openclaw`.

> **Security:** treat any API key that has appeared in chat or screenshots as **leaked** — rotate it in the Context7 dashboard and only paste the **new** key into `.cursor/mcp.json` (which is gitignored).

After it is enabled, ask the agent explicitly, for example:

- `use context7 for Ollama Linux install and OLLAMA_HOST`
- `use context7 for Open WebUI Docker OLLAMA_BASE_URL`
- `use context7 with /open-webui/open-webui` (if that library ID resolves)

**Install (official):** [Context7 — Cursor client](https://context7.com/docs/clients/cursor)

```bash
npx ctx7 setup --cursor
```

That flow configures Cursor and can add a skill/rule so Context7 runs when you ask for library docs.

**Project-level MCP (this repo):** copy [`.cursor/mcp.json.example`](../.cursor/mcp.json.example) to **`.cursor/mcp.json`**, set `CONTEXT7_API_KEY` to your key, and restart Cursor. The real `mcp.json` is **gitignored** so keys are not committed. Prefer a **new** key if one was ever pasted into chat or a ticket.

For global install only, use **user** config (`~/.cursor/mcp.json`) — see Context7’s doc under “Project vs Global Config”.

**Tip:** In prompts, include **version or year** when it matters (e.g. “Ubuntu 24.04”, “Open WebUI Docker `main` tag”).

---

## Canonical documentation (bookmark these)

| Topic | Primary docs | Machine-readable index (when available) |
|--------|----------------|----------------------------------------|
| **Ollama** (install, Linux, systemd, ROCm) | [docs.ollama.com/linux](https://docs.ollama.com/linux), [FAQ / server config](https://docs.ollama.com/faq) | [docs.ollama.com/llms.txt](https://docs.ollama.com/llms.txt) |
| **Open WebUI** (Docker, env, troubleshooting) | [docs.openwebui.com](https://docs.openwebui.com/), [Getting started](https://docs.openwebui.com/getting-started/) | [GitHub README (install section)](https://raw.githubusercontent.com/open-webui/open-webui/main/README.md) |
| **Tailscale** (Linux install) | [tailscale.com/download/linux](https://tailscale.com/download/linux) | [tailscale.com/docs/install/linux](https://tailscale.com/docs/install/linux) |
| **OpenClaw** | [docs.openclaw.ai/install](https://docs.openclaw.ai/install), [Hostinger](https://docs.openclaw.ai/install/hostinger), [Linux VPS](https://docs.openclaw.ai/vps) | [docs.openclaw.ai/llms.txt](https://docs.openclaw.ai/llms.txt) |
| **Docker Engine (Ubuntu)** | [docs.docker.com/engine/install/ubuntu](https://docs.docker.com/engine/install/ubuntu) | — |
| **Ubuntu** | [Ubuntu Desktop](https://ubuntu.com/download/desktop), release notes | — |

---

## Repo maintenance checklist (quarterly or before big changes)

1. Enable **Context7** in Cursor and re-ask for the four rows above (install + env vars that affect you).
2. Open each **llms.txt** (where linked) and spot-check paths you rely on (`OLLAMA_HOST`, `OLLAMA_BASE_URL`, Tailscale install, Open WebUI Docker).
3. Run through **Verification** sections in `setup/ai-server/`, `setup/vps-apps/`, and `setup/vps-openclaw/` on a non-production VM if possible.
4. Update the **“Last doc sweep”** line in `setup/README.md` with the date you did this.

---

## What we intentionally do not mirror here

- Full Open WebUI / Ollama / Tailscale / OpenClaw reference manuals (they go stale in git).
- Exact **image tags** beyond `:main` unless you pin versions for reproducibility — if you pin, record the digest in your own notes or a private env file.
