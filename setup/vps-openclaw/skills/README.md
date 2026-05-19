# OpenClaw workspace skills (repo → VPS)

Bundled skills for Felix on the OpenClaw VPS. After `git pull` on the VPS:

```bash
bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork --restart
```

Enable in gateway config via `--config-merge` (see `openclaw.json.example` → `skills.entries`).

**Rule:** Felix must read `SKILL.md` and use skill scripts — not invent workflows (see `AGENTS.md` → Skills first).

| Skill | Use when | Needs env / infra |
|-------|----------|-------------------|
| [hostinger-email](hostinger-email/) | Inbox, draft, send (approved) | `AGENT_EMAIL`, SMTP/IMAP |
| [deep-research](deep-research/) | Research, briefs, **leads without websites** | Web search; optional `heavy` |
| [lead-site-pipeline](lead-site-pipeline/) | **Trial:** lead → HTML site → ngrok | Chain of skills below |
| [cn-html-design](cn-html-design/) | 高颜值 HTML landing pages | ClawHub `frontend-design` optional |
| [ui-ux-build](ui-ux-build/) | Build static site from lead pack | `workspace/docs/leads/` |
| [site-preview-ngrok](site-preview-ngrok/) | Share preview URL with Joshua | `NGROK_AUTHTOKEN`, `ngrok` binary |
| [ui-ux-review](ui-ux-review/) | UX critique on URLs | Browser |
| [local-image-gen](local-image-gen/) | ComfyUI health + generate | Scripts from [ai-server/05-image-video/local](../../ai-server/05-image-video/local/); `COMFYUI_BASE_URL` |
| [crypto-watch](crypto-watch/) | Read-only prices | Optional `CRYPTO_WATCH_SYMBOLS` |
| [goal](goal/) | `/goal` create/update/done/list workflow | `goal_tracker.py`; stores in `workspace/docs/goals/` |
| [proactive-ops](proactive-ops/) | Heartbeats, cron | Discord + cron |
| [ralph-loop](ralph-loop/) | **5-min progress pings** on long tasks | `ralph_status.py`; optional `RALPH_PING_INTERVAL_SEC` |

## ClawHub (free) — Chinese docs often recommend

```bash
bash setup/vps-openclaw/scripts/install-clawhub-skills.sh
```

| Install | Purpose |
|---------|---------|
| `steipete/frontend-design` | Production-grade HTML/CSS; avoid generic AI UI ([W3Cschool CN manual](https://m.w3cschool.cn/openclaw_skills_manual/clawhub-skills-steipete-frontend-design.html)) |
| `html-designer` | Alternative on [clawhub.ai](https://clawhub.ai/skills/html-designer) |

When **frontend-design** is installed, Felix follows it; **cn-html-design** is the bundled fallback.

## Lead → site trial (human doc)

[../reference/lead-site-trial-workflow.md](../reference/lead-site-trial-workflow.md)

## Adding a new repo skill

1. Create `skills/<name>/SKILL.md` (and optional `scripts/`).
2. Set `"<name>": { "enabled": true }` in `openclaw.json.example`.
3. Mention in `08-workspace/workspace/AGENTS.md` and `TOOLS.md`.
4. Sync script copies every folder under `skills/` automatically.
