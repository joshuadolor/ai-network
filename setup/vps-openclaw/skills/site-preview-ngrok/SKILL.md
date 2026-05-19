---
name: site-preview-ngrok
description: Serve a static site folder locally and expose a temporary ngrok URL for Joshua to preview. Trial only — stop tunnel when done if Joshua asks.
user-invocable: true
---

# Site preview (ngrok)

## Environment

- `NGROK_AUTHTOKEN` — from https://dashboard.ngrok.com (free tier OK for trial)
- `ngrok` binary on PATH (`snap install ngrok` or official package)
- Site path: folder containing `index.html`

Never read `~/.openclaw/.env` in chat.

## Start preview (exec)

    python3 {baseDir}/scripts/site_preview.py --dir /path/to/workspace/docs/leads/<slug>/site --port 8765

Script prints JSON: `{"url":"https://....ngrok-free.app","port":8765,"pid":...}`

Share **url** with Joshua in the completion report.

## Stop preview (when Joshua says stop tunnel / done preview)

    python3 {baseDir}/scripts/site_preview.py --stop

## Rules

- **Trial only** — ngrok URLs are temporary; do not treat as production.
- One active preview per VPS is enough; `--stop` before starting another if port conflicts.
- Do not expose admin paths or `.env` — only the `site/` directory.
- If ngrok fails, report error and offer local path + `python3 -m http.server` instructions for Joshua on Tailscale (fallback).

## VPS setup (once)

```bash
# ngrok authtoken
ngrok config add-authtoken "$NGROK_AUTHTOKEN"
```

See repo: `setup/vps-openclaw/scripts/install-ngrok.sh`
