# Nexus OS

Nexus OS is the public code engine for an LLM-maintained knowledge system: a personal LLM Wiki, startup/team memory layer, and future agent workflow engine for private Obsidian vaults.

The central idea comes from Karpathy's LLM Wiki pattern: instead of only retrieving raw documents at query time, an LLM incrementally builds a persistent, interlinked Markdown wiki. Raw sources remain the source of truth; generated wiki pages become the compounding synthesis layer; a schema tells the LLM how to maintain the system.

The first two target use cases are:

- Personal knowledge wiki: goals, health, psychology, self-improvement, journal entries, articles, podcast notes, saved posts, and a structured picture of yourself over time.
- Startup, business, and team knowledge wiki: project notes, technical notes, business notes, customer research, meeting transcripts, Slack-style discussions, project documents, and decisions.

## Public Repo, Private Vault

This repository must never contain your real notes, clipped articles, raw sources, generated wiki pages, or personal vault files. It only contains code, templates, and documentation.

Your real Obsidian vault lives outside this repo and is selected with:

```sh
export VAULT_PATH="/absolute/path/to/your/private/obsidian/vault"
```

You can also copy `.env.example` to `.env` for local use. `.env` is ignored by git.

Nexus OS refuses to run if:

- `VAULT_PATH` is missing.
- `VAULT_PATH` resolves inside this repository.

This protects the public codebase/private vault separation.

## Vault Architecture

Nexus OS initializes and expects this structure inside the external vault:

```text
vault/
  raw/
    sources/
      instagram/
      youtube/
      articles/
      meetings/
      journals/
      documents/
    assets/
  wiki/
    index.md
    log.md
    _schema.md
    areas/
      personal/
      career/
      ai-learning/
      startups/
      projects/
    concepts/
    decisions/
    questions/
    summaries/
    people/
    organizations/
```

- `raw/` contains curated source documents organized by source type. Raw sources are immutable: tools may add files, but they must not overwrite or delete existing raw files automatically.
- `raw/sources/` separates capture workflows such as Instagram, YouTube, articles, meetings, journals, and documents.
- `wiki/areas/` contains knowledge domains such as personal, career, AI learning, startups, and projects.
- `wiki/` also contains general folders for concepts, decisions, questions, summaries, people, and organizations.
- `wiki/` contains LLM-generated Markdown pages. The LLM owns this layer and may update summaries, area pages, concept pages, decisions, questions, people, organizations, comparisons, and syntheses.
- `wiki/_schema.md` records local conventions for future LLM sessions.
- `wiki/index.md` is the content catalog.
- `wiki/log.md` is the chronological append-only activity record.

The structure is intentionally flexible. Source type and knowledge domain are separate so one Instagram post, YouTube transcript, meeting, or journal entry can update several wiki areas. Add new `raw/sources/` folders only when a new capture workflow needs them; add new `wiki/areas/` pages or folders when the knowledge base naturally grows.

## Setup

1. Create or choose a private Obsidian vault outside this repo.
2. Set `VAULT_PATH`:

```sh
export VAULT_PATH="/absolute/path/to/your/private/obsidian/vault"
```

3. Optional: use a local `.env`:

```sh
cp .env.example .env
```

Then edit `.env` with your private vault path.

4. Run commands from this checkout with Python:

```sh
PYTHONPATH=src python -m nexus_os --help
```

Or install the package in editable mode:

```sh
python -m pip install -e .
nexus-os --help
```

## Initialize The Vault

Initialize the external vault folders and starter wiki files:

```sh
PYTHONPATH=src python -m nexus_os init
```

This creates missing directories and starter Markdown files. It does not modify existing raw sources.

Check the configured vault:

```sh
PYTHONPATH=src python -m nexus_os check
```

## Add First Notes

Add a Markdown source to the immutable raw layer:

```sh
PYTHONPATH=src python -m nexus_os add-note ./my-first-note.md --source-type documents
```

The file is copied into:

```text
$VAULT_PATH/raw/sources/documents/
```

