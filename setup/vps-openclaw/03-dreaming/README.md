# OpenClaw — dreaming (background memory consolidation)

[Dreaming](https://docs.openclaw.ai/concepts/dreaming) is OpenClaw's background **memory consolidation** sweep (light → REM → deep). Only the **deep** phase writes durable items into `MEMORY.md`, and only after passing **score / recall-frequency / query-diversity** thresholds — so it stays high-signal.

## Defaults

- **Disabled** by default.
- When enabled, runs daily at `0 3 * * *`.
- Promotion preview: `openclaw memory promote` (dry-run) → `--apply` to commit.

## Enable

In your gateway config (Option B exposes a config field in hPanel; Option C — edit the gateway config file you onboarded with):

```json5
{
  plugins: {
    entries: {
      "memory-core": {
        config: {
          dreaming: {
            enabled: true,
            timezone: "Europe/Madrid",
            frequency: "0 3 * * *"
          }
        }
      }
    }
  }
}
```

Restart the gateway:

- **Option B (Hostinger Docker Manager):** click **Restart**.
- **Option C (plain Ubuntu):** `openclaw gateway restart` (or `systemctl --user restart openclaw-gateway.service`).

## Slash commands (in your channel)

```
/dreaming status
/dreaming on
/dreaming off
/dreaming help
```

## CLI workflow

```bash
openclaw memory promote                     # preview promotions
openclaw memory promote --apply             # commit promotions to MEMORY.md
openclaw memory promote-explain "vlan tag"  # why a candidate would or would not promote
openclaw memory rem-harness                 # preview REM reflections without writing
openclaw memory status --deep
```

## Outputs you will see

- `MEMORY.md` — only durable, promoted items (deep phase).
- `DREAMS.md` — Dream Diary entries + per-phase summaries (human review).
- `memory/.dreams/` — machine state (recall store, phase signals, checkpoints).

## Tuning

- Tighter cadence on a sleepy box: `frequency: "0 4 */2 * *"` (every 2 days) — or only run `openclaw memory promote --apply` manually.
- Specific local model for the Dream Diary subagent:

```json5
{
  plugins: {
    entries: {
      "memory-core": {
        subagent: { allowModelOverride: true },
        config: {
          dreaming: {
            enabled: true,
            model: "ollama/qwen2.5:7b"
          }
        }
      }
    }
  }
}
```

## Backfill / rollback

```bash
openclaw memory rem-backfill --path ./memory --stage-short-term   # replay history into the dreaming store
openclaw memory rem-backfill --rollback                           # undo backfill artifacts
openclaw memory rem-backfill --rollback-short-term
```

## Next

[../04-security/README.md](../04-security/README.md)
