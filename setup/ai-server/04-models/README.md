# AI server — Model pulls

## Upstream reference

Model names and sizes change — browse [ollama.com/library](https://ollama.com/library) (the CLI has `pull` / `list`, not a built-in search). Doc index: [docs.ollama.com/llms.txt](https://docs.ollama.com/llms.txt).

## Strategy

- **Do not** pull everything at once if disk or RAM is tight; **one large pull at a time**.
- You have **1 TB SSD** — 72B + 33B + smaller models fits, but watch free space (`df -h`).

## Order suggested

1. Small test model (already done when you tested Ollama) — proves Ollama works.
2. **Fast chat:** `qwen2.5:7b` (aligns with family used for 72B).
3. **Embeddings:** `nomic-embed-text` (small).
4. **Coding:** `deepseek-coder:33b` (large).
5. **Main chat:** `qwen2.5:72b` (largest — do when GPU/RAM path is stable).
6. **Vision / documents:** pull a **multimodal** GLM tag Ollama documents for your use case — verify with `ollama show <tag>` or model card that it supports **images**.

## Commands (copy one at a time)

```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
ollama pull deepseek-coder:33b
ollama pull qwen2.5:72b
```

GLM (only after you confirm the correct **vision** tag on [ollama.com](https://ollama.com)):

```bash
# Example — replace with the exact tag you choose:
# ollama pull glm4:xxx
```

## VRAM / RAM note

72B quantized still needs **many GB** of memory at runtime. With **128 GB** unified system RAM you can run it **if** you are not also loading 33B + 72B simultaneously. Use `ollama ps` and unload models when switching (`/bye` in CLI or stop the runner).

## Verification

- [ ] `ollama list` shows pulled models.
- [ ] `ollama run qwen2.5:7b` responds.
- [ ] Optional: `ollama run qwen2.5:72b` responds (may be slow until GPU path is good).

## Next

Optional creative stack: [../05-image-video/README.md](../05-image-video/README.md)  
Tailscale (both machines): [../../network-tailscale/README.md](../../network-tailscale/README.md)
