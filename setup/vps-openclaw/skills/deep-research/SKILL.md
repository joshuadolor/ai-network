---
name: deep-research
description: Multi-step research with web search, synthesis, and saved briefs. Use for market scans, competitor analysis, AI news digests, and "go deep" questions.
user-invocable: true
---

# Deep research

## When to use

Joshua asks for thorough research, not a one-line answer: trends, comparisons, "what should I know about X", prep for decisions.

Also use for **lead-site-pipeline** phase 1: local businesses **without a real website** (see section below).

## Workflow

1. **Clarify** (one short message if needed): topic, depth, audience, deadline.
2. **Search** — use gateway **web search** (DuckDuckGo). Run **3–6 distinct queries** (synonyms, competitors, "2025 2026", site-specific if useful).
3. **Browser** — only if search is thin or a primary source must be read (paywalls, docs). Snapshot → extract → cite URL.
4. **Synthesize** — for long reports, ask Joshua to use **heavy** (`ollama/qwen2.5:72b`) or switch model before the final write-up.
5. **Deliver** in Discord:
   - **Executive summary** (3–5 bullets)
   - **Findings** (grouped headings)
   - **Sources** (linked titles or URLs)
   - **Open questions / risks**
6. **Persist** — save the full brief to `workspace/docs/research-YYYY-MM-DD-<slug>.md` and note the path in chat.

## Quality bar

- Prefer **primary** or **official** sources for facts; label speculation.
- Call out **conflicts** between sources.
- No fabricated citations — if unsure, say so.
- Never paste secrets or full paywalled content.

## Cron / recurring digests

If Joshua wants this **daily or weekly**, do **not** promise in chat only — create a cron job (`openclaw cron add`, model **7b**, `--timeout-seconds 300`, deliver to the agreed Discord channel). See skill **proactive-ops** and `reference/CRON-EXAMPLES.md`.

## Businesses without websites (lead gen)

When Joshua runs **lead-site-pipeline** or asks for leads:

1. Get **city/region** + **niche** (e.g. "barber Manila", "plumber Quezon City").
2. Search listings (Maps, directories, Facebook pages, local guides). Prefer **verifiable** name + address + phone.
3. **No website** means: no dedicated business domain; Instagram/Facebook-only counts as **no site** for this workflow.
4. Per lead, write `workspace/docs/leads/<slug>/`:
   - `lead.json` — see **ui-ux-build** schema
   - `research.md` — how you verified, source URLs, competitor notes, copy angles
   - `assets/README.md` — what to use (placeholders if no licensed images)
5. Deliver a short table: name | category | contact | website status | folder path.
6. Do **not** contact businesses or claim you built their site yet.

## Model hints

| Task | Model |
|------|--------|
| Quick scan | `ollama/qwen2.5:7b` or default 32b |
| Final synthesis / strategy | `heavy` / 72b |
| Lead pack (5+ businesses) | `heavy` recommended |
