---
name: ralph-loop
description: Long-task progress loop — message Joshua on Discord at least every 5 minutes until done. Use for research, pipelines, multi-step builds. Pair with completion report in AGENTS.md.
user-invocable: true
---

# Ralph loop (5-minute progress pings)

Joshua must **never** wait in silence on a long task. Inspired by the [Ralph Wiggum / Ralph loop](https://github.com/openclaw/skills/tree/main/skills/qlifebot-coder/ralph-loops) pattern: **iterate and report**, don’t disappear.

## When to start Ralph

Start when a task is **long** (same as AGENTS.md):

- 3+ tool rounds expected, browser session, **deep-research**, **lead-site-pipeline**, ComfyUI generate, or **>2 minutes** wall time.

## Mandatory flow

### 1. Start (exec)

    python3 {baseDir}/scripts/ralph_status.py start "Short task title"

### 2. Tell Joshua immediately (Discord)

One **complete** message (not streaming fragments):

```
🔄 Ralph loop started: <title>
Updates every ~5 min until done.
```

### 3. During work — ping every 5 minutes

**Before or after each tool batch**, run:

    python3 {baseDir}/scripts/ralph_status.py should-ping

If JSON shows `"should_ping": true`:

1. Post a **complete** Discord message to Joshua (same channel/thread as the task):

```
⏱ Ralph update (~5 min): <title>
• Done so far: <2–4 bullets>
• Now: <current step>
• Next: <what happens next>
• Blockers: <none or one line>
```

2. Record it:

    python3 {baseDir}/scripts/ralph_status.py record-ping "one-line summary of what you sent"

**Also ping early** if something important happens (error, blocker, surprise finding) — do not wait 5 minutes for bad news.

### 4. Finish

1. Post the **completion report** from AGENTS.md (`✅ Done: …`).
2. Clear state:

    python3 {baseDir}/scripts/ralph_status.py done

## Rules

- **Never** run 5+ tool calls in a row without checking `should-ping`.
- **Never** end a long task without a final `✅ Done` message.
- Pings are **short** — bullets only, no essays.
- Do **not** spam: at most one ping per 5 minutes unless Joshua asked or there is a blocker.
- Optional env: `RALPH_PING_INTERVAL_SEC` (default **300** = 5 minutes).

## Pair with

- **proactive-ops** — cron jobs use `--announce` (separate from Ralph)
- **deep-research**, **lead-site-pipeline**, **local-image-gen** — always wrap with Ralph when long

## Optional ClawHub

For full autonomous multi-iteration loops: `clawhub install qlifebot-coder/ralph-loops` (heavy; not required for 5-min pings).
