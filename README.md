# Nexus OS

Nexus OS is a personal operating layer around a private Markdown/Obsidian "brain," shared across every AI agent you use. It is **not** a memory engine — [GBrain](https://github.com/garrytan/gbrain) is the engine that indexes and serves the brain. Nexus OS is the public repo that holds the schemas, workflows, prompts, roadmap, and thin glue that make that brain useful for personal, career, and startup work.

One brain, many agents: Codex, Claude Code, claude.ai, and ChatGPT all read the same memory.

## Architecture

Four layers:

- **Markdown/Obsidian vault** — the private, human-readable source of truth (`raw/`, `wiki/`, `inbox/`). Lives outside this repo.
- **GBrain** — local engine: indexing, keyword + semantic search, MCP, skills. Backed by **local Postgres** + **pgvector**, with **local embeddings** (Ollama).
- **Nexus OS** (this repo) — personalization: workflow specs, schemas, prompts, roadmap, decision log, service scripts.
- **Agents** — clients that use the shared brain (see access model below).

Shared memory = shared vault files + the GBrain index. Not shared chat histories.

## How agents connect

| Agent | Transport | Access |
|---|---|---|
| Codex | raw local stdio MCP | full (read/write) |
| Claude Code | raw local stdio MCP (`~/.claude.json`) | full (read/write) |
| claude.ai | always-on HTTP MCP (OAuth 2.1) over an ngrok static URL | **read-only** (`read` scope, server-enforced) |
| ChatGPT | same always-on HTTP MCP, its own read client | **read-only** |

Cloud surfaces get a `read`-scoped token only — writes are refused by the server. Raw MCP stays local-only and is never tunneled. Details: [docs/claude-chat-gbrain-plan.md](docs/claude-chat-gbrain-plan.md), [docs/chatgpt-readonly-connector.md](docs/chatgpt-readonly-connector.md).

## Running system

Everything auto-starts at login as background services (macOS launchd / brew services):

- `postgresql@17` — the brain database
- `ollama` — local embeddings (`nomic-embed-text`)
- `com.nexus.claude-chat-gbrain` — `gbrain serve --http` + ngrok static tunnel (the cloud connector)
- `com.nexus.brain-sync` — imports the vault into the brain every 5 min (see `scripts/`)

So: edit a note in Obsidian → it's searchable by every agent within ~5 minutes; no manual commands.

## Setup (outline)

Personal setup; paths are examples. High level:

1. Install GBrain; `gbrain init` a brain on Postgres (`gbrain migrate --to supabase --url postgresql://localhost/<db>` migrates an existing PGLite brain). Add `pgvector` + `pg_trgm`.
2. Local embeddings: install Ollama, `ollama pull nomic-embed-text`, set `embedding_model: ollama:nomic-embed-text` (768d) in `~/.gbrain/config.json`, `gbrain embed --stale`.
3. Connect local agents: Codex + Claude Code use raw stdio `gbrain serve` (Claude Code config lives in `~/.claude.json`, not `settings.json`).
4. Cloud connector: register a `read`-scoped public PKCE OAuth client per surface; run `gbrain serve --http` behind a stable tunnel (this repo uses an ngrok static domain); add the custom connector in claude.ai / ChatGPT.
5. Install the launchd services in `scripts/` (connector + brain-sync). See each `*.plist` header for install commands.

Full, current operating plan: **[docs/master-plan.md](docs/master-plan.md)**.

## Repo layout

- `docs/master-plan.md` — the living operating plan (read first).
- `docs/architecture.md`, `docs/roadmap.md`, `docs/decision-log.md` — architecture, phases, decisions.
- `docs/workflows/` — invocable workflow specs (capture pipeline, weekly-checklist engine).
- `docs/*-operating-instructions.md`, connector docs — per-agent contracts.
- `scripts/` — service scripts + launchd plists (connector, brain-sync). Local config (`scripts/tunnel.env`) is gitignored.
- `docs/archive/` — historical planning notes (superseded; kept for provenance).
- `src/`, `templates/` — prototype/fallback CLI helpers (legacy; retired once GBrain fully covers the workflows).

## Boundaries

- This public repo must never contain private brain content (notes, sources, generated wiki). The vault lives outside it; `raw/ wiki/ inbox/ …` are gitignored.
- Cloud agents are read-only; vault writes happen only with explicit approval.
- Don't duplicate GBrain (no custom vector DB / search / MCP / skills / cron engine here).

Day-to-day usage (trigger phrases, capturing sources, managing services): **[docs/usage-tips.md](docs/usage-tips.md)**.
