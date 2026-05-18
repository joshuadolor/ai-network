# KUBB OCTO — what you can do with this machine (AI)

## Hardware snapshot

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen AI Max+ 395 (16 cores / 32 threads) |
| GPU (iGPU) | AMD Radeon 8060S — 40 compute units, RDNA 3.5 (gfx1151) |
| RAM / VRAM | **128 GB LPDDR5X** (unified — CPU + GPU share the same pool) |
| GPU-allocatable VRAM | Up to ~96 GB (AMD recommends setting dedicated graphics memory to 64 GB in BIOS) |
| Bandwidth | ~256 GB/s memory bandwidth |
| NPU | XDNA 2 — **50 TOPS** |
| Storage | 1 TB NVMe SSD |

---

## 1. Private LLM server (already in your plan)

Your architecture already covers this (Ollama + Open WebUI), but it is worth knowing how capable the hardware really is.

| Model size | Reality on your box |
|------------|---------------------|
| 7B – 14B (Q4) | ~70–108 tok/s generation — very comfortable for real-time chat |
| 33B (DeepSeek Coder, Q4) | Runs well; coding assistant use case |
| 72B (Qwen 2.5, Q4) | Fits in the 96 GB GPU allocation; 62–71 tok/s at **250 K token context** — rare on consumer hardware |
| 122B (Qwen 3.5) | Benchmarked at 62 tok/s even at 250 K context on Ryzen AI Max+ 395 |

The **large unified memory pool** is what sets this apart: most "AI PCs" have 32 GB. You can run a 70B model without swapping to CPU.

**What to try:**
- `qwen2.5:72b` — main reasoning model (already in your plan)
- `qwen3:30b-a3b` — Mixture of Experts (MoE), very fast and cheap on VRAM
- `llama3.3:70b` — strong open model, fits easily
- `deepseek-r1:70b` — strong reasoning / coding chain-of-thought

---

## 2. Local image generation (Stable Diffusion / FLUX)

The Radeon 8060S with ROCm runs image generation workloads well. AMD published a **3.9× advantage** over Apple M4 Pro MacBook on Stable Diffusion 3.5.

| Tool | What it does |
|------|--------------|
| **ComfyUI + ROCm** | Node-based image / video workflow. AMD ROCm 7.1.1 / 7.2 have an official ComfyUI integration with up to 5.4× perf improvement on Windows (Linux: see note). |
| **Stable Diffusion XL (SDXL)** | High-res image generation (~1 MP+) |
| **FLUX** | Newer architecture, excellent image quality; supported in ComfyUI on AMD |
| **IP-Adapter / ControlNet** | Pose / style / depth-guided generation inside ComfyUI |
| **AUTOMATIC1111 / Forge** | Alternative UI to ComfyUI |

