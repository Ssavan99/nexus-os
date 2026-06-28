# Nexus OS — Master Plan (living document)

> **Purpose:** the single, durable reference for *what we are building and in what order*, so any agent (Claude Code, Codex, claude.ai, ChatGPT) can pick up the work in a fresh session/chat. When context windows fill or you switch tools, point the agent here.
>
> **Canonical copy:** this file in the Nexus OS repo. **Cross-agent copy:** mirrored as a brain page so cloud agents (claude.ai/ChatGPT), which only see the brain (not the repo), can retrieve it via GBrain search. Keep the two in sync; the repo copy wins on conflict.
>
> Last updated: 2026-06-27.

## Where things live (so agents read the right place)

- **Repo (`/Users/ssavan99/repos/nexus-os`)** — workflows, schemas, roadmap, decision log, scripts. Visible to **local** agents (Codex, Claude Code).
- **Private vault (`/Users/ssavan99/Desktop/Personal-Obsidian`)** — source-of-truth Markdown brain (raw/, wiki/, inbox/). Indexed by GBrain.
- **GBrain (local Postgres engine)** — memory/search/MCP for ALL agents. Cloud agents see ONLY this (read-only).
- **Always-on connector** — `gbrain serve --http` + ngrok static URL under launchd; claude.ai + ChatGPT connect read-only.

## Current state (done)

- **Phase 2 complete** — all agents share one brain: Codex + Claude Code (raw local stdio, full access); claude.ai + ChatGPT (read-only via one always-on HTTP MCP, OAuth `read` scope, auto-start at login).
- **Engine** — migrated PGLite → **local Postgres** (crash-safe, concurrent); auto-starts via brew service.
- **Embeddings** — local Ollama `nomic-embed-text` (768d); 299/299 chunks; semantic search live; $0/private.
- **Phase 3 foundation** — coverage gap mapped (20/48 raw un-integrated); weekly-checklist engine spec written (`docs/workflows/weekly-checklist-engine.md`).

## The 3 goal-categories (the lens for everything)

| # | Category | Outcome | Phases | Status |
|---|---|---|---|---|
| 1 | **Startup loops** | Automated loops: development, networking, customer discovery, sales | 3 + 5 | Material mostly captured; activate via checklist engine |
| 2 | **Job system** | Application tracking board; auto-apply N Greenhouse roles/24h with tailored resume; FAANG/Fortune-250 referral alerts before manual apply | 4 + 3 + execution | Blocked on capturing job reels; most automation-heavy; human-gated |
| 3 | **Improve Nexus/GBrain** | Complete phases; presentable/open-source; team-ready; evolve toward no-prompt (loop + harness engineering) | 6 + polish | Foundation + incremental |

## Unifying primitive — Weekly Checklist Engine (heart of Phase 3)

Both Startup and Job plug into this. Per-area **implementation backlog** (priority-ordered, derived from resources) → **done/archive** → an auto-generated **weekly combined checklist** the user reviews once a week → later **exportable to Notion/Jira/Trello**. Two item kinds: **(1, build first)** implementation/setup tasks ("set up auto-apply system", "run LLM council on the idea", "revise LinkedIn", "find investors/founders to reach out"); **(2, later)** recurring ops ("apply X jobs/week", "reach N people/week"). Full spec: `docs/workflows/weekly-checklist-engine.md`.

## Sequence

### NOW — Foundation primitive
1. ✅ Map raw→wiki coverage gap.
2. ✅ Engine spec.
3. ✅ Local embeddings.
4. ⬜ Generate first artifacts: startup area backlog + first weekly checklist (vault writes, user-approved). Job area stub waits on capture.
5. ⬜ Confirm "show/refresh my weekly checklist" runs from every agent.

### THEN — Category 2: Job system (capture-first)
1. Make IG-reel capture **repeatable** (saved reel → vault → brain), then run it on the job reels (Phase 4).
2. Job-search workflow + backlog (the job twin of `founder-operating-system`).
3. Application tracking board (Markdown/brain records; Notion-exportable).
4. Automation, **human-gated**: Apify/Greenhouse scrape roles ≤24h → tailor resume → queue for approval before submit; separate referral-alert path for FAANG/Fortune-250. Flags: job-site ToS, human-in-the-loop on submit.

### ONGOING — Category 1: Startup loops
Activate existing playbooks via the engine: customer discovery, build/launch, networking, sales; run the weekly evidence loop already in `founder-operating-system`. Little new capture.

### LATER — Category 3: System evolution (incremental)
- **Docs:** professional README + a separate terse tips/tricks doc + de-clutter current docs.
- **Dedup pass:** flag notes that add nothing; delete on approval.
- **Open-source prep:** license, contributor docs, secrets hygiene (already good).
- **Team / Notion:** personal vault stays private per-person; **Notion = shared team layer** (tracking, meetings, boards); checklist engine exports there.
- **Shared writeback** (open decision): today cloud agents are read-only; local agents write. A reviewed/scoped cloud-write path is a future architecture decision.
- **Multi-agent + OSS models:** premium models (Claude/ChatGPT) for planning + PR review; open-source/local models for bulk dev/execution.
- **Omnigent (Databricks, OSS meta-harness):** orchestrates Claude Code/Codex/Pi with portable context, policy + async approvals, sandbox, web/mobile UI. Strong candidate for the Category-3 orchestration + UI + human-approval layer; leverages subscription-backed harnesses (not paid API). Evaluate after foundation (alpha).
- **UI:** don't build custom soon — Obsidian (vault) + GBrain `/admin` + native chat apps cover it; neither Claude nor ChatGPT exposes subscription models to external API, so a custom app can't cheaply wrap them. Let Omnigent/GBrain-admin be the UI later.
- **Agent operating convention:** treat the brain as ONE source, combined with web + model reasoning — not brain-in-isolation. (Add to agent docs.)
- **Social-media video pipeline** (loose-note): user voice/image → daily AI videos for startup identity. Later marketing automation.
- **Embeddings:** done (local). Revisit API only if scale/quality ever demands.

## Guardrails (carry across all work)

- Public repo vs private vault boundary; never commit private brain content.
- Cloud surfaces are **read-only** (`read` scope, server-enforced); raw stdio MCP stays local-only.
- Vault writes only on explicit user approval.
- Stop the always-on server gracefully (`launchctl unload`), not `kill -9` (Postgres makes this safe now, but still).
- Don't duplicate GBrain (no custom search/RAG/MCP/cron engine in Nexus OS).
- Don't over-build Category 3 (no-prompt/harness/Omnigent) before Categories 1 & 2 deliver value manually.

## Pointers

- Phase overview: `docs/roadmap.md`
- Architecture: `docs/architecture.md`
- Decisions (chronological): `docs/decision-log.md`
- Checklist engine spec: `docs/workflows/weekly-checklist-engine.md`
- Cloud connector ops: `docs/claude-chat-gbrain-plan.md`, `docs/chatgpt-readonly-connector.md`
