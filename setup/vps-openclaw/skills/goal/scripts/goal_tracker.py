#!/usr/bin/env python3
"""Simple local goal tracker for Felix/OpenClaw."""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s[:48] or "goal"


def workspace_goals_dir() -> Path:
    base = Path.home() / ".openclaw" / "workspace" / "docs" / "goals"
    base.mkdir(parents=True, exist_ok=True)
    return base


def state_path() -> Path:
    return workspace_goals_dir() / "goals.json"


def load_state() -> dict[str, Any]:
    p = state_path()
    if not p.exists():
        return {"goals": []}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("goals"), list):
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return {"goals": []}


def save_state(data: dict[str, Any]) -> None:
    p = state_path()
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_goal_doc(goal: dict[str, Any]) -> str:
    fname = f"{goal['id']}-{slugify(goal['title'])}.md"
    path = workspace_goals_dir() / fname
    body = [
        f"# Goal: {goal['title']}",
        "",
        f"- ID: `{goal['id']}`",
        f"- Status: **{goal['status']}**",
        f"- Created: `{goal['created_at']}`",
    ]
    if goal.get("deadline"):
        body.append(f"- Deadline: `{goal['deadline']}`")
    if goal.get("success"):
        body.extend(["", "## Success Criteria", goal["success"]])
    if goal.get("next_actions"):
        body.extend(["", "## Next Actions"])
        body.extend([f"- {x}" for x in goal["next_actions"]])
    body.extend(["", "## Updates"])
    for upd in goal.get("updates", []):
        body.append(f"- `{upd['at']}` [{upd['status']}] {upd['note']}")
    path.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    return str(path)


def find_goal(goals: list[dict[str, Any]], goal_id: str) -> dict[str, Any] | None:
    for g in goals:
        if g.get("id") == goal_id:
            return g
    return None


def cmd_start(args: argparse.Namespace) -> int:
    data = load_state()
    gid = uuid.uuid4().hex[:8]
    goal = {
        "id": gid,
        "title": args.title.strip(),
        "status": "active",
        "created_at": now_iso(),
        "deadline": args.deadline or "",
        "success": args.success or "",
        "next_actions": args.next or [],
        "updates": [
            {
                "at": now_iso(),
                "status": "active",
                "note": args.note or "Goal created",
            }
        ],
    }
    data["goals"].append(goal)
    save_state(data)
    doc = write_goal_doc(goal)
    print(json.dumps({"ok": True, "action": "start", "id": gid, "doc": doc}))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    data = load_state()
    goal = find_goal(data["goals"], args.id)
    if not goal:
        print(json.dumps({"ok": False, "error": f"goal {args.id} not found"}), file=sys.stderr)
        return 1
    if args.status:
        goal["status"] = args.status
    note = args.note or "Updated"
    goal.setdefault("updates", []).append({"at": now_iso(), "status": goal["status"], "note": note})
    if args.next is not None:
        goal["next_actions"] = args.next
    save_state(data)
    doc = write_goal_doc(goal)
    print(json.dumps({"ok": True, "action": "update", "id": goal["id"], "status": goal["status"], "doc": doc}))
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    data = load_state()
    goal = find_goal(data["goals"], args.id)
    if not goal:
        print(json.dumps({"ok": False, "error": f"goal {args.id} not found"}), file=sys.stderr)
        return 1
    goal["status"] = "done"
    goal.setdefault("updates", []).append(
        {"at": now_iso(), "status": "done", "note": args.note or "Completed"}
    )
    save_state(data)
    doc = write_goal_doc(goal)
    print(json.dumps({"ok": True, "action": "done", "id": goal["id"], "doc": doc}))
    return 0


def cmd_list(_args: argparse.Namespace) -> int:
    data = load_state()
    goals = [
        {
            "id": g.get("id"),
            "title": g.get("title"),
            "status": g.get("status"),
            "deadline": g.get("deadline", ""),
            "created_at": g.get("created_at"),
        }
        for g in data.get("goals", [])
    ]
    print(json.dumps({"ok": True, "goals": goals}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Goal tracker for OpenClaw")
    sp = p.add_subparsers(dest="cmd", required=True)

    p_start = sp.add_parser("start", help="Create a goal")
    p_start.add_argument("title")
    p_start.add_argument("--success", default="", help="Success criteria")
    p_start.add_argument("--deadline", default="", help="Deadline text")
    p_start.add_argument("--note", default="", help="Initial note")
    p_start.add_argument("--next", action="append", help="Next action (repeat)")
    p_start.set_defaults(func=cmd_start)

    p_upd = sp.add_parser("update", help="Update goal status/notes")
    p_upd.add_argument("id")
    p_upd.add_argument("--status", choices=["active", "blocked", "done"])
    p_upd.add_argument("--note", default="")
    p_upd.add_argument("--next", action="append", help="Replace next-actions list")
    p_upd.set_defaults(func=cmd_update)

    p_done = sp.add_parser("done", help="Mark goal done")
    p_done.add_argument("id")
    p_done.add_argument("--note", default="")
    p_done.set_defaults(func=cmd_done)

    p_list = sp.add_parser("list", help="List goals")
    p_list.set_defaults(func=cmd_list)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
