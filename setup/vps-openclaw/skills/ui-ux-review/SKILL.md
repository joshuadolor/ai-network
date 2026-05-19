---
name: ui-ux-review
description: UX and UI critique — flows, hierarchy, accessibility, and actionable fixes. Use for landing pages, apps, and Discord/web layouts before ship.
user-invocable: true
---

# UI / UX review

## When to use

Joshua shares a URL, screenshot, Figma link, or component description and wants **clear, prioritized** design feedback — not vague "looks nice."

## Workflow

1. **Goal** — user job, primary CTA, success metric (one sentence).
2. **Evidence**
   - **URL:** `browser` tool (profile `openclaw`) — snapshot at desktop width; second pass mobile if layout matters.
   - **Screenshot / file:** analyze what Joshua attached; ask for missing states (empty, error, loading).
3. **Review dimensions** (score 1–5 briefly each):
   - Visual hierarchy and scan path
   - Typography, spacing, consistency
   - Color contrast (WCAG AA target)
   - Forms, errors, focus states
   - Navigation and wayfinding
   - Performance perception (skeletons, layout shift)
   - Copy / microcopy clarity
4. **Output format**
   - **Top 3 wins** (quick)
   - **Top 5 fixes** (ordered: impact × effort)
   - **Accessibility** blockers (if any)
   - **Optional:** wireframe-level suggestion in ASCII or bullet layout — not full Figma unless asked
5. **Save** substantial reviews to `workspace/docs/ux-review-YYYY-MM-DD-<slug>.md`.

## Boundaries

- Do not claim legal compliance (GDPR, etc.) — flag "needs human review."
- Do not push live CSS/deploy without Joshua's **approved**.
- For **code changes**, note file paths if repo context exists; delegate heavy frontend to Byte when that agent is online.

## Pair with

- **deep-research** — competitor / pattern research
- **ui-ux-build** + **cn-html-design** — build trial sites; this skill reviews the ngrok URL
- **lead-site-pipeline** — full trial workflow
- **local-image-gen** — hero / thumbnail concepts after UX direction is set
