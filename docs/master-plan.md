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

**Current single focus: complete the Nexus system (v1 → straight into v2).** Rationale: the user works best finishing one thing fully before starting another; Nexus is already mid-build, so we finish it end-to-end (core + nice infrastructure + easy accessibility/UI) before doing deep startup/job *execution*. Implement the full Nexus vision, dropping only pieces we jointly decide aren't worth it (e.g. possibly loop engineering). **Parked until Nexus is complete:** Startup execution (plan captured in `wiki/areas/startups/backlog.md`, idea TBD in Claude chat) and the Job system (job reels to be uploaded when possible).

### Foundation — done
1. ✅ raw→wiki coverage gap mapped · 2. ✅ engine spec · 3. ✅ local embeddings · 4. ✅ startup backlog generated (weekly checklist deferred until execution).

### Nexus v1 — COMPLETE (2026-07-01)
1. ✅ **Vault → brain sync** — `gbrain import` under launchd (`scripts/nexus-brain-sync.sh`, every 5 min + login); no git (Drive-safe); idempotent; verified picking up new notes.
2. ✅ **Capture pipeline** — `docs/workflows/capture-pipeline.md`; handles all post/reel types (caption/transcript/screenshot/URL) with a mandatory content summary.
3. ✅ **Runnable checklist engine** — workflows mirrored to the brain (`wiki/areas/nexus-os/workflows.md`) with trigger phrases; any agent (incl. cloud) can run capture + checklist.
4. ✅ **Docs polish** — README rewritten to current state; `docs/usage-tips.md` added; stale planning docs archived under `docs/archive/`.
5. ✅ **Dedup pass** — vault scanned: no empty/stub files, 0 identical-content pairs; clean, nothing to remove.

**Nexus v1 is usable day-to-day:** edit notes → synced in ≤5 min; capture from any agent; checklist workflows invocable everywhere; read-only cloud + full local access; everything auto-starts at login.

### Nexus v2 — continue right after v1 (complete the vision)
- **Nice infrastructure + accessibility/UI** — a mission-control surface over the brain/workflows/dashboards (Obsidian + GBrain `/admin` today; evaluate **Omnigent** — Databricks OSS meta-harness orchestrating Claude Code/Codex/Pi with portable context, async approvals, sandbox, web/mobile UI — as the unified UI + orchestration layer, leveraging subscription-backed harnesses, not paid API). Realistic constraint: a UI manages the brain/agents/tasks; it does **not** wrap the chat models (Claude/ChatGPT don't expose subscription models to external API).
- **Multi-agent + OSS models** — premium (Claude/ChatGPT) for planning + PR review; OSS/local for bulk dev/execution.
- **Team / Notion** — personal vault stays private per-person; Notion = shared team layer; checklist engine exports there.
- **Shared writeback** (open decision) — today cloud agents are read-only; a reviewed/scoped cloud-write path is a deliberate future call.
- **Agent operating convention** — treat the brain as ONE source combined with web + model reasoning, not brain-in-isolation (add to agent docs).
- **Loop / harness engineering toward no-prompt operation** — implement only the parts that prove worth it.
- **Social-media video pipeline** — note: this is a *startup* tool, not Nexus; build under startup execution.

### After Nexus is complete — resume the parked work
- **Job system** (capture job reels → workflow + backlog → tracking board → human-gated auto-apply + referral alerts).
- **Startup execution** (run the captured `backlog.md` Phase A→C once the idea is chosen).

## Guardrails (carry across all work)

- Public repo vs private vault boundary; never commit private brain content.
- Cloud surfaces are **read-only** (`read` scope, server-enforced); raw stdio MCP stays local-only.
- Vault writes only on explicit user approval.
- Stop the always-on server gracefully (`launchctl unload`), not `kill -9` (Postgres makes this safe now, but still).
- Don't duplicate GBrain (no custom search/RAG/MCP/cron engine in Nexus OS).
- Finish Nexus (v1 → v2) before deep startup/job execution — the user's chosen sequencing (one thing fully, to avoid overwhelm). Within v2, implement the full vision but drop pieces that don't earn their keep.

## Pointers

- Phase overview: `docs/roadmap.md`
- Architecture: `docs/architecture.md`
- Decisions (chronological): `docs/decision-log.md`
- Checklist engine spec: `docs/workflows/weekly-checklist-engine.md`
- Cloud connector ops: `docs/claude-chat-gbrain-plan.md`, `docs/chatgpt-readonly-connector.md`
