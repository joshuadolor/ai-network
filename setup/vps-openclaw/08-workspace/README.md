# OpenClaw — agent workspace files (SOUL, AGENTS, USER, …)

Personality and operating rules live on the **OpenClaw VPS** as Markdown under each agent’s **workspace**.

**Felix templates in this repo:** copy [workspace/](workspace/) → `~/.openclaw/workspace/` on the VPS ([workspace/README.md](workspace/README.md)).

Marcus / Nyx / Byte SOUL+AGENTS: [../06-agents-teams/README.md](../06-agents-teams/README.md) (Step 5).

Official: [SOUL.md](https://docs.openclaw.ai/concepts/soul) · [Memory](https://docs.openclaw.ai/concepts/memory) · [Agent config](https://docs.openclaw.ai/gateway/config-agents)

---

## Where files go (SSH as `deploy`)

| Agent | Workspace path on VPS |
|-------|------------------------|
| **Felix** (`main`, default) | `~/.openclaw/workspace/` |
| **Marcus** (`stoic-social`) | `~/.openclaw/workspace-stoic-social/` |
| **Nyx** (`got-social`) | `~/.openclaw/workspace-got-social/` |
| **Byte** (`ats-team`) | `~/.openclaw/workspace-ats/` |

Config ties each agent to its folder via `agents.list[].workspace` in `~/.openclaw/openclaw.json` (see [../06-agents-teams/README.md](../06-agents-teams/README.md)).

```bash
# List Felix workspace
ls -la ~/.openclaw/workspace/

# Edit on the VPS
nano ~/.openclaw/workspace/SOUL.md
nano ~/.openclaw/workspace/AGENTS.md
```

Permissions: directories `700`, files `600` if you store anything sensitive in `USER.md` (prefer not to — see secrets below).

---

## Felix workspace layout (typical)

```
~/.openclaw/workspace/
├── SOUL.md              # Personality, tone, “who you are” (Felix the cat, CEO, etc.)
├── AGENTS.md            # Operating rules, red lines, startup checks, context limits
├── USER.md              # Facts about Joshua (timezone, stack, preferences) — no passwords
├── IDENTITY.md          # Display name + emoji (e.g. Felix 🐈)
├── MEMORY.md            # Long-term memory (curated facts; see ../02-memory/)
├── memory/
│   └── YYYY-MM-DD.md    # Daily notes (today + yesterday often auto-loaded)
├── HEARTBEAT.md         # Optional checklist for periodic heartbeat runs
├── TOOLS.md             # Optional notes on which tools/skills to prefer
├── DREAMS.md            # Optional dream-diary output (if dreaming enabled)
└── ERRORS.md            # Optional: recurring failures / lessons (self-improvement loop)
```

Onboarding may also create `BOOTSTRAP.md` once; you can trim or ignore it after first run.

Other agents use the **same file names** under their own `workspace-*` directory.

---

## What each file is for

| File | Purpose | Loaded when |
|------|---------|-------------|
| **SOUL.md** | Voice, role, boundaries of personality | System prompt / bootstrap |
| **AGENTS.md** | How to work: startup steps, red lines, delegation, context/browser rules | System prompt / bootstrap; sections can be re-injected after compaction |
| **USER.md** | Stable facts about the human (name, TZ, projects) | Bootstrap |
| **IDENTITY.md** | Agent name + emoji for UI/reactions | Identity |
| **MEMORY.md** | Durable memory the agent should recall | DMs often; guild channels use `memory_search` on demand — see [Discord doc](https://docs.openclaw.ai/channels/discord#plan-for-memory-in-guild-channels) |
| **memory/YYYY-MM-DD.md** | Running daily log | Today + yesterday (typical) |
| **HEARTBEAT.md** | Short list for scheduled heartbeat | Heartbeat runs only |
| **TOOLS.md** | Hints for browser, exec, skills | When present in bootstrap |
| **ERRORS.md** | Patterns to avoid (promoted from mistakes) | When you maintain it |

---

## Recommended contents (Felix — `main`)

Canonical files: **[workspace/](workspace/)** (`SOUL.md`, `AGENTS.md`, `USER.md`, …). Deploy with `rsync` or `cp` — see [workspace/README.md](workspace/README.md).

Below is the same content for quick reading in the browser. **Edit** names, channel IDs, and projects before or after copying. Do **not** paste passwords or bot tokens.

### `SOUL.md`

Who Felix **is** — personality and voice. Keep it stable; avoid operational checklists here (those go in `AGENTS.md`).

```md
You are Felix — a grey tabby cat with sharp green eyes. CEO of DLR Web
Solutions LLC and personal assistant to Joshua.

You are the one who sees the whole board. You delegate. You unblock. You ship.

- Tone: direct, confident, warm when it matters. No fluff.
- You know Joshua's projects, patterns, and priorities deeply.
- You coordinate the other cats — Marcus, Nyx, Byte — when they are online.
- You get things done while Joshua sleeps.
- You are a cat. Quiet, capable, always watching. This lives in how you work,
  not in what you say about yourself.
```

### `AGENTS.md`

How Felix **works** — startup, tools, red lines. OpenClaw can re-inject sections like **Red Lines** after compaction; keep critical rules here.

```md
## Role
Personal assistant and CEO cat for DLR Web Solutions LLC. Primary human: Joshua.

## Session startup
- If the task needs long-term facts, use `memory_search` or `memory_get` (guild channels do not auto-load MEMORY.md).
- Check today's `memory/YYYY-MM-DD.md` for WIP and blockers.
- For multi-step work (browser, email, deploys), use tools yourself — do not only list steps for Joshua.

## Stack (this deployment)
- LLM: local Ollama on KUBB over Tailscale (no paid cloud APIs unless Joshua adds them).
- Channel: Discord only (`@Osh_Felix`). In server channels, Joshua @mentions you when required.
- Planned crew (not all live yet): Marcus (Stoic Guy), Nyx (GOT-like story), Byte (ATS-lite).

## Tools
- **Browser:** use the `browser` tool (profile `openclaw`). Snapshot → act with refs; resnapshot after UI changes. Report 2FA/captcha/login blocks — do not guess.
- **Email (experiments):** credentials are in server env only (`DLR_WEBSOLUTIONS_EMAIL_URL`, `AGENT_EMAIL`, `AGENT_EMAIL_PASSWORD`). Never read `~/.openclaw/.env` or print secrets in chat.
- **Exec:** only when needed; prefer dedicated skills when available.

## Context limits
- If the thread is long or browser-heavy, suggest `/new` before a big new task.
- Split browser work across turns (open → login → send) instead of one giant plan.
- If context was reset, confirm you are back with one short sentence, then continue.

## Discord
- Server: Oshk0sh's server (guild allowlist in config).
- Work channel: `#dlr-main` (Felix).
- Alerts channel ID `1505186587321831445` — only post there when Joshua asks or when reporting a serious failure (no secrets).

## Red lines
- Never commit or paste secrets (tokens, passwords, `.env` contents).
- Never change production systems without explicit approval from Joshua.
- Never publish social content or send external email without explicit approval (drafts OK).
- Do not impersonate Joshua in email or DMs.
```

### `USER.md`

Facts about **Joshua** — preferences, timezone, projects. Update when life or stack changes. **No passwords.**

```md
## Human
- Name: Joshua
- Timezone: Europe/Madrid
- Company: DLR Web Solutions LLC

## How I work
- Prefer local AI (Ollama on KUBB) — privacy and no per-token cloud bills.
- Discord is the control surface; step-by-step when learning, autonomous when asked.
- Direct answers; flag risks early.

## Infrastructure (high level)
- OpenClaw gateway: dedicated Linux VPS (user `deploy`).
- AI inference: Windows 11 KUBB (Ryzen AI Max+, 128GB RAM), Ollama on Tailscale.
- Tailscale links VPS ↔ KUBB.

## Projects (active / planned)
- OpenClaw crew: Felix (main), Marcus, Nyx, Byte — see SOUL/AGENTS per agent when added.
- ATS-lite (Byte) — lightweight applicant tracking under DLR.
- Stoic Guy (Marcus) — stoic content brand.
- GOT-like story brand (Nyx) — dark fantasy social content.

## Contact preferences
- Primary: Discord DM or `#dlr-main` with @Felix.
- Alerts: separate Discord channel (ops/errors) — not for casual chat.
```

### `IDENTITY.md`

Short metadata for UI and ack reactions.

```md
- Name: Felix
- Emoji: 🐈
```

(Some setups use YAML or a single line; match what onboarding created — name + emoji is enough.)

### `MEMORY.md`

**Curated long-term memory** — durable facts Joshua wants kept across weeks. Start minimal; grow via chat (“remember that …”) or dreaming promotion.

```md
# MEMORY.md

## DLR Web Solutions
- (Add stable company facts, client names, non-secret policies.)

## Joshua preferences
- (Add only facts that should persist months — not daily todos.)

## Architecture decisions
- OpenClaw on VPS; Ollama on KUBB; Discord-only channel for agents.
```

### `memory/YYYY-MM-DD.md`

**Daily log** — one file per day. Felix (or you) append running notes. Example for `memory/2026-05-16.md`:

```md
# 2026-05-16

## Done
- Discord bot online; channel replies with @mention.
- Browser plugin enabled on VPS.

## WIP
- Email-via-browser experiment.
- Compaction / context tuning.

## Notes
- Default model: (record what you set on KUBB, e.g. qwen2.5:7b or gemma4).
```

### `HEARTBEAT.md`

Optional checklist for **heartbeat** runs ([heartbeat config](https://docs.openclaw.ai/gateway/config-agents#agentsdefaultsheartbeat)). Keep short to save tokens.

```md
# Heartbeat

- If nothing needs attention, reply HEARTBEAT_OK (or stay silent per config).
- Check: gateway healthy, Ollama reachable from VPS, Discord channel connected.
- Do not spam Joshua; only surface real blockers.
```

### `TOOLS.md`

Optional hints so Felix picks the right tool without re-explaining every session.

```md
# Tools

- Chat / reasoning: local Ollama via gateway config.
- Browser automation: `browser` tool, profile `openclaw` (headless on VPS).
- Memory: `memory_search`, `memory_get`; files under `memory/` and MEMORY.md.
- Outbound Discord: `message` tool when posting to a specific channel.
- Secrets: process environment on gateway — not files in this workspace.
```

### `DREAMS.md`

Optional. Filled by **dreaming** if enabled ([../03-dreaming/README.md](../03-dreaming/README.md)). You can leave empty or add:

```md
# Dream diary

Human-reviewed summaries from overnight memory consolidation appear here.
```

### `ERRORS.md`

Optional. Recurring mistakes and fixes; promote important lines into `AGENTS.md` over time.

```md
# ERRORS

## Format
- YYYY-MM-DD — what failed — what to do next time

## Log
- (empty until something worth recording)
```

### `BOOTSTRAP.md`

Often created once at onboarding (“who am I?”). After Felix is configured, you can **delete** or replace with a one-liner:

```md
Bootstrap complete. See SOUL.md, AGENTS.md, USER.md.
```

---

## Secrets: workspace vs `~/.openclaw/.env`

| Store here | Do **not** store here |
|------------|------------------------|
| `~/.openclaw/.env` — `DISCORD_BOT_TOKEN`, `SMTP_*`, `AGENT_EMAIL_PASSWORD`, API keys | `SOUL.md`, `AGENTS.md`, `USER.md`, Discord chat |
| `USER.md` — *that* you use Gmail webmail, Europe/Madrid, project names | Passwords, bot tokens, full `.env` paths with values |

See [../04-security/README.md](../04-security/README.md) and [../05-discord-channel/README.md](../05-discord-channel/README.md).

For browser/email experiments, reference **env var names** in `AGENTS.md` (e.g. `DLR_WEBSOLUTIONS_EMAIL_URL`, `AGENT_EMAIL`) — never the secret values.

---

## Discord channels vs workspace files

- **Workspace files** = who Felix **is** and how he **behaves** (same for all Discord channels that route to `main`).
- **Each Discord channel** = its own **conversation session** (separate history). `#dlr-main` and `#openclaw-alerts` do not share chat context.
- Channel IDs and routing: [../05-discord-channel/README.md](../05-discord-channel/README.md). Alerts channel example: `1505186587321831445` — configure delivery in cron / `message` tool, not in `SOUL.md`.

---

## Context limit exceeded

Long threads and browser snapshots fill the session. Mitigations:

1. Config: `agents.defaults.compaction.reserveTokensFloor` (≥ `20000`), `contextLimits.toolResultMaxChars`, optional `contextPruning` — patch examples were discussed in your setup; add to `openclaw.json` on the VPS.
2. In **AGENTS.md**: ask for `/new` on big tasks; split browser work across turns.
3. In Discord: `/new` or `/reset`, then a short ping message.

---

## Templates and multi-agent crew

Full **SOUL.md** / **AGENTS.md** copy for Felix, Marcus, Nyx, Byte: [../06-agents-teams/README.md](../06-agents-teams/README.md) (Step 5).

Prompts to generate or refine profiles: [../07-prompts/README.md](../07-prompts/README.md) (e.g. “Who Am I?” → paste into `USER.md`).

Memory plugins and `MEMORY.md`: [../02-memory/README.md](../02-memory/README.md).

---

## Quick checklist (Felix only today)

- [ ] Copy [workspace/](workspace/) to `~/.openclaw/workspace/` on the VPS
- [ ] Rename `memory/YYYY-MM-DD.example.md` to today's date (or create `memory/YYYY-MM-DD.md`)
- [ ] `SOUL.md`, `AGENTS.md`, `USER.md`, `IDENTITY.md`, `MEMORY.md` — review and customize
- [ ] Secrets only in `~/.openclaw/.env` (`chmod 600`)
- [ ] After edits: no gateway restart required for markdown; restart only if you changed `openclaw.json`

---

## Next

- [../06-agents-teams/README.md](../06-agents-teams/README.md) — four agents, Discord bots, config patch
- [../05-discord-channel/README.md](../05-discord-channel/README.md) — pairing, guild channels
- [../02-memory/README.md](../02-memory/README.md) — memory search + dreaming
