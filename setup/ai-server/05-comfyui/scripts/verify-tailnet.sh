#!/usr/bin/env bash
# Run from apps VPS or OpenClaw VPS to verify ComfyUI on KUBB over Tailscale.
set -euo pipefail

KUBB_IP="${KUBB_TAILSCALE_IP:-100.86.160.110}"
BASE="http://${KUBB_IP}:8188"

echo "ComfyUI: ${BASE}/system_stats"
if curl -sf "${BASE}/system_stats" | head -c 200; then
  echo ""
  echo "OK"
else
  echo "FAIL — check ComfyUI --listen, UFW on tailscale0:8188, Tailscale" >&2
  exit 1
fi
