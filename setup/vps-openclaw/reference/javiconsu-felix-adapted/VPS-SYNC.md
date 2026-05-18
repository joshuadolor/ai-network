# VPS sync checklist (Felix + javi-adapted)

Run on the **OpenClaw VPS** as user `deploy` (paths assume `~/.openclaw`).

## 1. Pull repo (Mac → VPS however you usually deploy)

```bash
cd ~/AINetwork && git pull
```

## 2. One-command update (workspace MD, skill, reference, optional config)

```bash
cd ~/AINetwork && git pull

# Safe default: refresh SOUL/AGENTS/HEARTBEAT/TOOLS + email skill; backup first
bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork

# Full recommended pass (first time or after repo changes):
bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork \
  --config-merge --env-init --cron --restart
```

`sync-openclaw-from-repo.sh` is an alias for the same script.

**Dry run:** add `--dry-run` to preview changes.

**Files written:**

| VPS path | Source in repo |
|----------|----------------|
| `~/.openclaw/workspace/SOUL.md` | `08-workspace/workspace/SOUL.md` |
| `~/.openclaw/workspace/AGENTS.md` | `08-workspace/workspace/AGENTS.md` |
| `~/.openclaw/workspace/HEARTBEAT.md` | `08-workspace/workspace/HEARTBEAT.md` |
| `~/.openclaw/workspace/TOOLS.md` | `08-workspace/workspace/TOOLS.md` |
| `~/.openclaw/workspace/skills/hostinger-email/` | `skills/hostinger-email/` |

**Do not overwrite** (keep your data): `MEMORY.md`, `memory/YYYY-MM-DD.md`, `USER.md` unless you choose to merge manually.

## 3. Gateway config

Edit `~/.openclaw/openclaw.json` — merge from `setup/vps-openclaw/openclaw.json.example`:

- `agents.defaults.model.primary` → `ollama/qwen2.5:7b` with fallbacks 32b, 72b
- `agents.defaults.timeoutSeconds` → `600`
- compaction + contextPruning + contextLimits (already in example)
- `tools.alsoAllow` → includes `browser`
- `channels.discord.token` → env `DISCORD_BOT_TOKEN`
- `commands.ownerAllowFrom` → your Discord user id

**Keep** your existing `gateway.auth.token` (do not paste from example).

## 4. Secrets

```bash
nano ~/.openclaw/.env   # DISCORD_BOT_TOKEN, AGENT_EMAIL*, SMTP_*, IMAP_*
chmod 600 ~/.openclaw/.env
```

## 5. Fix Daily AI cron (7b + channel delivery)

```bash
CHANNEL_ID=1505186587321831445 bash ~/AINetwork/setup/vps-openclaw/scripts/recreate-daily-ai-cron.sh
openclaw cron run <new-job-id>
openclaw cron runs --id <new-job-id> --limit 10
openclaw cron runs --id <new-job-id>
```

## 6. Restart + fresh Discord session

```bash
set -a && source ~/.openclaw/.env && set +a
openclaw gateway restart
```

Discord: `/new`

## 7. Quick tests

```bash
curl -s -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" https://discord.com/api/v10/users/@me
openclaw cron list
python3 ~/.openclaw/workspace/skills/hostinger-email/scripts/mail.py list --limit 3
```
