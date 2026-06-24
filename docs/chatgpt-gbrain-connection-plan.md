# ChatGPT GBrain MCP Connection Plan

Phase: 2B ChatGPT MCP feasibility and safety preflight.

Status: superseded for daily use by `docs/chatgpt-readonly-connector.md`.

Daily ChatGPT access must use:

```text
ChatGPT -> Secure MCP Tunnel -> tunnel-client -> nexus-gbrain-readonly-mcp -> GBrain CLI/search -> real GBrain index
```

Do not use raw GBrain MCP as the daily ChatGPT connector. Raw GBrain MCP exposed write/admin/destructive tools. Disable/delete `GBrain Local Memory Read Test` or any connector exposing tools such as `put_page`, `delete_page`, `add_link`, `add_tag`, `submit_job`, `sync_brain`, `schema_apply_mutations`, or `sources_remove`.

## Current Local State

- Private brain path: `/Users/ssavan99/Desktop/Personal-Obsidian`
- GBrain executable: `/Users/ssavan99/.bun/bin/gbrain`
- GBrain version observed during Phase 2A: `0.42.38.0`
- Current Codex MCP command: `/Users/ssavan99/.bun/bin/gbrain serve`
- Current engine: local PGLite under `~/.gbrain`
- Current import mode: keyword-only, `--no-embed`
- Current external exposure: none

This preflight did not read, edit, import, sync, watch, embed, or expose private vault files.

## Why ChatGPT Is Different From Codex And Claude

Codex can run GBrain locally over stdio:

```text
/Users/ssavan99/.bun/bin/gbrain serve
```

That keeps the MCP transport local to the same machine and does not require a public URL, tunnel, bearer token, OAuth flow, or API key.

ChatGPT is different because ChatGPT runs as an OpenAI-hosted product and cannot directly spawn a local stdio process on this machine. The daily route uses OpenAI Secure MCP Tunnel so ChatGPT can reach a local read-only MCP wrapper without exposing raw GBrain MCP or starting `gbrain serve --http`.

Sources:

