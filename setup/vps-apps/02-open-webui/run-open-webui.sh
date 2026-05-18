#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ROOT}/open-webui.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Missing ${ENV_FILE}"
  echo "Copy open-webui.env.example to open-webui.env and set OLLAMA_BASE_URL."
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

if [[ -z "${OLLAMA_BASE_URL:-}" || "${OLLAMA_BASE_URL}" == *"REPLACE_"* ]]; then
  echo "Set OLLAMA_BASE_URL in ${ENV_FILE} to http://<ai-server-tailscale-ip>:11434"
  exit 1
fi

docker rm -f open-webui 2>/dev/null || true

exec docker run -d \
  -p 3000:8080 \
  -e "OLLAMA_BASE_URL=${OLLAMA_BASE_URL}" \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
