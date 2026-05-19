#!/usr/bin/env bash
# Install ngrok on Ubuntu VPS for site-preview-ngrok skill.
set -euo pipefail

if command -v ngrok >/dev/null 2>&1; then
  echo "ngrok already installed: $(ngrok version 2>/dev/null || ngrok --version)"
  exit 0
fi

echo "Installing ngrok via snap (or use https://ngrok.com/download)..."
if command -v snap >/dev/null 2>&1; then
  sudo snap install ngrok
else
  echo "Install manually: https://ngrok.com/download" >&2
  exit 1
fi

if [[ -n "${NGROK_AUTHTOKEN:-}" ]]; then
  ngrok config add-authtoken "$NGROK_AUTHTOKEN"
  echo "Authtoken configured."
else
  echo "Add NGROK_AUTHTOKEN to ~/.openclaw/.env then: ngrok config add-authtoken \$NGROK_AUTHTOKEN"
fi
