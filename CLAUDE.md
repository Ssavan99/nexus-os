# Nexus OS — Claude Code Instructions

Nexus OS is the public workflow/config/control layer around a private GBrain-backed Markdown/Obsidian brain.

Nexus OS is not a standalone replacement for GBrain. GBrain is the intended core memory/search/MCP/skills engine.

> Note: `AGENTS.md` holds the same guidance for other agents (e.g. Codex). This `CLAUDE.md` is the authoritative version for Claude Code. Keep the two in sync when the shared rules change.

## Current Architecture Decision

- Markdown/Obsidian brain files are the human-readable source of truth.
- GBrain indexes and serves the brain through local search, MCP, skills, and future dream-cycle/cron workflows.
- Nexus OS stores personalization: schemas, prompts, roadmap, job-search workflows, startup workflows, weekly planning workflows, ingestion instructions, and future custom skills/UI.
- Codex, Claude Code, ChatGPT via MCP, and later Hermes/OpenClaw should connect to the same GBrain-backed memory.
- Shared memory means shared brain files plus the GBrain index, not shared chat histories.

Current client boundary:

- Codex may use raw local GBrain MCP over stdio.
- Claude Code uses raw local GBrain MCP registered at user scope in `~/.claude.json` (global, all sessions).
- ChatGPT must use the read-only wrapper connector only: `Nexus GBrain Readonly Memory` via `/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp`.
- Claude chat / claude.ai uses GBrain's native `serve --http` (OAuth 2.1) with a `read`-scoped client — read-only is enforced server-side, so no custom wrapper is needed. See `docs/claude-chat-gbrain-plan.md`.
- Do not expose raw GBrain MCP (full scope) to ChatGPT or Claude chat. Cloud surfaces get a `read`-scoped token only; raw stdio MCP stays local-only (Codex, Claude Code) and is never tunneled.

## GBrain MCP For Claude Code

Claude Code connects to GBrain through a local stdio MCP server registered at **user scope** in `~/.claude.json` (top-level `mcpServers` key — this is where Claude Code reads MCP servers; `~/.claude/settings.json` is for permissions/hooks/env only and does NOT load MCP servers):

```json
{
  "mcpServers": {
    "gbrain": {
      "type": "stdio",
      "command": "/Users/ssavan99/.bun/bin/gbrain",
      "args": ["serve"]
    }
  }
}
```

The equivalent CLI command (if `claude` is on PATH) is `claude mcp add gbrain --scope user -- /Users/ssavan99/.bun/bin/gbrain serve`. User scope makes GBrain available in all Claude Code sessions and projects, matching Codex.

Use the `gbrain` MCP tools for memory search and retrieval. Do not rebuild search or copy private content into this repo. See `docs/claude-code-gbrain-operating-instructions.md` for the full operating contract (allowed searches, write rules, prohibited commands).

If GBrain MCP tools are unavailable, do not silently fall back to direct private-vault reads — verify the `gbrain` entry and absolute binary path in `~/.claude.json`, and restart Claude Code (MCP servers load at startup).

Read these docs before making architecture changes:

- `docs/architecture.md`
- `docs/gbrain-integration.md`
- `docs/decision-log.md`
- `docs/roadmap.md`
- `docs/claude-code-gbrain-operating-instructions.md`

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
- MCP installs and MCP repositories must be created under `/Users/ssavan99/MCPs`. Always install, download, or create any MCP inside this directory.
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
