# Felix (`main`) workspace templates

Copy this folder to the OpenClaw VPS as Felix's workspace:

```bash
# From your laptop (repo root), adjust host and user:
rsync -avz setup/vps-openclaw/08-workspace/workspace/ \
  deploy@YOUR_VPS:/home/deploy/.openclaw/workspace/

# Or on the VPS after cloning the repo:
cp -r /path/to/AINetwork/setup/vps-openclaw/08-workspace/workspace/* \
  ~/.openclaw/workspace/
chmod 700 ~/.openclaw/workspace
chmod 600 ~/.openclaw/workspace/*.md
```

Remove `memory/YYYY-MM-DD.example.md` after copying, or rename it to today's date.

**Do not commit secrets** into these files. Tokens and passwords belong in `~/.openclaw/.env` on the VPS only.

Other agents (Marcus, Nyx, Byte): duplicate this structure under `workspace-stoic-social/`, etc., and replace SOUL/AGENTS from [../../06-agents-teams/README.md](../../06-agents-teams/README.md) Step 5.
