# ChatGPT GBrain Dry-Run Implementation Plan

Phase: 2B.1 ChatGPT connector dry-run implementation plan.

Status: planning only. No ChatGPT connector has been created, no tunnel has been started, no token or OAuth client has been created, and `gbrain serve --http` has not been run.

## Goal

Design the safest possible dry run for connecting ChatGPT Developer Mode to the existing GBrain-backed private brain, without changing the private vault or building duplicate Nexus OS memory infrastructure.

The preferred path is OpenAI Secure MCP Tunnel to a local/private GBrain MCP server. The fallback is a public tunnel such as ngrok or Cloudflare Tunnel to GBrain's HTTP MCP server, but only if Secure MCP Tunnel is unavailable or incompatible.

## Confirmed Inputs

- ChatGPT Developer Mode exists in the user's Advanced Settings.
- User still needs to confirm whether ChatGPT Settings -> Apps & Connectors shows `Create` or `Create app`.
- GBrain executable: `/Users/ssavan99/.bun/bin/gbrain`
- Safe Codex MCP command: `/Users/ssavan99/.bun/bin/gbrain serve`
- GBrain version: `0.42.38.0`
- GBrain state: local PGLite under `~/.gbrain`
- Private brain path: `/Users/ssavan99/Desktop/Personal-Obsidian`
- Current index: full private brain imported keyword-only with `--no-embed`
- Current external exposure: none

## Key Finding: Stdio Versus HTTP

Secure MCP Tunnel can forward to an MCP server reachable from the local machine by either stdio command or HTTP URL. That means the preferred dry run should first try GBrain's existing stdio MCP command through `tunnel-client --mcp-command`:

```text
/Users/ssavan99/.bun/bin/gbrain serve
```

This avoids starting `gbrain serve --http` for the preferred path.

GBrain HTTP MCP is still relevant as a fallback because `gbrain --help` advertises:

```text
serve --http [--port N]            HTTP MCP server with OAuth 2.1
  --token-ttl N                    Access token TTL in seconds (default: 3600)
  --enable-dcr                     Enable Dynamic Client Registration
  --public-url URL                 Public issuer URL (required behind proxy/tunnel)
```

Use HTTP only if Secure MCP Tunnel cannot run a stdio MCP command with GBrain, or if ChatGPT's connector UI/tunnel flow requires an HTTP MCP target in this account.

Sources:

- OpenAI Secure MCP Tunnel: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
- OpenAI ChatGPT connector setup: https://developers.openai.com/apps-sdk/deploy/connect-chatgpt
- OpenAI Developer Mode: https://developers.openai.com/api/docs/guides/developer-mode

## Path A: Preferred Secure MCP Tunnel

Recommendation: use Secure MCP Tunnel unless GBrain or ChatGPT compatibility blocks it.

Why:

- It keeps the private MCP server inside the local trust boundary.
- It avoids public inbound exposure.
- It can reach a local MCP server over stdio or HTTP.
- It keeps the private server address local to the machine running `tunnel-client`.
- It is the OpenAI-documented path for private MCP servers that should be reachable by ChatGPT without opening inbound firewall ports.

Expected shape:

1. ChatGPT connector uses a Tunnel connection.
2. OpenAI-hosted tunnel endpoint queues MCP requests.
3. Local `tunnel-client` long-polls over outbound HTTPS.
4. `tunnel-client` invokes local GBrain over stdio with `/Users/ssavan99/.bun/bin/gbrain serve`.
5. GBrain reads its existing local PGLite index and returns MCP tool results.

Approval-only command shape:

```bash
export CONTROL_PLANE_API_KEY="<runtime key with Tunnels Read + Use>"

tunnel-client init \
  --sample sample_mcp_stdio_local \
  --profile gbrain-local-stdio \
  --tunnel-id "<tunnel_id>" \
  --mcp-command "/Users/ssavan99/.bun/bin/gbrain serve"

tunnel-client doctor --profile gbrain-local-stdio --explain
tunnel-client run --profile gbrain-local-stdio
```

Do not run these commands until the user explicitly approves the dry run and provides the required tunnel details.

