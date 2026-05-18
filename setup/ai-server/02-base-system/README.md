# AI server — Base system packages

## Goal

Updated system and common CLI tools used in later steps.

## Option A — Run the script (recommended)

From this repo on the KUBB (clone repo with git, or copy the script over):

```bash
chmod +x setup/ai-server/02-base-system/scripts/bootstrap.sh
./setup/ai-server/02-base-system/scripts/bootstrap.sh
```

## Option B — Manual commands

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget htop ca-certificates build-essential
```

## Verification

- [ ] `git --version`, `curl --version` work.
- [ ] No pending critical errors from `apt upgrade`.

## Put this repo on the KUBB

Clone (replace URL with yours) or copy the `setup/` folder from USB:

```bash
git clone <YOUR_REPO_URL> AINetwork
cd AINetwork
```

## Next

Docker is optional on **KUBB** if you only run Ollama natively. You **do** need Docker (or similar) on the **VPS** for Open WebUI.

- **This machine only:** skip to [../03-ollama/README.md](../03-ollama/README.md) (optional: install Docker on the AI server only if you want containers here).
- **Hostinger VPS:** Docker is in [../../vps/01-docker/README.md](../../vps/01-docker/README.md).
