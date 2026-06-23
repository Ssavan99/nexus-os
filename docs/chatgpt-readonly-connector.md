# ChatGPT Read-Only GBrain Connector

Status: Phase 2B.11 success.

Use this path for daily ChatGPT memory lookup:

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

## Allowed Tools

The read-only wrapper exposes exactly:

- `get_brain_identity`
- `search`

## Do Not Use Raw GBrain MCP For ChatGPT

The raw GBrain MCP connector exposed destructive/admin tools, including write, job, sync, source-management, and schema mutation tools. It is not safe as the daily ChatGPT connector.

Do not connect ChatGPT directly to raw GBrain MCP unless GBrain later provides a verified read-only/native tool-filtered surface.

## Boundaries

- The private vault is not modified.
- No `gbrain serve --http` path is used.
- No public tunnel is used.
- No embeddings are enabled.
- No real-brain import, sync, watch, or writeback is run.
- No write/admin/destructive tools are exposed to ChatGPT.
