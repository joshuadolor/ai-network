# Heartbeat

- If nothing needs attention, reply **HEARTBEAT_OK** (or stay silent per config).
- Check: gateway healthy, Ollama reachable from VPS (`openclaw` → KUBB), Discord connected.
- Check `openclaw cron list` for any job with last status **error** — surface job name and suggest fix (usually 7b + longer timeout).
- Do not spam Joshua; only surface real blockers.

Optional log to today's daily note:

`[HH:MM] HEARTBEAT: ok` or `[HH:MM] HEARTBEAT: cron error on <job-name>`
