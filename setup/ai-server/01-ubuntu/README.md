# AI server — Install Ubuntu (bare metal)

## Goal

Ubuntu as the **only** OS on the KUBB OCTO (Windows removed).

## Steps

1. Boot from the USB installer (BIOS boot menu / one-time boot key per machine).
2. Choose **Install Ubuntu**.
3. When asked about disk: **Erase disk and install Ubuntu** (full wipe).
4. Create your **user account** and **strong password**.
5. Enable **Install third-party drivers** if the installer offers it (helps Wi‑Fi / GPU firmware).
6. Finish install, reboot, remove USB.

## First login

- Run **Software Updater** or open a terminal and run updates (the [base-system bootstrap script](../02-base-system/README.md) does this too).
- Confirm **network** works (`ping -c 3 1.1.1.1`).

## Verification

- [ ] `lsb_release -a` shows Ubuntu 22.04 or 24.04 (or newer LTS).
- [ ] You can `ping` the internet.
- [ ] `sudo` works for your user.

## Next

[../02-base-system/README.md](../02-base-system/README.md)
