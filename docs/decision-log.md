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
