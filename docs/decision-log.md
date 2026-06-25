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

## [2026-06-10] Integration Risk: Codex MCP Needs Stable GBrain PATH

Observation: Phase 1B confirmed that GBrain CLI commands work when `/Users/ssavan99/.bun/bin` is added to `PATH`, but the configured Codex MCP server uses the bare command `gbrain serve`. In the fresh Codex shell used for Phase 1B, `gbrain` was not resolvable without a PATH override, and GBrain MCP tools were not visible to the session.

Decision: do not proceed to full private brain import as a completed MCP integration milestone until a fresh Codex session can launch GBrain MCP and verify `get_brain_identity`, `list_skills`, and MCP search. Keep the integration local/stdio and no-token for now.

## [2026-06-11] Workflow Decision: Raw, Inbox, And Wiki Capture Flow

Decision: organize the private brain around three simple stages: `raw/` for immutable or minimally edited sources, `inbox/` for fast and messy capture, and `wiki/` for cleaned, synthesized, durable knowledge.

Broad areas, reusable concepts, durable decisions, open questions, summaries, people, and organizations live under `wiki/` when useful. During large import sessions, capture speed takes priority over detailed organization; GBrain and agent workflows can help synthesize material later without duplicating memory infrastructure in Nexus OS.

## [2026-06-23] Workflow Decision: Startup Source Coverage And Dashboard Pages

Decision: startup synthesis should maintain an explicit `source-coverage.md` page and a direct-answer `startup-dashboard.md` page inside the private vault.

Reason: the first startup synthesis passes were useful but underused broader founder/build resources. A coverage page makes it clear which raw assets, Instagram notes, YouTube notes, idea notes, and inbox notes have been integrated, while the dashboard gives agents and the user a concise operating surface for focus, active/parked ideas, next experiments, and missing evidence.

This remains a private-vault workflow convention. Nexus OS records the decision, but private startup notes and generated wiki pages stay outside the public repo.

## [2026-06-23] Phase 2A Decision: Codex Uses GBrain MCP As Memory Boundary

Decision: Codex should use the local GBrain MCP server as the read/search boundary for private-brain context, with `/Users/ssavan99/.bun/bin/gbrain serve` as the expected stdio command.

Nexus OS remains the public workflow/config/control repo. Private brain content stays in the private Markdown/Obsidian vault and is accessed through GBrain or explicit private-vault tasks. If GBrain MCP tools are unavailable, Codex should inspect MCP configuration and report the exact failure rather than improvising with imports, sync, embeddings, or private-file copying.

Reason: this keeps Codex connected to shared memory while avoiding a duplicate Nexus OS memory engine and preserving the public repo/private brain boundary.

## [2026-06-23] Phase 2A.1 Verification: Fresh-Session Codex MCP Runtime

Verification: a fresh Codex session successfully launched the configured local GBrain MCP server with `/Users/ssavan99/.bun/bin/gbrain serve` over stdio. `get_brain_identity` returned the local PGLite-backed brain identity, and read-only MCP searches for startup dashboard, customer discovery, weekly startup review, and shared organizational brain queries returned results from the indexed private brain.

Follow-up: `list_skills` reached the MCP server but returned a GBrain `storage_error` because no skills directory is configured on the server host. Treat this as a skills-publication configuration gap, not the earlier MCP transport failure.

## [2026-06-23] Phase 2B Order Decision: ChatGPT Preflight Before Claude Code

Decision: evaluate ChatGPT MCP feasibility and safety before moving to Claude Code because the user explicitly requested this Phase 2 order change.

Reason: ChatGPT is a remote OpenAI-hosted client, unlike local stdio MCP clients. Any GBrain connection for ChatGPT may require an HTTPS MCP endpoint, authentication, and possibly a tunnel, so remote exposure of the private brain requires a separate explicit approval before implementation.

## [2026-06-23] Phase 2B.1 Planning: ChatGPT Connector Dry Run

Decision: plan the first ChatGPT connector dry run around OpenAI Secure MCP Tunnel to a local GBrain MCP server, preferably using the existing GBrain stdio command before considering GBrain HTTP mode or a public tunnel.

Reason: Secure MCP Tunnel is the safer local-first path because it avoids public inbound exposure and can forward MCP requests to a private stdio or HTTP MCP server. Any server start, tunnel start, token creation, OAuth configuration, connector creation, or use of the full private-brain index still requires separate explicit approval.

## [2026-06-23] Phase 2B.6 Verification: Disposable ChatGPT Tunnel Smoke Test

Verification: the ChatGPT Secure MCP Tunnel path succeeded against a disposable GBrain state, using the `gbrain-disposable-stdio` tunnel-client profile and a stdio command scoped with `GBRAIN_HOME=/Users/ssavan99/repos/nexus-gbrain-chatgpt-state`.

