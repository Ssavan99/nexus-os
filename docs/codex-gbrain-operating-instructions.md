# Codex GBrain Operating Instructions

Status: Phase 2A Codex connection hardening.

These instructions define how Codex should use the GBrain-backed private Markdown/Obsidian brain while preserving the public repo/private brain boundary.

## Roles

- Nexus OS is the public workflow, configuration, documentation, and control layer.
- The private Markdown/Obsidian brain is the human-readable source of truth for personal notes, raw sources, and generated wiki pages.
- GBrain is the memory/search/MCP/skills engine that indexes and serves the private brain.
- Codex is a client/operator that should use GBrain memory for context and write durable outputs only when explicitly asked.

Shared memory means shared Markdown brain files plus the GBrain index. It does not mean shared chat histories.

## MCP Configuration

Codex should use the local stdio GBrain MCP server:

```text
command: /Users/ssavan99/.bun/bin/gbrain
args: serve
transport: stdio
```

If GBrain MCP tools are unavailable or return `Transport closed`, do not silently fall back to private-vault reads. Inspect Codex MCP config with:

```sh
codex mcp list
codex mcp get gbrain
```

The expected config is the absolute executable path above, not a bare `gbrain` command that depends on shell `PATH`.

## How Codex Should Use GBrain Memory

For Nexus OS work, Codex should use GBrain as the retrieval layer rather than rebuilding search or copying private content into this repo.

Read-only GBrain use is appropriate for:

- Understanding current startup, job-search, weekly planning, and personal workflow context.
- Locating private wiki pages relevant to a task.
- Checking whether a concept has already been synthesized.
- Finding source paths that should be cited in private-vault wiki updates.

Codex should treat GBrain results as context, not as permission to expose private note contents in public repo docs or final responses.

## Searches To Run Before Nexus OS Tasks

Before architecture or integration tasks:

```text
architecture
gbrain integration
decision log
roadmap
```

Before startup workflow tasks:

```text
startup-dashboard
source coverage
customer discovery playbook
weekly startup review
```

Before job/career workflow tasks:

```text
job search
career
resume
applications
```

Before private-brain organization tasks:

```text
raw inbox wiki
source coverage
chronological log
```

When searching, prefer high-level page names and safe phrases. Do not quote private raw-note excerpts into Nexus OS docs.

## Private Brain File Rules

The private brain path is outside this repository:

```text
/Users/ssavan99/Desktop/Personal-Obsidian
```

Codex may read or write private-vault files only when the user explicitly asks for private brain work. When writing, prefer durable wiki pages under `wiki/` and preserve source paths to raw notes.

Codex must not:

- Copy private notes, raw sources, generated wiki pages, or personal brain files into Nexus OS.
- Delete, move, rename, or overwrite raw/source notes unless explicitly requested.
- Print private note contents in public docs or final responses.
- Expose `.env` values, API keys, credentials, tokens, or credential-like raw note material.
- Initialize git inside the private vault unless explicitly requested.

## When Codex May Write To The Private Vault

Allowed with explicit user request:

- Create or update private wiki pages.
- Append private wiki log entries.
- Create concise synthesis pages that cite vault-relative source paths.
- Update private workflow pages such as startup dashboards, review pages, or action lists.

Not allowed without explicit user request:

- Raw/source note edits.
- Bulk taxonomy changes.
- Moving private notes.
- Deleting duplicates.
- Rewriting imported captures.

## What Codex Must Not Do

Do not run these during normal Codex/Nexus work unless the user explicitly approves:

```sh
gbrain embed
gbrain sync --watch
gbrain serve --http
gbrain auth create
gbrain connect
```

Also do not:

- Add API keys or provider credentials.
- Configure remote HTTP, ChatGPT OAuth, Hermes, or OpenClaw.
- Install Claude Code.
- Create repositories outside `/Users/ssavan99/repos`.
- Create MCP installs or MCP repositories outside `/Users/ssavan99/MCPs`.
- Build custom vector database, RAG, search, MCP, or skills infrastructure inside Nexus OS.

## Avoid Duplicating GBrain

When a workflow needs memory search, indexing, retrieval, MCP, skills, or scheduled memory operations, assume GBrain owns that capability.

Nexus OS may contain:

- Operating instructions.
- Workflow docs.
- Prompt conventions.
- Roadmaps and decision logs.
- Thin glue that preserves the public repo/private brain boundary.

Nexus OS should not become another memory engine between agents and the brain.

## Smoke Test Expectations

When GBrain MCP tools are available, a read-only Codex smoke test should run:

```text
get_brain_identity
list_skills
search startup-dashboard
search customer discovery playbook
search weekly startup review
search shared organizational brain
```

If this fails with transport errors, record the exact failure and inspect MCP config. Do not import, sync, embed, or read private vault files as a substitute for the MCP smoke test.
