# AI server — Ollama

## Goal

Ollama installed, listening for **Tailscale/VPS** requests, using **GPU** when supported.

## Upstream references (prefer over this file if they differ)

- Install + Linux + systemd + **AMD ROCm tarball**: [docs.ollama.com/linux](https://docs.ollama.com/linux)
- **`OLLAMA_HOST`**, logs, GPU column in `ollama ps`: [docs.ollama.com/faq](https://docs.ollama.com/faq)
- Doc index for agents: [docs.ollama.com/llms.txt](https://docs.ollama.com/llms.txt)

## Install

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Same command as [ollama.com/download/linux](https://ollama.com/download/linux). Re-run the script to **upgrade** Ollama later.

## Listen on all interfaces (required for VPS → KUBB)

Ollama binds **127.0.0.1:11434** by default. For the VPS to reach Ollama over Tailscale, set **`OLLAMA_HOST`** per the [FAQ — configure Ollama server (Linux)](https://docs.ollama.com/faq#how-do-i-configure-ollama-server).

1. Open a systemd drop-in:

```bash
sudo systemctl edit ollama.service
```

2. In the editor, add:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

3. Apply:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

4. Confirm:

```bash
ss -tlnp | grep 11434
```

You should see `0.0.0.0:11434` (or similar), not only `127.0.0.1`.

5. If something fails, check service logs:

```bash
journalctl -e -u ollama
```

## Firewall (if you use `ufw`)

Allow only **Tailscale** interface if possible; at minimum do **not** expose `11434` on the public WAN.

Example (rough — adjust interface name `tailscale0`):

```bash
sudo ufw allow in on tailscale0 to any port 11434 proto tcp
sudo ufw enable
```

See [../06-security/README.md](../06-security/README.md).

## GPU (AMD Radeon on Ryzen AI Max)

- Official Linux path: optional **ROCm** bundle + driver notes on [docs.ollama.com/linux](https://docs.ollama.com/linux) (AMD GPU / ROCm sections).
- After loading a model, run `ollama ps` — the **Processor** column (`100% GPU`, `100% CPU`, or split) is documented in the [FAQ](https://docs.ollama.com/faq#how-can-i-tell-if-my-model-was-loaded-onto-the-gpu).
- If everything stays on CPU, large models will be **very slow** — finish GPU acceleration before relying on 72B day-to-day.

## Quick test

```bash
ollama run llama3.2:3b "say hi in one sentence"
```

(Any small model is fine if `llama3` is not available.)

## Verification

- [ ] `ollama --version` works.
- [ ] `curl -s http://127.0.0.1:11434/api/tags` returns JSON.
- [ ] From **another Tailscale node** (e.g. laptop): `curl -s http://<KUBB_TAILSCALE_IP>:11434/api/tags` works.

## Next

[../04-models/README.md](../04-models/README.md)
