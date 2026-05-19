---
name: crypto-watch
description: Read-only crypto prices and watchlist summaries via public APIs. Use for monitoring and research — never auto-trade without explicit approval.
user-invocable: true
---

# Crypto watch (read-only)

## Hard rules

- **No live trades**, wallet moves, or exchange API orders unless Joshua says **execute** or **approved** in the same thread — and even then prefer human confirmation on the exchange UI.
- **No secrets** in chat: never print API keys from env.
- This skill is for **prices, trends, alerts drafts, and research** only.
- Not financial advice — add a one-line disclaimer on substantive summaries.

## Environment

- `CRYPTO_WATCH_SYMBOLS` — optional comma list, e.g. `btc,eth,sol` (CoinGecko ids). Default: `bitcoin,ethereum,solana`.

## Commands (exec)

Watchlist snapshot (USD, 24h change):

    python3 {baseDir}/scripts/watch.py

Custom ids:

    python3 {baseDir}/scripts/watch.py --ids bitcoin,ethereum,chainlink

## Workflow

1. Run `watch.py` for a quick table.
2. For **why** price moved, use skill **deep-research** (news, not chain gossip alone).
3. For **recurring** price checks, create **cron** (7b, 300s timeout) → Discord channel Joshua chooses — see **proactive-ops**.
4. Save longer notes to `workspace/docs/crypto-YYYY-MM-DD.md`.

## Optional later

Joshua may add exchange read-only API keys to `.env` — document new scripts then; do not invent trading endpoints.