If a file with the same name already exists, Nexus OS fails instead of overwriting it.

`--source-type` defaults to `documents`. Use source-type folders such as `articles`, `meetings`, `journals`, `instagram`, or `youtube` when that better describes the raw capture format.

After adding sources, the intended LLM workflow is:

1. Read one raw source at a time.
2. Identify its source type and the knowledge areas it touches.
3. Write a source summary under `wiki/summaries/`.
4. Update `wiki/index.md`.
5. Update relevant area, concept, decision, question, people, and organization pages.
6. Append an entry to `wiki/log.md`.

## Manual Ingest Workflow

Phase 1 is a Codex-driven manual LLM Wiki workflow. Nexus OS provides helper commands, templates, and guardrails, but it does not call an LLM API and does not require an OpenAI API key yet.

Example flow:

1. Add a note:

```sh
PYTHONPATH=src python -m nexus_os add-note ./note.md --source-type documents
```

2. Plan the ingest:

```sh
PYTHONPATH=src python -m nexus_os plan-ingest raw/sources/documents/note.md
```

3. Draft the source summary:

```sh
PYTHONPATH=src python -m nexus_os draft-summary raw/sources/documents/note.md
```

4. Ask Codex to complete the summary and update related pages:

```text
Process raw/sources/documents/note.md using AGENTS.md.
Complete the draft summary, update related wiki pages, rebuild the index, and append the log.
```

5. Rebuild the index:

```sh
PYTHONPATH=src python -m nexus_os rebuild-index
```

6. Append the log:

```sh
PYTHONPATH=src python -m nexus_os append-log \
  --type ingest \
  --title "Note Title" \
  --path "raw/sources/documents/note.md" \
  --page "wiki/summaries/note-title.md"
```

`plan-ingest` only prints a structured plan. `draft-summary` creates a structured page from `templates/source_summary.md`, but it does not pretend to summarize with AI. Codex or a human should complete the summary and related wiki updates.

## Future Capture Workflows

Instagram may start with a manually maintained raw file:

```text
raw/sources/instagram/instagram_saved_links.md
```

Later, Nexus OS should process those links or pasted post contents into major categories such as career/job notes, AI learning/implementation notes, and startup/business notes. That processor is not built yet.

YouTube links and transcripts should eventually become source summaries with metadata such as video title, channel, URL, date captured, transcript source, key ideas, implementation notes, and related wiki pages. That processor is roadmap work, not current behavior.

## Search

Search the external vault:

```sh
PYTHONPATH=src python -m nexus_os search "query text"
```

Search only generated wiki pages:

```sh
PYTHONPATH=src python -m nexus_os search "query text" --layer wiki
```

Search only raw sources:

```sh
PYTHONPATH=src python -m nexus_os search "query text" --layer raw
```

The current search is intentionally simple: local, case-insensitive text search over Markdown and text files. It is enough for early vaults and keeps the first version dependency-free.

## Current Scope

Implemented now:

- Safe `VAULT_PATH` resolution.
- Refusal to operate inside this public repo.
- External vault initialization.
- Immutable add-by-copy behavior for raw notes under `raw/sources/documents/`.
- Manual ingest planning.
- Draft source-summary creation from templates.
- Log append and deterministic index rebuild helpers.
- Basic local search.
- README and roadmap documentation.

Intentionally future work:

- LLM-driven ingest that updates many wiki pages in one pass.
- Entity/concept page generation.
- Contradiction detection and source-aware claim revision.
- Wiki linting for stale claims, orphans, missing links, and weak synthesis.
- Instagram saved-link and pasted-post processing.
- YouTube link/transcript processing with source metadata.
- Hybrid BM25/vector search or `qmd` integration.
- MCP tools for agent-native wiki operations.
- Optional outputs like Marp slide decks, Dataview-ready frontmatter, charts, and canvases.
- Human review workflows for team or business wikis.

See [docs/roadmap.md](docs/roadmap.md) for the phased product direction.
