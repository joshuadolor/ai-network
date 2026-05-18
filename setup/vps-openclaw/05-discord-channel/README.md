# OpenClaw — Discord channel

This is how you talk to your bot. **Discord is the chosen channel** for this setup; Telegram/WhatsApp are not used.

## Official source of truth

- [Discord channel doc](https://docs.openclaw.ai/channels/discord) — copy commands from there if anything below ever drifts.
- [Pairing](https://docs.openclaw.ai/channels/pairing)
- [Channel troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)

## What you will end up with

- A **Discord application + bot** in your own private server.
- A `.env` (or hPanel field) holding `DISCORD_BOT_TOKEN`.
- An OpenClaw config patch enabling the **Discord** channel.
- DMs working with your bot, optionally also a **guild workspace** (each Discord channel = its own agent session/context).

---

## 1. Create a Discord server (private)

If you do not already have one, create a server **for you and your bot**: [How to create a server](https://support.discord.com/hc/en-us/articles/204849977) → *Create My Own → For me and my friends*.

## 2. Create the bot in the Developer Portal

1. Open the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**, call it `OpenClaw` (or whatever).
2. **Bot** tab → set the username to your agent's name.
3. **Privileged Gateway Intents** — enable:
   - **Message Content Intent** (required)
   - **Server Members Intent** (recommended; required for role allowlists / name-to-ID matching)
   - **Presence Intent** (optional)
4. **Reset Token** → copy it. **This is your bot token.** Save it in a password manager — *never paste it into chat*.

## 3. Invite the bot to your server

1. **OAuth2** tab → *OAuth2 URL Generator*. Enable scopes:
   - `bot`
   - `applications.commands`
2. **Bot Permissions** that appear — minimum:
   - General: **View Channels**
   - Text: **Send Messages**, **Read Message History**, **Embed Links**, **Attach Files**, *(optional: Add Reactions)*
   - If you'll use **threads/forum/media channels**, also enable **Send Messages in Threads**.
3. Copy the generated URL → paste into your browser → choose your server → **Continue/Authorize**.

## 4. Collect IDs (Developer Mode)

1. In the Discord client, **User Settings → Advanced → Developer Mode = ON**.
2. Right-click **your server icon → Copy Server ID**.
3. Right-click **your own avatar → Copy User ID**.

Keep both alongside the bot token.

## 5. Allow your bot to DM you

Right-click your **server icon → Privacy Settings → Direct Messages = ON**.  
You can turn this off later if you only intend to use guild channels.

## 6. Put the token on the OpenClaw VPS

Pick the path that matches how you installed OpenClaw ([`../01-install/README.md`](../01-install/README.md)).

### Option A or B — Hostinger managed (1-Click or Docker template)

In **hPanel → OpenClaw / Docker Manager**:

- Add an environment variable **`DISCORD_BOT_TOKEN`** = your bot token (use the secrets/env field if available; otherwise the container env).
- Apply / restart the container.

If hPanel does not expose env vars directly for the OpenClaw template, store the token in **`~/.openclaw/.env`** on the VPS (SSH session) and rely on the SecretRef pattern below.

### Option C — Plain Ubuntu (SSH)

```bash
# 1. Put the token in ~/.openclaw/.env so the systemd user service can resolve it after restart
mkdir -p ~/.openclaw
grep -q '^DISCORD_BOT_TOKEN=' ~/.openclaw/.env 2>/dev/null \
  || echo 'DISCORD_BOT_TOKEN=PASTE_YOUR_BOT_TOKEN_HERE' >> ~/.openclaw/.env
chmod 600 ~/.openclaw/.env
# 2. Apply the channel config
export DISCORD_BOT_TOKEN="$(grep ^DISCORD_BOT_TOKEN= ~/.openclaw/.env | cut -d= -f2-)"

cat > /tmp/discord.patch.json5 <<'JSON5'
{
  channels: {
    discord: {
      enabled: true,
      token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN" }
    }
  }
}
JSON5

openclaw config patch --file /tmp/discord.patch.json5 --dry-run
openclaw config patch --file /tmp/discord.patch.json5
openclaw gateway restart
```

> If your VPS sometimes hits Discord's startup application lookup limit, also set `channels.discord.applicationId` to your **Application ID** from the Developer Portal so OpenClaw can skip that REST call.

## 7. Pair the bot to OpenClaw

1. After the gateway restarts, **DM your bot** in Discord — it will reply with a **pairing code**.
2. Approve it from a CLI on the VPS:

```bash
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

Pairing codes expire in **1 hour**.

You should now be able to chat with your agent in Discord DMs.

## 8. (Optional) Use your Discord server as a workspace

Each Discord channel becomes its own agent session/context.

```json5
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        YOUR_SERVER_ID: {}
      }
    }
  }
}
```

Apply it the same way (`openclaw config patch --file ...`).

## 9. Verify

```bash
openclaw doctor
openclaw gateway status
openclaw pairing list discord
```

- [ ] Bot reachable in DMs.
- [ ] (Optional) Bot reachable in your allowlisted guild.
- [ ] Memory + dreaming working ([`../02-memory/README.md`](../02-memory/README.md), [`../03-dreaming/README.md`](../03-dreaming/README.md)).

## Troubleshooting

- **Bot offline / not responding:** check `openclaw gateway status`, then logs (Docker Manager or `journalctl --user -u openclaw-gateway.service`). Confirm the **bot token** is still valid in the Developer Portal.
- **Privileged intents missing:** without **Message Content Intent**, the bot cannot read what you write. Re-enable it and restart.
- **DM "Bot is not allowed to send DMs":** server **Privacy Settings → Direct Messages** must be ON.
- **Pairing code never arrives:** verify you DM'd the *correct* bot user and that the gateway has actually restarted with the Discord config patch applied.

---

## Multiple Discord bots later (optional)

The official doc supports per-account tokens and Application IDs. Pattern (place under `channels.discord.accounts`):

```json5
{
  channels: {
    discord: {
      enabled: true,
      accounts: {
        personal: {
          token: { source: "env", provider: "default", id: "DISCORD_PERSONAL_TOKEN" },
          applicationId: "111111111111111111"
        },
        work: {
          token: { source: "env", provider: "default", id: "DISCORD_WORK_TOKEN" },
          applicationId: "222222222222222222"
        }
      }
    }
  }
}
```
