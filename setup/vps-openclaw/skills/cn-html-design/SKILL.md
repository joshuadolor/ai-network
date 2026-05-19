---
name: cn-html-design
description: High-quality single-file HTML landing pages (中文落地页风格). Use ClawHub frontend-design when installed; otherwise follow this skill exactly. Pair with ui-ux-build and lead-site-pipeline.
user-invocable: true
---

# CN HTML design (高颜值落地页)

## Install the community skill (VPS, once)

Chinese OpenClaw docs commonly use **frontend-design** (steipete) for production-grade, non-generic UI:

```bash
cd ~/AINetwork
bash setup/vps-openclaw/scripts/install-clawhub-skills.sh
```

Or manually:

```bash
npx clawhub@latest install steipete/frontend-design
# or: clawhub install steipete/frontend-design
```

Enable in `~/.openclaw/openclaw.json` under `skills.entries` if your build requires it. Re-run `update-vps-openclaw.sh --config-merge --restart`.

**If `frontend-design` is installed:** read and follow **that** skill’s SKILL.md for all HTML/CSS work — this file is fallback only.

**If not installed:** follow the rules below (do not improvise a different stack).

## Output contract (trial sites)

Deliver **one folder per business**:

```
workspace/docs/leads/<lead-slug>/site/
  index.html      # semantic HTML5, self-contained
  assets/         # optional images (placeholders OK)
  README.md       # 1 paragraph: stack, fonts, colors used
```

- **Single-page** landing: hero, services, about, contact, footer CTA.
- **Mobile-first** responsive CSS (no build step required for trial).
- **No** React/Vue/npm unless Joshua explicitly asks.
- **Language:** match lead locale (English or 中文 as appropriate).
- **Accessibility:** contrast, `alt` on images, focus states, logical heading order.

## Design principles (中文社区常用 — avoid “AI slop”)

1. **Clear visual hierarchy** — one primary CTA above the fold.
2. **Typography** — one display + one body font (Google Fonts CDN OK); avoid Inter/Roboto-only defaults without reason.
3. **Color** — intentional palette (primary + neutral + one accent); not purple-gradient-on-white cliché.
4. **Whitespace** — generous section padding; readable line length (~65ch).
5. **Trust** — phone, address, hours, map link placeholder if data exists in lead pack.
6. **Performance** — minimal JS; prefer CSS; images compressed or placeholder.

## Data source

Only use facts from the lead pack (`workspace/docs/leads/<slug>/lead.json` or `research.md`). **Do not invent** addresses, awards, or reviews.

## Boundaries

- Trial / draft — not live customer domain until Joshua **approved** publish.
- No scraping competitor sites for copy-paste; paraphrase positioning only.

## Pair with

- **ui-ux-build** — generates files from lead pack
- **site-preview-ngrok** — shares preview URL with Joshua
- **lead-site-pipeline** — end-to-end trial workflow
