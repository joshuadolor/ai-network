#!/usr/bin/env bash
# Recreate Daily AI Summary cron with 7b + 300s timeout (fixes 72b timeout errors).
# Usage: CHANNEL_ID=123456789 bash recreate-daily-ai-cron.sh [old-job-id]

set -euo pipefail

CHANNEL_ID="${CHANNEL_ID:-1505186587321831445}"
OLD_JOB="${1:-0a2f7e5e-664e-4178-97e1-24811b48bdea}"

set -a
# shellcheck source=/dev/null
[[ -f "${HOME}/.openclaw/.env" ]] && source "${HOME}/.openclaw/.env"
set +a

if openclaw cron list 2>/dev/null | grep -q "$OLD_JOB"; then
  echo "Removing old job $OLD_JOB"
  openclaw cron remove "$OLD_JOB" || true
fi

echo "Creating Daily AI Summary → channel:$CHANNEL_ID"
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
  --to "channel:${CHANNEL_ID}"

echo ""
openclaw cron list
echo ""
echo "Trigger test: openclaw cron trigger <new-job-id>"
