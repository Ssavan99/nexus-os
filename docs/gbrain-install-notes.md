# GBrain Install Notes

Date: 2026-06-10

Scope: Phase 1A safe local install rehearsal with a disposable test brain only.

No real private Markdown/Obsidian brain was imported or modified.

## Safety Plan Used

- Nexus OS repo: `/Users/ssavan99/repos/nexus-os`
- GBrain global install method: `bun install -g github:garrytan/gbrain`
- Fallback clone location, not used: `/Users/ssavan99/gbrain`
- Disposable test brain: `/Users/ssavan99/nexus-gbrain-test-brain`
- GBrain state/config/database location observed: `/Users/ssavan99/.gbrain`

All planned GBrain clone, test brain, state, config, cache, and database paths were outside the Nexus OS repo.

## Install Method Used

Bun was not installed initially, so Bun was installed with the official Bun installer:

```sh
curl -fsSL https://bun.sh/install | bash
```

GBrain was installed globally with:

```sh
bun install -g github:garrytan/gbrain
```

Fallback clone install was not needed.

## Versions

- Bun: `1.3.14`
- GBrain: `gbrain 0.42.38.0`

Install note:

- Bun reported: `Blocked 1 postinstall. Run bun pm -g untrusted for details.`
- GBrain still installed and ran successfully.

## PGLite Initialization

Initial command:

```sh
gbrain init --pglite
```

Result:

- Failed because no embedding provider was configured.
- GBrain printed a clear no-key path:

```sh
gbrain init --pglite --no-embedding
```

Final init command used:

```sh
gbrain init --pglite --no-embedding
```

Result:

- PGLite initialized successfully.
- GBrain applied schema migrations.
- GBrain reported: `Brain ready at /Users/ssavan99/.gbrain/brain.pglite`
- GBrain tentatively set search mode to `conservative`.
- No search-mode override was applied.
- No skills were installed.
- No remote HTTP server was configured.
- No OAuth, ChatGPT, Hermes, or OpenClaw setup was configured.
- No tokens were created.

Doctor command:

```sh
gbrain doctor --json
```

Doctor result:

- Overall status: `warnings`
- Health score: `70`
- Brain checks score: `90`
- Expected warnings included no embeddings, missing embedding provider key, no pages at the time of doctor, and a pack upgrade suggestion.

## Observed GBrain State Files

Observed user-level GBrain files:

```text
/Users/ssavan99/.gbrain/config.json
/Users/ssavan99/.gbrain/brain.pglite/
/Users/ssavan99/.gbrain/.gitignore
/Users/ssavan99/.gbrain/.locks
/Users/ssavan99/.gbrain/audit/
/Users/ssavan99/.gbrain/last-update-check
```

Observed config keys only, values not printed:

```text
database_path
embedding_disabled
engine
mcp
schema_pack
self_upgrade
```

## Disposable Test Brain

Path:

```text
/Users/ssavan99/nexus-gbrain-test-brain
```

Files created with fake content only:

```text
goals.md
projects.md
decision-log.md
people.md
```

Test phrases:

```text
nexus-test-phrase-alpha
startup-roadmap-test-beta
weekly-review-test-gamma
```

A git repo was initialized inside the disposable test brain before import to verify source-file safety.

## Import Command

Command used:

```sh
gbrain import /Users/ssavan99/nexus-gbrain-test-brain --no-embed
```

Result:

- 4 markdown files found.
- 4 pages imported.
- 4 chunks created.
- 0 skipped.
- 0 errors.
- No embeddings were generated.

## Source Markdown Safety Result

Before import:

- Test brain git status was clean.
- Markdown timestamps were recorded.

After import:

- Test brain git status remained clean.
- Markdown timestamps remained unchanged.
- No files were created in the test brain by GBrain.
- No Markdown files were modified, deleted, moved, or rewritten.

Conclusion: for this disposable test, `gbrain import --no-embed` indexed files without modifying source Markdown.

## Search And Query Results

Worked without API keys:

```sh
gbrain search "nexus-test-phrase-alpha"
gbrain search "startup-roadmap-test-beta"
gbrain search "weekly-review-test-gamma"
gbrain search "weekly review"
gbrain query "weekly-review-test-gamma"
```

Observed behavior:

- Exact phrase search found the expected fake pages.
- `gbrain query "weekly-review-test-gamma"` returned the matching page.
- `gbrain query "What does the test brain say about weekly review?"` returned `No results.`

Interpretation:

- Keyword search works locally without API keys.
- Exact-marker query works.
- Natural-language synthesis/query quality is limited in no-embedding/no-LLM mode.
- No API keys were added.
- No embeddings were run.

## Codex MCP

Codex CLI was available:

```text
codex-cli 0.136.0
```

Configured local stdio MCP:

```sh
codex mcp add gbrain -- gbrain serve
```

