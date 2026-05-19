#!/usr/bin/env bash
# Install ~/.openclaw/comfyui-workflow-api.json from repo example if missing (or --force).
set -euo pipefail

REPO_ROOT="${HOME}/AINetwork"
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    -h|--help)
      echo "Usage: install-comfyui-workflow.sh [REPO_ROOT] [--force]"
      echo "  Installs comfyui-workflow-api.json to ~/.openclaw/"
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
    *)
      REPO_ROOT="$1"
      shift
      ;;
  esac
done

OC="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
SRC="$REPO_ROOT/setup/vps-openclaw/assets/comfyui-workflow-api.example.json"
DEST="$OC/comfyui-workflow-api.json"

if [[ ! -f "$SRC" ]]; then
  echo "Missing example workflow: $SRC" >&2
  exit 1
fi

mkdir -p "$OC"

if [[ -f "$DEST" && "$FORCE" -eq 0 ]]; then
  echo "Kept existing $DEST (use --force to overwrite from repo example)"
  exit 0
fi

cp "$SRC" "$DEST"
chmod 600 "$DEST"
echo "Installed $DEST"

if [[ -f "$OC/.env" ]]; then
  if ! grep -q '^COMFYUI_WORKFLOW_API=' "$OC/.env" 2>/dev/null; then
    echo "" >> "$OC/.env"
    echo "COMFYUI_WORKFLOW_API=$DEST" >> "$OC/.env"
    echo "Appended COMFYUI_WORKFLOW_API to $OC/.env"
  fi
else
  echo "Tip: run update-vps-openclaw.sh --env-init or add COMFYUI_WORKFLOW_API=$DEST to $OC/.env"
fi

echo ""
echo "Checkpoint in workflow (edit if generate fails on KUBB):"
python3 -c "import json; d=json.load(open('$DEST')); print(' ', d.get('4',{}).get('inputs',{}).get('ckpt_name','?'))"
