# Claude Chat (claude.ai) GBrain Plan

Status: Phase 2D.1 — VERIFIED. claude.ai is connected read-only to the GBrain brain over a Cloudflare quick tunnel; read works, write refused end-to-end. Always-on (2D.2) pending.

This document covers how claude.ai (cloud-hosted Claude chat) accesses the GBrain-backed brain safely.

## Why Claude Chat Cannot Use Raw GBrain MCP

Claude chat runs as a cloud service and cannot reach a local stdio process. Raw GBrain MCP also exposes destructive/admin tools. The same boundary that protects ChatGPT applies.

## Chosen Approach: GBrain Native HTTP + OAuth `read` Scope

GBrain enforces an OAuth 2.1 scope hierarchy **server-side** — no custom wrapper or filter proxy is needed.

- Scopes: `read → write → admin` (+ `sources_admin`, `agent` siblings). Source: `gbrain/src/core/scope.ts`; enforced at `gbrain/src/commands/serve-http.ts:1496`.
- ~48 of 89 tools default to `read`; 41 require `write`/`admin`/`sources_admin`/`agent`.
- A `read`-scoped token is hard-blocked from every mutating tool.

This supersedes the earlier Phase 2D design (a custom HTTP filter proxy mirroring the ChatGPT stdio wrapper). The ChatGPT wrapper at `/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp` stays as-is because its tunnel is OpenAI-specific; it is **not** reused here.

### Verified locally (2026-06-24)

A `read`-scoped `client_credentials` client was registered and tested against `serve --http` on localhost:

- `search` (read) → success.
- `put_page` (write) → `{"error":"insufficient_scope","message":"Operation put_page requires 'write' scope","your_scopes":["read"]}`.

The throwaway test client was revoked. Read-only is enforced by the server, not by convention.

> Note: GBrain's HTTP `tools/list` returns all tools regardless of scope (enforcement is at call time). claude.ai will *display* write tools, but every write call is rejected. Cosmetic only.

## Connection Architecture

```text
claude.ai (custom connector, OAuth 2.1)
   -> HTTPS tunnel (Cloudflare)
   -> gbrain serve --http  (--bind 0.0.0.0 --public-url <tunnel> [--enable-dcr])
   -> OAuth: read-scoped client  -> GBrain index (read tools only)
```

## The PGLite Constraint (important)

The brain runs on **PGLite** (embedded, single-writer). A long-lived `serve --http` holds an exclusive file lock for its lifetime, so other gbrain processes / CLI ops can time out ("Timed out waiting for PGLite lock"). This shapes how the server is run for an always-on setup — see the phased rollout below. The single-owner model (2D.2) sidesteps this without a DB migration.

## Phased Rollout (cost-optimized: $0 now → robust always-on later)

| Stage | What | Cost | Always-on |
|---|---|---|---|
| 2D.1 validate | On-demand `serve --http` + quick Cloudflare tunnel; existing PGLite; no local-agent changes | $0 | No (manual) |
| 2D.2 durable | One `serve --http` as sole brain owner under macOS launchd; local agents (Codex, Claude Code) switch to `gbrain connect http://localhost:<port>/mcp` (full scope); **named** Cloudflare tunnel for a stable URL | $0 (opt. ~$8/yr domain) | Yes, while Mac awake |
| 2D.3 independent | Move gbrain + **Postgres** (`init --url`) to a small VPS or home server | ~$5/mo or 1-time HW | Yes, 24/7 |

Cost notes: Cloudflare Tunnel is free (stable hostname ideally needs a domain on Cloudflare). Supabase free tier is a poor always-on DB (pauses ~1 week idle, 500 MB cap); Neon free serverless Postgres is the preferred $0 cloud DB if 2D.3 is pursued.

## Runbook — 2D.1 Validation (VERIFIED 2026-06-24)

This is the method that actually worked. claude.ai's connector does **not** support
auto self-registration against a server with no registration endpoint — it shows
"Automatic client registration isn't supported … add an OAuth Client ID." So we use
a **manually pre-registered public (PKCE) read client with DCR off** (no secret),
which is also the safer posture (open DCR does not clamp scope to `read`).

1. **Register a read-only public client** (local, one-time; persists in the brain DB)
   ```sh
   gbrain auth register-client "claude-chat-readonly" \
     --scopes read \
     --grant-types authorization_code \
     --token-endpoint-auth-method none \
     --redirect-uri https://claude.ai/api/mcp/auth_callback
   ```
   - `--token-endpoint-auth-method none` = public client → **Client ID only, no secret**.
   - `https://claude.ai/api/mcp/auth_callback` is claude.ai's verified redirect URI.
   - The Client ID is not a secret (public PKCE client); the brain enforces `read` regardless.
   - For durable use, also include `refresh_token` in `--grant-types` (this validation run used
     `authorization_code` only, so claude.ai's token expires at the 3600s TTL and re-auths).
   - Revoke with `gbrain auth revoke-client <client_id>`.

2. 🔶 **Install the tunnel** (done: `brew install cloudflared`).

3. **Bring up server + tunnel** — run the helper in a terminal that stays open:
   ```sh
   bash scripts/claude-chat-gbrain-tunnel.sh
   ```
   It starts the Cloudflare quick tunnel, then `gbrain serve --http --bind 127.0.0.1
   --public-url <tunnel>` (DCR off, `--bind 127.0.0.1` is fine because cloudflared runs
   on the same host), and prints the connector URL. Logs: `/tmp/nexus-gbrain-http.log`,
   `/tmp/nexus-cf.log`. (Note: GBrain logs MCP/auth requests to the `mcp_request_log`
   DB table, not stdout — a quiet log file is normal.)

   > Run the server + tunnel in your **own** terminal, not via an assistant background
   > task — those get reaped while you switch to the browser, dropping the tunnel
   > mid-OAuth.

4. 🔶 **Add the custom connector in claude.ai**
   - Add custom connector → URL = `https://<tunnel>/mcp`.
   - Advanced / OAuth → **OAuth Client ID** = the id from step 1; **Client Secret** empty.
   - Connect → approve consent (no passwords).

5. **Acceptance test (from claude.ai) — PASSED**
   - Read (`search startup dashboard`) → returned results. ✅
   - Write (`create page slug zzz-test`) → refused by server (`insufficient_scope`). ✅

## Security Invariants

- Cloud connector gets `read` scope only; never `write`/`admin`. Enforced server-side.
- Client secret / tunnel token never committed to this public repo.
- `--public-url` must match the tunnel origin (OAuth issuer correctness).
- Raw stdio GBrain MCP stays local-only (Codex, Claude Code). Never tunneled.
- Negative test (write rejected) is a required acceptance criterion. ✅ verified end-to-end from claude.ai.
- DCR stays OFF: open DCR (`--enable-dcr`) does NOT clamp self-registered clients to `read` (they may request `write`/`admin`), so it must not be left exposed on a public tunnel.

## Open Items

- DCR vs pre-registered client: confirm which claude.ai's connector flow expects (try DCR first; fall back to manual client_id/secret).
- For 2D.2: launchd plist for `serve --http`; named Cloudflare tunnel; migrate local agents to `gbrain connect localhost`.
