"""Load COMFYUI_* from process env or ~/.openclaw/.env (scripts only — not for chat)."""
from __future__ import annotations

import os
import re
from pathlib import Path

# Non-secret default when .env missing (KUBB Tailscale — see workspace/docs/comfyui-workflow.md)
DEFAULT_BASE_URL = "http://100.86.160.110:8188"


def load_dotenv_comfyui() -> None:
    """Set COMFYUI_* in os.environ from ~/.openclaw/.env if not already set."""
    path = Path.home() / ".openclaw" / ".env"
    if not path.is_file():
        return
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if not key.startswith("COMFYUI_"):
            continue
        val = val.strip().strip("'\"")
        if key and val and key not in os.environ:
            os.environ[key] = val


def base_url() -> str:
    load_dotenv_comfyui()
    url = (os.environ.get("COMFYUI_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    reject_localhost(url)
    return url


def workflow_api_path() -> Path | None:
    load_dotenv_comfyui()
    raw = os.environ.get("COMFYUI_WORKFLOW_API", "").strip()
    candidates: list[Path] = []
    if raw:
        candidates.append(Path(raw).expanduser())
    candidates.append(Path.home() / ".openclaw" / "comfyui-workflow-api.json")
    for p in candidates:
        if p.is_file():
            return p
    return None


def reject_localhost(url: str) -> None:
    if re.search(r"localhost|127\.0\.0\.1", url, re.I):
        raise ValueError(
            "ComfyUI is on KUBB over Tailscale, not this VPS — "
            f"use {DEFAULT_BASE_URL} (see workspace/docs/comfyui-workflow.md)"
        )