Boundary: the test used fake disposable Markdown content only. The real private vault, real `/Users/ssavan99/.gbrain` state, GBrain HTTP mode, public tunnels, embeddings, real-brain import/sync/watch, OAuth/token values, and Claude Code setup were not used.

## [2026-06-23] Phase 2B.11 Verification: ChatGPT Read-Only GBrain Connector

Verification: the daily ChatGPT memory path should use the minimal read-only wrapper at `/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp`, connected as `Nexus GBrain Readonly Memory` through Secure MCP Tunnel. The wrapper exposes only `get_brain_identity` and `search`, and delegates search to the existing local GBrain CLI/index.

Decision: do not use raw GBrain MCP as the daily ChatGPT connector because it exposed write/admin/destructive tools. The raw private vault was not modified, and no GBrain HTTP mode, public tunnel, embeddings, real-brain import/sync/watch, or write tools were used.

## [2026-06-23] Phase 2B.12 Documentation Audit: ChatGPT Wrapper Runbook

Decision: document the daily ChatGPT connector as `Nexus GBrain Readonly Memory` using tunnel profile `gbrain-readonly-wrapper-stdio` and MCP command `/Users/ssavan99/.bun/bin/bun /Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp/src/index.ts`.

Reason: the earlier raw GBrain connector exposed destructive/admin tools, and the older wrapper command shape using `cd ... && bun run start` exited under `tunnel-client`. The safe daily ChatGPT path is the read-only wrapper only; Codex and planned Claude Code remain local raw GBrain MCP clients, while Claude chat / claude.ai should use a future read-only remote connector.

## [2026-06-24] Phase 2C Verification: Claude Code Uses Raw Local GBrain MCP

Verification: Claude Code connects to the local stdio GBrain MCP and a restarted session loaded all 89 `mcp__gbrain__*` tools; `get_brain_identity` returned the local PGLite brain. Full local raw access, matching Codex.

Decision: register the server at user scope in `~/.claude.json` (top-level `mcpServers`), NOT `~/.claude/settings.json`. Claude Code reads MCP servers from `~/.claude.json` / project `.mcp.json`; settings.json only handles permissions/hooks/env and silently ignores an `mcpServers` block (this was the initial misconfiguration). MCP servers load at startup, so a restart is required after config changes.

## [2026-06-24] Phase 2D Decision: Claude Chat Uses GBrain Native OAuth `read` Scope, Not A Custom Wrapper

Decision: claude.ai connects to GBrain through the native `gbrain serve --http` (OAuth 2.1) with a `read`-scoped client, rather than a bespoke read-only wrapper like the ChatGPT path.

Reason: GBrain enforces an OAuth scope hierarchy server-side (`read → write → admin`, plus `sources_admin`/`agent` siblings; `src/core/scope.ts`, enforced at `src/commands/serve-http.ts:1496`). ~48 tools default to `read`; 41 require elevated scopes. A `read` token is hard-blocked from every mutating tool — this makes the custom HTTP filter proxy (the earlier Phase 2D design) unnecessary. The ChatGPT wrapper is retained only because its tunnel is OpenAI-specific; it is not reused here.

Verification (local, 2026-06-24): registered a `read`-scoped `client_credentials` OAuth client, minted a token (granted `scope: read`), and against `serve --http` on localhost confirmed `search` (read) succeeds while `put_page` (write) is rejected with `{"error":"insufficient_scope","message":"Operation put_page requires 'write' scope","your_scopes":["read"]}`. The throwaway test client was revoked afterward.

Security posture: cloud surface gets `read` only (server-enforced, not convention). Raw stdio GBrain MCP stays local-only (Codex, Claude Code) and is never tunneled. Note: GBrain's HTTP `tools/list` returns all tools regardless of scope (enforcement is at call time), so claude.ai will display write tools but every call is rejected — a cosmetic wrinkle, not a security gap.

## [2026-06-24] Phase 2D Constraint: PGLite Single-Writer Lock Shapes The Always-On Design

Observation: the brain runs on PGLite (embedded). PGLite acquires an exclusive file lock for a process's lifetime (`src/core/pglite-engine.ts:217`; error "Could not acquire PGLite lock"). A long-lived `serve --http` holds that lock, so concurrent CLI ops time out ("Timed out waiting for PGLite lock"). This conflicts with keeping always-on local stdio agents against the same brain.

Decision (cost-driven, user goal: $0 now, robust always-on eventually): phase the rollout.
- 2D.1 (now, $0): on-demand `serve --http` + quick Cloudflare tunnel for validation; no local-agent changes.
- 2D.2 (durable, ~$0): one `serve --http` as the brain's sole owner under macOS launchd; local agents switch to `gbrain connect http://localhost:<port>/mcp` (full scope); claude.ai joins via a named Cloudflare tunnel (stable URL). Single-owner sidesteps the PGLite lock — no DB migration needed. Optional ~$8/yr domain for a clean hostname.
- 2D.3 (optional, later, ~$5/mo or 1-time HW): move gbrain + Postgres (GBrain supports a generic `postgres` engine via `init --url`) to an always-on host (small VPS or home server) for 24/7 access independent of the Mac.

