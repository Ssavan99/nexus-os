# ChatGPT GBrain MCP Connection Plan

Phase: 2B ChatGPT MCP feasibility and safety preflight.

Status: planning only. Do not expose GBrain to ChatGPT until the user explicitly approves a separate implementation step.

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

ChatGPT is different because ChatGPT runs as an OpenAI-hosted product and cannot directly spawn a local stdio process on this machine. The official ChatGPT Apps connection flow expects a remote MCP server reachable over HTTPS, with the connector URL pointing at the server's public `/mcp` endpoint. ChatGPT developer mode currently supports SSE and streaming HTTP for remote MCP apps.

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

GBrain appears to support an HTTP MCP mode that could be suitable for ChatGPT only after a separate, approved exposure/auth design.

The minimum ChatGPT-compatible shape is expected to be:

- A GBrain HTTP MCP server, likely started with `gbrain serve --http`.
- A reachable HTTPS URL for ChatGPT.
- A `/mcp` endpoint or endpoint shape accepted by ChatGPT connector setup.
- A security model, preferably OAuth for third-party cloud access.
- If behind a tunnel or reverse proxy, a correct `--public-url` issuer value.

This is not equivalent to the current safe Codex stdio setup.

## Does ChatGPT Require These?

Remote HTTP: yes, for ChatGPT. Official docs describe ChatGPT connectors as remote MCP servers reachable over HTTPS.

Auth token: possibly. GBrain supports bearer-token remote wiring, but bearer tokens are described by GBrain as simple, long-lived, and full-access. That is not the safest first choice for exposing a private brain to a cloud product.

OAuth: likely recommended if exposing GBrain to ChatGPT. ChatGPT supports OAuth, no authentication, and mixed authentication in developer mode, while GBrain HTTP mode advertises OAuth 2.1 options. OAuth should be treated as the safer path for any non-local exposure.

Tunnel: likely required for local-first testing unless GBrain is deployed to a real HTTPS host. Official OpenAI docs mention Secure MCP Tunnel for private MCP servers, or tools such as ngrok or Cloudflare Tunnel for exposing a local server. No tunnel should be installed or started without explicit approval.

API keys: not for GBrain keyword search itself. Secure MCP Tunnel or other hosted tooling may have its own account/auth requirements, but this preflight does not require adding OpenAI API keys, embedding keys, or provider keys.

## Safest Local-First Approach

1. Keep Codex using local stdio MCP as the verified baseline.
2. Treat ChatGPT connection as a separate remote-access project, not a continuation of local MCP.
3. Before starting any HTTP server, decide the exact auth model:
   - preferred: OAuth 2.1 with least-privilege read-only scopes if GBrain supports enforcing them for the needed tools;
   - avoid: no-auth exposure;
   - avoid unless explicitly accepted: bearer token exposure to ChatGPT.
4. Prefer an outbound-only private tunnel such as Secure MCP Tunnel over a public ngrok/Cloudflare URL if available for the user's ChatGPT/OpenAI account.
5. If testing proceeds, expose only read/search tools at first. Do not expose write, import, sync, watch, embed, files, jobs, or shell-like capabilities.
6. Confirm the connector's tool list in ChatGPT before using it in a chat.
7. Keep permission settings at the most conservative level, such as always asking before tool calls where available.

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

Run these only after explicit approval to start HTTP serving and configure a private ChatGPT connector:

1. Start GBrain HTTP MCP locally with the approved auth and URL settings.
2. Verify locally that the HTTP endpoint advertises only intended read/search tools.
3. Create the ChatGPT connector as a private draft.
4. Confirm ChatGPT shows the expected tool list before using the connector.
5. Run read-only identity or health check if exposed.
6. Search for a non-sensitive marker query first.
7. Search for the same safe startup workflow queries used in Codex Phase 2A:
   - `startup-dashboard`
   - `customer discovery playbook`
   - `weekly startup review`
   - `shared organizational brain`
8. Confirm results are summarized without copying broad private content into Nexus OS.
9. Confirm no write/import/sync/watch/embed/job/file tools are callable from ChatGPT.
10. Disconnect immediately after the test unless there is a separate approval to keep it available.

## Rollback And Disconnect Plan

- Disable or delete the connector in ChatGPT Settings -> Apps & Connectors.
- Stop the local `gbrain serve --http` process.
- Stop and remove any approved tunnel process.
- Revoke any generated OAuth client or bearer token.
- Remove any local config that was added only for the ChatGPT test.
- Re-run Codex local stdio smoke tests to confirm Phase 2A still works.
- Record the outcome in `docs/decision-log.md`.

## What Not To Do

- Do not expose the private vault over HTTP.
- Do not run `gbrain serve --http` without explicit approval.
- Do not create a public tunnel without explicit approval.
- Do not use no-auth exposure for the private brain.
- Do not create bearer tokens or OAuth clients during preflight.
- Do not paste tokens, secrets, private URLs, or raw private notes into ChatGPT.
- Do not enable embeddings or add API keys.
- Do not run import, sync, watch, embed, or background jobs.
- Do not install ChatGPT-specific tools during preflight.
- Do not build a duplicate Nexus OS RAG/search/MCP layer around GBrain.