Result:

- Added global MCP server `gbrain`.
- Transport: `stdio`
- Command: `gbrain`
- Args: `serve`
- No token.
- No remote HTTP.

Verification status:

- `codex mcp get gbrain` confirmed the config.
- Live MCP tool calls were not verified from this already-running Codex session because MCP config reload/tool discovery behavior was unclear.

Claude Code:

- `claude` CLI was not installed.
- Claude Code MCP was not configured.

## Repo Safety Check

Nexus OS repo status after rehearsal:

```text
 M AGENTS.md
 M README.md
 M docs/roadmap.md
?? docs/architecture.md
?? docs/decision-log.md
?? docs/gbrain-integration.md
?? docs/gbrain-local-setup-plan.md
?? docs/gbrain-install-notes.md
```

No private brain files, disposable test brain files, `.gbrain` files, or PGLite database files were copied into the Nexus OS repo.

Existing Nexus tests passed before and after install/import:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests
```

Result:

```text
Ran 6 tests
OK
```

## Errors And Warnings

Observed:

- `gbrain init --pglite` failed without embedding credentials and suggested `--no-embedding`.
- `gbrain init --pglite --no-embedding` succeeded.
- GBrain doctor reported warnings for missing embeddings/provider keys and related setup items.
- GBrain suggested optional skillpack installation; no skills were installed.
- Bun reported one blocked postinstall; no follow-up action was taken because GBrain worked.
- Natural-language `gbrain query "What does the test brain say about weekly review?"` returned `No results` in no-key/no-embedding mode.

## Rollback / Removal Notes

Potential rollback commands for a future cleanup, only if the user explicitly approves:

```sh
codex mcp remove gbrain
rm -rf /Users/ssavan99/nexus-gbrain-test-brain
mv /Users/ssavan99/.gbrain /Users/ssavan99/.gbrain.backup.$(date +%Y%m%d-%H%M%S)
```

Potential Bun/GBrain cleanup would need a separate explicit decision. Do not remove Bun or global packages without user approval.

## Recommended Next Step

Before importing the real Obsidian/Markdown brain:

1. Decide whether to keep search mode `conservative`.
2. Decide whether Phase 1B should import a tiny copied subset of real-like notes or the real brain directly.
3. Decide whether to configure embeddings/API keys now or continue with keyword-only local search.
4. Restart or open a fresh Codex session to verify GBrain MCP tools such as `get_brain_identity`, `list_skills`, and search.
5. Confirm the private brain is clean in git or otherwise backed up before any real import.

Recommended Phase 1B: real-brain dry import only after confirming Codex MCP can see GBrain and after choosing the embedding/key strategy.

## Phase 1B: Fresh MCP Verification And Tiny Real-Brain Subset

Date: 2026-06-10 CDT

Scope: fresh Codex session verification plus a tiny copied real-brain subset import. The full private Markdown/Obsidian brain was not imported.

## Phase 1B Preflight

- Nexus OS repo root: `/Users/ssavan99/repos/nexus-os`
- Initial repo status: clean
- GBrain version: `gbrain 0.42.38.0`
- `gbrain` was installed at `/Users/ssavan99/.bun/bin/gbrain`, but `/Users/ssavan99/.bun/bin` was not present in the Codex shell `PATH`.
- CLI GBrain commands worked when run with `PATH=/Users/ssavan99/.bun/bin:$PATH`.
- `gbrain doctor --json` completed with status `warnings`.
- Expected warnings included no embeddings, no embedding provider key, stale unembedded chunks, low brain score, pack upgrade availability, and related no-key/no-embedding checks.
- Existing Nexus tests passed before import:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests
```

Result:

```text
Ran 6 tests
OK
```

## Phase 1B Codex MCP Verification

Configured MCP entry:

```text
name: gbrain
transport: stdio
command: gbrain
args: serve
```

Config location inspected:

```text
/Users/ssavan99/.codex/config.toml
```

Relevant lines:

```toml
[mcp_servers.gbrain]
command = "gbrain"
args = ["serve"]
```

Result:

- GBrain MCP tools were not visible in this Codex session.
- `get_brain_identity` did not run through MCP.
- `list_skills` did not run through MCP.
- MCP search did not run.
- `codex mcp list` and `codex mcp get gbrain` confirmed the GBrain MCP server is configured and enabled.
- The likely issue is the fresh Codex session environment: `gbrain` is configured as a bare command, but this shell does not have `/Users/ssavan99/.bun/bin` on `PATH`.

Manual follow-up before relying on MCP:

1. Ensure Codex-launched MCP servers can resolve `gbrain`, either by making `/Users/ssavan99/.bun/bin` available on the Codex environment `PATH` or by updating the MCP command after an explicit decision.
2. Start a fresh Codex session after the environment/config change.
3. Verify `get_brain_identity`, `list_skills`, and MCP search.

