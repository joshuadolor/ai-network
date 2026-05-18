# OpenClaw prompt library — DLR Web Solutions LLC

A collection of ready-to-use prompts for setting up and running your OpenClaw crew.
All cat-themed. No octopus.

**How to use each prompt:**
- `→ paste to AI chatbot` — run in Claude / ChatGPT / Cursor chat first, use the output to fill in OpenClaw config
- `→ paste directly to openclaw` — send the prompt straight to your OpenClaw agent in Discord

---

## 1. Hardware Selector

> `→ paste to AI chatbot` — helps you pick the right always-on machine before you buy anything

```
I want help figuring out which hardware to use for running OpenClaw (a local AI
agent system that runs 24/7 and lets you build personal agents that talk to you
on Discord).

HARD RULES — never violate:
1. The host machine must be a DEDICATED, ALWAYS-ON machine, separate from my
   daily driver. A daily-driver MacBook, work laptop, or main desktop does NOT
   count, no matter how powerful.
2. For new purchases: 32GB RAM minimum, always. OpenClaw runs an agent loop with
   context windows, MCP servers, and long-running processes — 16GB ages badly
   and forecloses local models. Spare hardware with <32GB is fine to repurpose
   (don't waste what you own — it can still run a hybrid cloud + small local
   model setup).
3. Ask first, recommend second. Once you give a verdict, the question phase is
   over. No follow-up multiple-choice questions after recommending.
4. Don't push spending. If they have spare hardware that fits, that's the answer.
   If they don't, default to the cheapest viable option.

Ask questions ONE AT A TIME, wait for each answer. Use multiple choice. Don't
ask about budget if Q1 makes it irrelevant.

Q1 (always): Spare hardware. Do I have a SECOND machine I can leave running 24/7
as a dedicated agent host?
  A) Yes, <32GB RAM (fine for cloud APIs + small local models)
  B) Yes, 32GB+ RAM (works for mid-size local models too)
  C) Yes, a spare Apple Silicon Mac (unified memory punches above its weight)
  D) No

→ If A, B, or C: skip to Q4. Don't ask about budget. The answer is "use what
you have."
→ If D: continue to Q2.

Q2 (only if Q1 = D): Spending preference. Pay-as-you-go monthly, or one-time
hardware spend?
  A) Pay-as-you-go — $5–20/mo VPS, no commitment
  B) One-time spend — ~$800–1,400 for a 32GB Mac Mini
  C) Power user — $2,000–4,000+ for Mac Studio or DGX Spark
  D) Not sure — recommend based on the rest of my answers

Q3 (only if Q1 = D AND Q2 = A or D): Local vs. cloud.
  A) Cloud APIs are fine
  B) Local only (full privacy)
  C) Hybrid — local for sensitive, cloud for heavy lifting

Q4 (always): Technical comfort.
  A) Very comfortable — terminal is home turf
  B) Comfortable enough — can follow guides
  C) Simplest path — plug-and-play

RECOMMENDATION FORMAT:
1. One-line verdict ("Use your spare Mac. $0 upfront.")
2. 2–3 sentences max on why — tied to my specific answers.
3. If buying: include RAM tier (32GB+ minimum) and local-vs-cloud strategy.
4. One sentence acknowledging the alternative if there's a legitimate case.
5. End with an open question handing control back to me — not a new survey.

Be opinionated. Don't hedge.
```

---

## 2. Setup Wizard Cheat Sheet

> `→ paste to AI chatbot` — run before `openclaw onboard` to get a ready-made answer sheet for every wizard prompt

