---
name: proactive-ops
description: Proactive checks, heartbeat discipline, and cron-backed briefings. Use when Joshua wants Felix to notice issues and follow up without being pinged every time.
user-invocable: true
---

# Proactive operations

## Philosophy

**Proactive** means persisted, scheduled, or heartbeat-driven work — not spam in Discord. Chat promises do not run recurring jobs; **cron** does.

## Heartbeat (read HEARTBEAT.md)

On heartbeat turns:

1. If nothing needs attention → `HEARTBEAT_OK` (or silent per config).
2. Check `openclaw cron list` for jobs with last status **error** — one concise alert to alerts channel rules in AGENTS.md (no secrets).
3. Optional: verify Ollama reachable (gateway already uses it; only report if tools failed recently).
4. Log one line to today's `memory/YYYY-MM-DD.md` when something notable happened.

Do not DM Joshua for routine OK.

## Suggested cron patterns (Europe/Madrid)

| Job | Schedule | Model | Message sketch |
|-----|----------|-------|----------------|
| Daily AI summary | `0 9 * * *` | 7b | Web search; 5–8 bullets AI news |
| Crypto watch | `0 8 * * *` | 7b | Run crypto-watch skill; table + disclaimer |
| Weekly research | `0 10 * * 1` | 7b | Top 3 topics from MEMORY.md / Joshua's list |

Always: `--session isolated`, `--timeout-seconds 300`, `--announce --channel discord --to "channel:ID"`.

Repo helper: `scripts/recreate-daily-ai-cron.sh` and `reference/javiconsu-felix-adapted/CRON-EXAMPLES.md`.

## When Joshua asks to "be more proactive"

1. List **2–4 concrete** recurring jobs (name, schedule, channel, model).
2. Create them with `openclaw cron add` and return **job ids**.
3. Run one test: `openclaw cron run <id>` and report `openclaw cron runs --id <id>`.

## Follow-ups (no cron)

After finishing multi-step work, add to daily note: **next action** + **owner** + **date** if Joshua should be nudged later. Do not fake reminders without cron or explicit ask.

## Completion reports

Any long proactive or cron job must end with Joshua-visible closure — use AGENTS.md **Long tasks — completion report** (✅ Done / Did / Result / Files / Needs you). Low-stakes cron work: proceed without pre-approval; still announce results.

## Pair with

- **deep-research** — scheduled digests
- **crypto-watch** — scheduled tables
- **hostinger-email** — only after approval for send
