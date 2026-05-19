# Lead → site trial workflow (Joshua)

Trial only: Felix finds businesses without websites, builds a draft landing page, sends you an **ngrok** link. You approve before any outreach or real hosting.

## One-time VPS setup

```bash
cd ~/AINetwork && git pull

# Skills + workspace
bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork --config-merge --restart

# Chinese-community HTML skill (free, ClawHub)
bash setup/vps-openclaw/scripts/install-clawhub-skills.sh

# ngrok
# Add NGROK_AUTHTOKEN=... to ~/.openclaw/.env (https://dashboard.ngrok.com)
bash setup/vps-openclaw/scripts/install-ngrok.sh
source ~/.openclaw/.env && ngrok config add-authtoken "$NGROK_AUTHTOKEN"
```

## Discord prompts

- `run lead site trial for <niche> in <city>` — full pipeline (3–5 leads default)
- `build site for lead <slug>` — phase 2–3 only
- `preview lead <slug>` — ngrok only
- `stop preview` — tears down tunnel

## Outputs on VPS

```
~/.openclaw/workspace/docs/leads/<slug>/
  lead.json
  research.md
  site/index.html
```

## Approval gates (later)

| Step | Now (trial) | After you say **approved** |
|------|-------------|----------------------------|
| Research leads | ✅ | ✅ |
| Draft HTML + ngrok | ✅ | ✅ |
| Email/call business | ❌ | your call |
| Hostinger / DNS live | ❌ | future step |

## Skills chain

`lead-site-pipeline` → `deep-research` → `ui-ux-build` + `cn-html-design` → `site-preview-ngrok`