```
I'm about to run openclaw onboard to set up OpenClaw. Help me figure out the
right answer for each question the wizard asks.

Ask me 3–5 questions, ONE AT A TIME, then give me a complete cheat sheet in the
exact order the wizard asks them.

HARD CONSTRAINTS — do not violate:
1. The machine running OpenClaw must be a DEDICATED, ALWAYS-ON machine — not a
   daily-driver laptop that gets closed or restarted. Mention this once, move on.
2. Channel for talking to the agent: DISCORD ONLY. Do not suggest Telegram,
   WhatsApp, Slack, iMessage, or Signal. Discord is the only supported channel
   for this setup.
3. AI provider: LOCAL OLLAMA ONLY. The user runs their own AI server (KUBB OCTO,
   128 GB RAM) on their LAN/Tailscale. Do not suggest Anthropic, OpenAI, Codex,
   Gemini, xAI, MiniMax, OpenRouter, Kimi, or any paid cloud provider — even as
   a "start here, switch later" path. The user has explicitly opted out of paid
   cloud AI. If the wizard insists on a provider before Ollama is reachable,
   the user will skip onboarding model selection and configure Ollama manually
   afterwards via `openclaw config patch` (see setup/vps-openclaw/06-agents-teams).

Questions (one at a time):
1. Is your local Ollama server (KUBB OCTO) already reachable from this VPS?
   (Yes — I can curl http://AI_SERVER_TAILSCALE_IP:11434/api/tags / Not yet)
2. Which local model do you want as your primary?
   (qwen2.5:72b — best reasoning / qwen2.5:7b — fast / deepseek-coder:33b — code)
3. Discord bot: have you already created the bot and have the token ready?
   (Yes — token in hand / No — I'll create it after onboarding)
4. Web search: free DuckDuckGo for now, or Brave key (better quality)?
   (DuckDuckGo / Brave / Skip)
5. Any integrations you want on day one?
   (Apple Notes / Obsidian / 1Password / Notion / Voice / None)

CHEAT SHEET ORDER (wizard prompts in order):
1. Acknowledge personal-by-default → Yes.
2. QuickStart vs Advanced → ALWAYS QuickStart.
3. Model/auth provider → Ollama (local). If Q1 = Not yet, pick Ollama anyway
   and point baseUrl at http://AI_SERVER_TAILSCALE_IP:11434 (no /v1). Use the
   placeholder apiKey value "ollama-local" — local/LAN hosts don't need a
   real bearer token.
4. Filter models by provider → "Ollama only".
5. Default model → match Q2 (qwen2.5:72b / qwen2.5:7b / deepseek-coder:33b).
   If the wizard hasn't seen the model yet, pull it first on the AI server
   with `ollama pull <model>`.
6. API key → paste "ollama-local" (placeholder for local hosts).
7. Select channel → DISCORD. Skip every other channel option.
8. Discord credentials:
   - Q3 = Yes → paste the bot token now.
   - Q3 = No → pick "Skip for now"; you will wire Discord up afterwards via
     setup/vps-openclaw/05-discord-channel.
9. Web search → Q4 (DuckDuckGo / Brave / Skip).
10. Enable hooks → ON for session-memory AND command-logger. Skip boot-md and
    bootstrap-extra-files.
11. Missing skill dependencies → Q5. "None" = Skip for now; add later via
    `openclaw configure`.
12. Per-skill API keys → No to all on first run.
13. Shell completion → accept default. Run `source ~/.zshrc` after.
14. Daemon install → YES, ALWAYS YES. Without this the agent stops when the
    terminal closes.

End with: "Run openclaw onboard now and follow this list. If the wizard offers
any non-Discord channel or any non-Ollama model provider, skip / decline it.
If anything doesn't match your screen, paste the question back to me."

Be opinionated. Don't list options without picking one. Never recommend paid
cloud AI providers — the user runs everything on local Ollama.
```

---

## 3. About Me

> `→ paste to AI chatbot` — generates a rich self-description to paste into your OpenClaw agent's context

```
Give me a detailed description about me, my preferences, and my working style.
```

*(Simple by design — let the AI ask you questions and build your profile. Paste the result into OpenClaw with: "This is who I am. Update USER.md with this.")*

Save the result on the VPS at `~/.openclaw/workspace/USER.md` ([workspace file guide](../08-workspace/README.md)).

---

## 4. Mission Control Builder

> `→ paste to AI chatbot` — generates a project brief for building your own dashboard; paste the brief into OpenClaw (or Cursor/Claude Code) to build it

