# Felix workspace (adapted from javiConsu/felix-workspace)

Source: [github.com/javiConsu/felix-workspace](https://github.com/javiConsu/felix-workspace) · [ClawLodge pack](https://clawlodge.com/lobsters/javiconsu-felix-workspace)

This folder is a **trimmed DLR + local-Ollama** version. We kept CEO tone, production lock, cron discipline, and heartbeat checks. We dropped Paperclip `ROADMAP.md` / `TEAM.md` machinery, Spanish issue protocols, and `javi.md` persona overrides.

**Canonical copies for the VPS** live in [`../../08-workspace/workspace/`](../../08-workspace/workspace/) — sync those with:

```bash
bash setup/vps-openclaw/scripts/sync-openclaw-from-repo.sh /path/to/AINetwork
```

Gateway config: [`../../openclaw.json.example`](../../openclaw.json.example)

## What we took from javi's Felix

| Idea | In your stack |
|------|----------------|
| CEO voice + ownership | `SOUL.md` |
| Production lock (no external without approval) | `AGENTS.md` Red lines |
| Cron must be real (`openclaw cron add`) | `AGENTS.md` + `CRON-EXAMPLES.md` |
| Try tools first, report errors | `SOUL.md` Boundaries |
| Morning brief structure | `CRON-EXAMPLES.md` daily job |
| Light heartbeat | `HEARTBEAT.md` |

## Files in this reference folder

| File | Purpose |
|------|---------|
| `SOUL.md` | Same content as workspace template (reference copy) |
| `AGENTS.md` | Same content as workspace template (reference copy) |
| `HEARTBEAT.md` | Same content as workspace template (reference copy) |
| `CRON-EXAMPLES.md` | Copy-paste `openclaw cron` commands for VPS |