> **Linux note (important for your plan):** the gfx1151 GPU is RDNA 3.5. It is not yet in the standard PyTorch ROCm wheels. When you install Ubuntu, verify GPU support status in the latest Ollama + ROCm bundle before investing heavily in custom PyTorch builds. The situation improves quickly — check [docs.ollama.com/linux](https://docs.ollama.com/linux) (AMD GPU / ROCm section) at install time.

**What to try:** [setup/ai-server/05-image-video/README.md](setup/ai-server/05-image-video/README.md) (already in your plan).

---

## 3. Local video generation

With ComfyUI + ROCm you can run video diffusion models locally:

| Model | Notes |
|-------|-------|
| **AnimateDiff** | Short clips (~4 s); good for animation loops |
| **FLUX video / CogVideoX** | Longer, higher quality; needs VRAM — your 96 GB pool helps |
| **LTX-Video** | Fast; optimized for RTX but AMD users have had success with ROCm |
| **Wan2.1 / HunyuanVideo** | Newer open-weights video models; community AMD workflows exist in ComfyUI |

> Realistic expectation: local video gen is **not** Kling / Sora quality, but for drafts, loops, and experiments it is more than good enough. Quality improves fast.

---

## 4. Speech-to-text (local Whisper)

Run **OpenAI Whisper** locally — no cloud, no data leaving the machine.

| What | How |
|------|-----|
| **faster-whisper** | CTranslate2-based, fast on CPU; check GPU path for AMD |
| **whisper.cpp** | Runs on CPU well; experimental ROCm path exists |
| **Whisper via Ollama** | If an Ollama-packaged Whisper model ships; check `ollama.com/library` |

Use cases: transcribe meetings, voice notes → text, podcast chapters, multilingual subtitles.

OpenClaw also has a **Nodes audio** feature ([docs.openclaw.ai/nodes/audio](https://docs.openclaw.ai/nodes/audio)) — voice input through your Discord bot.

---

## 5. Text-to-speech (local TTS)

| Tool | Quality |
|------|---------|
| **Kokoro TTS** | High quality, very fast on CPU; Apache 2.0 |
| **Coqui TTS / XTTS** | Voice cloning, multilingual |
| **Piper** | Fast, low latency, good for real-time voice assistants |
| **OuteTTS** | Runs fully locally; Ollama-packaged variants available |

Good pairing with your OpenClaw Discord bot — give your agent a voice.

---

## 6. NPU use cases (50 TOPS XDNA 2)

The NPU is separate from the GPU and is best used for the **prefill phase** of LLM inference (processing your input prompt). AMD's hybrid NPU + iGPU approach can push prefill speeds well past pure-GPU numbers.

| Use case | Notes |
|----------|-------|
| **LLM prefill acceleration** | AMD hybrid mode (NPU for prefill, GPU for generation) — configured through ROCm / Windows AI SDK |
| **Windows Copilot+ features** | NPU-targeted; mostly Windows-only for now |
| **On-device AI PC models** (Phi-3.5, Mistral 7B ONNX) | Optimized for XDNA 2 via ONNX Runtime / DirectML / WinML |

> On Linux, NPU access requires `amdxdna` driver support. Check status before counting on NPU workloads there.

---

## 7. Local embeddings server

Instead of paying per-token for embeddings (OpenAI, Voyage), serve them yourself. Already in your plan as `nomic-embed-text` for OpenClaw memory.

| Model | Dimensions | Good for |
|-------|-----------|---------|
| `nomic-embed-text` | 768 | Docs, chat history, RAG |
| `mxbai-embed-large` | 1024 | Better recall quality |
| `bge-m3` (BAAI) | 1024 | Multilingual, strong cross-lingual RAG |

All pullable through Ollama. Cost: zero per query.

---

## 8. RAG (Retrieval-Augmented Generation)

Combine the local LLM + local embeddings + a vector database to chat with your own documents.

| Component | Option |
|-----------|--------|
| Vector DB | **ChromaDB**, **Qdrant** (Docker), **LanceDB** (already in OpenClaw memory) |
| Orchestration | **Open WebUI** has built-in RAG ([docs.openwebui.com](https://docs.openwebui.com/features/rag/)), **LlamaIndex**, **LangChain** |
| Sources | PDFs, Markdown files, web pages, Notion exports, emails |

Use case: chat with your business docs, notes, code repos — privately.

---

## 9. Local coding assistant / Cursor alternative

Already in your plan as **DeepSeek Coder 33B** via Ollama. You can point any editor or tool at your Ollama endpoint:

| Tool | How to connect |
|------|----------------|
| **Cursor** | Use "Ollama" as a provider in settings → `http://localhost:11434` |
| **Continue.dev** (VS Code) | Local Ollama provider |
| **Aider** | `OPENAI_API_BASE=http://localhost:11434/v1` |
| **OpenHands / SWE-agent** | Self-hosted coding agent; Docker |

---

## 10. Local AI agent server

Beyond OpenClaw, you can run full agentic frameworks locally:

| Framework | What it does |
|-----------|--------------|
| **OpenClaw** (your plan) | Personal AI gateway, Discord, memory, skills |
| **n8n** (Docker, self-hosted) | Visual automation + AI nodes; connect to Ollama |
| **Flowise** | Low-code LLM workflow builder, local LLM support |
| **AutoGen / CrewAI** | Multi-agent Python frameworks |
| **OpenHands** | Fully autonomous coding agent (Docker) |
| **Dify** | Self-hosted LLMOps platform — RAG, agents, API |
| **AnythingLLM** | Desktop/server all-in-one: chat + RAG + agents |

---

## 11. Fine-tuning / LoRA training (light)

Your 128 GB unified pool makes small-model fine-tuning feasible without a datacenter GPU.

| What | Tool |
|------|------|
| LoRA fine-tune a 7B model | **Unsloth** (fastest), **LLaMA-Factory**, **axolotl** |
| Dataset preparation | Label Studio, Argilla (both Docker) |
| Merge & export to Ollama | `Modelfile` + `ollama create` |

Realistic: you can LoRA-train a 7B model on a custom dataset in a few hours on this machine.

---

## 12. Computer vision (local)

| Task | Tool / Model |
|------|-------------|
| Object detection | **YOLOv8 / YOLOv11** (Ultralytics) |
| Image classification | Any torchvision / timm model |
| OCR | **Tesseract**, **EasyOCR**, **PaddleOCR**, **GLM-4V** (already in your Ollama plan) |
| Face recognition | **InsightFace** |
| Video analysis | Frame extraction + vision model pipeline |

---

## 13. Self-hosted data / productivity tools with AI

Things you can run on this machine (or the apps VPS) that gain AI capabilities via your Ollama:

| App | AI angle |
|-----|---------|
| **Nextcloud** | AI Assistant plugin → your Ollama |
| **Joplin** | Note-taking with local AI summarisation |
| **Immich** | Photo library + AI face/object recognition |
| **Paperless-ngx** | Document inbox with OCR; pair with a local LLM classifier |
| **Notion-like: AppFlowy** | AI writing features pointing at Ollama |
| **Obsidian** | Markdown vault + local AI plugin (Smart Connections) |

---

## Hardware positioning summary

| What you can do locally | Verdict |
|-------------------------|---------|
| 70B chat model at 250 K context | ✅ Yes, comfortably |
| 33B coding assistant | ✅ Yes |
| SDXL / FLUX image generation | ✅ Yes (ROCm — verify Linux support at install time) |
| Short video generation | ✅ Yes (AnimateDiff+, ComfyUI) |
| Local Whisper transcription | ✅ Yes |
| Local TTS | ✅ Yes |
| Local embeddings | ✅ Yes |
| RAG over your documents | ✅ Yes |
| LoRA fine-tune a 7B | ✅ Yes |
| Large model training (30B+) | ⚠️ Not practical (fine-tune small models only) |
| 4K+ video generation (Kling quality) | ❌ Needs cloud GPU |

---

## What is already in your repo plan

| This doc | Where in repo |
|----------|---------------|
| Ollama + models | [setup/ai-server/03-ollama/](setup/ai-server/03-ollama/README.md) |
| Model pulls (72B, 33B, embeddings, GLM) | [setup/ai-server/04-models/](setup/ai-server/04-models/README.md) |
| SDXL / AnimateDiff (Python venv) | [setup/ai-server/05-image-video/](setup/ai-server/05-image-video/README.md) |
| OpenClaw memory + dreaming | [setup/vps-openclaw/02-memory/](setup/vps-openclaw/02-memory/README.md), [03-dreaming/](setup/vps-openclaw/03-dreaming/README.md) |
| Discord bot | [setup/vps-openclaw/05-discord-channel/](setup/vps-openclaw/05-discord-channel/README.md) |

Everything else in this document is **future expansion** — no action needed until you want it.