## Path B: Fallback Public Tunnel To GBrain HTTP MCP

Use this only if Secure MCP Tunnel is unavailable or incompatible.

Why it is less safe:

- It exposes a local service through a public HTTPS URL.
- It requires extra care around auth, URL logging, and tunnel lifecycle.
- GBrain's remote HTTP path may require OAuth/public URL settings.
- A bearer-token approach would be broad and sensitive if leaked.

Expected shape:

1. Start GBrain HTTP MCP locally on a loopback port.
2. Expose the loopback HTTP MCP endpoint through an approved public tunnel.
3. Configure ChatGPT connector URL to the tunnel's public HTTPS `/mcp` endpoint.
4. Use OAuth if feasible; avoid no-auth exposure and avoid bearer tokens unless explicitly accepted for a short, manual test.

Approval-only command shapes:

```bash
/Users/ssavan99/.bun/bin/gbrain serve --http \
  --port 3131 \
  --public-url "https://<approved-public-url>"
```

For ngrok, only after installation and approval:

```bash
ngrok http 3131
```

For Cloudflare Tunnel, only after installation and approval:

```bash
cloudflared tunnel --url http://127.0.0.1:3131
```

Do not use this fallback without a separate auth decision and an explicit rollback window.

## Exact Prerequisites

Required before any implementation:

- ChatGPT UI confirms Developer Mode is enabled.
- ChatGPT Settings -> Apps & Connectors shows `Create` or `Create app`.
- User confirms whether the connector can be private/draft.
- User confirms whether the connector UI has a `Tunnel` connection option.
- User confirms which ChatGPT surface will be tested: Developer Mode chat, normal chat, deep research, or company knowledge.
- User approves the test data boundary: disposable/test-only GBrain state first, or current full GBrain index.
- User approves every command that starts a server, tunnel, token flow, OAuth flow, or connector.

Secure MCP Tunnel prerequisites:

- A Platform tunnel exists or the user is ready to create one manually in Platform tunnel settings.
- `tunnel_id` is available.
- `tunnel-client` binary is available, or the user explicitly approves downloading/installing it.
- A runtime API key exists for `tunnel-client` with Tunnels Read + Use.
- The Platform organization and ChatGPT workspace are associated so the tunnel appears in ChatGPT.
- The local machine can make outbound HTTPS requests to OpenAI tunnel endpoints.

Fallback public tunnel prerequisites:

- User explicitly approves public tunnel use.
- User chooses ngrok, Cloudflare Tunnel, or another tunnel provider.
- User explicitly approves installing the tunnel tool if it is not already installed.
- Auth design is approved before exposing the endpoint.
- Public URL lifetime and rollback time are agreed before starting.

## Inspection Commands Before Running Anything

These commands are safe inspection commands for a future implementation session. They do not start HTTP serving, create tokens, configure OAuth, start tunnels, or modify the private vault.

```bash
git status --short
git log --oneline -5
/Users/ssavan99/.bun/bin/gbrain --version
/Users/ssavan99/.bun/bin/gbrain --help
/Users/ssavan99/.bun/bin/gbrain serve --help
/Users/ssavan99/.bun/bin/gbrain auth --help
/Users/ssavan99/.bun/bin/gbrain connect --help
ps aux | grep gbrain
command -v tunnel-client
tunnel-client help quickstart
tunnel-client --help
command -v ngrok
command -v cloudflared
```

Only run `tunnel-client` help commands if `command -v tunnel-client` finds an existing binary. Do not install it during inspection.

Use `gbrain doctor --json` only if no active GBrain serve process is holding the PGLite lock, or after explicitly explaining the lock risk.

## Approval-Only Commands

These commands must not be run during planning.

Secure MCP Tunnel path:

```bash
export CONTROL_PLANE_API_KEY="<runtime key with Tunnels Read + Use>"
tunnel-client init --sample sample_mcp_stdio_local --profile gbrain-local-stdio --tunnel-id "<tunnel_id>" --mcp-command "/Users/ssavan99/.bun/bin/gbrain serve"
tunnel-client doctor --profile gbrain-local-stdio --explain
tunnel-client run --profile gbrain-local-stdio
```

