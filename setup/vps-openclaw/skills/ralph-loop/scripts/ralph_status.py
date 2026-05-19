#!/usr/bin/env python3
"""Ralph loop — track long tasks and whether a 5-minute progress ping is due."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

INTERVAL_SEC = int(os.environ.get("RALPH_PING_INTERVAL_SEC", "300"))
STATE_DIR = Path(
    os.environ.get(
        "RALPH_STATE_DIR",
        Path.home() / ".openclaw" / "workspace" / ".ralph-loop",
    )
)
STATE_FILE = STATE_DIR / "active.json"


def _load() -> dict:
    if not STATE_FILE.is_file():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def cmd_start(title: str) -> int:
    now = time.time()
    data = {
        "title": title,
        "started_at": now,
        "last_ping_at": now,
        "pings": [{"at": now, "message": "Ralph loop started"}],
    }
    _save(data)
    print(json.dumps({"ok": True, "action": "start", "title": title, "interval_sec": INTERVAL_SEC}))
    return 0


def cmd_should_ping() -> int:
    data = _load()
    if not data:
        print(json.dumps({"ok": True, "should_ping": False, "reason": "no_active_loop"}))
        return 0
    elapsed = time.time() - float(data.get("last_ping_at", 0))
    due = elapsed >= INTERVAL_SEC
    print(
        json.dumps(
            {
                "ok": True,
                "should_ping": due,
                "seconds_since_last_ping": int(elapsed),
                "interval_sec": INTERVAL_SEC,
                "title": data.get("title", ""),
            }
        )
    )
    return 0


def cmd_record_ping(message: str) -> int:
    data = _load()
    if not data:
        print(json.dumps({"ok": False, "error": "no active loop — run start first"}), file=sys.stderr)
        return 1
    now = time.time()
    data["last_ping_at"] = now
    data.setdefault("pings", []).append({"at": now, "message": message})
    _save(data)
    print(json.dumps({"ok": True, "action": "ping_recorded", "message": message}))
    return 0


def cmd_status() -> int:
    data = _load()
    if not data:
        print(json.dumps({"ok": True, "active": False}))
        return 0
    now = time.time()
    print(
        json.dumps(
            {
                "ok": True,
                "active": True,
                "title": data.get("title"),
                "started_at": data.get("started_at"),
                "seconds_running": int(now - float(data.get("started_at", now))),
                "seconds_since_last_ping": int(now - float(data.get("last_ping_at", now))),
                "interval_sec": INTERVAL_SEC,
                "ping_count": len(data.get("pings", [])),
            }
        )
    )
    return 0


def cmd_done() -> int:
    data = _load()
    if STATE_FILE.is_file():
        STATE_FILE.unlink(missing_ok=True)
    print(json.dumps({"ok": True, "action": "done", "had_active": bool(data)}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Ralph loop state for long OpenClaw tasks")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_start = sub.add_parser("start", help="Begin Ralph loop for a long task")
    p_start.add_argument("title", help="Short task title")

    sub.add_parser("should-ping", help="JSON: true if 5+ min since last ping")

    p_ping = sub.add_parser("record-ping", help="Record that a ping was sent")
    p_ping.add_argument("message", help="What you told Joshua")

    sub.add_parser("status", help="Current loop JSON")
    sub.add_parser("done", help="Clear active loop")

    args = parser.parse_args()
    if args.cmd == "start":
        return cmd_start(args.title)
    if args.cmd == "should-ping":
        return cmd_should_ping()
    if args.cmd == "record-ping":
        return cmd_record_ping(args.message)
    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "done":
        return cmd_done()
    return 1


if __name__ == "__main__":
    sys.exit(main())
