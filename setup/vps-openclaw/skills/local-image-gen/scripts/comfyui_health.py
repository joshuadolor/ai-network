#!/usr/bin/env python3
"""Ping ComfyUI system_stats or root. Exit 0 if reachable."""
from __future__ import annotations

import sys

from comfyui_client import base_url, get_system_stats


def main() -> int:
    try:
        base_url()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 2
    try:
        stats = get_system_stats()
        devices = stats.get("devices") or []
        print(f"ok {base_url()}/system_stats devices={len(devices)}")
        return 0
    except RuntimeError as e:
        print(f"fail: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
