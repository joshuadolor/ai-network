# Felix — adapted from Tina Huang’s “paste to OpenClaw” prompts

Use these on Discord or the gateway UI. Do **not** paste the doc’s Claude Opus / MiniMax defaults — your stack is Ollama on KUBB + VPS gateway.

Alerts channel (example): `1505186587321831445` — change if yours differs.

---

## Multi-agent crew (adapted)

```
Design and build a multi-agent crew for DLR Web Solutions.

You already know me from MEMORY.md, USER.md, daily memory files, and this workspace.

Stack constraints:
- Primary LLM: Ollama over Tailscale (KUBB). Models: qwen2.5:7b (cron/light), 32b (routine chat), 72b (hard reasoning only).
- Channel: Discord only. Joshua user id 1499833210237096007.
- Do not assume Claude Opus, OpenAI API, or Telegram unless Joshua adds them.

Steps:
1. Audit the workspace. Summarize what you found.
2. Ask only what you cannot infer (max 3–5 questions, one at a time).
3. Propose 3–7 specialists. For each: name, role, model tier (7b / 32b / 72b), cron vs on-demand, Discord channel for output.
4. Estimate load (not API $): which jobs must be 7b + 300s timeout to avoid cron failures.
5. Wait for Joshua’s approval.
6. Build ONE agent end-to-end, prove with openclaw cron trigger or a test message, then stop.
7. Repeat for the next agent only after approval.

Principles: 7b for scheduled scans and briefs; 32b for interactive work; 72b sparingly. Privacy-sensitive tasks stay on Ollama. Coordinate via workspace files and cron — no chat-only “I’ll do that every morning.”

Start with the audit. No code yet.
```

---

## Memory — aggressive notetaker (from doc; aligns with workspace)

```
Update SOUL.md and AGENTS.md so obsessive documentation is part of your identity:
- Log everything material you do to memory/YYYY-MM-DD.md.
- Save every report, brief, or artifact you produce under workspace docs/ (or memory) so it can be revisited.
- After /new or compaction, use memory_search before claiming you forgot something Joshua already told you.
- When Joshua corrects you, write the correction to memory the same session.
Do not remove production-lock or cron-mandatory rules already in AGENTS.md.
```

---

## Karpathy memory wiki (adapted)

```
Create an implementation plan for a Karpathy-style LLM wiki memory system for this workspace:
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Requirements:
- Works with existing MEMORY.md and memory/YYYY-MM-DD.md (no mock data).
- Searchable from Discord tasks (memory_search / files).
- Phased: plan first, Joshua approves, then build minimal v1 on VPS (no new paid APIs).
- Prefer filesystem + markdown over heavy new dependencies.
```

---

## Security audit (adapted)

```
Run a security review based on https://docs.openclaw.ai/gateway/security

Agent: Felix. Deployment: OpenClaw on VPS, Ollama on private Tailscale host, Discord bot.

Tasks:
1. Run openclaw security audit (or equivalent checks in the docs). Summarize critical/high findings.
2. Propose fixes; do not apply destructive changes without Joshua’s approval.
3. Add or update a cron job to run this audit daily at 23:00 Europe/Madrid, model ollama/qwen2.5:7b, timeout 300, deliver summary to Discord channel:1505186587321831445
4. Confirm cron with openclaw cron list and one openclaw cron trigger test.

Never paste secrets, .env contents, or gateway tokens into Discord.
```

---

## Project brief — Daily AI digest (Joshua-shaped, no chatbot step)

If you skip Tina’s 4-question chatbot flow, paste this to Felix:

```
Project: Daily AI news brief for Joshua

Intent: Every weekday 9:00 Europe/Madrid, web search + 5–8 bullets of notable AI news. Post to Discord alerts channel (not DM).

Constraints: ollama/qwen2.5:7b, --session isolated, --timeout-seconds 300, persisted openclaw cron only.

Process:
1. openclaw cron add with the above
2. openclaw cron trigger once
3. Reply with job id, cron expr, and openclaw cron runs status

Do not promise scheduling in chat without creating the cron job.
```

See also: `../javiconsu-felix-adapted/CRON-EXAMPLES.md`
