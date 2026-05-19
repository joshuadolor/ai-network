#!/usr/bin/env python3
"""
Queue a txt2img job on ComfyUI and save the output image.

Requires COMFYUI_BASE_URL (e.g. http://100.x.x.x:8188 over Tailscale).
Optional: COMFYUI_CHECKPOINT, COMFYUI_WORKFLOW (path to API JSON on the machine running this script).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from comfyui_client import (
    build_txt2img_workflow,
    download_image,
    load_workflow_json,
    queue_prompt,
    random_seed,
    resolve_checkpoint,
    wait_for_images,
)


DEFAULT_NEGATIVE = (
    "blurry, low quality, distorted, watermark, text, logo, ugly, deformed"
)


def _default_output_dir() -> str:
    return os.environ.get(
        "COMFYUI_OUTPUT_DIR",
        os.path.join(os.getcwd(), "comfyui_outputs"),
    )


def _apply_prompt_to_workflow(workflow: dict, prompt: str, negative: str) -> dict:
    """Best-effort: set text on first two CLIPTextEncode nodes."""
    encoders = [
        n for n in workflow.values()
        if isinstance(n, dict) and n.get("class_type") == "CLIPTextEncode"
    ]
    if len(encoders) >= 1:
        encoders[0].setdefault("inputs", {})["text"] = prompt
    if len(encoders) >= 2:
        encoders[1].setdefault("inputs", {})["text"] = negative
    return workflow


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an image via ComfyUI API")
    parser.add_argument("prompt", help="Positive prompt")
    parser.add_argument(
        "--negative", "-n",
        default=os.environ.get("COMFYUI_NEGATIVE_PROMPT", DEFAULT_NEGATIVE),
        help="Negative prompt",
    )
    parser.add_argument("--checkpoint", "-c", help="Checkpoint filename (see comfyui_list_models.py)")
    parser.add_argument("--seed", type=int, help="RNG seed (default: random)")
    parser.add_argument("--width", "-W", type=int, default=int(os.environ.get("COMFYUI_WIDTH", "1024")))
    parser.add_argument("--height", "-H", type=int, default=int(os.environ.get("COMFYUI_HEIGHT", "1024")))
    parser.add_argument("--steps", type=int, default=int(os.environ.get("COMFYUI_STEPS", "20")))
    parser.add_argument("--cfg", type=float, default=float(os.environ.get("COMFYUI_CFG", "7.0")))
    parser.add_argument(
        "--workflow", "-w",
        help="Path to exported API workflow JSON (overrides built-in graph)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output image path (default: COMFYUI_OUTPUT_DIR/comfyui_<timestamp>.png)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("COMFYUI_TIMEOUT", "600")),
        help="Max seconds to wait for generation",
    )
    parser.add_argument("--json", action="store_true", help="Print result metadata as JSON")
    args = parser.parse_args()

    try:
        checkpoint = resolve_checkpoint(args.checkpoint)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 2

    seed = args.seed if args.seed is not None else random_seed()

    workflow_path = args.workflow or os.environ.get("COMFYUI_WORKFLOW")
    if workflow_path:
        try:
            workflow = load_workflow_json(workflow_path)
            workflow = _apply_prompt_to_workflow(workflow, args.prompt, args.negative)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            print(f"workflow error: {e}", file=sys.stderr)
            return 2
    else:
        workflow = build_txt2img_workflow(
            prompt=args.prompt,
            negative=args.negative,
            checkpoint=checkpoint,
            seed=seed,
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg=args.cfg,
            filename_prefix="openclaw",
        )

    try:
        prompt_id = queue_prompt(workflow)
        images = wait_for_images(prompt_id, timeout_sec=float(args.timeout))
    except (RuntimeError, TimeoutError) as e:
        print(f"generation failed: {e}", file=sys.stderr)
        return 1

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = _default_output_dir()
    out_path = args.output or os.path.join(out_dir, f"comfyui_{stamp}.png")

    try:
        saved = download_image(images[0], out_path)
    except (RuntimeError, OSError) as e:
        print(f"download failed: {e}", file=sys.stderr)
        return 1

    result = {
        "ok": True,
        "path": os.path.abspath(saved),
        "prompt_id": prompt_id,
        "checkpoint": checkpoint,
        "seed": seed,
        "width": args.width,
        "height": args.height,
        "prompt": args.prompt,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"saved {result['path']}")
        print(f"prompt_id={prompt_id} checkpoint={checkpoint} seed={seed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
