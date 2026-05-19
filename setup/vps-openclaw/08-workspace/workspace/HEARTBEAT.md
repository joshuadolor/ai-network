# Heartbeat

- If nothing needs attention, reply **HEARTBEAT_OK** (or stay silent per config).
- Check: gateway healthy, Ollama reachable from VPS (`openclaw` → KUBB), Discord connected.
- Check `openclaw cron list` for any job with last status **error** — surface job name and suggest fix (usually 7b + longer timeout).
- Do not spam Joshua; only surface real blockers.
- If `workspace/.ralph-loop/active.json` exists, run `ralph_status.py status` — if a long task is stale (>30 min, no recent ping), one line nudge in daily note only (do not DM unless cron error rules apply).

Optional log to today's daily note:

`[HH:MM] HEARTBEAT: ok` or `[HH:MM] HEARTBEAT: cron error on <job-name>`
