"""Minimal ComfyUI HTTP API client (stdlib only)."""
from __future__ import annotations

import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any


def base_url() -> str:
    try:
        from comfyui_env import base_url as _skill_base_url

        return _skill_base_url()
    except ImportError:
        pass
    url = (os.environ.get("COMFYUI_BASE_URL") or "").rstrip("/")
    if not url:
        raise RuntimeError("COMFYUI_BASE_URL is not set")
    return url


def _request(
    method: str,
    path: str,
    *,
    data: dict | None = None,
    timeout: float = 30,
) -> Any:
    url = f"{base_url()}{path}"
    body = None
    headers: dict[str, str] = {}
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if not raw:
                return None
            return json.loads(raw.decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} {path}: {detail}") from e
    except OSError as e:
        raise RuntimeError(f"request failed {path}: {e}") from e


def get_system_stats() -> dict:
    return _request("GET", "/system_stats")


def get_checkpoint_names() -> list[str]:
    """Return checkpoint filenames from /object_info."""
    info = _request("GET", "/object_info")
    node = info.get("CheckpointLoaderSimple") or info.get("CheckpointLoader") or {}
    required = node.get("input", {}).get("required", {})
    ckpt = required.get("ckpt_name")
    if isinstance(ckpt, list) and ckpt and isinstance(ckpt[0], list):
        return list(ckpt[0])
    return []


def build_txt2img_workflow(
    *,
    prompt: str,
    negative: str,
    checkpoint: str,
    seed: int,
    width: int,
    height: int,
    steps: int = 20,
    cfg: float = 7.0,
    sampler_name: str = "euler",
    scheduler: str = "normal",
    filename_prefix: str = "openclaw",
) -> dict[str, Any]:
    """Standard SD/SDXL-compatible txt2img API prompt graph."""
    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler_name,
                "scheduler": scheduler,
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            },
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": checkpoint},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["4", 1]},
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": negative, "clip": ["4", 1]},
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": filename_prefix, "images": ["8", 0]},
        },
    }


def load_workflow_json(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "prompt" in data:
        return data["prompt"]
    if isinstance(data, dict):
        return data
    raise ValueError(f"invalid workflow file: {path}")


def queue_prompt(workflow: dict[str, Any], *, client_id: str | None = None) -> str:
    client_id = client_id or str(uuid.uuid4())
    payload = {"prompt": workflow, "client_id": client_id}
    result = _request("POST", "/prompt", data=payload, timeout=60)
    if not isinstance(result, dict) or "prompt_id" not in result:
        raise RuntimeError(f"unexpected /prompt response: {result!r}")
    if result.get("node_errors"):
        raise RuntimeError(f"node_errors: {json.dumps(result['node_errors'])}")
    return str(result["prompt_id"])


def get_history(prompt_id: str) -> dict[str, Any]:
    data = _request("GET", f"/history/{prompt_id}", timeout=30)
    if not isinstance(data, dict):
        return {}
    return data.get(prompt_id, data)


def wait_for_images(
    prompt_id: str,
    *,
    timeout_sec: float = 600,
    poll_sec: float = 2.0,
) -> list[dict[str, str]]:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        entry = get_history(prompt_id)
        if entry:
            outputs = entry.get("outputs") or {}
            images: list[dict[str, str]] = []
            for node_out in outputs.values():
                for img in node_out.get("images") or []:
                    if isinstance(img, dict) and img.get("filename"):
                        images.append(img)
            if images:
                return images
            status = entry.get("status") or {}
            if status.get("status_str") == "error":
                messages = status.get("messages") or []
                raise RuntimeError(f"comfyui job error: {messages}")
        time.sleep(poll_sec)
    raise TimeoutError(f"timed out after {timeout_sec}s waiting for prompt {prompt_id}")


def download_image(meta: dict[str, str], dest_path: str) -> str:
    params = urllib.parse.urlencode(
        {
            "filename": meta["filename"],
            "subfolder": meta.get("subfolder") or "",
            "type": meta.get("type") or "output",
        }
    )
    url = f"{base_url()}/view?{params}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)
    return dest_path


def resolve_checkpoint(explicit: str | None) -> str:
    if explicit:
        return explicit
    env = (os.environ.get("COMFYUI_CHECKPOINT") or "").strip()
    if env:
        return env
    names = get_checkpoint_names()
    if not names:
        raise RuntimeError(
            "no checkpoints found under ComfyUI models/checkpoints. "
            "Install a .safetensors checkpoint or set COMFYUI_CHECKPOINT."
        )
    return names[0]


def random_seed() -> int:
    return random.randint(0, 2**32 - 1)
