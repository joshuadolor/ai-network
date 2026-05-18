# Tina Huang — OpenClaw prompts (reference)

Source: [OpenClaw Prompts (Google Doc)](https://docs.google.com/document/d/1cJPzi3j0WioG-PzTZ5eQR7HxzEETLlr2zHRtYvIsUq0/edit) · Video: [My FULL OpenClaw Setup](https://www.youtube.com/watch?v=oOCN30ulVyo)

Full verbatim export: `prompts-export.txt` (from doc export). **Felix/Ollama/VPS** paste versions: [`FELIX-PASTE-PROMPTS.md`](FELIX-PASTE-PROMPTS.md).

## Prompt index

| Section | Use | Where |
|---------|-----|--------|
| Hardware Selector | Pick laptop / Mac Mini / VPS | Paste → ChatGPT/Claude → apply verdict |
| OpenClaw Setup Wizard | Cheat sheet for `openclaw onboard` | Paste → chatbot before onboard |
| About Me | Seed `USER.md` / identity | Paste → chatbot → paste answers to Felix |
| Mission Control Builder | Custom Next.js dashboard | Paste → chatbot (+ screenshots) → Felix/Cursor |
| Project Brief | First real automation project | Paste → chatbot → Felix |
| Multi Agent Framework | Design specialist crew | **Paste directly to Felix** — see FELIX file |
| Note Taking (memory) | Aggressive logging in SOUL/AGENTS | **Paste directly to Felix** |
| Karpathy LLM Wiki | Searchable memory wiki | **Paste directly to Felix** |
| Security Audit | Daily audit → alerts channel | **Paste directly to Felix** — see FELIX file |

## Not in the Google Doc (video only)

- Discord channel layout prompt (she says “in description” — may be email-gated variant only)
- “Proactive daily build” wake-up prompt
- Model-by-RAM chooser (separate chatbot prompt)
- Skills picker (referenced inside Setup Wizard Q6)

## Your stack vs Tina’s doc

| Tina (doc default) | Felix (you) |
|--------------------|-------------|
| Claude Opus/Sonnet API | Ollama `qwen2.5:7b` / `32b` / `72b` on KUBB |
| Mac 16GB + local 8B | VPS + Tailscale to 128GB OCTO |
| Agent name Inky | Felix (`@Osh_Felix`) |
| Telegram first | Discord |

Use [`FELIX-PASTE-PROMPTS.md`](FELIX-PASTE-PROMPTS.md) instead of raw doc text for multi-agent, security, and memory.
