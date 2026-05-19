#!/usr/bin/env python3
"""Ping ComfyUI system_stats or root. Exit 0 if reachable."""
import sys
import urllib.error
import urllib.request

from comfyui_env import base_url, reject_localhost

def main() -> int:
    base = base_url()
    try:
        reject_localhost(base)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    for path in ("/system_stats", "/"):
        url = f"{base}{path}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"ok {url} status={resp.status}")
                return 0
        except urllib.error.HTTPError as e:
            if e.code < 500:
                print(f"ok {url} status={e.code}")
                return 0
        except OSError as e:
            print(f"fail {url}: {e}", file=sys.stderr)
    return 1

if __name__ == "__main__":
    sys.exit(main())
