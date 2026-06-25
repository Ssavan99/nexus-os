# Claude Chat (claude.ai) GBrain Plan

Status: Phase 2D.2 — DONE. claude.ai is connected read-only to the GBrain brain over a **permanent** ngrok static URL, served by an always-on `gbrain serve --http` under launchd, backed by **local Postgres** (migrated off PGLite). Read works, write refused, end-to-end verified.

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

## Connection Architecture (as built)

```text
claude.ai (custom connector, OAuth 2.1, manual public PKCE client)
   -> HTTPS ngrok static domain (plaster-paving-water.ngrok-free.dev — value kept in scripts/tunnel.env, gitignored)
   -> gbrain serve --http  (--bind 127.0.0.1 --public-url <ngrok-url>, DCR off)
   -> OAuth: read-scoped client  -> local Postgres-backed GBrain (read tools only)
```

Both `gbrain serve --http` and `ngrok` run under one launchd unit (`scripts/com.nexus.claude-chat-gbrain.plist` → `scripts/claude-chat-gbrain-serve.sh`), KeepAlive, auto-start at login.

## Engine: migrated PGLite → local Postgres (important)

Originally the brain ran on **PGLite** (embedded, single-writer): a long-lived `serve --http` holds an exclusive file lock, and — critically — an **unclean stop corrupts the data dir** (cluster left "in production" → WAL-replay crash → `PGLite ... WASM ... Aborted()` on next open). We hit exactly this when a `serve --http` was `pkill`ed (see decision log 2026-06-24). Recovery: `pg_resetwal -f` on `~/.gbrain/brain.pglite` (needs `postgresql@17`).

That fragility is unacceptable for an always-on server, so the brain was **migrated to local Postgres**:

```sh
brew services start postgresql@17           # always-on DB service ($0, local)
brew install pgvector                        # GBrain schema needs the vector extension
createdb gbrain && psql -d gbrain -c 'CREATE EXTENSION vector; CREATE EXTENSION pg_trgm;'
gbrain migrate --to supabase --url postgresql://localhost:5432/gbrain   # "supabase" == generic postgres target
```

Postgres is crash-safe and supports concurrent connections, so: an unclean stop no longer corrupts the brain, and the always-on HTTP server coexists with the local stdio agents (Codex, Claude Code) — they read the new engine transparently via `~/.gbrain/config.json` (now `engine: postgres`). The old PGLite dir is preserved at `~/.gbrain/brain.pglite` as a backup.

## Rollout history (cost-optimized: $0 throughout)

| Stage | What | Cost | Always-on |
|---|---|---|---|
| 2D.1 validate | On-demand `serve --http` + quick Cloudflare tunnel; PGLite | $0 | No (manual) |
| 2D.2 durable (BUILT) | Local Postgres engine + `serve --http` + **ngrok static domain**, all under launchd (KeepAlive, login auto-start) | $0 | Yes, while Mac awake |
| 2D.3 independent (future) | Move gbrain + Postgres to a small VPS / home server | ~$5/mo or 1-time HW | Yes, 24/7 |

Cost notes: ngrok free tier includes 1 static domain ($0); it shows a one-time browser interstitial on the OAuth consent page (click "Visit Site" once — server-to-server MCP traffic never sees it). A Cloudflare named tunnel was the alternative but needs a recurring-fee domain, so ngrok was chosen.

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

## 2D.2 Operations (the live always-on setup)

- **Connector URL:** `https://plaster-paving-water.ngrok-free.dev/mcp` (permanent).
- **Client:** read-only public PKCE client `claude-chat-readonly`, grants `authorization_code,refresh_token` (refresh_token avoids the 1h TTL drop), redirect `https://claude.ai/api/mcp/auth_callback`. The Client ID is pasted into claude.ai's Advanced/OAuth field (no secret). Re-register with `gbrain auth register-client … --scopes read --token-endpoint-auth-method none --redirect-uri …`.
- **Service control:**
  ```sh
  launchctl list | grep com.nexus.claude-chat-gbrain      # status (PID, last exit)
  launchctl unload ~/Library/LaunchAgents/com.nexus.claude-chat-gbrain.plist   # stop
  launchctl load -w ~/Library/LaunchAgents/com.nexus.claude-chat-gbrain.plist  # start
  tail -f /tmp/nexus-launchd.out /tmp/nexus-gbrain-http.log /tmp/nexus-ngrok.log
  ```
- **Config:** `scripts/tunnel.env` (gitignored) holds `STABLE_DOMAIN`. ngrok authtoken is in the user's ngrok config. Postgres runs via `brew services` (also auto-start).
- **Gotcha fixed:** macOS `/bin/bash` is 3.2 — no `wait -n`; the serve script polls both child PIDs instead.
- **If PGLite is ever used again and crashes:** `pg_resetwal -f -D ~/.gbrain/brain.pglite` (via `postgresql@17`) clears the crashed WAL state. Not relevant now that the engine is Postgres.

## Security Invariants (recap)

- Cloud connector gets `read` scope only; enforced server-side. DCR stays OFF (it doesn't clamp self-registered clients to `read`).
- `scripts/tunnel.env`, ngrok authtoken, and any client secret stay out of the repo.
- Raw stdio GBrain MCP stays local-only (Codex, Claude Code); never tunneled.
- Stop the server gracefully; with Postgres an unclean stop is safe, but still prefer `launchctl unload` over `kill -9`.

## Open Items / Future

- 2D.3: move Postgres + gbrain to an always-on host (small VPS / home server) for 24/7 reach independent of the Mac being awake.
- Optional: a tiny `tools/list` filter so claude.ai only *displays* read tools (cosmetic; enforcement already correct).
