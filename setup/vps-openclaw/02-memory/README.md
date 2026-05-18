# OpenClaw — memory (smart way to store memories)

## How OpenClaw stores memory

Plain **Markdown** in the agent workspace ([overview](https://docs.openclaw.ai/concepts/memory)). File locations on the VPS: [../08-workspace/README.md](../08-workspace/README.md).

| File | Role |
|------|------|
| `MEMORY.md` | Long-term, durable facts (loaded each DM session) |
| `memory/YYYY-MM-DD.md` | Daily notes / running context (today + yesterday auto-loaded) |
| `DREAMS.md` | Optional Dream Diary + sweep summaries (human review) |

The **active memory plugin** does the searching and capture. Pick **one**:

| Plugin | Best when | Notes |
|--------|-----------|------|
| **`memory-core`** (default builtin) | Zero extra deps; hybrid (BM25 + vector) search | SQLite per agent; auto-detects an embedding provider from configured keys. |
| **QMD** | You want **reranking**, query expansion, and to index folders **outside** the workspace (project docs, vault) | Local sidecar binary; falls back to builtin if unavailable. |
| **`memory-lancedb`** | You want a dedicated **local vector DB** with explicit `autoRecall` / `autoCapture` and Ollama embeddings | Bundled plugin; one active memory slot at a time. |
| **`memory-wiki`** | Durable knowledge as a maintained **wiki** (claims, evidence, freshness) | **Companion** plugin — runs *beside* the active memory plugin, not instead of it. |
| **Honcho** | Cross-session, multi-agent user modeling | Separate service / plugin install — see official doc. |

## Recommended for this stack

You already have **Ollama on the AI server** (KUBB) including **`nomic-embed-text`** ([../../ai-server/04-models/README.md](../../ai-server/04-models/README.md)). Reuse it for memory embeddings over Tailscale so memory stays **local** and **free**.

### Option 1 — Builtin (`memory-core`) + Ollama embeddings (simplest)

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "ollama"
      }
    }
  },
  models: {
    providers: {
      ollama: {
        baseUrl: "http://<AI_SERVER_TAILSCALE_IP>:11434"
      }
    }
  }
}
```

Hybrid (BM25 + vector) search out of the box.

### Option 2 — `memory-lancedb` (local vector DB) + Ollama embeddings

```json5
{
  plugins: {
    slots: { memory: "memory-lancedb" },
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          embedding: {
            provider: "ollama",
            baseUrl: "http://<AI_SERVER_TAILSCALE_IP>:11434",
            model: "nomic-embed-text",
            dimensions: 768
          },
          autoRecall: true,
          autoCapture: true,
          recallMaxChars: 400
        }
      }
    }
  }
}
```

> Set `dimensions` for any non-default embedding model. `nomic-embed-text` is **768**; `mxbai-embed-large` is **1024** ([memory-lancedb docs](https://docs.openclaw.ai/plugins/memory-lancedb)).

### Optional — add `memory-wiki`

Companion to either of the above; structured knowledge with claims/evidence/freshness ([Memory Wiki](https://docs.openclaw.ai/plugins/memory-wiki)).

## Verify

```bash
openclaw memory status
openclaw memory search "test"
# memory-lancedb only:
openclaw ltm stats
openclaw ltm search "test"
```

## Reference

[Memory configuration reference](https://docs.openclaw.ai/reference/memory-config) — every config knob.

## Next

[../03-dreaming/README.md](../03-dreaming/README.md)
