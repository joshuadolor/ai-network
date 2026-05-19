#!/usr/bin/env python3
"""Queue a ComfyUI workflow with a text prompt; download first output image."""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any


def _base() -> str:
    return (os.environ.get("COMFYUI_BASE_URL") or "").rstrip("/")


def _workflow_path() -> Path | None:
    raw = os.environ.get("COMFYUI_WORKFLOW_API", "").strip()
    if not raw:
        return None
    p = Path(raw).expanduser()
    return p if p.is_file() else None


def _load_workflow(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("workflow JSON must be an object (API format)")
    return data


def _patch_workflow(
    workflow: dict[str, Any], positive: str, negative: str | None
) -> dict[str, Any]:
    w = json.loads(json.dumps(workflow))
    clips = [
        (nid, n)
        for nid, n in w.items()
        if isinstance(n, dict) and n.get("class_type") == "CLIPTextEncode"
    ]
    if clips:
        clips[0][1].setdefault("inputs", {})["text"] = positive
        if negative and len(clips) > 1:
            clips[1][1].setdefault("inputs", {})["text"] = negative
    for _nid, node in w.items():
        if not isinstance(node, dict):
            continue
        if node.get("class_type") == "KSampler":
            inputs = node.setdefault("inputs", {})
            if "seed" in inputs:
                inputs["seed"] = random.randint(0, 2**32 - 1)
    return w


def _post_json(url: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode())


def _get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.loads(resp.read().decode())


def _queue(workflow: dict, client_id: str, base: str) -> str:
    out = _post_json(f"{base}/prompt", {"prompt": workflow, "client_id": client_id})
    pid = out.get("prompt_id")
    if not pid:
        raise RuntimeError(f"no prompt_id in response: {out}")
    return str(pid)


def _wait_outputs(prompt_id: str, base: str, timeout: float = 600.0) -> list[dict]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        hist = _get_json(f"{base}/history/{prompt_id}")
        entry = hist.get(prompt_id) or {}
        status = entry.get("status", {})
        if status.get("completed"):
            outputs = entry.get("outputs", {})
            images: list[dict] = []
            for node_out in outputs.values():
                for img in node_out.get("images", []):
                    images.append(img)
            if images:
                return images
            raise RuntimeError("completed but no images in history")
        if status.get("status_str") == "error":
            raise RuntimeError(f"ComfyUI error: {entry}")
        time.sleep(2)
    raise TimeoutError(f"timed out waiting for prompt {prompt_id}")


def _download_image(meta: dict, base: str, dest: Path) -> None:
    q = urllib.parse.urlencode(
        {
            "filename": meta["filename"],
            "subfolder": meta.get("subfolder", ""),
            "type": meta.get("type", "output"),
        }
    )
    url = f"{base}/view?{q}"
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> int:
    parser = argparse.ArgumentParser(description="ComfyUI txt2img via API workflow")
    parser.add_argument("--prompt", required=True, help="Positive prompt")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--out", type=Path, required=True, help="Output image path")
    parser.add_argument("--workflow", type=Path, help="Override COMFYUI_WORKFLOW_API")
    args = parser.parse_args()

    base = _base()
    if not base:
        print("COMFYUI_BASE_URL not set", file=sys.stderr)
        return 2

    wf_path = args.workflow or _workflow_path()
    if not wf_path:
        print(
            "COMFYUI_WORKFLOW_API not set or missing file — export API workflow from ComfyUI "
            "(see setup/ai-server/05-comfyui/README.md)",
            file=sys.stderr,
        )
        return 3

    try:
        workflow = _patch_workflow(
            _load_workflow(wf_path), args.prompt, args.negative or None
        )
        client_id = str(uuid.uuid4())
        prompt_id = _queue(workflow, client_id, base)
        images = _wait_outputs(prompt_id, base)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        _download_image(images[0], base, args.out)
        print(json.dumps({"ok": True, "path": str(args.out), "prompt_id": prompt_id}))
        return 0
    except (urllib.error.URLError, OSError, RuntimeError, TimeoutError, ValueError) as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
