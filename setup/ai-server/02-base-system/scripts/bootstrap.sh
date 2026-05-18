#!/usr/bin/env bash
set -euo pipefail

echo "==> APT update & upgrade"
sudo apt update
sudo apt upgrade -y

echo "==> Base packages"
sudo apt install -y git curl wget htop ca-certificates build-essential

echo "==> Done. Reboot if the upgrade installed a new kernel."
echo "    uname -r"
