# ChatGPT Read-Only GBrain Connector

Status: Phase 2E (2026-06-25) — ChatGPT migrated to the always-on native HTTP MCP. The tunnel-client/wrapper path below is RETIRED (kept as fallback only).

## Current path (Phase 2E): native always-on HTTP MCP — zero manual commands

ChatGPT (Developer Mode custom connector) now uses the same always-on endpoint as claude.ai:

```text
ChatGPT custom connector (OAuth, "User-Defined OAuth Client")
  -> https://plaster-paving-water.ngrok-free.dev/mcp   (ngrok static domain)
  -> gbrain serve --http (local Postgres engine, DCR off, under launchd)
  -> OAuth: read-scoped public PKCE client "chatgpt-readonly"
```

- Connector URL: `https://plaster-paving-water.ngrok-free.dev/mcp`
- Registration method: **User-Defined OAuth Client**; Client ID = `chatgpt-readonly` client; **no secret**; token-endpoint auth method **none**.
- ChatGPT's per-connector redirect URI was `https://chatgpt.com/connector/oauth/<id>` (read off the New App dialog; re-register the client if recreated).
- Read-only enforced server-side (writes refused with `insufficient_scope`); ChatGPT individual tiers are read/fetch-only anyway.
- **No terminal commands per session** — the launchd stack (see `docs/claude-chat-gbrain-plan.md`) auto-starts at login. This is the success criterion vs the old wrapper.

Verified 2026-06-25: read (`search`) returns brain results from ChatGPT.

To decommission the old path: disconnect the old `Nexus GBrain Readonly Memory` connector in ChatGPT and stop running `openai-tunnel-client`. Keep the wrapper code (below) as fallback.

---

## RETIRED path (Phase 2B): tunnel-client + wrapper (fallback only)

Previously, daily ChatGPT lookup used:

```text
ChatGPT -> Secure MCP Tunnel -> tunnel-client -> nexus-gbrain-readonly-mcp -> GBrain CLI/search -> real GBrain index
```

Connector name:

```text
Nexus GBrain Readonly Memory
```

Wrapper path:

```text
/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp
```

Tunnel client path:

```text
/Users/ssavan99/MCPs/openai-tunnel-client/tunnel-client
```

Tunnel profile:

```text
gbrain-readonly-wrapper-stdio
```

Final working MCP command:

```text
/Users/ssavan99/.bun/bin/bun /Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp/src/index.ts
```

## Allowed Tools

The read-only wrapper exposes exactly:

- `get_brain_identity`
- `search`

ChatGPT permission setting:

```text
Always ask
```

## Do Not Use Raw GBrain MCP For ChatGPT

The raw GBrain MCP connector exposed destructive/admin tools, including write, job, sync, source-management, and schema mutation tools. It is not safe as the daily ChatGPT connector.

Disable or delete any raw ChatGPT connector such as:

- `GBrain Local Memory Read Test`
- any connector exposing raw GBrain tools such as `put_page`, `delete_page`, `add_link`, `add_tag`, `submit_job`, `sync_brain`, `schema_apply_mutations`, or `sources_remove`

Do not connect ChatGPT directly to raw GBrain MCP unless GBrain later provides a verified read-only/native tool-filtered surface.

## Daily Runbook

1. Open a local terminal.
2. Export the runtime key locally only:

```bash
export CONTROL_PLANE_API_KEY="..."
```

Do not paste `CONTROL_PLANE_API_KEY` into ChatGPT, Codex, docs, `.env`, `.zshrc`, README files, screenshots, or committed files. The key should have only Tunnels Read + Use.

3. Start the tunnel:

```bash
/Users/ssavan99/MCPs/openai-tunnel-client/tunnel-client run \
  --profile gbrain-readonly-wrapper-stdio
```

4. Leave the terminal open.
5. In ChatGPT, use the connector:

```text
Nexus GBrain Readonly Memory
```

6. Stop the tunnel with `Ctrl+C` when done.

## One-Time Profile Setup

`tunnel-client init` is one-time setup and should not be rerun unless changing the tunnel ID, command, or profile. If replacing an existing profile, use `--force` intentionally.

Preferred profile init command:

```bash
/Users/ssavan99/MCPs/openai-tunnel-client/tunnel-client init \
  --sample sample_mcp_stdio_local \
  --profile gbrain-readonly-wrapper-stdio \
  --force \
  --tunnel-id "<tunnel_id>" \
  --mcp-command "/Users/ssavan99/.bun/bin/bun /Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp/src/index.ts"
```

Doctor command:

```bash
/Users/ssavan99/MCPs/openai-tunnel-client/tunnel-client doctor \
  --profile gbrain-readonly-wrapper-stdio \
  --explain
```

`codex_plugin SKIP` from `tunnel-client doctor` is optional and not a blocker.

Run command:

```bash
/Users/ssavan99/MCPs/openai-tunnel-client/tunnel-client run \
  --profile gbrain-readonly-wrapper-stdio
```

Do not use the older command shape `cd /Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp && bun run start` as the preferred tunnel MCP command. It exited under `tunnel-client`; use the absolute Bun command above.

## Smoke-Test Prompts

```text
Use the Nexus GBrain Readonly Memory connector only. List the available tools. Do not retrieve private note content yet.
```

```text
Use the Nexus GBrain Readonly Memory connector only. Search for "startup-dashboard" and return only result titles/slugs, not note text.
```

```text
Use the Nexus GBrain Readonly Memory connector only. Search for "customer discovery playbook" and return only result titles/slugs, not note text.
```

## Boundaries

- The private vault is not modified.
- No `gbrain serve --http` path is used.
- No public tunnel is used.
- No embeddings are enabled.
- No real-brain import, sync, watch, or writeback is run.
- No write/admin/destructive tools are exposed to ChatGPT.
