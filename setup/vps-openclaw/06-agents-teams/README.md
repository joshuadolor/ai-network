# OpenClaw — DLR Web Solutions LLC: multi-agent team setup

This guide sets up **four isolated agents** inside one OpenClaw Gateway, all powered **exclusively by your local Ollama AI server** (the KUBB OCTO). No paid cloud AI APIs.

## Official references

- [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent)
- [Ollama provider](https://docs.openclaw.ai/providers/ollama) — use native API (`http://host:11434`), **never** `/v1`
- [SOUL.md guide](https://docs.openclaw.ai/concepts/soul)
- [Agent config](https://docs.openclaw.ai/gateway/config-agents)
- [Gateway configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)

---

## Team map

```
DLR Web Solutions LLC
│
├── 🐈  main          Felix   — grey tabby CEO, your personal assistant
├── 😼  stoic-social  Marcus  — stoic black cat, content for "Stoic Guy"
├── 🐈‍⬛  got-social    Nyx     — sleek shadow cat, content for "GOT-like story"
└── 🐾  ats-team      Byte    — wide-eyed orange hacker cat, "ATS-lite" dev
```

Each agent has:
- Its own **Discord bot** (separate application in the Developer Portal)
- Its own **workspace** folder with `SOUL.md`, `AGENTS.md`, `MEMORY.md`
- Its own **memory + dreaming** backed by your local `nomic-embed-text` embeddings
- The same **Ollama LLM** (no cloud API keys needed)

---

## Local AI model recommendations

Pull these on the AI server before you start ([../../ai-server/04-models/README.md](../../ai-server/04-models/README.md)):

| Agent | Recommended model | Why |
|-------|------------------|-----|
| `main` | `qwen2.5:72b` | Strong reasoning for general tasks |
| `stoic-social` | `qwen2.5:7b` | Fast, cheap for content drafts |
| `got-social` | `qwen2.5:7b` | Fast, cheap for content drafts |
| `ats-team` | `deepseek-coder:33b` | Best local coding model you have |

You can change any of these later by editing `agents.list[].model` in the config.

---

## Step 1 — Create a Discord bot for each agent

In the [Discord Developer Portal](https://discord.com/developers/applications), create **4 separate applications + bots**:

| Agent id | Bot name suggestion |
|----------|---------------------|
| `main` | `Felix 🐈` |
| `stoic-social` | `Marcus 😼` |
| `got-social` | `Nyx 🐈‍⬛` |
| `ats-team` | `Byte 🐾` |

For each bot:
1. **Bot tab** → set username → **Enable Message Content Intent + Server Members Intent**
2. **Reset Token** → copy it → save in password manager
3. **OAuth2** → enable `bot` + `applications.commands` → minimum permissions: View Channels, Send Messages, Read Message History, Embed Links, Attach Files
4. Invite each bot to your Discord server

> For the full Discord pairing walkthrough see [../05-discord-channel/README.md](../05-discord-channel/README.md).

---

## Step 2 — Store bot tokens on the VPS

SSH into your **OpenClaw VPS** and set tokens in `~/.openclaw/.env` (never committed):

```bash
mkdir -p ~/.openclaw
chmod 700 ~/.openclaw

cat >> ~/.openclaw/.env <<'EOF'
DISCORD_BOT_TOKEN_MAIN=paste-main-bot-token-here
DISCORD_BOT_TOKEN_STOIC=paste-stoic-bot-token-here
DISCORD_BOT_TOKEN_GOT=paste-got-bot-token-here
DISCORD_BOT_TOKEN_ATS=paste-ats-bot-token-here
EOF

chmod 600 ~/.openclaw/.env
```

---

## Step 3 — Create agent workspaces

```bash
openclaw agents add stoic-social
openclaw agents add got-social
openclaw agents add ats-team
```

The `main` agent workspace already exists from onboarding. Each command creates:

```
~/.openclaw/workspace-stoic-social/
  SOUL.md       ← personality (edit this — see Step 5)
  AGENTS.md     ← operating rules
  MEMORY.md     ← long-term memory (starts empty, grows over time)
  IDENTITY.md   ← name, emoji
  memory/       ← daily notes
```

---

## Step 4 — Apply the gateway config

**Recommended single-agent (Felix) baseline:** copy [openclaw.json.example](../openclaw.json.example) to the VPS, replace `REPLACE_*` placeholders, merge with your existing `~/.openclaw/openclaw.json` if needed (keep your gateway token). Secrets belong in [.env.example](../.env.example) → `~/.openclaw/.env`. Default chat model is **7b** for speed with **72b** as fallback.

```bash
# On the VPS (from a git clone or scp of this repo)
cp /path/to/AINetwork/setup/vps-openclaw/skills/hostinger-email -r ~/.openclaw/workspace/skills/
chmod 700 ~/.openclaw/workspace/skills/hostinger-email/scripts/mail.py
openclaw config patch --file /path/to/openclaw.json.example --dry-run
```

Multi-agent DLR patch (four Discord bots) is below. Apply it with:

```bash
cat > /tmp/dlr-agents.patch.json5 << 'JSON5'
{
  // ── Ollama provider (your KUBB AI server over Tailscale) ──────────────────
  models: {
    providers: {
      ollama: {
        baseUrl: "http://AI_SERVER_TAILSCALE_IP:11434",
        apiKey: "ollama-local"
      }
    }
  },

  // ── All agents default to local Ollama — zero cloud API calls ────────────
  agents: {
    defaults: {
      model: {
        primary: "ollama/qwen2.5:72b",
        fallbacks: ["ollama/qwen2.5:7b"]
      },
      memorySearch: {
        provider: "ollama"
      },
      userTimezone: "Europe/Madrid",
      heartbeat: {
        every: "1h"
      }
    },

    list: [
      // ── Felix — grey tabby CEO / personal assistant ──────────────────────
      {
        id: "main",
        default: true,
        name: "Felix",
        workspace: "~/.openclaw/workspace",
        agentDir: "~/.openclaw/agents/main/agent",
        identity: { name: "Felix", emoji: "🐈" },
        model: { primary: "ollama/qwen2.5:72b", fallbacks: ["ollama/qwen2.5:7b"] }
      },

      // ── Marcus — stoic black cat, Stoic Guy content ──────────────────────
      {
        id: "stoic-social",
        name: "Marcus",
        workspace: "~/.openclaw/workspace-stoic-social",
        agentDir: "~/.openclaw/agents/stoic-social/agent",
        identity: { name: "Marcus", emoji: "😼" },
        model: { primary: "ollama/qwen2.5:7b", fallbacks: ["ollama/qwen2.5:72b"] },
        tools: {
          deny: ["exec", "write", "edit", "apply_patch", "browser"]
        }
      },

      // ── Nyx — sleek shadow cat, GOT-like story content ───────────────────
      {
        id: "got-social",
        name: "Nyx",
        workspace: "~/.openclaw/workspace-got-social",
        agentDir: "~/.openclaw/agents/got-social/agent",
        identity: { name: "Nyx", emoji: "🐈‍⬛" },
        model: { primary: "ollama/qwen2.5:7b", fallbacks: ["ollama/qwen2.5:72b"] },
        tools: {
          deny: ["exec", "write", "edit", "apply_patch", "browser"]
        }
      },

      // ── Byte — wide-eyed orange hacker cat, ATS-lite dev ─────────────────
      {
        id: "ats-team",
        name: "Byte",
        workspace: "~/.openclaw/workspace-ats",
        agentDir: "~/.openclaw/agents/ats-team/agent",
        identity: { name: "Byte", emoji: "🐾" },
        model: { primary: "ollama/deepseek-coder:33b", fallbacks: ["ollama/qwen2.5:72b"] },
        tools: {
          allow: ["exec", "read", "write", "edit", "apply_patch", "browser"]
        }
      }
    ]
  },

  // ── Memory + dreaming (all agents, Ollama embeddings) ────────────────────
  plugins: {
    entries: {
      "memory-core": {
        config: {
          dreaming: {
            enabled: true,
            timezone: "Europe/Madrid",
            frequency: "0 3 * * *"
          }
        }
      }
    }
  },

  // ── Discord: one bot account per agent ───────────────────────────────────
  channels: {
    discord: {
      groupPolicy: "allowlist",
      accounts: {
        main: {
          token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN_MAIN" },
          guilds: { "YOUR_DISCORD_SERVER_ID": {} }
        },
        "stoic-social": {
          token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN_STOIC" },
          guilds: { "YOUR_DISCORD_SERVER_ID": {} }
        },
        "got-social": {
          token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN_GOT" },
          guilds: { "YOUR_DISCORD_SERVER_ID": {} }
        },
        "ats-team": {
          token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN_ATS" },
          guilds: { "YOUR_DISCORD_SERVER_ID": {} }
        }
      }
    }
  },

  // ── Bindings: which bot → which agent ────────────────────────────────────
  bindings: [
    { agentId: "main",         match: { channel: "discord", accountId: "main" } },
    { agentId: "stoic-social", match: { channel: "discord", accountId: "stoic-social" } },
    { agentId: "got-social",   match: { channel: "discord", accountId: "got-social" } },
    { agentId: "ats-team",     match: { channel: "discord", accountId: "ats-team" } }
  ]
}
JSON5

# Replace the placeholder with your real Tailscale IP before applying:
AI_IP="$(tailscale ip -4)"  # run on the AI server and paste the result here
sed -i "s/AI_SERVER_TAILSCALE_IP/${AI_IP}/" /tmp/dlr-agents.patch.json5

# Replace YOUR_DISCORD_SERVER_ID with your real server ID, then:
openclaw config patch --file /tmp/dlr-agents.patch.json5 --dry-run
# Review the dry-run output, then apply:
openclaw config patch --file /tmp/dlr-agents.patch.json5
```

---

## Step 5 — Write each agent's SOUL.md + AGENTS.md

These two files define who each agent **is** and what rules it follows. Edit them directly on the VPS or use `nano`.

> **Paths and file glossary:** [../08-workspace/README.md](../08-workspace/README.md) — all workspace locations (`~/.openclaw/workspace/`, `workspace-stoic-social/`, …), what belongs in each file, and what must stay in `~/.openclaw/.env` instead.

### `~/.openclaw/workspace/SOUL.md` (Felix — main)

```md
You are Felix — a grey tabby cat with sharp green eyes. CEO of DLR Web
Solutions LLC and personal assistant to Joshua.

You are the one who sees the whole board. You delegate. You unblock. You ship.

- Tone: direct, confident, warm when it matters. No fluff.
- You know Joshua's projects, patterns, and priorities deeply.
- You coordinate the other cats — Marcus, Nyx, Byte — and surface blockers.
- You get things done while Joshua sleeps.
- You are a cat. Quiet, capable, always watching. This lives in how you work,
  not in what you say about yourself.
```

### `~/.openclaw/workspace-stoic-social/SOUL.md`

```md
You are Marcus — a stoic black cat with amber eyes. Social media strategist
for Stoic Guy, a brand built around timeless stoic philosophy for modern men.

You move deliberately. You do not react. You observe, then you act.

- Tone: calm, grounded, direct. No hype. No fluff.
- Content pillars: discipline, resilience, mental clarity, brotherhood.
- Write like Epictetus taught: short, sharp, actionable.
- You know the brand voice deeply — if a draft strays from it, say so.
- Opinions are welcome. Hedging is not.
- Never use corporate buzzwords. Plain English always wins.
- You are a cat. This is subtle — it lives in your patience and your precision,
  not in what you say about yourself.
```

### `~/.openclaw/workspace-stoic-social/AGENTS.md`

```md
## Role
Social media content strategist for the Stoic Guy brand.

## Session Startup
- Check MEMORY.md for active campaigns, brand guidelines, content calendar.
- Check today's memory/YYYY-MM-DD.md for pending tasks.

## Red Lines
- No political opinions.
- Do not stray from stoic/masculine self-improvement.
- Always flag quotes attributed to real historical figures — confirm accuracy.
- No publishing decisions — you draft, the human approves.
```

---

### `~/.openclaw/workspace-got-social/SOUL.md`

```md
You are Nyx — a sleek shadow cat, black as a starless night. Social media
strategist for a dark fantasy world of political intrigue, power, and survival.

You see everything from the shadows. You reveal only what serves the story.

- Tone: dramatic, vivid, immersive. Make people feel the world.
- Content: lore drops, character moments, faction news, cryptic foreshadowing.
- Write in-universe whenever possible. Break the fourth wall only for CTAs.
- The audience is fantasy/lore fans. Give them depth, not clickbait.
- One sentence can be more powerful than a paragraph. Use that.
- You are a cat. This is subtle — it lives in your inscrutability and your
  eye for the perfect moment to strike, not in what you say about yourself.
```

### `~/.openclaw/workspace-got-social/AGENTS.md`

```md
## Role
Social media content strategist for the GOT-like story brand.

## Session Startup
- Check MEMORY.md for story arcs, character rosters, factions, lore timeline.
- Check today's memory/YYYY-MM-DD.md for scheduled posts and pending lore.

## Red Lines
- Never break canon. If unsure, flag it.
- No spoilers for story arcs not yet published.
- No publishing decisions — you draft, the human approves.
```

---

### `~/.openclaw/workspace-ats/SOUL.md`

```md
You are Byte — a wide-eyed orange tabby with ink-stained paws. Technical lead
for ATS-lite, a lightweight applicant tracking system under DLR Web Solutions LLC.

You are relentlessly curious. You bat at problems until they are solved or dead.

- Tone: precise, no-nonsense, engineering-first.
- You ship. You do not theorize endlessly about architecture.
- Call out bad approaches early. Prefer simple over clever.
- You know the codebase. Ask for context before making sweeping changes.
- A well-placed "that's a bad idea, here's why" beats agreeing and shipping bugs.
- You are a cat. This shows in your focused intensity and your habit of
  knocking things off tables that don't belong there.
```

### `~/.openclaw/workspace-ats/AGENTS.md`

```md
## Role
Technical lead and developer for ATS-lite.

## Session Startup
- Check MEMORY.md for architecture decisions, tech stack, open issues.
- Check today's memory/YYYY-MM-DD.md for WIP tasks and blockers.

## Red Lines
- Never modify production config without explicit confirmation.
- Never commit secrets or credentials.
- Always test before claiming something is done.
```

---

## Step 6 — Set up Discord channels (one per team)

In your Discord server, create and assign:

| Discord channel | Bot to add | `CHANNEL_ID` to note |
|-----------------|-----------|----------------------|
| `#dlr-main` | `Felix 🐈` | Right-click → Copy Channel ID |
| `#stoic-content` | `Marcus 😼` | |
| `#got-content` | `Nyx 🐈‍⬛` | |
| `#ats-dev` | `Byte 🐾` | |

To restrict each bot to only its channel (recommended), update the config channel entries:

```json5
"stoic-social": {
  token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN_STOIC" },
  guilds: {
    "YOUR_SERVER_ID": {
      channels: {
        "STOIC_CHANNEL_ID": { allow: true, requireMention: false }
      }
    }
  }
}
```

Apply the update the same way (`openclaw config patch`).

---

## Step 7 — Restart and verify

```bash
# Load ~/.openclaw/.env into the session and restart
set -a && source ~/.openclaw/.env && set +a
openclaw gateway restart

# Confirm all four agents loaded
openclaw agents list --bindings

# Confirm all four Discord bots connected
openclaw channels status --probe

# Confirm Ollama is reachable from OpenClaw
openclaw models list --provider ollama
```

Then in Discord, **DM each bot** — it will reply with a pairing code. Approve:

```bash
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

Do this for all four bots.

---

## Step 8 — Let agents learn over time

Once bots are paired, each agent builds its own memory automatically:

- **Daily notes** accumulate in `memory/YYYY-MM-DD.md`.
- **Dreaming** runs at 3 AM every night → promotes strong signals into `MEMORY.md`.
- **Manual promotion preview**: `openclaw memory promote --agent stoic-social`

Tell each agent what you want it to remember: *"Remember that our Stoic Guy content calendar runs Mon/Wed/Fri and target audience is 25–40 y/o men."* — it writes it to memory.

---

## Model note — why no paid AI

This config uses `ollama/qwen2.5:72b` and `ollama/deepseek-coder:33b` pointing at `http://<AI_SERVER_TAILSCALE_IP>:11434`. The KUBB OCTO's **128 GB unified RAM** can run these models locally. All inference stays on your hardware. No Anthropic, OpenAI, or other paid provider keys are needed.

> **Important:** `baseUrl` must be `http://host:11434` (no `/v1`). Using `/v1` breaks tool calling in OpenClaw. The `apiKey: "ollama-local"` value is a required placeholder for local/LAN hosts — it is not a real credential.

---

## Checklist

- [ ] 4 Discord bots created, tokens stored in `~/.openclaw/.env`
- [ ] `openclaw agents add` run for stoic-social, got-social, ats-team
- [ ] Config patch applied (Tailscale IP + Discord server ID filled in)
- [ ] `SOUL.md` + `AGENTS.md` written for each workspace
- [ ] Discord channels created and bots assigned
- [ ] `openclaw gateway restart` done
- [ ] `openclaw agents list --bindings` shows all 4
- [ ] All 4 bots paired via DM + `openclaw pairing approve`
- [ ] `openclaw models list --provider ollama` returns models
- [ ] Dreaming enabled + first `openclaw memory promote` reviewed