```
I want to build my own Mission Control dashboard for my OpenClaw agent — a
single web interface that lets me see and control everything my agent is doing.

Ask me 5 questions, ONE AT A TIME. After my answers, write a project brief I'll
paste to my OpenClaw agent (or to Claude Code / Cursor).

Mission Control is a Next.js app on localhost with up to 7 screens:
1. Tasks — backlog / in-progress / done. Agent picks up assigned tasks on heartbeat.
2. Calendar — every cron job and scheduled task. Proves the agent actually
   scheduled what it said it would.
3. Projects — every project with progress, linked tasks, memories, and docs.
4. Memory — journal-style view of daily memory files + long-term MEMORY.md.
   Searchable.
5. Docs — every doc the agent has written (content, briefs, reports). Indexed
   and searchable.
6. Team — agents, sub-agents, roles, org chart, mission statement.
7. Visual Office — 2D pixel-art office with CATS at their desks when working,
   away when idle. Each agent is a cat with its own look.

The 5 questions:
1. Which screens matter most right now? Pick top 3–5 to build first.
2. What does my agent crew look like? How many agents, names, roles, is there a
   chief-of-staff routing work?
3. What's my mission statement? One or two sentences. If unsure, ask 3
   follow-ups and synthesize one.
4. Visual style — dark UI with pixel-art cats, or something else? Describe or
   let the agent decide.
5. Which integrations on day one? Discord webhook / Obsidian / Google Calendar /
   GitHub / file watcher / none.

After my answers, write a project brief for the agent. Treat it as a brief for
a smart collaborator. Format:
- Project name (short, evocative)
- What we're building (3–5 sentences on intent)
- Why it matters (1–2 sentences on the human problem)
- Screens to build first (one sentence per screen — intent, not feature list)
- Agent crew + mission statement
- Visual direction: pixel-art cats in a dark office. Each cat has its own
  personality: Felix is the grey tabby CEO, Marcus is the stoic black cat,
  Nyx is the sleek shadow cat, Byte is the wide-eyed orange hacker cat.
  Leave the rest open to the agent's design judgment.
- Integrations
- REAL DATA from day one — no mock data. Pull from ~/.openclaw/workspace/,
  memory/YYYY-MM-DD.md, MEMORY.md, USER.md, AGENTS.md, openclaw.json.
  Discover what exists first, then build around it.
- Tech stack: Next.js (App Router) + Tailwind + shadcn/ui + SQLite or
  filesystem-only. Runs on localhost.
- What I'm NOT specifying: data model, component structure, visual treatment,
  file org, exact layouts — agent's call. Ask if genuinely ambiguous.
- Process: 1) explore workspace, report what data exists per screen.
  2) clarifying questions. 3) propose phased plan, wait for approval.
  4) build phase 1 wired to real data. 5) show me, iterate. 6) phase 2.

End with: "Paste this brief to your agent. First reply = workspace audit +
questions or plan. Not code."

Be opinionated. Don't offer a menu of stack options.
```

---

## 5. First Project Brief

> `→ paste to AI chatbot` — figures out what your agent should build first, then writes the brief

```
I want to figure out my first OpenClaw project — something my agent can start
building that will actually make my daily life better.

HARD CONSTRAINTS:
- The agent ALWAYS replies via DISCORD. Never propose a project where the
  agent posts to Telegram, WhatsApp, Slack, iMessage, or Signal as its reply
  channel. Reading from those is fine (e.g. WhatsApp triage), but the agent's
  output goes to Discord.
- The agent ALWAYS uses LOCAL OLLAMA on the KUBB OCTO. No paid AI providers.

Ask me 4 questions, ONE AT A TIME. After my answers:
1. Recommend ONE specific project with a clear reason why it fits my life.
2. Write a project brief I'll paste to my OpenClaw agent.

The 4 questions:
1. What's the most annoying recurring task or moment in my week right now?
   (Inbox chaos / WhatsApp pile-up / unprepared for meetings / money tracking /
   losing track of content comments / calendar chaos / something else)
2. What would I love to wake up to?
   (Overnight catch-up brief / clear "do this today" plan / inbox already triaged /
   something delightful / progress on a personal goal)
3. What data does my agent already have access to? (Pick all that apply —
   these are READ sources for the agent, not its reply channel. The agent
   always replies via DISCORD only.)
   (Email / Calendar / External messaging accounts I want triaged
   (WhatsApp / Telegram inboxes you want summarized, not the agent's own
   channel) / Financial accounts / Content platforms / Health-fitness /
   Notes-docs / None yet)
4. How ambitious should this first build be?
   (Small — one daily message / Medium — small dashboard or daily ritual /
   Large — full mini-app with multiple integrations)

9 proven starter shapes (suggest based on answers):
- Investor brief — overnight news on top 10 holdings, earnings/events in 7 days.
- WhatsApp triage — read unread, draft replies in my voice, group by urgency.
- Calendar defender — flag conflicts, unprepped meetings, suggest declines.
- Appointment scheduler — anyone asking to meet → 3 slot proposals + draft reply.
- Founder dashboard — yesterday vs. today on key metrics, one anomaly surfaced.
- Inbox executor — auto-archive newsletters, draft replies, flag what needs me.
- Budget pulse — spending trends 30/60/90 days, one habit worth changing.
- Comment radar — cluster comments on last 5 videos, surface one worth replying.
- Learning loop — daily language practice from yesterday's mistakes with audio.

Brief format:
- Project name (short, evocative)
- What it should do (2–4 sentences, intent not implementation)
- Why it matters to me (1–2 sentences on the human problem)
- Where it shows up (DISCORD — which Discord channel and roughly when. The
  agent always replies via Discord; format and exact timing are open)
- Data it draws on
- Build size (small / medium / large)
- Constraints (zero AI inference cost — runs on local Ollama; runs
  autonomously; internal only; replies via Discord)
- What I'm NOT specifying (format, schedule, edge cases, visual treatment —
  agent's call; ask about anything genuinely ambiguous)
- Process: 1) clarifying questions, 2) propose plan + approval, 3) build,
  4) test before scheduling, 5) log to memory.

End with: "Paste the brief to your OpenClaw agent. First reply = questions or
plan, not code."

Be opinionated. Pick ONE and own the call.
```

