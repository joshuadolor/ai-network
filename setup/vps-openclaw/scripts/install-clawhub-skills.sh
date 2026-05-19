#!/usr/bin/env bash
# Install ClawHub skills used by this repo (run on OpenClaw VPS once).
set -euo pipefail

echo "=== ClawHub skills (optional but recommended for HTML) ==="

install_one() {
  local spec="$1"
  if command -v clawhub >/dev/null 2>&1; then
    echo "clawhub install $spec"
    clawhub install "$spec" || true
  elif command -v npx >/dev/null 2>&1; then
    echo "npx clawhub@latest install $spec"
    npx --yes clawhub@latest install "$spec" || true
  else
    echo "Skip $spec — install Node/npx or clawhub CLI first" >&2
    return 1
  fi
}

# Popular in Chinese OpenClaw guides (steipete / Anthropic-style frontend quality)
install_one "steipete/frontend-design"

echo ""
echo "Enable in ~/.openclaw/openclaw.json skills.entries if needed, then:"
echo "  bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork --config-merge --restart"
echo "Felix: prefer skill frontend-design when present; else cn-html-design fallback."
