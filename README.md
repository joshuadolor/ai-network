# 🧠 PRIVATE AI SERVER (KUBB OCTO + VPS + TAILSCALE)

## 🎯 GOAL

Build a private ChatGPT-like system with:

* 💬 70B chat model
* 🧑‍💻 coding assistant (Cursor alternative)
* 📄 OCR (GLM local)
* 🖼 image generation
* 🎬 basic video generation
* 👥 users (you + wife)
* 🔒 fully private via Tailscale

---

# 🧱 ARCHITECTURE

```text
Browser (you / wife)              Discord (you)
        │                              │
        ▼                              ▼
  VPS — apps              VPS — OpenClaw (cats)
  (Open WebUI)            Felix 🐈  Marcus 😼
        │                 Nyx  🐈‍⬛  Byte   🐾
        │                              │
        └──────► Tailscale Network ◄───┘
                       │
                       ▼
        KUBB OCTO AI (Ollama + models)
        — qwen2.5:72b, deepseek-coder:33b,
          nomic-embed-text, glm4 —
```

**One channel only:** every agent talks to you on **Discord**. No Telegram / WhatsApp / Slack / iMessage / Signal in this stack. **One AI provider only:** every agent uses **local Ollama** on the KUBB OCTO. No Anthropic / OpenAI / Gemini / xAI / OpenRouter / MiniMax / paid cloud AI.

**What else can you do with the KUBB OCTO?** → [AI-SERVER-CAPABILITIES.md](AI-SERVER-CAPABILITIES.md)  
**Step-by-step setup:** [setup/README.md](setup/README.md) — split by machine: **[setup/ai-server/](setup/ai-server/README.md)** (KUBB / Ollama), **[setup/vps-apps/](setup/vps-apps/README.md)** (Hostinger VPS #1 — Open WebUI), **[setup/vps-openclaw/](setup/vps-openclaw/README.md)** (Hostinger VPS #2 — OpenClaw only), **[setup/network-tailscale/](setup/network-tailscale/README.md)** (all machines).  
**Doc freshness:** [setup/DOCUMENTATION-SOURCES.md](setup/DOCUMENTATION-SOURCES.md) lists official links and **Context7 MCP** for staying aligned with upstream.  
You are installing **Ubuntu only** (Windows removed) on the KUBB; the **ai-server** folder matches that plan.

---

# 💻 PHASE 1 — AI SERVER (KUBB) SETUP

## 1. Install Ubuntu

Download:
Ubuntu 22.04 LTS

Flash USB with balenaEtcher
Install → “Erase disk and install Ubuntu”

---

## 2. Base system setup

sudo apt update && sudo apt upgrade -y

sudo apt install -y git curl htop build-essential

---

## 3. Install Docker

sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
sudo reboot

---

# 🧠 PHASE 2 — INSTALL AI ENGINE

## Install Ollama

curl -fsSL https://ollama.com/install.sh | sh

---

## Test

ollama run llama3

---

# 🧠 PHASE 3 — CORE MODELS (IMPORTANT)

## 💬 MAIN CHAT (70B)

ollama pull qwen2.5:72b

---

## ⚡ FAST MODEL

ollama pull qwen:7b

---

## 🧑‍💻 CODING ASSISTANT (Cursor replacement)

ollama pull deepseek-coder:33b

---

## 📄 EMBEDDINGS (RAG / memory)

ollama pull nomic-embed-text

---

## 🧠 OCR MODEL (YOU ALREADY HAVE)

GLM via Ollama:
ollama run glm4

Use for:

* screenshots
* document understanding
* OCR + reasoning

---

# 🖼 PHASE 4 — IMAGE GENERATION

Install:

pip install diffusers transformers accelerate

Use:

* Stable Diffusion XL (SDXL)

---

# 🎬 PHASE 5 — VIDEO GENERATION (LIMITED LOCAL)

Install:

pip install diffusers

Use:

* AnimateDiff (recommended)

Note:

* short clips only
* NOT Kling / SeedDance level (requires cloud GPUs)

---

# 🔐 PHASE 6 — TAILSCALE (SECURITY)

Install on BOTH machines:

curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

---

Get AI server IP:
tailscale ip

Example:
100.x.x.x

---

# 🌐 PHASE 7 — VPS UI (CHATGPT INTERFACE)

Install Open WebUI:

docker run -d 
-p 3000:8080 
-e OLLAMA_BASE_URL=http://100.x.x.x:11434 
-v open-webui:/app/backend/data 
--name open-webui 
ghcr.io/open-webui/open-webui:main

(REPLACE 100.x.x.x with KUBB Tailscale IP)

---

# 👥 PHASE 8 — USERS SETUP

Open:

http://YOUR-VPS-IP:3000

## First login = YOU (admin)

Then:
Admin Panel → Users → Add user (your wife)

---

# 🔒 PHASE 9 — SECURITY RULES

✔ Only access via Tailscale
✔ Do NOT expose Ollama publicly
✔ VPS only serves UI
✔ AI server stays private

---

# 🧠 PHASE 10 — HOW MODELS ARE USED

## 💬 Chat

* Qwen 72B

## ⚡ Fast replies

* Qwen 7B

## 🧑‍💻 Coding (Cursor alternative)

* DeepSeek Coder 33B

## 📄 OCR

* GLM (Ollama multimodal)

## 🖼 Images

* SDXL

## 🎬 Video

* AnimateDiff (basic local)

---

# ⚙️ PHASE 11 — BEST PRACTICES

## RAM usage

* keep under 80%
* never max 128GB fully

## Model strategy

* 70B = thinking
* 7B = speed
* coder = dev tasks

## Don’t do:

* run all models at once
* expose server to internet
* rely on single model for everything

---

# 🧠 FINAL SYSTEM RESULT

You now have:

✔ Private ChatGPT
✔ Multi-user system (you + wife)
✔ 70B reasoning model
✔ Coding assistant (Cursor replacement)
✔ OCR + vision system
✔ Image generation
✔ Basic video generation
✔ Fully private via Tailscale

---

# 🚀 FUTURE UPGRADES

* multi-model routing (auto-switch 70B / 7B)
* agent system (OpenClaw) — dedicated Hostinger VPS guide: [setup/vps-openclaw/README.md](setup/vps-openclaw/README.md)
* RAG memory system
* automation workflows (your SaaS ideas)

---

END.