No MCP server was removed or re-added during this phase.

## Phase 1B Tiny Real-Brain Test Subset

Subset path:

```text
/Users/ssavan99/nexus-real-brain-test-subset
```

Observed subset contents:

```text
/Users/ssavan99/nexus-real-brain-test-subset/Y combinator - How to Build SuperIntelligence Inside Your Company.md
```

Note:

- The request called for 2-5 copied notes and the user indicated 2 new notes, but only 1 Markdown file was visible in the subset folder at import time.
- Because the visible file was outside the Nexus OS repo and the task was a tiny real-subset import, the import proceeded with this one-file subset and this mismatch was recorded as a warning.

Safety snapshot:

```sh
git init
git add .
git commit -m "baseline before gbrain import"
```

Result:

- Baseline commit succeeded in `/Users/ssavan99/nexus-real-brain-test-subset`.
- Git used an automatically configured local committer identity.
- Git status was clean before import.
- Source Markdown timestamp before import:

```text
2026-06-10 19:06:34 /Users/ssavan99/nexus-real-brain-test-subset/Y combinator - How to Build SuperIntelligence Inside Your Company.md
```

## Phase 1B Import

Exact import command used:

```sh
PATH=/Users/ssavan99/.bun/bin:$PATH gbrain import /Users/ssavan99/nexus-real-brain-test-subset --no-embed
```

Result:

- 1 Markdown file found.
- 1 page imported.
- 22 chunks created.
- 0 skipped.
- 0 errors.
- No embeddings were generated.

Warning:

- GBrain emitted a content-sanity warning that the imported page was 50,305 bytes and exceeded the warning threshold, suggesting it could be split later.
- No splitting or source-note modification was performed.

## Phase 1B Source Markdown Safety Result

After import:

- Git status inside `/Users/ssavan99/nexus-real-brain-test-subset` remained clean.
- Source Markdown timestamp remained unchanged:

```text
2026-06-10 19:06:34 /Users/ssavan99/nexus-real-brain-test-subset/Y combinator - How to Build SuperIntelligence Inside Your Company.md
```

- No new non-git files were created in the subset folder.
- No Markdown/source files were modified, created, deleted, moved, or rewritten by GBrain.

Conclusion: for this tiny real-brain subset, `gbrain import --no-embed` indexed the copied Markdown without modifying source files.

## Phase 1B CLI Search And Query Results

CLI searches that worked:

```sh
PATH=/Users/ssavan99/.bun/bin:$PATH gbrain search "shared organizational brain"
PATH=/Users/ssavan99/.bun/bin:$PATH gbrain search "building layer for everything"
PATH=/Users/ssavan99/.bun/bin:$PATH gbrain search "agent infrastructure at YC"
```

Observed behavior:

- All three searches returned the imported real-subset page.
- The earlier Phase 1A fake phrase search also still worked:

```sh
PATH=/Users/ssavan99/.bun/bin:$PATH gbrain search "nexus-test-phrase-alpha"
```

Query attempted:

```sh
PATH=/Users/ssavan99/.bun/bin:$PATH gbrain query "What does the tiny real-brain subset say about shared organizational brain?"
```

Result:

```text
No results.
```

Interpretation:

- Keyword search works locally without API keys.
- Natural-language `gbrain query` remains limited in the no-embedding/no-key setup.
- No API keys were added.
- No embeddings were enabled or run.

## Phase 1B Repo Safety Check

Back in the Nexus OS repo:

- `git status --short` was clean before documentation updates.
- No copied real notes or test subset files were found in the Nexus OS repo.
- No `.gbrain` files, PGLite database files, cache files, or private note files were copied into the Nexus OS repo.

