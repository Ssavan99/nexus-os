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
