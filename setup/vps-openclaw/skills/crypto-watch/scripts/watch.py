#!/usr/bin/env python3
"""CoinGecko public simple price — no API key required."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

DEFAULT_IDS = "bitcoin,ethereum,solana"


def fetch(ids: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "ids": ids,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        }
    )
    url = f"https://api.coingecko.com/api/v3/simple/price?{params}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    parser = argparse.ArgumentParser(description="Crypto watchlist (read-only)")
    parser.add_argument(
        "--ids",
        default=os.environ.get("CRYPTO_WATCH_SYMBOLS", DEFAULT_IDS),
        help="Comma-separated CoinGecko coin ids",
    )
    args = parser.parse_args()
    ids = ",".join(x.strip() for x in args.ids.split(",") if x.strip())
    try:
        data = fetch(ids)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if not data:
        print("no data returned")
        return 1
    print(f"{'id':<16} {'usd':>12} {'24h %':>10}")
    print("-" * 42)
    for coin_id, row in sorted(data.items()):
        usd = row.get("usd")
        ch = row.get("usd_24h_change")
        usd_s = f"{usd:,.2f}" if isinstance(usd, (int, float)) else "n/a"
        ch_s = f"{ch:+.2f}" if isinstance(ch, (int, float)) else "n/a"
        print(f"{coin_id:<16} {usd_s:>12} {ch_s:>10}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
