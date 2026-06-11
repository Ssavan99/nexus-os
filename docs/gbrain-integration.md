# GBrain Integration

Nexus OS will use GBrain as the core memory/search/MCP/skills engine.

This repository should not rebuild GBrain's core functionality unless the user explicitly requests it later.

## Why GBrain

GBrain is the better home for memory infrastructure because it is intended to provide the shared brain engine:

- Indexing over Markdown brain files.
- Search and retrieval.
- MCP access for multiple tools.
- Skills and reusable memory operations.
- Future scheduled or dream-cycle workflows.

Using GBrain lets Nexus OS focus on personalization instead of reimplementing memory plumbing.

## How Nexus OS Should Use GBrain

Nexus OS should treat GBrain as the core service that connects agents to the Markdown brain.

Nexus OS should provide:

- Repo-level architecture and workflow docs.
- Personal schemas and prompt conventions.
- Workflow playbooks for job search, startups, weekly planning, research, ingestion, and review.
- Configuration or glue code that helps personal workflows call into GBrain.
- Future custom UI or skills that are specific to the user's operating system.

When a workflow needs memory search, retrieval, MCP access, skill execution, or indexing, the default assumption should be: use GBrain.

## What Stays In Nexus OS

Keep these in Nexus OS:

- Personal operating principles.
- Workflow prompts.
- Documentation.
- Roadmaps and decision logs.
- Capture and ingestion instructions.
- Personal schemas for how knowledge should be organized.
- Thin integration scripts or adapters when needed.
- Prototype/fallback helpers while GBrain is not installed or not yet wired into a workflow.

## What Stays In GBrain

Keep these in GBrain:

- Indexing.
- Search.
- Retrieval.
- MCP server and tool surfaces.
- Skills engine.
- Memory engine internals.
- Scheduled maintenance, dream cycles, cron-style workflows, or equivalent core automation.
- Cross-client memory access patterns.

Do not duplicate these features in Nexus OS without a later explicit decision.

## Current Prototype/Fallback Helpers

The current Nexus OS CLI/search/ingest implementation is reclassified as prototype/fallback workflow helpers.

That includes:

- `check`
- `init`
- `add-note`
- `search`
- `plan-ingest`
- `draft-summary`
- `append-log`
- `rebuild-index`
- Markdown page templates

These helpers can remain while GBrain is not installed and while workflows are being proven. Do not delete them yet. Remove or retire them only after GBrain is installed, tested, and the Nexus workflows no longer depend on them.

## Future Updates And Upgrades

When GBrain changes:

1. Prefer upgrading or configuring GBrain over duplicating behavior in Nexus OS.
2. Update Nexus OS docs and workflows to reflect the new GBrain behavior.
3. Keep compatibility notes in `docs/decision-log.md` when architecture changes.
4. Add thin adapters only when they preserve a clean boundary.
5. Avoid storing private brain content in this public repo during integration work.

## When To Consider Forking GBrain

Forking GBrain is rejected for now.

Consider a fork only if all of these become true:

- GBrain is central to Nexus OS workflows.
- A required capability cannot be added through configuration, extension, plugin, or upstream contribution.
- The divergence is important enough to maintain long term.
- The fork can be tested without risking private brain files.

Until then, use GBrain as an upstream core and keep Nexus OS as the personalized workflow layer.
