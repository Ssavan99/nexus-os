# Nexus OS Architecture

Nexus OS is the personalized workflow, configuration, and control layer around a GBrain-backed Markdown brain. It is not a standalone replacement for GBrain.

## Plain-Language Model

There are three durable layers:

1. Markdown/Obsidian brain files are the human-readable source of truth.
2. GBrain indexes and serves that brain through local memory, search, MCP, skills, and future scheduled workflows.
3. Nexus OS stores personal operating rules, schemas, prompts, workflows, roadmaps, and future custom UI or skills that sit on top of GBrain.

Agents and interfaces connect to the same brain through GBrain rather than each building their own separate memory system.

## What Obsidian And Markdown Do

The Markdown brain is where knowledge lives in a format humans can read, edit, back up, diff, and understand.

Obsidian is the primary human interface for browsing and editing those files. It should remain useful even if every agent or tool is turned off. Notes, source captures, summaries, plans, decisions, and workflow artifacts should be stored as Markdown files in the private brain folder, not in this public repository.

Markdown/Obsidian provides:

- Human-readable source of truth.
- Local ownership of personal and business knowledge.
- Durable files that are easy to inspect and version.
- A graph-friendly knowledge workspace for browsing links and relationships.

## What GBrain Does

GBrain is the core memory/search/MCP/skills engine for Nexus OS.

GBrain should handle:

- Indexing the Markdown brain.
- Local search and retrieval over the brain.
- MCP access for Codex, Claude Code, ChatGPT, and future agents.
- Reusable skills and memory operations.
- Future dream-cycle, cron, or scheduled maintenance workflows when those are available and reliable.

Nexus OS should integrate with GBrain instead of rebuilding these systems.

## What Nexus OS Does

Nexus OS is the personalized operating layer around GBrain.

It should store:

- Personal schemas and wiki conventions.
- Workflow prompts and operating instructions.
- Roadmaps and architecture decisions.
- Job-search workflows.
- Startup and business workflows.
- Weekly planning workflows.
- Ingestion instructions and capture conventions.
- Future custom skills, dashboards, UI, or orchestration glue that are specific to this personal operating system.

Nexus OS may keep lightweight helper scripts while workflows are being designed, but those helpers are prototype/fallback tooling unless explicitly promoted later.

## What Codex, Claude, ChatGPT, Hermes, And OpenClaw Do

Codex, Claude Code, ChatGPT via MCP, and later Hermes/OpenClaw are clients and operators.

They should:

- Use GBrain-backed memory to search and read the shared brain.
- Follow Nexus OS workflow instructions when performing personal or business workflows.
- Write durable outputs back to the Markdown brain when asked.
- Respect the public repo/private brain boundary.

They should not each maintain separate hidden memory stores that become the source of truth.

## How Shared Memory Works

Shared memory means shared brain files plus the GBrain index.

It does not mean shared chat histories. A conversation in Codex and a conversation in ChatGPT may remain separate, but both can use the same GBrain-backed Markdown brain as persistent memory.

The durable loop is:

```text
Markdown brain files -> GBrain index/search/MCP -> agent/client workflows -> Markdown brain files
```

If an insight matters beyond one chat, it should be written into the brain as a file or update. GBrain can then index it and make it available to other clients.

## Why Nexus OS Is Not An Extra Engine Layer

Nexus OS should not become another memory engine between agents and the brain. That would create duplicate indexing, duplicate search, duplicate MCP surfaces, and confusing ownership.

The intended division is:

- GBrain owns memory infrastructure.
- The Markdown brain owns durable knowledge.
- Nexus OS owns personal workflow design and configuration.
- Agents own task execution through the shared memory layer.

This keeps Nexus OS focused and reduces the chance of building a fragile parallel system.