Rejected for now: Supabase free tier as the always-on DB (pauses after ~1 week idle, 500 MB cap). Neon free serverless Postgres is the preferred $0 cloud DB option if/when 2D.3 is pursued.

## [2026-06-24] Phase 2D.1 Verification: claude.ai Connected Read-Only End-to-End

Verification: claude.ai connected to GBrain's native `serve --http` over a Cloudflare quick tunnel and passed the acceptance test — a `search` returned brain results; a `put_page` was refused server-side with `insufficient_scope`. Read-only confirmed on the real surface, not just locally.

Auth model (decided from observed claude.ai behavior): claude.ai's custom connector does **not** self-register against a server lacking a registration endpoint — it errors "Automatic client registration isn't supported … add an OAuth Client ID." So the working model is a **manually pre-registered public (PKCE) client, DCR off**: `register-client --scopes read --grant-types authorization_code --token-endpoint-auth-method none --redirect-uri https://claude.ai/api/mcp/auth_callback`. The user pastes the Client ID into the connector's Advanced/OAuth field (no secret). claude.ai's verified redirect URI is `https://claude.ai/api/mcp/auth_callback`.

Security: DCR is kept OFF — confirmed that open DCR (`--enable-dcr`) does not clamp self-registered clients to `read` (oauth-provider.ts validates but does not downscope), so it must never be left exposed on a public tunnel. The Client ID is a public PKCE identifier, not a secret; the brain enforces `read` server-side regardless.

Operational: quick-tunnel URLs are ephemeral and the server must run in a user-owned terminal (assistant background tasks get reaped mid-flow, dropping the tunnel). Helper script: `scripts/claude-chat-gbrain-tunnel.sh`. For always-on (2D.2): include `refresh_token` in the client grants, use a stable tunnel, and run the server under launchd.

## [2026-06-24] Incident + Decision: Migrate Brain PGLite → Local Postgres For Robust Always-On

Incident: during the 2D.2 transition, a long-running PGLite `gbrain serve --http` was stopped with `pkill`. The unclean stop left the PGLite cluster in "in production" state; on next open, WASM Postgres crashed during WAL-replay recovery (`PGLite failed to initialize its WASM runtime … Aborted()`), taking the brain offline for ALL local clients. Root-caused via `pg_controldata` (cluster state) after ruling out lock/sandbox/process issues. Recovered with **zero data loss** by `pg_resetwal -f -D ~/.gbrain/brain.pglite` (using `postgresql@17`), which reset the crashed WAL and let PGLite reopen all 84 pages. The crashed dir was copied to `brain.pglite.crashed-bak-*` first.

Decision: PGLite's single-writer model + corruption-on-unclean-stop is unacceptable for an always-on, internet-exposed server (a reboot, OOM, or launchd SIGKILL could re-trigger it). Migrated the brain to **local Postgres** (`postgresql@17` via `brew services`, free, on-device) with `pgvector` + `pg_trgm`:

```sh
gbrain migrate --to supabase --url postgresql://localhost:5432/gbrain
```

(`--to supabase` selects the generic `postgres` engine; the `--url` points at local Postgres.) Config auto-switched to `engine: postgres`; PGLite dir kept as backup. Verified: 84 pages, search, and concurrent reads (two at once — impossible under PGLite's lock). Local stdio agents (Codex, Claude Code) pick up the new engine transparently via `~/.gbrain/config.json`; no client reconfig needed.

Reason: Postgres gives crash-safe recovery + concurrent connections, so the always-on HTTP server can run continuously alongside local agents without the lock contention or corruption risk that defined the PGLite era. This also lays the groundwork for 2D.3 (move Postgres to an always-on host).

## [2026-06-24] Phase 2D.2 Done: Always-On claude.ai Connector (Postgres + ngrok + launchd)

Decision/outcome: the always-on stack is one launchd unit (`scripts/com.nexus.claude-chat-gbrain.plist` → `scripts/claude-chat-gbrain-serve.sh`, KeepAlive, login auto-start) running `gbrain serve --http` (Postgres-backed, DCR off) plus `ngrok` pinned to a **free static domain** (`*.ngrok-free.dev`, value in gitignored `scripts/tunnel.env`). claude.ai uses a manual read-only public PKCE client with `refresh_token`. End-to-end verified from claude.ai: read works, write refused.

Choices: ngrok free static domain over a Cloudflare named tunnel because the latter needs a recurring-fee domain; ngrok's one-time OAuth-page interstitial is acceptable (server-to-server traffic never sees it). Script polls child PIDs instead of `wait -n` (macOS `/bin/bash` is 3.2). Everything stays $0.
