#!/usr/bin/env bash
#
# start_comfyui.sh — Start, supervise, and auto-restart ComfyUI on a headless Linux VPS.
#
# Run from the directory that contains the ComfyUI tree (main.py, venv/, etc.).
# Listens on 0.0.0.0:8188 by default. Logs to comfyui_server.log in the same directory.
#
# Usage:
#   cp start_comfyui.env.example start_comfyui.env   # edit paths, then:
#   set -a && source ./start_comfyui.env && set +a && ./start_comfyui.sh
#   chmod +x start_comfyui.sh
#
# Optional environment overrides:
#   COMFYUI_ROOT      — path to ComfyUI install (default: current working directory)
#   COMFYUI_VENV      — path to venv directory (default: $COMFYUI_ROOT/venv or .venv)
#   COMFYUI_PORT      — listen port (default: 8188)
#   COMFYUI_LISTEN    — bind address (default: 0.0.0.0)
#   COMFYUI_LOG       — log file path (default: $COMFYUI_ROOT/comfyui_server.log)
#   COMFYUI_RESTART_DELAY — seconds between restarts (default: 10)
#   COMFYUI_EXTRA_ARGS — extra arguments passed to main.py (quoted string)

set -uo pipefail

# ---------------------------------------------------------------------------
# Configuration (overridable via environment)
# ---------------------------------------------------------------------------
COMFYUI_ROOT="${COMFYUI_ROOT:-$(pwd)}"
COMFYUI_PORT="${COMFYUI_PORT:-8188}"
COMFYUI_LISTEN="${COMFYUI_LISTEN:-0.0.0.0}"
COMFYUI_LOG="${COMFYUI_LOG:-${COMFYUI_ROOT}/comfyui_server.log}"
COMFYUI_RESTART_DELAY="${COMFYUI_RESTART_DELAY:-10}"

# Resolve venv: explicit COMFYUI_VENV, else venv/, else .venv/
if [[ -n "${COMFYUI_VENV:-}" ]]; then
  VENV_DIR="${COMFYUI_VENV}"
elif [[ -d "${COMFYUI_ROOT}/venv" ]]; then
  VENV_DIR="${COMFYUI_ROOT}/venv"
elif [[ -d "${COMFYUI_ROOT}/.venv" ]]; then
  VENV_DIR="${COMFYUI_ROOT}/.venv"
else
  VENV_DIR="${COMFYUI_ROOT}/venv"
fi

# Linux/macOS: venv/bin/python — Windows (Git Bash): venv/Scripts/python.exe
if [[ -x "${VENV_DIR}/bin/python" ]]; then
  PYTHON_BIN="${VENV_DIR}/bin/python"
elif [[ -x "${VENV_DIR}/Scripts/python.exe" ]]; then
  PYTHON_BIN="${VENV_DIR}/Scripts/python.exe"
elif [[ -x "${VENV_DIR}/Scripts/python" ]]; then
  PYTHON_BIN="${VENV_DIR}/Scripts/python"
else
  PYTHON_BIN="${VENV_DIR}/bin/python"
fi
MAIN_PY="${COMFYUI_ROOT}/main.py"

RUNNING=1
CHILD_PID=""

# ---------------------------------------------------------------------------
# Logging helpers (script messages + timestamps)
# ---------------------------------------------------------------------------
log() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$msg"
  echo "$msg" >> "${COMFYUI_LOG}"
}

log_err() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*"
  echo "$msg" >&2
  echo "$msg" >> "${COMFYUI_LOG}"
}

# ---------------------------------------------------------------------------
# Graceful shutdown on SIGINT / SIGTERM
# ---------------------------------------------------------------------------
shutdown() {
  RUNNING=0
  echo ""
  log "Shutdown requested — stopping ComfyUI supervisor..."

  if [[ -n "${CHILD_PID}" ]] && kill -0 "${CHILD_PID}" 2>/dev/null; then
    log "Sending SIGTERM to ComfyUI (PID ${CHILD_PID})..."
    kill -TERM "${CHILD_PID}" 2>/dev/null || true

    local waited=0
    while kill -0 "${CHILD_PID}" 2>/dev/null && [[ ${waited} -lt 30 ]]; do
      sleep 1
      waited=$((waited + 1))
    done

    if kill -0 "${CHILD_PID}" 2>/dev/null; then
      log "ComfyUI did not exit in time — sending SIGKILL (PID ${CHILD_PID})..."
      kill -KILL "${CHILD_PID}" 2>/dev/null || true
    fi
  fi

  log "Supervisor stopped. Goodbye."
  exit 0
}

trap shutdown INT TERM

# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------
preflight() {
  if [[ ! -d "${COMFYUI_ROOT}" ]]; then
    log_err "COMFYUI_ROOT does not exist: ${COMFYUI_ROOT}"
    exit 1
  fi

  if [[ ! -f "${MAIN_PY}" ]]; then
    log_err "ComfyUI main.py not found at: ${MAIN_PY}"
    log_err "COMFYUI_ROOT must be the folder that contains main.py (app code), not your models folder."
    log_err "ComfyUI Desktop (Windows): COMFYUI_ROOT is usually .../AppData/Local/Programs/ComfyUI/resources/ComfyUI"
    log_err "  and COMFYUI_EXTRA_ARGS should include: --base-directory /path/to/Documents/ComfyUI"
    exit 1
  fi

  if [[ ! -d "${VENV_DIR}" ]]; then
    log_err "Virtual environment not found at: ${VENV_DIR}"
    log_err "Create one with: python3 -m venv venv"
    exit 1
  fi

  if [[ ! -x "${PYTHON_BIN}" ]]; then
    log_err "Python interpreter not found or not executable: ${PYTHON_BIN}"
    exit 1
  fi

  # Ensure log file exists and is writable
  touch "${COMFYUI_LOG}" 2>/dev/null || {
    log_err "Cannot write to log file: ${COMFYUI_LOG}"
    exit 1
  }
}

build_comfy_args() {
  COMFY_ARGS=(
    "${MAIN_PY}"
    --listen "${COMFYUI_LISTEN}"
    --port "${COMFYUI_PORT}"
  )
  if [[ -n "${COMFYUI_EXTRA_ARGS:-}" ]]; then
    # shellcheck disable=SC2206
    read -r -a _extra <<< "${COMFYUI_EXTRA_ARGS}"
    COMFY_ARGS+=("${_extra[@]}")
  fi
}

# Print the last ComfyUI error block from the log (helps diagnose restart loops).
log_last_comfyui_error() {
  if [[ ! -f "${COMFYUI_LOG}" ]]; then
    return
  fi
  local hint
  hint="$(grep -E 'ERROR|comfyui-frontend-package|comfyui-workflow-templates|Address already in use' "${COMFYUI_LOG}" | tail -n 5 || true)"
  if [[ -n "${hint}" ]]; then
    log "Recent log errors:"
    while IFS= read -r line; do
      log "  ${line}"
    done <<< "${hint}"
  fi
}

# ---------------------------------------------------------------------------
# Main supervisor loop
# ---------------------------------------------------------------------------
main() {
  cd "${COMFYUI_ROOT}" || {
    log_err "Cannot cd to COMFYUI_ROOT: ${COMFYUI_ROOT}"
    exit 1
  }

  preflight
  build_comfy_args

  log "============================================================"
  log "ComfyUI supervisor starting"
  log "  Root:          ${COMFYUI_ROOT}"
  log "  Python:        ${PYTHON_BIN}"
  log "  Listen:        ${COMFYUI_LISTEN}:${COMFYUI_PORT}"
  log "  Virtual env:   ${VENV_DIR}"
  log "  Log file:      ${COMFYUI_LOG}"
  log "  Restart delay: ${COMFYUI_RESTART_DELAY}s"
  log "============================================================"
  log "Press Ctrl+C to stop the supervisor and ComfyUI."

  local restart_count=0

  while [[ ${RUNNING} -eq 1 ]]; do
    if [[ ${restart_count} -gt 0 ]]; then
      log "Restarting ComfyUI (attempt #${restart_count})..."
    else
      log "Launching ComfyUI..."
    fi

    log "Command: ${PYTHON_BIN} ${COMFY_ARGS[*]}"

    {
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] ----- ComfyUI process output begin -----"
    } >> "${COMFYUI_LOG}"

    # Run in background so we capture the real Python PID (no pipe — pipes break kill/wait).
    "${PYTHON_BIN}" "${COMFY_ARGS[@]}" >> "${COMFYUI_LOG}" 2>&1 &
    CHILD_PID=$!

    log "ComfyUI started with PID ${CHILD_PID} (live output: tail -f ${COMFYUI_LOG})"

    # Wait for child; if supervisor is shutting down, loop exits via RUNNING flag
    local exit_code=0
    wait "${CHILD_PID}" 2>/dev/null || exit_code=$?
    CHILD_PID=""

    if [[ ${RUNNING} -eq 0 ]]; then
      break
    fi

    restart_count=$((restart_count + 1))

    {
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] ----- ComfyUI process exited (code ${exit_code}) -----"
    } >> "${COMFYUI_LOG}"

    if [[ ${exit_code} -eq 0 ]]; then
      log "ComfyUI exited cleanly (code 0)."
    else
      log "ComfyUI exited unexpectedly (code ${exit_code})."
      log_last_comfyui_error
    fi

    log "Waiting ${COMFYUI_RESTART_DELAY} seconds before restart..."
    sleep "${COMFYUI_RESTART_DELAY}"
  done
}

main "$@"
