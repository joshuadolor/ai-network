---
name: ui-ux-build
description: Build a static trial landing site from a lead research pack. Uses cn-html-design rules. Does not publish to production or contact the business without approval.
user-invocable: true
---

# UI/UX build (static site from lead pack)

## When to use

After **deep-research** (or **lead-site-pipeline** phase 1) produced a lead folder under `workspace/docs/leads/<slug>/`.

## Prerequisites

- Lead folder contains at least `lead.json` or `research.md` with business name, category, location, contact hints.
- Skill **cn-html-design** (or installed **frontend-design**) governs HTML quality.

## Workflow

1. Read `workspace/docs/leads/<slug>/lead.json` (create from research if missing).
2. Follow **cn-html-design** (or **frontend-design** if installed) — write `site/index.html` + optional `assets/`.
3. Add `site/README.md` (palette, fonts, sections).
4. Run **site-preview-ngrok** — pass Joshua the public URL in the completion report.
5. Run **ui-ux-review** on the ngrok URL (self-critique); fix obvious issues if low-stakes.
6. **Stop** — do not email the business, buy domains, or deploy to Hostinger without Joshua **approved**.

## lead.json schema (minimal)

```json
{
  "businessName": "",
  "category": "",
  "location": "",
  "phone": "",
  "email": "",
  "hasWebsite": false,
  "notes": "",
  "sources": []
}
```

## Output

Post completion report (AGENTS.md) with path + ngrok URL.

## Pair with

- **lead-site-pipeline** — orchestrator
- **ui-ux-review** — critique after build
