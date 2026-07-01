# GBrain Local Setup Plan

This is a Phase 1 implementation plan only. Do not install GBrain, modify the private Markdown/Obsidian brain, or remove Nexus OS prototype helpers until the user explicitly asks.

## Sources Consulted

Official GitHub sources checked on 2026-06-10:

- [garrytan/gbrain README](https://github.com/garrytan/gbrain)
- [docs/INSTALL.md](https://github.com/garrytan/gbrain/blob/master/docs/INSTALL.md)
- [INSTALL_FOR_AGENTS.md](https://github.com/garrytan/gbrain/blob/master/INSTALL_FOR_AGENTS.md)
- [docs/tutorials/connect-coding-agent.md](https://github.com/garrytan/gbrain/blob/master/docs/tutorials/connect-coding-agent.md)
- [docs/mcp/CODEX.md](https://github.com/garrytan/gbrain/blob/master/docs/mcp/CODEX.md)
- [docs/mcp/CLAUDE_CODE.md](https://github.com/garrytan/gbrain/blob/master/docs/mcp/CLAUDE_CODE.md)
- [docs/ENGINES.md](https://github.com/garrytan/gbrain/blob/master/docs/ENGINES.md)

## 1. Recommended Local Setup Path

Recommended path for the current Nexus OS stage:

1. Local first.
2. PGLite first.
3. Existing private Markdown/Obsidian brain as source material.
4. Local stdio MCP for Codex and Claude Code.
5. No remote HTTP server yet.
6. No ChatGPT OAuth yet.
7. No Hermes/OpenClaw yet.
8. Keep Nexus OS prototype helpers as fallback until GBrain is proven.

Rationale:

- GBrain's README describes the recommended coding-agent starting point as a local brain with `gbrain init --pglite` and local MCP via `gbrain serve`.
- GBrain's engine docs describe PGLite as the zero-friction local default: embedded Postgres via WASM, no server, no Docker.
- The local coding-agent tutorial describes this as zero server, zero token, zero tunnel.
- Remote HTTP, OAuth, ChatGPT, Perplexity, Claude Desktop remote connectors, Hermes, and OpenClaw can wait until the local brain is indexed and useful.

## 2. Exact Commands To Likely Run Later

These commands are for a future install session. Do not run them during this planning step.

### 2.1 Preflight

```sh
cd /Users/ssavan99/repos/nexus-os
git status --short

# Local shell convenience only. Do not commit the real path.
export BRAIN_PATH="/absolute/path/to/private/Markdown-or-Obsidian-brain"
test -d "$BRAIN_PATH"
```

Optional Nexus fallback check:

```sh
PYTHONPATH=src python -m nexus_os check
```

### 2.2 Install GBrain

Official docs say GBrain is a Bun + TypeScript runtime.

```sh
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"
bun install -g github:garrytan/gbrain
gbrain --version
```

Fallback deterministic install path if global install or migrations fail:

```sh
git clone https://github.com/garrytan/gbrain.git ~/gbrain
cd ~/gbrain
bun install
bun link
gbrain --version
```

If install reports schema/migration issues:

```sh
gbrain apply-migrations --yes
```

### 2.3 Initialize Local PGLite Brain

Official docs show both `gbrain init --pglite` and `gbrain init` as PGLite/no-server paths. Prefer the explicit command first:

```sh
gbrain init --pglite
gbrain doctor --json
```

If current docs or CLI help indicate `gbrain init` is now the preferred PGLite default:

```sh
gbrain init
gbrain doctor --json
```

Confirm search mode with the user before continuing if GBrain prints a setup matrix:

```sh
gbrain search modes
gbrain config set search.mode conservative   # only if selected
gbrain config set search.mode balanced       # only if selected
gbrain config set search.mode tokenmax       # only if selected
```

For this stage, prefer a cost-conscious local start unless the user explicitly wants maximal retrieval payloads.

### 2.4 Configure Optional Keys

Do not commit keys to this repo.

GBrain docs currently mention:

```sh
export ZEROENTROPY_API_KEY="ze-..."
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

Planning stance:

- Start with the minimum needed for local keyword search and health checks.
- Add embedding/reranker keys only when we are ready to index for vector search.
- Keep secrets in shell profile, GBrain config, or an ignored local env file, never in Nexus OS git.

### 2.5 Import / Sync / Search / Query

First import should point at the existing private brain folder, not this public Nexus OS repo:

```sh
gbrain import "$BRAIN_PATH" --no-embed
gbrain search "known phrase from a private note"
gbrain query "what themes appear in my notes?"
```

If embedding keys are configured and we are ready for vector search:

```sh
gbrain embed --stale
gbrain query "what themes appear in my notes?"
```

For ongoing sync after initial import:

```sh
gbrain sync --repo "$BRAIN_PATH"
gbrain embed --stale
```

Optional watch mode only after confirming write/read behavior and resource usage:

```sh
gbrain sync --watch
```

### 2.6 Graph Extraction

Only after import is verified:

```sh
gbrain extract links --source db --dry-run | head -20
gbrain extract links --source db
gbrain extract timeline --source db
gbrain stats
```

For Obsidian-style bare wikilinks, do not enable basename resolution until we inspect `gbrain doctor` hints and understand duplicate-name risks:

```sh
gbrain config set link_resolution.global_basename true
gbrain extract links --source db
```

### 2.7 Local MCP For Claude Code

Official Claude Code local setup:

```sh
claude mcp add gbrain -- gbrain serve
```

Verification prompt inside Claude Code:

```text
Call get_brain_identity, list_skills, then search my brain for [known topic].
```

Removal if needed:

```sh
claude mcp remove gbrain
```

### 2.8 Local MCP For Codex

Official Codex docs say local stdio works on the same machine:

```sh
codex mcp add gbrain -- gbrain serve
```

Verification prompt inside Codex:

```text
Call get_brain_identity, list_skills, then search my brain for [known topic].
```

Removal if needed:

```sh
codex mcp remove gbrain
```

### 2.9 Remote Commands To Defer

Do not run these in Phase 1 unless the plan changes:

```sh
gbrain serve --http
gbrain auth create "codex"
gbrain connect https://your-host/mcp --token gbrain_xxx --agent codex --install
gbrain connect https://your-host/mcp --token gbrain_xxx --install
```

Reason: remote HTTP introduces tokens, public URLs, OAuth questions, and config surfaces we do not need for local-first setup.

## 3. Brain Folder Decision

GBrain should point to the existing private Markdown/Obsidian brain folder.

The brain folder must remain outside `/Users/ssavan99/repos/nexus-os`.

Recommended local convention:

```sh
export BRAIN_PATH="/absolute/path/to/private/Markdown-or-Obsidian-brain"
gbrain import "$BRAIN_PATH" --no-embed
```

This is a pointer/indexing relationship. Nexus OS should not copy private brain files into the public repo. If GBrain needs database files, config files, embeddings, or indexes, those should live in GBrain's configured storage location such as `~/.gbrain/`, not inside this public repo.

Before running import or sync, confirm:

- The brain folder is correct.
- The folder is not inside this repo.
- The first import is read/index-oriented and does not rewrite source Markdown.
- Any generated files are known and acceptable.

## 4. Compatibility With Current Nexus OS

Current Nexus OS helpers remain prototype/fallback.

| Current Nexus helper | Long-term GBrain replacement or role |
| --- | --- |
| `nexus-os check` | Fallback boundary check for `VAULT_PATH`; GBrain setup should have its own health checks via `gbrain doctor --json`. |
| `nexus-os init` | Fallback vault scaffold only; long-term brain structure should follow GBrain-compatible Markdown conventions and Nexus workflow docs. |
| `nexus-os add-note` | Fallback file-copy helper; long-term use GBrain capture/import/sync workflows where appropriate. |
| `nexus-os search` | Replaced by `gbrain search` and MCP search tools. |
| `nexus-os plan-ingest` | May remain as a Nexus workflow prompt helper, but search/context should come from GBrain. |
| `nexus-os draft-summary` | May remain as a Markdown template helper, but long-term summaries should be generated/written through GBrain-backed workflows. |
| `nexus-os append-log` | Fallback log helper; long-term durable logs/decisions should be pages in the brain and indexed by GBrain. |
| `nexus-os rebuild-index` | Replaced by GBrain indexing/search. Manual Markdown indexes may remain human-facing if useful. |
| `templates/` | Keep as Nexus personalization/workflow templates unless GBrain skills supersede them. |

Do not delete current code during Phase 1. Retire helpers only after:

1. GBrain is installed.
2. The private brain is imported/indexed.
3. Codex and Claude can search it through GBrain.
4. Nexus workflows no longer rely on the fallback helpers.

## 5. Risks / Questions Before Install

Clarify these before running install/import/sync:

1. Does `gbrain import "$BRAIN_PATH"` modify source Markdown files, or only index them?
2. Does `gbrain sync --repo "$BRAIN_PATH"` write back to source files, create metadata files, or only update the database?
3. Where exactly will PGLite database files live on this machine? Verify the active GBrain version's storage path during install.
4. Are any database, cache, embedding, or source registration files created inside the private brain folder?
5. Does the current GBrain version require Bun only, or also Node/Python for any optional integrations?
6. Which keys are required for the first useful local test? Official docs mention ZeroEntropy, OpenAI fallback, and optional Anthropic; keyword search can work without an embedding provider.
7. Where are tokens and config stored? Official docs mention `~/.gbrain/config.json`; remote Codex tokens use `GBRAIN_REMOTE_TOKEN`, but Phase 1 should avoid remote tokens.
8. How should secrets be stored locally without touching this repo?
9. What is the rollback path if import/indexing behaves unexpectedly?
10. Does GBrain support dry-run or source registration inspection before importing the full private brain?
11. Are Obsidian attachments ignored, indexed, copied, or transformed?
12. How should duplicate Obsidian bare wikilinks be handled before enabling basename resolution?
13. What is the expected cost of embeddings for the current brain size?
14. Should the first import target the whole brain or a small test subfolder?

Recommended rollback preparation:

```sh
cp -R ~/.gbrain ~/.gbrain.backup.$(date +%Y%m%d-%H%M%S)
git -C "$BRAIN_PATH" status --short        # if the private brain is a git repo
find /Users/ssavan99/repos/nexus-os -maxdepth 2 -type f -name '*.md' | sort
```

If GBrain state must be reset during testing, do not delete anything until we have identified the exact files created and backed them up.

## 6. Suggested Verification Checklist

Run this checklist only during the future install session.

### Install And Health

- `gbrain --version` prints a version.
- `gbrain doctor --json` runs.
- PGLite engine is active.
- Any setup warnings are understood and recorded.
- Search mode is explicitly chosen by the user.

### Brain Import / Index

- `BRAIN_PATH` points to the private Markdown/Obsidian brain.
- `BRAIN_PATH` is outside `/Users/ssavan99/repos/nexus-os`.
- Initial import completes:

```sh
gbrain import "$BRAIN_PATH" --no-embed
```

- Search returns an expected known note:

```sh
gbrain search "known phrase from a private note"
```

- Query returns a useful answer with citations or a clear gap:

```sh
gbrain query "what do I know about [known topic]?"
```

- If embeddings are enabled:

```sh
gbrain embed --stale
gbrain query "what themes appear in my notes?"
```

### MCP

- Claude Code can connect locally:

```sh
claude mcp add gbrain -- gbrain serve
```

- Codex can connect locally:

```sh
codex mcp add gbrain -- gbrain serve
```

- In each client, verify:

```text
Call get_brain_identity, list_skills, then search my brain for [known topic].
```

### Repo Safety

- No private files entered Nexus OS:

```sh
cd /Users/ssavan99/repos/nexus-os
git status --short
find . -maxdepth 3 -type f | sort
```

- Existing Nexus tests still pass:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests
```

### GBrain State

- Confirm where GBrain stored database/config files.
- Confirm whether the private brain git status changed.
- Record any GBrain warnings or setup choices in `docs/decision-log.md` if they affect architecture.

## 7. No Action Yet

This document is the only Phase 1 setup output for now.

Do not:

- Install GBrain.
- Run Bun install commands.
- Run `gbrain init`.
- Run `gbrain import`.
- Run `gbrain sync`.
- Connect Codex or Claude MCP.
- Modify the private Markdown/Obsidian brain.
- Remove or rewrite Nexus OS fallback helpers.

The next action should be an explicit user-approved install session.
