#!/usr/bin/env bash
# Update OpenClaw VPS state from AINetwork repo (Felix = javi + Tina patterns, Ollama stack).
#
# Run on the VPS after: cd ~/AINetwork && git pull
#
#   bash setup/vps-openclaw/scripts/update-vps-openclaw.sh
#   bash setup/vps-openclaw/scripts/update-vps-openclaw.sh ~/AINetwork --config-merge --restart
#
# Options:
#   --dry-run              Print actions only
#   --no-backup            Skip timestamped backup under ~/.openclaw/backups/
#   --force-user           Overwrite workspace/USER.md from repo template
#   --force-memory         Overwrite workspace/MEMORY.md from repo template
#   --templates-all        Overwrite BOOTSTRAP ERRORS DREAMS IDENTITY from repo
#   --config-merge         Merge openclaw.json.example into openclaw.json (keeps tokens/URLs)
#   --env-init             Copy .env.example → .env if .env missing (chmod 600)
#   --restart              openclaw gateway restart (sources .env first)
#   --cron                 Run recreate-daily-ai-cron.sh (set CHANNEL_ID or --channel)
#   --channel ID           Default Discord channel for --cron (default: alerts channel)
#   -h, --help             This help

set -euo pipefail

REPO_ROOT="${HOME}/AINetwork"
DRY_RUN=0
NO_BACKUP=0
FORCE_USER=0
FORCE_MEMORY=0
TEMPLATES_ALL=0
CONFIG_MERGE=0
ENV_INIT=0
DO_RESTART=0
DO_CRON=0
CHANNEL_ID="${CHANNEL_ID:-1505186587321831445}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VPS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage ;;
    --dry-run) DRY_RUN=1; shift ;;
    --no-backup) NO_BACKUP=1; shift ;;
    --force-user) FORCE_USER=1; shift ;;
    --force-memory) FORCE_MEMORY=1; shift ;;
    --templates-all) TEMPLATES_ALL=1; shift ;;
    --config-merge) CONFIG_MERGE=1; shift ;;
    --env-init) ENV_INIT=1; shift ;;
    --restart) DO_RESTART=1; shift ;;
    --cron) DO_CRON=1; shift ;;
    --channel)
      CHANNEL_ID="${2:?--channel requires id}"
      shift 2
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
WS_SRC="$REPO_ROOT/setup/vps-openclaw/08-workspace/workspace"
SKILLS_SRC="$REPO_ROOT/setup/vps-openclaw/skills"
REF_SRC="$REPO_ROOT/setup/vps-openclaw/reference"

if [[ ! -d "$REPO_ROOT/setup/vps-openclaw" ]]; then
  echo "Missing $REPO_ROOT/setup/vps-openclaw — pass repo path as first argument." >&2
  exit 1
fi

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

copy_file() {
  local src="$1" dest="$2"
  if [[ ! -f "$src" ]]; then
    echo "Skip (missing in repo): $src" >&2
    return 0
  fi
  run mkdir -p "$(dirname "$dest")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] cp $src -> $dest"
  else
    cp "$src" "$dest"
    echo "  updated $dest"
  fi
}

backup_if_exists() {
  local f="$1" backup_dir="$2"
  [[ -f "$f" ]] || return 0
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] backup $f -> $backup_dir/"
    return 0
  fi
  mkdir -p "$backup_dir"
  cp "$f" "$backup_dir/$(basename "$f")"
}

echo "=== update-vps-openclaw ==="
echo "Repo:      $REPO_ROOT"
echo "OpenClaw:  $OC"
echo "Stack:     Felix (javiConsu) + Tina Huang patterns → Ollama VPS + Discord"
echo ""

BACKUP_DIR=""
if [[ "$NO_BACKUP" -eq 0 ]]; then
  BACKUP_DIR="$OC/backups/$(date +%Y%m%d-%H%M%S)"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] backup dir: $BACKUP_DIR"
  else
    mkdir -p "$BACKUP_DIR"
    echo "Backup:    $BACKUP_DIR"
  fi
fi

# --- Workspace MD (always refresh operational rules) ---
echo ""
echo "Workspace templates (SOUL, AGENTS, HEARTBEAT, TOOLS):"
ALWAYS_SYNC=(SOUL.md AGENTS.md HEARTBEAT.md TOOLS.md)
for f in "${ALWAYS_SYNC[@]}"; do
  if [[ -n "$BACKUP_DIR" ]]; then
    backup_if_exists "$OC/workspace/$f" "$BACKUP_DIR/workspace"
  fi
  copy_file "$WS_SRC/$f" "$OC/workspace/$f"
done

# --- Optional templates ---
OPTIONAL_SYNC=(BOOTSTRAP.md ERRORS.md DREAMS.md IDENTITY.md)
for f in "${OPTIONAL_SYNC[@]}"; do
  dest="$OC/workspace/$f"
  if [[ "$TEMPLATES_ALL" -eq 1 ]]; then
    [[ -n "$BACKUP_DIR" ]] && backup_if_exists "$dest" "$BACKUP_DIR/workspace"
    copy_file "$WS_SRC/$f" "$dest"
  elif [[ ! -f "$dest" ]] && [[ -f "$WS_SRC/$f" ]]; then
    copy_file "$WS_SRC/$f" "$dest"
    echo "  (created missing $f)"
  fi
done

