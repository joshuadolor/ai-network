# Tools

- Chat / reasoning: local Ollama via gateway config (7b/32b routine; 72b when needed).
- Web search: DuckDuckGo (config) — prefer for research and daily briefs.
- Email: skill **hostinger-email** → `python3 {baseDir}/scripts/mail.py list|send` via `exec`.
- Browser: `browser` tool, profile `openclaw` (headless on VPS); email fallback only.
- Memory: `memory_search`, `memory_get`; files under `memory/` and MEMORY.md.
- Scheduling: `openclaw cron add|list|trigger|runs` — never rely on chat alone for recurring work.
- Outbound Discord: `message` tool when posting to a specific channel.
- Secrets: process environment on gateway — not files in this workspace.
