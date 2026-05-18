#!/usr/bin/env python3
"""Merge safe keys from openclaw.json.example into live ~/.openclaw/openclaw.json.

Preserves: gateway.auth.token, models.providers.ollama.baseUrl (if not placeholder),
commands.ownerAllowFrom (if not REPLACE_*), cron.failureDestination.to (if not REPLACE_*).
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

PLACEHOLDER_MARKERS = ("REPLACE_", "REPLACE_WITH")


def _is_placeholder(val: Any) -> bool:
    if not isinstance(val, str):
        return False
    return any(m in val for m in PLACEHOLDER_MARKERS)


def _deep_merge(base: dict, patch: dict, path: str = "") -> dict:
    out = deepcopy(base)
    for key, patch_val in patch.items():
        cur_path = f"{path}.{key}" if path else key
        if key not in out:
            out[key] = deepcopy(patch_val)
            continue
        if isinstance(patch_val, dict) and isinstance(out[key], dict):
            # Never overwrite live gateway token from example
            if cur_path == "gateway.auth":
                live_token = out.get("gateway", {}).get("auth", {}).get("token")
                merged = _deep_merge(out[key], patch_val, cur_path)
                if live_token and not _is_placeholder(str(live_token)):
                    if isinstance(merged, dict) and "token" in merged:
                        merged["token"] = live_token
                out[key] = merged
                continue
            # Preserve Ollama baseUrl if already set
            if cur_path == "models.providers.ollama" and isinstance(out[key], dict):
                live_url = out[key].get("baseUrl")
                merged = _deep_merge(out[key], patch_val, cur_path)
                if live_url and not _is_placeholder(live_url):
                    merged["baseUrl"] = live_url
                out[key] = merged
                continue
            out[key] = _deep_merge(out[key], patch_val, cur_path)
        else:
            # Skip placeholder scalars when live value exists
            if _is_placeholder(patch_val) and out[key] and not _is_placeholder(str(out[key])):
                continue
            out[key] = deepcopy(patch_val)
    return out


def main() -> int:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <example.json> <live.json> <output.json>", file=sys.stderr)
        return 2
    example_path, live_path, out_path = map(Path, sys.argv[1:4])
    example = json.loads(example_path.read_text())
    if live_path.exists():
        live = json.loads(live_path.read_text())
    else:
        live = {}
    merged = _deep_merge(live, example)
    out_path.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"Wrote merged config to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
