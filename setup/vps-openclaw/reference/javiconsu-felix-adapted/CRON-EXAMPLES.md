# Cron examples (run on OpenClaw VPS)

Timezone: `Europe/Madrid`. Replace channel id before running.

Get channel id: Discord → channel → right-click → Copy Channel ID.

## Daily AI summary (9:00) — use 7b, not 72b

```bash
set -a && source ~/.openclaw/.env && set +a

# Remove broken job if it still exists (optional)
openclaw cron list
# openclaw cron remove <old-job-id>

openclaw cron add \
  --name "Daily AI Summary" \
  --cron "0 9 * * *" \
  --tz "Europe/Madrid" \
  --session isolated \
  --message "Use web search. Summarize notable AI news from the last 24 hours in 5-8 bullets for Joshua. Be concise. No secrets." \
  --model "ollama/qwen2.5:7b" \
  --timeout-seconds 300 \
  --announce \
  --channel discord \
  --to "channel:1505186587321831445"

openclaw cron list
openclaw cron trigger <new-job-id>
openclaw cron runs --id <new-job-id>
```

Expect `status: ok`. If `error` and `model-call-started` timeout, confirm KUBB Ollama is up and the job uses **7b**.

## Memory dreaming (already in openclaw.json.example)

Plugin `memory-core` dreaming at `0 3 * * *` — separate from CLI cron. Check with `openclaw cron list`.

## Failure alerts

`openclaw.json` should include `cron.failureDestination` so failed jobs post to your alerts channel (see `openclaw.json.example`).