---

## 6. Multi-Agent Crew Builder

> `→ paste directly to openclaw` — your agent audits your workspace and proposes a full crew design

```
Design and build a multi-agent crew.

You already know me — my work, projects, recurring patterns, and what's
automated. Use what's in MEMORY.md, USER.md, daily memory files, and the
workspace.

HARD CONSTRAINTS:
- Channel: DISCORD ONLY. Every agent talks to me through Discord. Do not
  propose Telegram, WhatsApp, Slack, iMessage, or Signal. Each agent gets its
  own Discord bot account (separate Developer Portal application + token).
- Models: LOCAL OLLAMA ONLY on my KUBB OCTO AI server, reached over Tailscale
  at http://<AI_SERVER_TAILSCALE_IP>:11434 (no /v1). Do not propose any paid
  cloud AI — no Anthropic, OpenAI, Codex, Gemini, xAI, MiniMax, OpenRouter,
  Kimi, etc. Cost estimate is $0/month for inference; the only running costs
  are the VPS itself and electricity for the AI server.

Steps:
1. Audit the workspace. Tell me what you found.
2. Ask me only what you can't figure out (likely hardware status, naming
   preferences, which Ollama models are pulled). Max 3–5 questions, one at a time.
3. Propose a crew of 3–7 specialists. For each: name, role, model tier
   (heavy / mid / light), specific Ollama model (e.g. qwen2.5:72b,
   deepseek-coder:33b, qwen2.5:7b, glm4, nomic-embed-text), cadence, and which
   tools they should have access to (read-only vs full exec). Confirm $0 cloud
   inference cost.
4. Wait for my approval.
5. Build ONE agent end-to-end. Prove it works against local Ollama and Discord.
   Then come back.
6. Repeat for the next.

Principles: match model to job difficulty (don't waste qwen2.5:72b on a daily
content draft when qwen2.5:7b will do). Coordinate through workspace files —
no exotic protocols.

Each agent gets a cat identity in SOUL.md — name, coat colour, personality
notes. Keep it subtle but consistent (shows up in tone, not in every sentence).

Start with the audit. No code yet.
```

---

## 7. Memory: Note-Taking Identity

> `→ paste directly to openclaw` — bakes obsessive documentation into your agent's identity

```
Update your SOUL.md and AGENTS.md so obsessive documentation is part of your
identity: log everything you do, and save every document, report, or artifact
you produce so it can be revisited later.
```

---

## 8. Memory: Karpathy LLM Wiki

> `→ paste directly to openclaw` — implements Karpathy's wiki-style memory improvement idea

```
Create an implementation plan of the Karpathy LLM Wiki idea to improve your
memory: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
```

---

## 9. Security Audit (daily)

> `→ paste directly to openclaw` — schedules a nightly security audit based on official docs

```
Use this to run a security audit based on this documentation:
https://docs.openclaw.ai/gateway/security

Run it at 11pm every day and report back to the #alerts channel.
```

---

## 10. Self-Improving Agent (install)

> Install the most-starred Clawhub skill to give each agent a persistent learning loop

```bash
# Install on the OpenClaw VPS — repeat for each agent workspace
clawhub install pskoett/self-improving-agent
```

Each agent workspace gets:

```
.learnings/
├── LEARNINGS.md        ← corrections, insights, patterns
├── ERRORS.md           ← auto-captured command failures
└── FEATURE_REQUESTS.md ← things the agent wished it could do
```

When an entry is flagged enough times, the agent **promotes** it into `AGENTS.md` permanently — the mistake cannot happen again next session. Workspace paths and file roles: [../08-workspace/README.md](../08-workspace/README.md). SOUL/AGENTS templates: [../06-agents-teams/README.md](../06-agents-teams/README.md).

---

## Quick reference — which prompt goes where

| # | Prompt | Where to run |
|---|--------|-------------|
| 1 | Hardware Selector | AI chatbot → pick your machine |
| 2 | Setup Wizard Cheat Sheet | AI chatbot → run before `openclaw onboard` |
| 3 | About Me | AI chatbot → paste result into OpenClaw |
| 4 | Mission Control Builder | AI chatbot → paste brief into agent / Cursor |
| 5 | First Project Brief | AI chatbot → paste brief into agent |
| 6 | Multi-Agent Crew Builder | Directly to OpenClaw |
| 7 | Memory: Note-Taking Identity | Directly to OpenClaw |
| 8 | Memory: Karpathy LLM Wiki | Directly to OpenClaw |
| 9 | Security Audit | Directly to OpenClaw |
| 10 | Self-Improving Agent | `clawhub install` on VPS |
