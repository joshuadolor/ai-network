#!/usr/bin/env bash
# One-shot: health check + ComfyUI txt2img. Run on OpenClaw VPS via exec.
# Usage: bash {baseDir}/scripts/generate_image.sh "prompt" [absolute-output-path]
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT="${1:?usage: generate_image.sh \"prompt\" [out.png]}"
OUT="${2:-}"
if [[ -z "$OUT" ]]; then
  SLUG="$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/-\+/-/g;s/^-//;s/-$//' | cut -c1-48)"
  OUT="${HOME}/.openclaw/workspace/docs/images/${SLUG:-image}-$(date -u +%Y%m%d-%H%M%S).png"
fi
mkdir -p "$(dirname "$OUT")"
python3 "$DIR/comfyui_health.py" || { echo '{"ok":false,"error":"comfyui health failed — check COMFYUI_BASE_URL and KUBB ComfyUI"}'; exit 1; }
python3 "$DIR/comfyui_generate.py" "$PROMPT" --output "$OUT" --json