Fallback HTTP path:

```bash
/Users/ssavan99/.bun/bin/gbrain serve --http --port 3131 --public-url "https://<approved-public-url>"
ngrok http 3131
cloudflared tunnel --url http://127.0.0.1:3131
```

Auth-related commands:

```bash
/Users/ssavan99/.bun/bin/gbrain auth create
/Users/ssavan99/.bun/bin/gbrain auth register-client
```

Run auth commands only after a separate auth plan is approved.

## Test Data Boundary

Strongest safety recommendation: first test with a disposable/test-only GBrain state, not the current full private-brain index.

Reason:

- ChatGPT connector discovery and smoke prompts may send tool metadata and tool outputs through ChatGPT.
- A dry run can prove transport compatibility without exposing the full private memory index.
- If the connector accidentally exposes broad tools or returns too much context, the blast radius is limited.

Open question before implementation:

- Confirm whether GBrain supports an isolated temporary state/config directory through documented environment variables or flags in this installation.

If isolated GBrain state is easy and documented, use a disposable test index with fake notes. If it is not straightforward, the second-best path is to use the current full index but only after the user accepts that ChatGPT may receive private search snippets during smoke tests.

Do not copy private brain content into Nexus OS to make a test state. Use fake disposable content only.

## Avoiding Private Vault Exposure

- Do not serve the private vault path directly over HTTP.
- Do not point a web server or tunnel at `/Users/ssavan99/Desktop/Personal-Obsidian`.
- Do not run import, sync, watch, embed, files upload, jobs, or write tools.
- Prefer stdio GBrain behind Secure MCP Tunnel, because the only local target is the MCP command, not a file server.
- Confirm the ChatGPT connector tool list before asking any query.
- If the tool list includes write/import/sync/watch/embed/job/file tools, stop before smoke testing.
- Use short, targeted search prompts and avoid broad personal queries.
- Do not paste raw private notes, token values, vault paths beyond this documented path, or tunnel secrets into ChatGPT.

## Connector Name And Description

Recommended connector name:

```text
GBrain Local Memory Dry Run
```

Recommended description:

```text
Private draft connector for testing read-only access to a local GBrain MCP server. Use only for explicit memory lookup smoke tests approved by the user.
```

If testing a disposable state first, use:

```text
GBrain Disposable Test Memory
```

Avoid names that imply production readiness, company-wide availability, or automatic writeback.

## ChatGPT Permission Setting

Choose the most conservative permission setting available.

Preferred:

```text
Always ask
```

If ChatGPT offers separate read/write behavior, choose the option that asks before retrieving information and before making changes. Do not choose broad automatic access during the dry run.

## Safest Test Sequence

1. Confirm worktree is clean and Phase 2B.1 plan is committed if required.
2. Confirm ChatGPT UI has Developer Mode and connector creation.
3. Confirm whether Tunnel connection is available in the connector UI.
4. Inspect local GBrain/tunnel tool help only.
5. Prefer disposable/test-only GBrain state if isolation is documented and easy.
6. If approved, configure Secure MCP Tunnel with GBrain stdio command.
7. Run tunnel-client doctor and confirm healthy local readiness.
8. Create a private/draft ChatGPT connector using Tunnel connection.
9. Confirm the connector's advertised tool list before invoking tools.
10. Disable any non-read/search tools if the UI supports tool toggles.
11. Run one identity/tool-list prompt.
12. Run one fake or non-sensitive marker search.
13. Only then run limited startup workflow search prompts.
14. Stop the tunnel and disconnect the connector immediately after testing unless separately approved to keep it available.

## Smoke-Test Prompts For ChatGPT

Use these only after the connector is created and the tool list has been reviewed.

Initial safety checks:

```text
Use the GBrain Local Memory Dry Run connector only. What tools are available? Do not retrieve private note content yet.
```

```text
Use the GBrain Local Memory Dry Run connector only. Get the brain identity or health summary if that tool is available. Keep the answer to counts and version metadata only.
```

