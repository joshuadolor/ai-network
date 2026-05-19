# AINetwork project — where to look when something is missing

Joshua’s infra and Felix setup live in the **AINetwork** git repo on this VPS. **Do not guess** URLs, commands, or file paths — search here first.

## Repo root (on OpenClaw VPS)

```text
~/AINetwork/                    # git clone — source of truth for setup docs & skills
~/.openclaw/workspace/          # your live workspace (SOUL, AGENTS, docs, skills copy)
~/.openclaw/openclaw.json       # gateway config (merge from repo example)
~/.openclaw/.env                # secrets — scripts may load; never paste in Discord
```

If `~/AINetwork` is missing: tell Joshua to `git clone` the repo on the VPS.

## Lookup order (when lost)

1. **`workspace/docs/PROJECT-LOOKUP.md`** (this file)
2. **`workspace/skills/<name>/SKILL.md`** — task-specific procedures
3. **`workspace/reference/`** — cron examples, lead-site trial, Tina prompts
4. **`workspace/docs/`** — research, leads, images, comfyui-workflow
5. **`memory_search`** + `MEMORY.md` + `memory/YYYY-MM-DD.md`
6. **`~/AINetwork/setup/`** — full tree (grep/find below)
7. Web search — only after the repo has no answer

## Search the repo (exec)

```bash
# Keyword in setup + skills
grep -ri "KEYWORD" ~/AINetwork/setup --include="*.md" | head -40

# Find a filename
find ~/AINetwork -iname "*comfy*" -o -iname "*cron*" 2>/dev/null | head -30

# OpenClaw VPS docs only
ls -la ~/AINetwork/setup/vps-openclaw/
```

Replace `KEYWORD` with: `comfyui`, `ngrok`, `cron`, `discord`, `ollama`, `lead-site`, `email`, etc.

## What lives where (quick map)

| Topic | Repo path |
|-------|-----------|
| **Felix workspace templates** | `setup/vps-openclaw/08-workspace/workspace/` |
| **Skills (source)** | `setup/vps-openclaw/skills/` |
| **Apply repo → live** | `setup/vps-openclaw/scripts/update-vps-openclaw.sh` |
| **Gateway config example** | `setup/vps-openclaw/openclaw.json.example` |
| **Env template** | `setup/vps-openclaw/.env.example` |
| **ComfyUI + KUBB** | `setup/ai-server/05-comfyui/` |
| **Ollama on KUBB** | `setup/ai-server/03-ollama/` |
| **Open WebUI (apps VPS)** | `setup/vps-apps/02-open-webui/` |
| **Tailscale** | `setup/network-tailscale/` |
| **Lead → site trial** | `setup/vps-openclaw/reference/lead-site-trial-workflow.md` |
| **Multi-agent team** | `setup/vps-openclaw/06-agents-teams/` |
| **Cron examples** | `setup/vps-openclaw/reference/javiconsu-felix-adapted/CRON-EXAMPLES.md` |
| **Architecture overview** | `~/AINetwork/README.md` |
| **KUBB capabilities** | `~/AINetwork/AI-SERVER-CAPABILITIES.md` |

## Live workspace copies (after `update-vps-openclaw.sh`)

| Live path | Content |
|-----------|---------|
| `~/.openclaw/workspace/AGENTS.md` | Rules, skills-first, autonomy |
| `~/.openclaw/workspace/skills/` | Synced skills |
| `~/.openclaw/workspace/docs/` | Your artifacts + this lookup |
| `~/.openclaw/workspace/reference/` | Copied reference docs |

## Common “lost” fixes

| Problem | Check |
|---------|--------|
| ComfyUI URL wrong (localhost) | `docs/comfyui-workflow.md`, skill **local-image-gen**, `05-comfyui/README.md` |
| `comfyui-workflow-api.json` missing | `bash setup/vps-openclaw/scripts/install-comfyui-workflow.sh ~/AINetwork` |
| Cron not running | `CRON-EXAMPLES.md`, `scripts/recreate-daily-ai-cron.sh` |
| Discord / token | `05-discord-channel/README.md`, `.env` (do not leak) |
| Ollama IP / model | `openclaw.json` `models.providers.ollama`, `03-ollama/README.md` |
| ngrok preview | skill **site-preview-ngrok**, `lead-site-trial-workflow.md` |
| No updates on long task | skill **ralph-loop** — ping every 5 min |
| Email | skill **hostinger-email** |

## If still not found

Tell Joshua exactly what you searched (paths + keywords) and what was missing. Propose adding a doc or skill under `setup/vps-openclaw/` in the repo — do not invent a permanent workaround.