- OpenAI Apps SDK: [Connect from ChatGPT](https://developers.openai.com/apps-sdk/deploy/connect-chatgpt)
- OpenAI docs: [Developer mode](https://developers.openai.com/api/docs/guides/developer-mode)
- OpenAI docs: [MCP and Connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)

## Local GBrain Capability Findings

`/Users/ssavan99/.bun/bin/gbrain --help` shows two relevant serving modes:

```text
serve                              MCP server (stdio)
serve --http [--port N]            HTTP MCP server with OAuth 2.1
  --token-ttl N                    Access token TTL in seconds (default: 3600)
  --enable-dcr                     Enable Dynamic Client Registration
  --public-url URL                 Public issuer URL (required behind proxy/tunnel)
```

`/Users/ssavan99/.bun/bin/gbrain connect --help` says the remote MCP URL is a `gbrain serve --http` endpoint and rejects bare hosts; it requires an explicit `https://` URL. It also describes bearer-token mode as simple and full-access, and OAuth client credentials as better for anything exposed to a third-party cloud.

`gbrain serve --help` and `gbrain auth --help` did not expose additional command-specific details beyond the top-level help in this version.

## Feasibility Conclusion

GBrain supports raw stdio and HTTP MCP modes, but raw GBrain MCP is not safe for daily ChatGPT use because it exposes write/admin/destructive tools.

The safe ChatGPT-compatible shape is:

- `Nexus GBrain Readonly Memory` connector.
- OpenAI Secure MCP Tunnel.
- `gbrain-readonly-wrapper-stdio` tunnel profile.
- MCP command: `/Users/ssavan99/.bun/bin/bun /Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp/src/index.ts`
- Wrapper tools only: `get_brain_identity`, `search`.

This is not equivalent to the current safe Codex stdio setup.

## Does ChatGPT Require These?

Remote HTTP: not from GBrain directly for the daily path. ChatGPT reaches the local wrapper through Secure MCP Tunnel.

Auth token: possibly. GBrain supports bearer-token remote wiring, but bearer tokens are described by GBrain as simple, long-lived, and full-access. That is not the safest first choice for exposing a private brain to a cloud product.

OAuth: not part of the current daily wrapper path.

Tunnel: yes. Use OpenAI Secure MCP Tunnel, not public tunnel tools.

API keys: no OpenAI/GBrain embedding keys are needed for keyword search. The Secure MCP Tunnel runtime key must be exported locally only, must have Tunnels Read + Use, and must never be pasted into ChatGPT, Codex, docs, `.env`, `.zshrc`, screenshots, or committed files.

## Safest Local-First Approach

1. Keep Codex using raw local GBrain stdio MCP.
2. Use the read-only wrapper for ChatGPT.
3. Keep ChatGPT permission set to `Always ask`.
4. Expose only `get_brain_identity` and `search`.
5. Do not expose raw GBrain tools to ChatGPT.

## Security Risks

- Private brain search results could leave the local machine and appear in ChatGPT conversations.
- A remote MCP endpoint could expose private memory to anyone with the URL or token if auth is misconfigured.
- Bearer tokens are high-risk if long-lived, logged, pasted into chats, or stored in screenshots.
- OAuth misconfiguration can create overbroad access, broken audience checks, missing scope enforcement, or callback issues.
- Public tunnels can make a local service internet-reachable.
- Tool descriptions and tool outputs can be prompt-injection surfaces.
- ChatGPT may retrieve more context than intended if broad search tools are exposed.
- Current GBrain tools may include write-capable or background-job operations unless restricted by auth/tool policy.

## Manual ChatGPT UI Checks

Before implementation, check these manually in ChatGPT:

1. Confirm the account/workspace has Apps/Connectors developer mode available.
2. In ChatGPT, open Settings -> Apps & Connectors -> Advanced settings.
3. Confirm Developer mode can be enabled by the user or workspace admin.
4. Confirm there is a Create button for an app/connector.
5. Confirm the connector creation UI asks for a remote MCP connector URL.
6. Confirm the UI supports the desired auth mode: OAuth, no auth, or mixed auth.
7. Confirm app permissions can be set conservatively, preferably requiring confirmation before tool calls.
8. Confirm whether the connector can be kept private/draft and not published to a workspace.
9. Confirm whether the connector supports the intended surface: normal chat, deep research, company knowledge, or developer mode only.
10. Do not paste a private GBrain URL, token, OAuth secret, or tunnel URL until the implementation plan has been approved.

## Recommended Smoke Tests If Later Approved

Use these with `Nexus GBrain Readonly Memory`:

```text
Use the Nexus GBrain Readonly Memory connector only. List the available tools. Do not retrieve private note content yet.
```

```text
Use the Nexus GBrain Readonly Memory connector only. Search for "startup-dashboard" and return only result titles/slugs, not note text.
```

```text
Use the Nexus GBrain Readonly Memory connector only. Search for "customer discovery playbook" and return only result titles/slugs, not note text.
```

## Rollback And Disconnect Plan

- Disable or delete the connector in ChatGPT Settings -> Apps & Connectors.
- Stop `tunnel-client run --profile gbrain-readonly-wrapper-stdio`.
- Stop and remove any approved tunnel process.
- Revoke any generated OAuth client or bearer token.
- Disable/delete raw GBrain ChatGPT connectors.
- Re-run Codex local stdio smoke tests to confirm Phase 2A still works.
- Record the outcome in `docs/decision-log.md`.

## What Not To Do

- Do not expose the private vault over HTTP.
- Do not run `gbrain serve --http` without explicit approval.
- Do not create a public tunnel without explicit approval.
- Do not use raw GBrain MCP for the daily ChatGPT connector.
- Do not use no-auth exposure for the private brain.
- Do not create bearer tokens or OAuth clients during preflight.
- Do not paste tokens, secrets, private URLs, or raw private notes into ChatGPT.
- Do not enable embeddings or add API keys.
- Do not run import, sync, watch, embed, or background jobs.
- Do not install ChatGPT-specific tools during preflight.
- Do not build a duplicate Nexus OS RAG/search/MCP layer around GBrain.