Disposable-state search, if using fake test data:

```text
Use the GBrain Disposable Test Memory connector only. Search for "nexus-test-phrase-alpha" and summarize only whether a result exists.
```

Full-index searches, only if explicitly approved:

```text
Use the GBrain Local Memory Dry Run connector only. Search for "startup-dashboard" and return only result titles/slugs, not note text.
```

```text
Use the GBrain Local Memory Dry Run connector only. Search for "customer discovery playbook" and return only result titles/slugs, not note text.
```

```text
Use the GBrain Local Memory Dry Run connector only. Search for "weekly startup review" and return only result titles/slugs, not note text.
```

```text
Use the GBrain Local Memory Dry Run connector only. Search for "shared organizational brain" and return only result titles/slugs, not note text.
```

Stop if ChatGPT returns large private snippets, asks for broader permission than expected, or exposes unexpected write-capable tools.

## Rollback And Disconnect Plan

Secure MCP Tunnel rollback:

- Stop `tunnel-client run`.
- Delete or disable the ChatGPT connector from Settings -> Apps & Connectors.
- Revoke the runtime API key if it was created only for this test.
- Disable or delete the tunnel in Platform tunnel settings if it was created only for this test.
- Remove the local tunnel-client profile if it was created only for this test.
- Re-run Codex local stdio MCP smoke test.
- Record the outcome in `docs/decision-log.md`.

Fallback public tunnel rollback:

- Stop the public tunnel process.
- Stop `gbrain serve --http`.
- Delete or disable the ChatGPT connector.
- Revoke OAuth clients or bearer tokens created for the test.
- Confirm no tunnel URL is still live.
- Re-run Codex local stdio MCP smoke test.
- Record the outcome in `docs/decision-log.md`.

## What Not To Do

- Do not run `gbrain serve --http` during planning.
- Do not start `tunnel-client`, ngrok, or Cloudflare Tunnel during planning.
- Do not create ChatGPT connectors during planning.
- Do not create bearer tokens, OAuth clients, runtime API keys, or secrets in repo docs.
- Do not configure OAuth until a separate auth plan is approved.
- Do not install tunnel tools without explicit approval.
- Do not expose `/Users/ssavan99/Desktop/Personal-Obsidian` over HTTP.
- Do not copy private brain files into Nexus OS.
- Do not enable embeddings or add API keys for search.
- Do not run import, sync, watch, embed, files, jobs, or background workers.
- Do not install Claude Code, Hermes, OpenClaw, or ChatGPT-related tooling as part of this phase.
- Do not build a duplicate GBrain/RAG/search/MCP/skills layer in Nexus OS.

## Recommendation

Proceed only after the user confirms the ChatGPT connector UI has `Create` or `Create app`, and whether it offers the `Tunnel` connection option.

If Tunnel is available, the recommended implementation path is:

```text
Secure MCP Tunnel -> GBrain stdio command -> disposable/test-only GBrain state first
```

Move to current full-index testing only after the tunnel, connector discovery, permission settings, and tool list are proven safe.

## Phase 2B.6 Result

The disposable ChatGPT Secure MCP Tunnel smoke test succeeded with fake/test-only GBrain data.

- Fake Markdown brain: `/Users/ssavan99/repos/nexus-gbrain-chatgpt-fake-brain`
- Disposable GBrain state: `/Users/ssavan99/repos/nexus-gbrain-chatgpt-state/.gbrain`
- Fake marker: `chatgpt-secure-tunnel-alpha`
- tunnel-client profile: `gbrain-disposable-stdio`
- Profile path: `/Users/ssavan99/.config/tunnel-client/gbrain-disposable-stdio.yaml`
- Profile command: `env GBRAIN_HOME=/Users/ssavan99/repos/nexus-gbrain-chatgpt-state /Users/ssavan99/.bun/bin/gbrain serve`

No real private vault content was exposed, no real `/Users/ssavan99/.gbrain` state was mutated, no `gbrain serve --http` path or public tunnel was used, and no real-brain import/sync/watch/embed step was run.
