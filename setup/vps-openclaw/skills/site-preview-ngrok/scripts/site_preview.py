#!/usr/bin/env python3
"""Serve a static directory and expose via ngrok. Trial previews for lead sites."""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

STATE_DIR = Path(os.environ.get("OPENCLAW_STATE_DIR", Path.home() / ".openclaw"))
PID_FILE = STATE_DIR / "preview-http.pid"
NGROK_PID_FILE = STATE_DIR / "preview-ngrok.pid"
PORT_FILE = STATE_DIR / "preview-port.txt"


def _read_pid(path: Path) -> int | None:
    if not path.is_file():
        return None
    try:
        return int(path.read_text().strip())
    except (ValueError, OSError):
        return None


def _kill(pid: int | None, sig: int = signal.SIGTERM) -> None:
    if pid is None:
        return
    try:
        os.kill(pid, sig)
    except ProcessLookupError:
        pass


def stop_preview() -> int:
    _kill(_read_pid(NGROK_PID_FILE))
    _kill(_read_pid(PID_FILE))
    for f in (PID_FILE, NGROK_PID_FILE, PORT_FILE):
        f.unlink(missing_ok=True)
    print(json.dumps({"status": "stopped"}))
    return 0


def _wait_ngrok_url(timeout: float = 25.0) -> str | None:
    deadline = time.time() + timeout
    api = "http://127.0.0.1:4040/api/tunnels"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(api, timeout=2) as resp:
                data = json.loads(resp.read().decode())
            for tunnel in data.get("tunnels", []):
                url = tunnel.get("public_url") or ""
                if url.startswith("https://"):
                    return url
        except (urllib.error.URLError, OSError, json.JSONDecodeError):
            pass
        time.sleep(0.5)
    return None


def start_preview(site_dir: Path, port: int) -> int:
    if not (site_dir / "index.html").is_file():
        print(f"error: missing {site_dir}/index.html", file=sys.stderr)
        return 1
    token = os.environ.get("NGROK_AUTHTOKEN", "").strip()
    if not token:
        print("error: NGROK_AUTHTOKEN not set", file=sys.stderr)
        return 2

    stop_preview()

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ngrok", "config", "add-authtoken", token],
        check=False,
        capture_output=True,
    )

    http = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=str(site_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    PID_FILE.write_text(str(http.pid))
    PORT_FILE.write_text(str(port))

    ngrok = subprocess.Popen(
        ["ngrok", "http", str(port), "--log=stdout"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    NGROK_PID_FILE.write_text(str(ngrok.pid))

    url = _wait_ngrok_url()
    if not url:
        print(
            json.dumps(
                {
                    "status": "partial",
                    "port": port,
                    "local": f"http://127.0.0.1:{port}",
                    "error": "ngrok URL not ready — check ngrok dashboard or 4040 API",
                }
            )
        )
        return 3

    print(json.dumps({"status": "ok", "url": url, "port": port, "dir": str(site_dir)}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Static site + ngrok preview")
    parser.add_argument("--dir", type=Path, help="Site folder with index.html")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--stop", action="store_true")
    args = parser.parse_args()
    if args.stop:
        return stop_preview()
    if not args.dir:
        parser.error("--dir required unless --stop")
    return start_preview(args.dir.resolve(), args.port)


if __name__ == "__main__":
    sys.exit(main())