Existing Nexus tests passed again after import:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests
```

Result:

```text
Ran 6 tests
OK
```

## Phase 1B Recommendation

It is not yet recommended to proceed directly to Phase 1C full private brain import.

Reasons:

- Codex MCP tools were still not visible in this fresh session.
- The configured MCP command uses bare `gbrain`, while this Codex shell cannot resolve `gbrain` unless `/Users/ssavan99/.bun/bin` is added to `PATH`.
- The tiny real-brain test imported only one visible note rather than the requested 2-5 note subset.

Safe next step:

1. Fix or confirm the Codex MCP environment so `gbrain serve` can launch in fresh sessions.
2. Verify `get_brain_identity`, `list_skills`, and MCP search.
3. Optionally rerun one more tiny subset import with 2-5 visible notes.
4. Proceed to Phase 1C full private brain import only after MCP visibility is confirmed and the private brain has an explicit safety snapshot or backup.

## Phase 1B.5: Codex MCP PATH Fix

Date: 2026-06-11 CDT

Scope: replace the bare GBrain MCP command with the absolute Bun-installed executable path and verify the existing local PGLite brain through MCP. No import, sync, embedding, token, API key, or remote HTTP configuration was performed.

GBrain executable:

```text
/Users/ssavan99/.bun/bin/gbrain
```

Codex MCP configuration before:

```text
transport: stdio
command: gbrain
args: serve
```

The registration was replaced through the official Codex CLI:

```sh
codex mcp remove gbrain
codex mcp add gbrain -- /Users/ssavan99/.bun/bin/gbrain serve
```

Codex MCP configuration after:

```text
transport: stdio
command: /Users/ssavan99/.bun/bin/gbrain
args: serve
```

Verification results:

- GBrain MCP tools became visible in the current Codex session.
- `get_brain_identity` succeeded and reported GBrain `0.42.38.0`, PGLite, 5 pages, and 26 chunks.
- `list_skills` reached the server but returned `storage_error` because no skills directory is configured. This is consistent with the earlier setup state where no skills were installed.
- MCP search for `nexus-test-phrase-alpha` succeeded and returned the disposable test page.
- MCP search for `shared organizational brain` succeeded and returned the tiny real-brain subset page.
- Another fresh Codex session was not required for this verification. Future sessions should use the corrected absolute executable path automatically.

No manual step is required for the MCP PATH fix. Configuring a skills directory would be a separate future task if published GBrain skills are needed.

Phase 1C full private-brain import is not automatically approved by this fix. The MCP blocker is resolved, but the private brain still requires an explicit safety snapshot or backup and a separate instruction before full import.

## Phase 1C: Full Private Brain Import, Keyword-Only

Date: 2026-06-11 CDT

Scope: full import of the current private Markdown/Obsidian brain into the existing local PGLite brain. No embeddings, API keys, remote HTTP, tokens, watch mode, or source-file writes were enabled.

### Preflight

- Nexus OS repo: `/Users/ssavan99/repos/nexus-os`
- Initial repo status: clean
- GBrain version: `gbrain 0.42.38.0`
- Existing Nexus tests: 6 passed
- Private brain path: `/Users/ssavan99/Desktop/Personal-Obsidian`
- `VAULT_PATH` was empty, so the explicitly approved fallback path was used.
- The private brain resolved outside Nexus OS and outside `/Users/ssavan99/repos`.
- The private brain was not Git-tracked.
- Markdown files found before import: 3
- Total files found before import: 10
- No GBrain, PGLite, SQLite, or database artifacts were present in the private brain.

The first `gbrain doctor --json` and a read-only CLI search timed out on the PGLite lock because two local `gbrain serve` stdio processes were active. Those processes were stopped before import. A repeated doctor check connected successfully to the existing 5-page brain.

### Import

Exact command:

```sh
/Users/ssavan99/.bun/bin/gbrain import /Users/ssavan99/Desktop/Personal-Obsidian --no-embed
```

Result:

- 3 Markdown files found.
- 3 pages imported.
- 50 chunks created.
- 0 pages skipped.
- 0 errors.
- No embeddings generated.
- Post-import doctor connected successfully and reported 8 total pages and 76 unembedded chunks.

Warnings:

- Two source pages exceeded GBrain's content-sanity size warning threshold. No pages were split or modified.
- One imported page shared a content hash with the previously imported tiny real-brain subset page but had a different frontmatter ID. GBrain indexed both records.
- Expected doctor warnings remain for missing embeddings/provider credentials and optional quality features.

### Source Safety

The private brain is not Git-tracked, so source safety was checked with path and metadata snapshots stored outside the vault.

After import:

- Total file inventory was identical.
- Markdown file count remained 3.
- All Markdown sizes and modification/change timestamps were identical.
- No files were created, deleted, moved, or rewritten.
- No GBrain metadata, cache, config, PGLite, SQLite, or database files appeared inside the private brain.

GBrain state remains under:

```text
/Users/ssavan99/.gbrain
```

Conclusion: `gbrain import --no-embed` indexed the full current private brain without modifying its source files.

### CLI Search And Query

The following approved non-sensitive phrases were searched:

```text
shared organizational brain
building layer for everything
agent infrastructure at YC
```

All three CLI searches returned one matching page, the expected safe Y Combinator/company-superintelligence page. No private note excerpts were recorded in this document.

The optional lightweight query was run:

```sh
/Users/ssavan99/.bun/bin/gbrain query "What high-level topics are represented in this brain?"
```

Result: `No results.`

Keyword search works. Natural-language synthesis remains deferred in the no-key/no-embedding configuration.

### MCP Verification

The existing Codex MCP registration remains enabled and correctly uses:

```text
command: /Users/ssavan99/.bun/bin/gbrain
args: serve
transport: stdio
```

Live MCP verification was not completed in this Phase 1C session. The GBrain stdio processes had to be stopped to release PGLite's single-process lock for CLI import, and GBrain tools were not re-exposed in the already-running Codex session afterward. Dynamic tool discovery returned unrelated connector tools only.

No MCP configuration was changed. A fresh Codex session should rerun `get_brain_identity`, `list_skills`, and the same three safe searches. Phase 1B.5 had already verified the corrected absolute executable path and successful MCP search before this import.

### Repo Safety

Before documentation:

- Nexus OS repo status remained clean.
- No private brain files entered Nexus OS.
- No GBrain database, cache, config, or PGLite files entered Nexus OS.
- Existing `.env` contents were not printed or changed.

### Phase 1D And Rollback

The full import and keyword-search path are ready for Phase 1D search-quality evaluation. Enabling embeddings, adding API keys, or incurring provider cost still requires a separate explicit decision. A fresh-session MCP smoke test should be completed before treating Phase 1C MCP verification as closed.

Rollback notes:

- The private source requires no rollback because it was unchanged.
- GBrain's imported index data is isolated under `/Users/ssavan99/.gbrain`.
- No automatic database deletion or reinitialization was performed.
- Any destructive removal or restoration of GBrain state requires explicit approval and should preserve or back up the current local brain first.

## Phase 1C.5: Fresh MCP Smoke Test After Full Import

Date: 2026-06-11 CDT

Scope: read-only verification of the existing full private-brain index through GBrain MCP and CLI. No import, sync, embedding, API key, token, remote HTTP, or private-source write operation was performed.

### Preflight And Configuration

- GBrain version: `gbrain 0.42.38.0`
- Existing Nexus tests: 6 passed
- `codex mcp list` confirmed that the enabled `gbrain` stdio server uses:

```text
/Users/ssavan99/.bun/bin/gbrain serve
```

- `gbrain doctor --json` completed with health score 95 and brain checks score 100. It reported a connection warning while the MCP process held the PGLite database lock.

### MCP Results

- `get_brain_identity`: succeeded and reported PGLite, 8 pages, and 76 chunks.
- `list_skills`: reached the MCP server, but did not return a skill catalog. It returned `storage_error` because no skills directory is configured.
- Fake phrase search for `nexus-test-phrase-alpha`: succeeded with 1 result, the fake `Goals` page.
- Approved private-brain phrase search for `shared organizational brain`: succeeded with 1 result, the documented Y Combinator/company-superintelligence page.
- No private note excerpts were recorded in this repository.

### CLI Comparison And Process Handoff

The first CLI search attempt timed out waiting for the PGLite lock because the active GBrain MCP process owned the single-process database connection.

After the MCP checks completed, only the active `/Users/ssavan99/.bun/bin/gbrain serve` process was stopped gracefully. The same read-only CLI search then returned 1 result for the same documented page.

Comparison result: CLI and MCP matched.

Stopping the MCP server closed this Codex session's GBrain transport. A later MCP call in the same session returned `Transport closed`; a new Codex session is required before the next MCP operation. The absolute command configuration remains correct and unchanged.

### Source And Repo Safety

- The private brain aggregate file-metadata snapshot recorded 10 files, including 3 Markdown files.
- The final aggregate metadata hash matched the initial snapshot exactly.
- No private-source write commands were run.
- No private source files changed during the checked window.
- No private content was copied into Nexus OS.

### Phase 1D Readiness

Phase 1D embeddings/search-quality evaluation is safe to plan from the import and MCP-integration perspective. Enabling embeddings, adding a provider key, or incurring provider cost still requires separate explicit approval.

Operational constraint: PGLite CLI commands that need a database connection may require gracefully stopping the active GBrain MCP process first. Start a fresh Codex session afterward when MCP access is needed again.

Blockers:

- No blocker for keyword-only CLI or MCP search.
- `list_skills` remains unavailable until a skills directory is explicitly configured; that is outside this smoke-test scope.
- The current session's MCP transport is closed after the required CLI cross-check and will be restored by starting a fresh Codex session.

## Phase 1D: Private Brain Structure Bootstrap

Date: 2026-06-11 CDT

Scope: create the missing private Obsidian/Markdown brain structure and starter guidance before a manual note-import session. No existing vault file was overwritten, moved, renamed, or deleted.

### Private Vault And Preflight

- Private vault path: `/Users/ssavan99/Desktop/Personal-Obsidian`
- The resolved path was outside Nexus OS and outside `/Users/ssavan99/repos`.
- The vault contained an Obsidian configuration and was not a Git repository.
- Git was not initialized in the private vault.
- GBrain version: `gbrain 0.42.38.0`
- `gbrain doctor --json` completed with health score 95 and brain checks score 100. Its only reported issue was the expected connection warning while active GBrain MCP processes held the PGLite lock.
- Existing Nexus tests passed before the bootstrap: 6 tests, `OK`.

### Folders Created

Only missing folders were created:

```text
raw/
raw/sources/
raw/sources/articles/
raw/sources/documents/
raw/sources/journals/
raw/sources/meetings/
raw/sources/instagram/
raw/sources/youtube/
raw/sources/ideas/
raw/sources/transcripts/
raw/assets/
wiki/
wiki/areas/
wiki/areas/personal/
wiki/areas/career/
wiki/areas/ai-learning/
wiki/areas/startups/
wiki/areas/projects/
wiki/concepts/
wiki/decisions/
wiki/questions/
wiki/summaries/
wiki/people/
wiki/organizations/
inbox/
inbox/loose-notes/
```

### Starter Files Created

Only missing files were created:

```text
wiki/index.md
wiki/log.md
wiki/_schema.md
inbox/README.md
raw/README.md
wiki/README.md
inbox/how-to-add-notes.md
```

The schema defines `raw/` as immutable or minimally edited sources, `inbox/` as messy unprocessed notes, and `wiki/` as cleaned and synthesized durable knowledge. The import guide routes common capture types and recommends capturing first rather than over-organizing.

Markdown file count:

- Before: 3
- After: 10

### Keyword-Only Import

The active `gbrain serve` processes were stopped gracefully so the CLI could acquire the PGLite database connection.

Exact import command:

```sh
/Users/ssavan99/.bun/bin/gbrain import /Users/ssavan99/Desktop/Personal-Obsidian --no-embed
```

Result:

- 10 Markdown files found.
- 7 new pages imported.
- 3 unchanged pages skipped.
- 7 chunks created.
- 0 errors.
- No embeddings generated.

### Search Verification

Keyword searches succeeded for all requested safe terms:

- `raw sources` found `raw/readme`.
- `loose-notes` found `inbox/readme`.
- `human navigation page` found `wiki/index`.
- `chronological log` found `wiki/log`.

### Source And Repo Safety

- All vault writes were limited to the requested missing folders and starter files.
- Existing private files were not overwritten, moved, renamed, or deleted.
- The private vault remains outside Nexus OS and outside `/Users/ssavan99/repos`.
- No private vault files or GBrain database artifacts entered Nexus OS.
- Embeddings and API keys remain deferred.
- No `gbrain embed`, `gbrain sync`, watch mode, remote HTTP, OAuth, Hermes, or OpenClaw configuration was run.

### Recommended Manual Import

The vault is ready for a 3-4 hour manual note-import session. Capture quickly using `inbox/how-to-add-notes.md`, leave messy material in `inbox/` or the appropriate `raw/sources/` folder, and defer synthesis into `wiki/` until after capture. Run another keyword-only import after the session so GBrain can index the added Markdown.

## Phase 1E: Startup Synthesis Pass

Date: 2026-06-22 CDT

Scope: re-index the updated private Markdown/Obsidian brain and create the first durable startup synthesis pages under the private vault's `wiki/areas/startups/` folder. No embeddings, API keys, watch mode, remote HTTP, OAuth, Hermes, or OpenClaw setup was run.

### Preflight

- Nexus OS repo root: `/Users/ssavan99/repos/nexus-os`
- Initial Nexus OS repo status: clean
- GBrain version: `gbrain 0.42.38.0`
- `gbrain doctor --json` completed with status `warnings`, health score 95, and brain checks score 100. The reported issue was a DB connection warning while a local `gbrain serve` process held the PGLite lock.
- Existing Nexus tests passed before the import: 6 tests, `OK`.
- Private vault path: `/Users/ssavan99/Desktop/Personal-Obsidian`
- The private vault resolved outside Nexus OS and outside `/Users/ssavan99/repos`.
- The private vault was not a git repository, and git was not initialized.

### Initial Snapshot

- Markdown files before synthesis: 61
- The vault contained the expected `raw/`, `inbox/`, and `wiki/` structure.
- No private note contents were copied into this public repo.

### First Keyword-Only Re-Import

The first import attempt timed out on the PGLite lock because an active `gbrain serve` process was running. That serving process was stopped gracefully, then the import was rerun.

Exact import command:

```sh
/Users/ssavan99/.bun/bin/gbrain import /Users/ssavan99/Desktop/Personal-Obsidian --no-embed
```

Result:

- 61 Markdown files found.
- 55 pages imported.
- 6 unchanged pages skipped.
- 200 chunks created.
- 0 errors.
- No embeddings generated.

Warnings:

- Several large source notes exceeded GBrain's content-sanity warning threshold.
- A few imported pages shared content hashes with previously imported paths but had different frontmatter IDs, so GBrain indexed both.
- No raw/source files were split, moved, deleted, or rewritten.

### Startup Search Check

Safe high-level searches were run for startup-related terms. Broad startup and company-brain terms returned results. Some specific idea phrases did not return results before the synthesis pages existed, which was expected because the source notes used different labels or did not yet contain those exact terms.

### Startup Pages Created

Created six private-vault synthesis pages:

```text
wiki/areas/startups/index.md
wiki/areas/startups/convenience-store-platform.md
wiki/areas/startups/civil-engineering-platform.md
wiki/areas/startups/ai-interactive-story-game-platform.md
wiki/areas/startups/open-questions.md
wiki/areas/startups/next-actions.md
```

The pages intentionally separate raw ideas from durable conclusions. The civil-engineering page was marked as a source gap because no direct civil-engineering source note was found in the current vault during this pass.

`wiki/log.md` was appended with a short "First startup synthesis pass" entry and a note that job/career notes remain incomplete and can be added incrementally later.

Sensitive credential-like details found in one raw resource note were not copied into the synthesis pages.

### Second Keyword-Only Re-Import

After the wiki updates, the private vault contained 67 Markdown files.

Exact import command:

```sh
/Users/ssavan99/.bun/bin/gbrain import /Users/ssavan99/Desktop/Personal-Obsidian --no-embed
```

Result:

- 67 Markdown files found.
- 7 pages imported.
- 60 unchanged pages skipped.
- 7 chunks created.
- 0 errors.
- No embeddings generated.

### Search Verification

Post-update search verification succeeded:

- `First startup synthesis pass` found the vault log and startup index.
- Slug searches for `convenience-store-platform`, `civil-engineering-platform`, and `ai-interactive-story-game-platform` found the startup index links.
- Title searches found the individual idea pages:
  - `Convenience Store Platform`
  - `Civil Engineering Platform`
  - `AI Interactive Story-Game Platform`
- `Startup Open Questions` found `wiki/areas/startups/open-questions`.
- `Startup Next Actions` found `wiki/areas/startups/next-actions`.

### Source And Repo Safety

- Raw/source notes were preserved.
- No raw notes were deleted, moved, renamed, or intentionally modified.
- The private vault remained outside Nexus OS and outside `/Users/ssavan99/repos`.
- No private vault files, GBrain database files, PGLite files, cache files, or `.gbrain` state entered Nexus OS.
- Nexus OS fallback helpers were not changed or removed.

### Recommended Next Step

Use the new startup synthesis pages as a review surface. The most useful next step is to add direct raw notes for the civil-engineering direction, then run a small validation sprint around one primary startup idea before another keyword-only GBrain import.

## Phase 1F: Startup Synthesis Hardening

Date: 2026-06-23 CDT

Scope: review and harden the first startup synthesis so it is useful for daily and weekly startup work. No raw/source notes were modified, deleted, moved, or renamed. No embeddings, API keys, sync/watch, remote HTTP, OAuth, Hermes, or OpenClaw setup was run.

### Preflight

- Nexus OS repo root: `/Users/ssavan99/repos/nexus-os`
- Initial Nexus OS repo status: clean
- GBrain version: `gbrain 0.42.38.0`
- `gbrain doctor --json` connected successfully and reported 75 pages, with expected warnings related to missing embeddings/search quality and optional setup.
- Existing Nexus tests passed before edits: 6 tests, `OK`.

### Pages Updated

Updated private-vault startup pages:

```text
wiki/areas/startups/index.md
wiki/areas/startups/convenience-store-platform.md
wiki/areas/startups/civil-engineering-platform.md
wiki/areas/startups/ai-interactive-story-game-platform.md
wiki/areas/startups/open-questions.md
wiki/areas/startups/next-actions.md
wiki/log.md
```

Created:

```text
wiki/areas/startups/weekly-startup-review.md
```

The hardening pass made the current priority explicit: AI interactive story-game is the clearest next validation sprint, convenience-store operations is second if operator access is available, and civil engineering is parked until direct source notes and conversations exist.

### Import Result

Exact import command:

```sh
/Users/ssavan99/.bun/bin/gbrain import "/Users/ssavan99/Desktop/Personal-Obsidian" --no-embed
```

Result:

- 67 Markdown files found.
- 8 pages imported.
- 59 unchanged pages skipped.
- 8 chunks created.
- 0 errors.
- No embeddings generated.

Warnings:

- Existing large raw/source notes again exceeded GBrain's content-sanity warning threshold.
- No source notes were split or modified.

### Search Verification

Post-import search verification succeeded:

- `weekly startup review` found `wiki/areas/startups/weekly-startup-review`.
- `first validation experiment` found startup action and idea pages.
- `not building yet` found the hardened build-status language on startup idea pages.

### Source And Repo Safety

- Raw/source notes were preserved.
- No private brain files entered Nexus OS.
- No GBrain database, PGLite, cache, or `.gbrain` state entered Nexus OS.
- Nexus OS fallback helpers were not changed or removed.
- A raw convenience-store resource note still appears to contain credential-like material and needs manual user inspection. The sensitive values were not copied into generated wiki pages or this public repo.

### Recommended Next Step

Use `wiki/areas/startups/weekly-startup-review.md` at the end of the next 7-day validation cycle. The practical next move is to choose one track, run the first validation experiment, save raw evidence, and then re-import keyword-only.

## Phase 1G: Startup Resource Integration Pass

Date: 2026-06-23 CDT

Scope: integrate previously ignored startup/founder/build resources into practical private-vault startup operating pages. No raw/source notes were modified, deleted, moved, renamed, or overwritten. No embeddings, API keys, sync/watch, remote HTTP, OAuth, Hermes, or OpenClaw setup was run.

### Preflight

- Nexus OS repo root: `/Users/ssavan99/repos/nexus-os`
- Initial Nexus OS repo status: clean
- GBrain version: `gbrain 0.42.38.0`
- `gbrain doctor --json` connected successfully and reported 76 pages, with expected warnings related to missing embeddings/search quality and optional setup.
- Existing Nexus tests passed before edits: 6 tests, `OK`.

### Initial Import

Exact import command:

```sh
/Users/ssavan99/.bun/bin/gbrain import "/Users/ssavan99/Desktop/Personal-Obsidian" --no-embed
```

Result:

- 66 Markdown files found.
- 0 pages imported.
- 66 unchanged pages skipped.
- 0 chunks created.
- 0 errors.
- No embeddings generated.

### Ignored Resources Integrated

Resource groups processed:

- Raw assets: AI cofounder references, investor list, free founder programs, GStack, NameGPT, and Notion Developer Platform.
- Raw idea notes: company superintelligence/company brain and random startup ideas.
- Instagram/founder resources: app launch checklist, founder-thinking prompts, compliance notes, build/launch guide, AI-native company operations, Claude founder workflows, startup stack, SaaS validation, plus pitch/legal/listing/startup-term notes.
- YouTube/build resources: full SaaS stack, app-growth case study, and vibe-coding fundamentals.
- Inbox/loose notes: loose startup thoughts and Nexus/GBrain system workflow notes.

Sensitive/token-like raw URL material was not copied into generated wiki pages or this public repo.

### Pages Created

Created private-vault startup operating pages:

```text
wiki/areas/startups/source-coverage.md
wiki/areas/startups/founder-operating-system.md
wiki/areas/startups/customer-discovery-playbook.md
wiki/areas/startups/app-build-and-launch-playbook.md
wiki/areas/startups/ai-startup-tech-stack.md
wiki/areas/startups/founder-resources-and-programs.md
wiki/areas/startups/compliance-and-launch-checklist.md
wiki/areas/startups/startup-dashboard.md
```

### Pages Updated

Updated private-vault pages:

```text
wiki/areas/startups/index.md
wiki/areas/startups/next-actions.md
wiki/areas/startups/ai-interactive-story-game-platform.md
wiki/areas/startups/convenience-store-platform.md
wiki/areas/startups/civil-engineering-platform.md
wiki/log.md
```

`next-actions.md` is now source-grounded: each action references a playbook, source group, or explicit deferred work item. `startup-dashboard.md` can now answer direct startup questions such as what to focus on, what resources to use, which idea is active, what is parked, the next concrete experiment, and missing evidence.

### Post-Update Import

Exact import command:

```sh
/Users/ssavan99/.bun/bin/gbrain import "/Users/ssavan99/Desktop/Personal-Obsidian" --no-embed
```

Result:

- 74 Markdown files found.
- 14 pages imported.
- 60 unchanged pages skipped.
- 16 chunks created.
- 0 errors.
- No embeddings generated.

Warnings:

- Existing large raw/source notes again exceeded GBrain's content-sanity warning threshold.
- No source notes were split or modified.

### Search Verification

Post-import search verification succeeded:

- `source coverage` found `wiki/areas/startups/source-coverage` and `startup-dashboard`.
- `founder operating system` found `wiki/areas/startups/founder-operating-system`.
- `customer discovery playbook` found `wiki/areas/startups/customer-discovery-playbook`.
- `app build and launch playbook` found `wiki/areas/startups/app-build-and-launch-playbook`.
- `AI startup tech stack` found `wiki/areas/startups/ai-startup-tech-stack`.
- `compliance and launch checklist` found `wiki/areas/startups/compliance-and-launch-checklist`.

### Source And Repo Safety

- Raw/source notes were preserved.
- No private brain files entered Nexus OS.
- No GBrain database, PGLite, cache, or `.gbrain` state entered Nexus OS.
- Nexus OS fallback helpers were not changed or removed.

### Recommended Next Phase

Phase 1H should run the first source-grounded weekly startup review: choose one validation track, use the customer-discovery playbook, capture raw evidence, update the dashboard, and re-import keyword-only.
