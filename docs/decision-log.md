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

## [2026-06-23] Phase 2B Order Decision: ChatGPT Preflight Before Claude Code

Decision: evaluate ChatGPT MCP feasibility and safety before moving to Claude Code because the user explicitly requested this Phase 2 order change.

Reason: ChatGPT is a remote OpenAI-hosted client, unlike local stdio MCP clients. Any GBrain connection for ChatGPT may require an HTTPS MCP endpoint, authentication, and possibly a tunnel, so remote exposure of the private brain requires a separate explicit approval before implementation.

## [2026-06-23] Phase 2B.1 Planning: ChatGPT Connector Dry Run

Decision: plan the first ChatGPT connector dry run around OpenAI Secure MCP Tunnel to a local GBrain MCP server, preferably using the existing GBrain stdio command before considering GBrain HTTP mode or a public tunnel.

Reason: Secure MCP Tunnel is the safer local-first path because it avoids public inbound exposure and can forward MCP requests to a private stdio or HTTP MCP server. Any server start, tunnel start, token creation, OAuth configuration, connector creation, or use of the full private-brain index still requires separate explicit approval.

## [2026-06-23] Phase 2B.6 Verification: Disposable ChatGPT Tunnel Smoke Test

Verification: the ChatGPT Secure MCP Tunnel path succeeded against a disposable GBrain state, using the `gbrain-disposable-stdio` tunnel-client profile and a stdio command scoped with `GBRAIN_HOME=/Users/ssavan99/repos/nexus-gbrain-chatgpt-state`.

Boundary: the test used fake disposable Markdown content only. The real private vault, real `/Users/ssavan99/.gbrain` state, GBrain HTTP mode, public tunnels, embeddings, real-brain import/sync/watch, OAuth/token values, and Claude Code setup were not used.

## [2026-06-23] Phase 2B.11 Verification: ChatGPT Read-Only GBrain Connector

Verification: the daily ChatGPT memory path should use the minimal read-only wrapper at `/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp`, connected as `Nexus GBrain Readonly Memory` through Secure MCP Tunnel. The wrapper exposes only `get_brain_identity` and `search`, and delegates search to the existing local GBrain CLI/index.

Decision: do not use raw GBrain MCP as the daily ChatGPT connector because it exposed write/admin/destructive tools. The raw private vault was not modified, and no GBrain HTTP mode, public tunnel, embeddings, real-brain import/sync/watch, or write tools were used.

## [2026-06-23] Phase 2B.12 Documentation Audit: ChatGPT Wrapper Runbook

Decision: document the daily ChatGPT connector as `Nexus GBrain Readonly Memory` using tunnel profile `gbrain-readonly-wrapper-stdio` and MCP command `/Users/ssavan99/.bun/bin/bun /Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp/src/index.ts`.

Reason: the earlier raw GBrain connector exposed destructive/admin tools, and the older wrapper command shape using `cd ... && bun run start` exited under `tunnel-client`. The safe daily ChatGPT path is the read-only wrapper only; Codex and planned Claude Code remain local raw GBrain MCP clients, while Claude chat / claude.ai should use a future read-only remote connector.
