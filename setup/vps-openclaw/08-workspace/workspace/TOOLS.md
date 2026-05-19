# Tools

- Chat / reasoning: local Ollama via gateway config (7b/32b routine; 72b / `heavy` when needed).
- Web search: DuckDuckGo (config) — pair with skill **deep-research** for multi-step briefs.
- Skills catalog: repo `setup/vps-openclaw/skills/README.md` (synced to `workspace/skills/`). **Read SKILL.md before acting.**
- **lead-site-pipeline** — leads without websites → HTML site → ngrok preview (trial).
- **cn-html-design** — 高颜值 landing HTML; install ClawHub `steipete/frontend-design` on VPS when possible.
- **site-preview-ngrok** — `site_preview.py --dir …/site`; needs `NGROK_AUTHTOKEN`.
- **deep-research** — multi-query synthesis; save to `workspace/docs/research-*.md`.
- **local-image-gen** — `python3 {baseDir}/scripts/comfyui_health.py`; needs `COMFYUI_BASE_URL`.
- **crypto-watch** — `python3 {baseDir}/scripts/watch.py`; read-only; optional `CRYPTO_WATCH_SYMBOLS`.
- **ui-ux-review** — structured UX critique; browser for URLs.
- **proactive-ops** — cron + heartbeat discipline; see HEARTBEAT.md.
- **hostinger-email** — `python3 {baseDir}/scripts/mail.py list|send` via `exec`.
- Browser: `browser` tool, profile `openclaw` (headless on VPS); email fallback; UX reviews.
- Memory: `memory_search`, `memory_get`; files under `memory/` and MEMORY.md.
- Scheduling: `openclaw cron add|list|trigger|runs` — never rely on chat alone for recurring work.
- Outbound Discord: `message` tool when posting to a specific channel.
- Secrets: process environment on gateway — not files in this workspace.
