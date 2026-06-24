# Nexus OS Agent Instructions

Nexus OS is the public workflow/config/control layer around a private GBrain-backed Markdown/Obsidian brain.

Nexus OS is not a standalone replacement for GBrain. GBrain is the intended core memory/search/MCP/skills engine.

## Current Architecture Decision

- Markdown/Obsidian brain files are the human-readable source of truth.
- GBrain indexes and serves the brain through local search, MCP, skills, and future dream-cycle/cron workflows.
- Nexus OS stores personalization: schemas, prompts, roadmap, job-search workflows, startup workflows, weekly planning workflows, ingestion instructions, and future custom skills/UI.
- Codex, Claude Code, ChatGPT via MCP, and later Hermes/OpenClaw should connect to the same GBrain-backed memory.
- Shared memory means shared brain files plus the GBrain index, not shared chat histories.

Current client boundary:

- Codex may use raw local GBrain MCP over stdio.
- Claude Code is planned to use raw local GBrain MCP.
- ChatGPT must use the read-only wrapper connector only: `Nexus GBrain Readonly Memory` via `/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp`.
- Claude chat / claude.ai should use a planned read-only remote connector only.
- Do not expose raw GBrain MCP to ChatGPT or Claude chat unless GBrain later provides a verified read-only/native tool-filtered surface.

Read these docs before making architecture changes:

- `docs/architecture.md`
- `docs/gbrain-integration.md`
- `docs/decision-log.md`
- `docs/roadmap.md`

## Boundary Rules

- Do not install GBrain unless the user explicitly asks.
- Do not modify the private brain unless the user explicitly asks.
- Do not store private notes, raw sources, generated wiki pages, or personal brain files in this public repo.
- Preserve the public repo/private brain boundary.
- Read private brain locations from `VAULT_PATH` only when using prototype helpers.
- Refuse to operate if `VAULT_PATH` is missing or resolves inside this repository.
- Do not expose private `.env` values in responses.
- Never silently delete, move, rename, or overwrite raw sources.

## Local Path Conventions

- Repositories, projects, and test repositories should default to `/Users/ssavan99/repos`.
- MCP installs and MCP repositories should default to `/Users/ssavan99/MCPs`.
- Do not create repositories or MCP installs directly under `/Users/ssavan99` unless explicitly requested.
- User-level tool state may remain in tool-default locations such as `~/.gbrain`, `~/.bun`, or `~/.codex`.
- The private brain must remain outside Nexus OS and must not be moved without explicit instruction.

## Do Not Duplicate GBrain

Do not build duplicate versions of GBrain functionality in Nexus OS unless explicitly requested later.

Avoid adding:

- Custom vector database infrastructure.
- Custom RAG/search engine.
- Custom MCP server.
- Custom skills engine.
- Duplicate memory engine internals.
- Background dream-cycle or cron engine.

When a workflow needs memory search, indexing, MCP access, reusable skills, or scheduled memory operations, assume the correct long-term answer is to use GBrain.

## What Belongs In Nexus OS

Use Nexus OS for:

- Personal workflow prompts.
- Schemas and conventions.
- Architecture docs and decision logs.
- Job-search workflows.
- Startup and business workflows.
- Weekly planning workflows.
- Capture and ingestion instructions.
- Thin GBrain integration glue when needed.
- Future custom UI or skills that personalize and orchestrate the GBrain-backed system.

## Prototype/Fallback Helpers

The current custom CLI/search/ingest implementation is prototype/fallback tooling unless explicitly revived.

This includes:

- `check`
- `init`
- `add-note`
- `search`
- `plan-ingest`
- `draft-summary`
- `append-log`
- `rebuild-index`
- Markdown templates under `templates/`

Do not delete this code yet. Remove or retire it only after GBrain is installed, tested, and Nexus workflows no longer depend on it.

If editing these helpers, keep changes minimal and clearly scoped to fallback/prototype workflow support.

## Taxonomy And Workflow Changes

- Ask before major taxonomy changes.
- Prefer documenting workflow rules over building new infrastructure.
- Propose new workflows when repeated user needs appear, but keep GBrain as the core engine.
- Record major architecture decisions in `docs/decision-log.md`.
