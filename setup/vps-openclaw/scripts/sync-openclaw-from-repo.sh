#!/usr/bin/env bash
# Back-compat wrapper — use update-vps-openclaw.sh instead.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/update-vps-openclaw.sh" "$@"
