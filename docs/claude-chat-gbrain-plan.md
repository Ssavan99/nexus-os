# Claude Chat GBrain Plan

Status: Phase 2D planned.

This document covers how claude.ai (cloud-hosted Claude chat) will access the GBrain-backed brain safely.

## Why Claude Chat Cannot Use Raw GBrain MCP

Claude chat runs as a cloud service. It cannot reach a local stdio process. Raw GBrain MCP also exposes destructive and admin tools (write, delete, sync, embed, autopilot, admin). The same boundary that protects ChatGPT applies here.

## Chosen Approach: HTTP Read-Only Filter Proxy

GBrain already ships with a native HTTP MCP server with OAuth 2.1:

```sh
gbrain serve --http [--port N] [--public-url URL]
```

Rather than building a new stdio wrapper + tunnel client (as was done for ChatGPT), Phase 2D will use a thin HTTP read-only filter proxy that sits in front of `gbrain serve --http`. This approach:

- Reuses GBrain's native OAuth 2.1 infrastructure (no custom token management).
- Exposes only safe read-only tools by intercepting the tool list before passing it to Claude.ai.
- Works natively with Claude.ai's Remote MCP support (HTTP + OAuth 2.1).
- Avoids building a new tunnel client from scratch.

## Connection Path

```text
Claude chat -> HTTPS -> read-only HTTP filter proxy -> gbrain serve --http -> GBrain index
```

The filter proxy:

- Accepts MCP HTTP requests from Claude.ai.
- Passes auth through to GBrain's OAuth 2.1 layer.
- Overrides `tools/list` to return only the allowed read-only tools.
- Passes `tools/call` through only for allowed tools; rejects all others.
- Exposed via cloudflared tunnel or equivalent with a stable public URL.

## Allowed Tools For Claude Chat

The filter proxy will expose exactly:

- `get_brain_identity` — same as ChatGPT connector.
- `search` — tsvector keyword search, same as ChatGPT connector.
- `query` — hybrid RRF + semantic expansion search. This is strictly more powerful than `search` and is appropriate for claude.ai, which benefits from semantic relevance ranking.

The `query` tool is not exposed to ChatGPT (conservative first deployment). Claude chat is the first surface to expose it.

## Why Not Reuse The ChatGPT Stdio Wrapper

The ChatGPT wrapper (`nexus-gbrain-readonly-mcp`) is a stdio MCP process bridged to ChatGPT via an OpenAI-specific tunnel client. Claude.ai uses a different protocol (HTTP MCP with OAuth 2.1), so the ChatGPT tunnel architecture does not transfer directly.

However, the tool filtering logic and safety constraints from that wrapper are directly reusable in the HTTP proxy.

## Build Steps (When Ready)

1. Create `/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp-http` as a small Bun/Node HTTP server.
2. On startup, spawn `gbrain serve --http` on a local port.
3. Proxy all MCP HTTP requests to that local gbrain HTTP server.
4. Filter `tools/list` to return only `get_brain_identity`, `search`, and `query`.
5. Reject `tools/call` for any tool not in the allowed list.
6. Expose the proxy over a cloudflared tunnel with a stable `--public-url`.
7. Register the tunnel URL in Claude.ai as a Remote MCP connector.

## Alternative: Native GBrain Read-Only Mode

If GBrain introduces a native read-only mode or tool-scope flag in a future version, replace this proxy with that native surface. Check `gbrain --help` and GBrain release notes before building the proxy.

## Security Constraints

- Never expose raw `gbrain serve --http` directly to Claude.ai without the filter layer.
- The allowed tool list must be hardcoded in the proxy, not configurable at runtime.
- The tunnel must use HTTPS only.
- Rotate the cloudflared tunnel token if compromised.
- Keep the public URL out of this public repo; store it in `.env`.

## Relationship To ChatGPT Connector

| Surface | Transport | Wrapper | Auth | Allowed Tools |
|---|---|---|---|---|
| ChatGPT | stdio + tunnel client | nexus-gbrain-readonly-mcp | OpenAI OAuth | search, get_brain_identity |
| Claude chat | HTTP + cloudflared | nexus-gbrain-readonly-mcp-http | GBrain OAuth 2.1 | search, get_brain_identity, query |
| Codex | stdio | raw gbrain serve | local | all tools |
| Claude Code | stdio | raw gbrain serve | local | all tools |
