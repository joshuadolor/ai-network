---
name: lead-site-pipeline
description: Trial workflow — find local businesses without websites, gather a lead pack, build a static HTML site, ngrok preview to Joshua. No outreach or publish without approved.
user-invocable: true
---

# Lead → site pipeline (trial)

End-to-end **trial** for DLR: research leads → build draft site → preview via ngrok. Production outreach, DNS, and client handoff are **later phases**.

## Phases (follow in order)

### Phase 1 — Research (`deep-research`)

Joshua provides: **geo** (city/area), **niche** (e.g. plumbers, salons), optional **count** (default 3–5 for trial).

1. Use skill **deep-research** with focus **businesses without websites**:
   - Queries: `"<niche> <city>"`, Maps/listings, `"no website"`, Facebook-only presence, directory pages.
   - Verify: no real business domain (social-only ≠ website).
2. For each lead create:

```
workspace/docs/leads/<slug>/
  lead.json          # schema in ui-ux-build
  research.md        # sources, evidence, screenshots notes
  assets/            # logos/photos only if legally public; else placeholders
```

3. **Gather resources** for Phase 2: category copy angles, competitor site patterns (structure only, no copy-paste), stock/placeholder image URLs, color hints from niche.

Deliver: table in Discord + paths. Use completion report template.

### Phase 2 — Build (`ui-ux-build` + `cn-html-design`)

For each approved lead (trial: Joshua may say **build all** or name slugs):

1. Read lead pack — **no invented facts**.
2. Apply **cn-html-design** (or installed **frontend-design**).
3. Write `site/index.html` under the lead folder.

### Phase 3 — Preview (`site-preview-ngrok`)

1. Use skill **site-preview-ngrok** — `exec` its `site_preview.py --dir workspace/docs/leads/<slug>/site`.
2. Send Joshua the **https ngrok URL** in completion report.
3. Optional: **ui-ux-review** on that URL; fix low-stakes issues.

### Phase 4 — Gate (mandatory)

| Action | Allowed in trial? |
|--------|-------------------|
| ngrok preview to Joshua | ✅ |
| Save drafts in workspace | ✅ |
| Email/call the business | ❌ |
| Buy domain / DNS / Hostinger deploy | ❌ until **approved** |
| Claim site is live | ❌ |

When Joshua says **approved** for a lead → future skill/deploy step (not in trial).

## Joshua triggers

- `run lead site trial for <niche> in <city>`
- `build site for lead <slug>`
- `preview lead <slug>`

## Models

- Research synthesis: **heavy** if many leads; else 32b.
- HTML build: 32b or **heavy** for polish.
- Cron batch: **7b** only for short listing scans — full pipeline is interactive.

## Skills used (do not substitute)

| Phase | Skill |
|-------|--------|
| 1 | **deep-research** |
| 2 | **cn-html-design**, **ui-ux-build** |
| 3 | **site-preview-ngrok** |
| Orchestration | **this skill** |

If a skill is missing from disk, run `update-vps-openclaw.sh` — do not hallucinate commands.
