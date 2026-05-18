# AI server — Image & video (optional, Python)

## Upstream references

- PyTorch install selector: [pytorch.org](https://pytorch.org/)
- Hugging Face Diffusers: [huggingface.co/docs/diffusers](https://huggingface.co/docs/diffusers)

## Goal

Separate **Python venv** for Stable Diffusion XL / AnimateDiff-style workflows without breaking system Python.

## Prereqs (Ubuntu)

```bash
sudo apt install -y python3-venv python3-pip
```

## Create a project directory and venv

```bash
mkdir -p ~/ai-diffusion && cd ~/ai-diffusion
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install diffusers transformers accelerate torch --extra-index-url https://download.pytorch.org/whl/cpu
```

> **Note:** The `torch` line above is **CPU** wheels for maximum compatibility. For **AMD GPU** on Linux you must follow **current** PyTorch + ROCm docs for your GPU generation; that stack changes often — do not treat this README as the source of truth for ROCm.

## Expectations

- **SDXL:** heavy; needs a good GPU path for pleasant speed.
- **AnimateDiff:** short clips only; not cloud “Kling” quality.

## Verification

- [ ] `python -c "import diffusers; print(diffusers.__version__)"` works inside the venv.

## Next

[../../network-tailscale/README.md](../../network-tailscale/README.md)
