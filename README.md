# Nexus OS

Nexus OS is a personalized GBrain-based operating layer for a private Markdown/Obsidian brain.

It is not a standalone memory engine and not a replacement for GBrain. GBrain is the intended core memory/search/MCP/skills engine. Nexus OS stores the personal schemas, prompts, workflows, roadmap, and control logic that make the GBrain-backed brain useful for personal, career, startup, and agent workflows.

## Final Architecture

The system has four main parts:

- Markdown/Obsidian brain: the private, human-readable source of truth.
- GBrain: the local engine that indexes and serves the brain through search, MCP, skills, and future dream-cycle or cron workflows.
- Nexus OS: this public repo, containing personalization, workflow instructions, prompts, schemas, roadmap, and future custom UI or skills.
- Agents and clients: Codex, Claude Code, ChatGPT via MCP, and later Hermes/OpenClaw, all connecting to the same GBrain-backed memory.

Shared memory means shared brain files plus the GBrain index. It does not mean shared chat histories.

See:

- [docs/architecture.md](docs/architecture.md)
- [docs/gbrain-integration.md](docs/gbrain-integration.md)
- [docs/decision-log.md](docs/decision-log.md)
- [docs/roadmap.md](docs/roadmap.md)

## Public Repo, Private Brain

This repository must never contain your real notes, clipped articles, raw sources, generated wiki pages, or personal brain files. It only contains code, templates, prompts, workflows, schemas, and documentation.

Your real Markdown/Obsidian brain lives outside this repo. Existing prototype helpers read that location from:

```sh
export VAULT_PATH="/absolute/path/to/your/private/obsidian/brain"
```

You can also copy `.env.example` to `.env` for local use. `.env` is ignored by git.

Prototype helpers refuse to run if:

- `VAULT_PATH` is missing.
- `VAULT_PATH` resolves inside this repository.

This protects the public repo/private brain boundary.

## What Nexus OS Owns

Nexus OS should contain:

- Personal operating principles.
- Workflow prompts.
- Job-search workflows.
- Startup and business workflows.
- Weekly planning workflows.
- Capture and ingestion instructions.
- Roadmaps and architecture decisions.
- Personal schemas and conventions.
- Thin integration glue around GBrain when needed.
- Future custom UI or skills specific to this operating layer.

## What GBrain Owns

GBrain should own:

- Indexing.
- Search.
- Retrieval.
- MCP server/tool surfaces.
- Skills engine.
- Memory engine internals.
- Future scheduled or dream-cycle workflows.

Do not build duplicate GBrain features in Nexus OS unless explicitly requested later.

## Prototype/Fallback Helpers

The current Nexus OS CLI/search/ingest implementation is reclassified as prototype/fallback workflow helpers.

These commands may remain while GBrain is not installed or while workflows are being validated:

```sh
PYTHONPATH=src python -m nexus_os --help
```

Current helper commands include:

- `check`
- `init`
- `add-note`
- `search`
- `plan-ingest`
- `draft-summary`
- `append-log`
- `rebuild-index`

Do not remove these helpers yet. Retire or delete them only after GBrain is installed, tested, and Nexus workflows no longer depend on them.

## Manual Workflow During Transition

Until GBrain is installed and connected, the prototype helpers can still support a manual Codex-driven workflow:

```sh
PYTHONPATH=src python -m nexus_os add-note ./note.md --source-type documents
PYTHONPATH=src python -m nexus_os plan-ingest raw/sources/documents/note.md
PYTHONPATH=src python -m nexus_os draft-summary raw/sources/documents/note.md
PYTHONPATH=src python -m nexus_os rebuild-index
PYTHONPATH=src python -m nexus_os append-log --type ingest --title "Note Title" --path "raw/sources/documents/note.md"
```

This is not the final memory architecture. It is a fallback path for early workflow design.

## What Not To Build Here

Do not build these in Nexus OS unless a later explicit architecture decision changes this:

- Custom vector database.
- Custom RAG/search engine.
- Custom MCP server.
- Custom skills engine.
- Duplicate GBrain memory engine.
- Background dream-cycle/cron engine.

Prefer configuring, extending, or integrating with GBrain.

## Next Step

The next implementation step is Phase 1: install and configure GBrain against the private Markdown/Obsidian brain, then verify indexing/search and agent connection paths without copying private brain files into this public repo.