# USER / MEMORY — never overwrite unless forced
for f in USER.md MEMORY.md; do
  dest="$OC/workspace/$f"
  force=0
  [[ "$f" == "USER.md" && "$FORCE_USER" -eq 1 ]] && force=1
  [[ "$f" == "MEMORY.md" && "$FORCE_MEMORY" -eq 1 ]] && force=1
  if [[ "$force" -eq 1 ]]; then
    [[ -n "$BACKUP_DIR" ]] && backup_if_exists "$dest" "$BACKUP_DIR/workspace"
    copy_file "$WS_SRC/$f" "$dest"
  elif [[ -f "$dest" ]]; then
    if [[ "$f" == "USER.md" ]]; then
      echo "  kept $dest (use --force-user to overwrite)"
    else
      echo "  kept $dest (use --force-memory to overwrite)"
    fi
  elif [[ -f "$WS_SRC/$f" ]]; then
    copy_file "$WS_SRC/$f" "$dest"
    echo "  (created missing $f)"
  fi
done

run mkdir -p "$OC/workspace/memory" "$OC/workspace/docs" "$OC/workspace/reference"

# --- Workspace skills (every subfolder under skills/ except README) ---
echo ""
echo "Workspace skills:"
if [[ ! -d "$SKILLS_SRC" ]]; then
  echo "  missing $SKILLS_SRC" >&2
  exit 1
fi
run mkdir -p "$OC/workspace/skills"
shopt -s nullglob
for skill_dir in "$SKILLS_SRC"/*/; do
  name="$(basename "$skill_dir")"
  [[ "$name" == .* ]] && continue
  if [[ -n "$BACKUP_DIR" && -d "$OC/workspace/skills/$name" ]]; then
    run cp -R "$OC/workspace/skills/$name" "$BACKUP_DIR/skills-$name"
  fi
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] cp -R $skill_dir -> $OC/workspace/skills/$name"
  else
    cp -R "$skill_dir" "$OC/workspace/skills/"
    for py in "$OC/workspace/skills/$name"/scripts/*.py; do
      [[ -f "$py" ]] && chmod 700 "$py"
    done
    echo "  updated $OC/workspace/skills/$name/"
  fi
done
shopt -u nullglob

# --- Reference docs for Felix / you (not loaded as soul; handy in workspace) ---
echo ""
echo "Reference copies (cron + Tina paste prompts):"
copy_file "$REF_SRC/javiconsu-felix-adapted/CRON-EXAMPLES.md" "$OC/workspace/reference/CRON-EXAMPLES.md"
copy_file "$REF_SRC/tina-huang-openclaw-prompts/FELIX-PASTE-PROMPTS.md" "$OC/workspace/reference/FELIX-PASTE-PROMPTS.md"
copy_file "$REF_SRC/lead-site-trial-workflow.md" "$OC/workspace/reference/lead-site-trial-workflow.md"
run mkdir -p "$OC/workspace/docs/leads"

# --- .env ---
if [[ "$ENV_INIT" -eq 1 ]]; then
  echo ""
  echo ".env:"
  if [[ -f "$OC/.env" ]]; then
    echo "  kept existing $OC/.env"
  else
    copy_file "$REPO_ROOT/setup/vps-openclaw/.env.example" "$OC/.env"
    run chmod 600 "$OC/.env"
    echo "  EDIT $OC/.env — add DISCORD_BOT_TOKEN, email, Ollama host"
  fi
fi

# --- openclaw.json merge ---
if [[ "$CONFIG_MERGE" -eq 1 ]]; then
  echo ""
  echo "Config merge (openclaw.json):"
  EXAMPLE="$REPO_ROOT/setup/vps-openclaw/openclaw.json.example"
  LIVE="$OC/openclaw.json"
  MERGE_PY="$SCRIPT_DIR/lib/merge-openclaw-config.py"
  if [[ ! -f "$EXAMPLE" ]]; then
    echo "  missing example: $EXAMPLE" >&2
    exit 1
  fi
  [[ -n "$BACKUP_DIR" && -f "$LIVE" ]] && backup_if_exists "$LIVE" "$BACKUP_DIR"
  TMP="$(mktemp)"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] python3 $MERGE_PY $EXAMPLE $LIVE $TMP && mv $TMP $LIVE"
  else
    python3 "$MERGE_PY" "$EXAMPLE" "$LIVE" "$TMP"
    mv "$TMP" "$LIVE"
    echo "  merged $LIVE (gateway token + Ollama baseUrl preserved if set)"
    echo "  verify: models.providers.ollama.baseUrl, commands.ownerAllowFrom, cron.failureDestination"
  fi
fi

# --- Daily AI cron ---
if [[ "$DO_CRON" -eq 1 ]]; then
  echo ""
  echo "Daily AI cron:"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] CHANNEL_ID=$CHANNEL_ID bash $SCRIPT_DIR/recreate-daily-ai-cron.sh"
  else
    set -a
    # shellcheck source=/dev/null
    [[ -f "$OC/.env" ]] && source "$OC/.env"
    set +a
    CHANNEL_ID="$CHANNEL_ID" bash "$SCRIPT_DIR/recreate-daily-ai-cron.sh"
  fi
fi

# --- Gateway restart ---
if [[ "$DO_RESTART" -eq 1 ]]; then
  echo ""
  echo "Gateway:"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] source .env && openclaw gateway restart"
  else
    set -a
    # shellcheck source=/dev/null
    [[ -f "$OC/.env" ]] && source "$OC/.env"
    set +a
    openclaw gateway restart
    echo "  restarted — use Discord /new for a fresh session"
  fi
fi

echo ""
echo "=== done ==="
if [[ "$CONFIG_MERGE" -eq 0 ]]; then
  echo "Tip: add --config-merge once to apply compaction/browser/cron from openclaw.json.example"
fi
if [[ "$DO_RESTART" -eq 0 ]]; then
  echo "Tip: add --restart after reviewing changes"
fi
echo "Manual: edit $OC/.env if needed; merge config if not using --config-merge"
echo "Docs:   $REPO_ROOT/setup/vps-openclaw/reference/javiconsu-felix-adapted/VPS-SYNC.md"
