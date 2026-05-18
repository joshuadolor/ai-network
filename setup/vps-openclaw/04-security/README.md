# OpenClaw VPS — security

## References

- [Gateway security](https://docs.openclaw.ai/gateway/security)
- [Linux server — Harden admin access first](https://docs.openclaw.ai/vps)
- [Authentication](https://docs.openclaw.ai/gateway/authentication)
- [Remote access](https://docs.openclaw.ai/gateway/remote) · [Tailscale](https://docs.openclaw.ai/gateway/tailscale)
- [Secrets management](https://docs.openclaw.ai/gateway/secrets)

## Principles

- **One purpose per VPS.** This box is **only** for OpenClaw — no Open WebUI, no random Docker apps. That stays on [../../vps-apps/README.md](../../vps-apps/README.md).
- **Loopback by default.** Where possible, keep the gateway bound to localhost and reach the dashboard via **SSH tunnel** or **Tailscale Serve**.
- **Public ports = surface area.** If you must expose a port, gate it with `gateway.auth.token` or `gateway.auth.password`.
- **Tailscale-only admin.** Join the VPS to your tailnet, verify a second SSH session over the Tailscale IP / MagicDNS, then restrict public SSH.

## Checklist

- [ ] **SSH:** key-based login, password auth disabled (`/etc/ssh/sshd_config`).
- [ ] **Firewall (`ufw` or hPanel):** only the ports you need; prefer `allow in on tailscale0` patterns.
- [ ] **Gateway exposure:** loopback by default; if exposed, **token or password auth** is set.
- [ ] **Secrets:** API keys / **Discord bot token** stored via the gateway secrets surface (env var or `~/.openclaw/.env`), not pasted in repo files, **SOUL.md / AGENTS.md / USER.md**, or chat ([workspace files](../08-workspace/README.md#secrets-workspace-vs-openclawenv)).
- [ ] **Tailscale ACLs (later):** restrict which devices can reach the gateway port.
- [ ] **Updates:** `sudo apt update && sudo apt upgrade -y` on a schedule; OpenClaw via `openclaw update` (or hPanel **Update** in Docker Manager).

## OpenClaw users / channels

- [ ] **Discord** channel verified end-to-end ([../05-discord-channel/README.md](../05-discord-channel/README.md)).
- [ ] **Discord bot token** stored as `DISCORD_BOT_TOKEN` (env var or `~/.openclaw/.env`), **never** committed.
- [ ] **Gateway token** stored in a password manager.
- [ ] If multiple humans will message OpenClaw, decide whether you want a **shared agent** or **per-user agents** ([Linux server — shared company agent](https://docs.openclaw.ai/vps)).

## Done

Continue routine VPS maintenance with your other services. The chat UI users (you, your wife) live on the apps VPS: [../../vps-apps/03-security/README.md](../../vps-apps/03-security/README.md).
