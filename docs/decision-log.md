# Nexus OS Decision Log

## [2026-06-10] Architecture Decision: GBrain Core, Nexus OS Workflow Layer

Decision: chose Option 2, using GBrain as the core memory/search/MCP/skills engine and Nexus OS as the personalized configuration, workflow, and control layer around it.

## Context

Nexus OS began with local CLI/search/ingest helpers to prove the LLM Wiki workflow and protect the public repo/private brain boundary. That scaffold is useful, but the long-term system should not become a standalone replacement for a mature memory engine.

The desired future is a shared brain usable by Codex, Claude Code, ChatGPT via MCP, and later Hermes/OpenClaw. Shared memory should mean shared Markdown brain files plus a shared GBrain index, not shared chat histories or duplicate hidden stores.

## Chosen Option

Use GBrain as core.

Nexus OS will store:

- Personal schemas.
- Workflow prompts.
- Roadmaps.
- Job-search workflows.
- Startup workflows.
- Weekly planning workflows.
- Ingestion instructions.
- Future custom skills, UI, and orchestration glue.

GBrain will provide:

- Indexing.
- Search.
- MCP access.
- Skills engine.
- Memory engine behavior.
- Future dream-cycle or cron-like workflow infrastructure.

## Rejected For Now: Forking GBrain

Forking GBrain is rejected for now because the current goal is to use a mature upstream memory engine rather than own the burden of a divergent infrastructure fork.

A fork can be reconsidered only if GBrain becomes essential, cannot be extended upstream or through configuration, and Nexus OS needs a capability important enough to maintain independently.

## Rejected: Rewriting GBrain Features In Nexus OS

Rewriting GBrain features in Nexus OS is rejected.

Do not build duplicate versions of:

- Vector database infrastructure.
- Search/RAG engine.
- MCP server.
- Skills engine.
- Memory engine internals.
- Background dream-cycle/cron engine.

The current Nexus OS CLI/search/ingest code remains prototype/fallback workflow tooling until GBrain is installed, tested, and Nexus workflows no longer depend on it.

## Reason

This keeps the system simpler:

- GBrain handles mature memory infrastructure.
- The Markdown brain remains the human-readable source of truth.
- Nexus OS keeps personalization, workflows, prompts, and control logic.
- Multiple agents can share the same memory through GBrain without each building separate memory stacks.

## [2026-06-10] Integration Risk: Codex MCP Needs Stable GBrain PATH

Observation: Phase 1B confirmed that GBrain CLI commands work when `/Users/ssavan99/.bun/bin` is added to `PATH`, but the configured Codex MCP server uses the bare command `gbrain serve`. In the fresh Codex shell used for Phase 1B, `gbrain` was not resolvable without a PATH override, and GBrain MCP tools were not visible to the session.

Decision: do not proceed to full private brain import as a completed MCP integration milestone until a fresh Codex session can launch GBrain MCP and verify `get_brain_identity`, `list_skills`, and MCP search. Keep the integration local/stdio and no-token for now.

## [2026-06-11] Workflow Decision: Raw, Inbox, And Wiki Capture Flow

Decision: organize the private brain around three simple stages: `raw/` for immutable or minimally edited sources, `inbox/` for fast and messy capture, and `wiki/` for cleaned, synthesized, durable knowledge.

Broad areas, reusable concepts, durable decisions, open questions, summaries, people, and organizations live under `wiki/` when useful. During large import sessions, capture speed takes priority over detailed organization; GBrain and agent workflows can help synthesize material later without duplicating memory infrastructure in Nexus OS.

## [2026-06-23] Workflow Decision: Startup Source Coverage And Dashboard Pages

Decision: startup synthesis should maintain an explicit `source-coverage.md` page and a direct-answer `startup-dashboard.md` page inside the private vault.

Reason: the first startup synthesis passes were useful but underused broader founder/build resources. A coverage page makes it clear which raw assets, Instagram notes, YouTube notes, idea notes, and inbox notes have been integrated, while the dashboard gives agents and the user a concise operating surface for focus, active/parked ideas, next experiments, and missing evidence.

This remains a private-vault workflow convention. Nexus OS records the decision, but private startup notes and generated wiki pages stay outside the public repo.

## [2026-06-23] Phase 2A Decision: Codex Uses GBrain MCP As Memory Boundary

Decision: Codex should use the local GBrain MCP server as the read/search boundary for private-brain context, with `/Users/ssavan99/.bun/bin/gbrain serve` as the expected stdio command.

Nexus OS remains the public workflow/config/control repo. Private brain content stays in the private Markdown/Obsidian vault and is accessed through GBrain or explicit private-vault tasks. If GBrain MCP tools are unavailable, Codex should inspect MCP configuration and report the exact failure rather than improvising with imports, sync, embeddings, or private-file copying.

Reason: this keeps Codex connected to shared memory while avoiding a duplicate Nexus OS memory engine and preserving the public repo/private brain boundary.

## [2026-06-23] Phase 2A.1 Verification: Fresh-Session Codex MCP Runtime

Verification: a fresh Codex session successfully launched the configured local GBrain MCP server with `/Users/ssavan99/.bun/bin/gbrain serve` over stdio. `get_brain_identity` returned the local PGLite-backed brain identity, and read-only MCP searches for startup dashboard, customer discovery, weekly startup review, and shared organizational brain queries returned results from the indexed private brain.

Follow-up: `list_skills` reached the MCP server but returned a GBrain `storage_error` because no skills directory is configured on the server host. Treat this as a skills-publication configuration gap, not the earlier MCP transport failure.
