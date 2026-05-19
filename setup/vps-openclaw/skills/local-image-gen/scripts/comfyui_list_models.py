#!/usr/bin/env python3
"""List ComfyUI checkpoint names (for COMFYUI_CHECKPOINT)."""
from __future__ import annotations

import argparse
import json
import sys

from comfyui_client import get_checkpoint_names


def main() -> int:
    parser = argparse.ArgumentParser(description="List ComfyUI checkpoints")
    parser.add_argument("--json", action="store_true", help="JSON array output")
    args = parser.parse_args()
    try:
        names = get_checkpoint_names()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(names, indent=2))
    else:
        if not names:
            print("(no checkpoints — add a .safetensors file to models/checkpoints)")
        for name in names:
            print(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
