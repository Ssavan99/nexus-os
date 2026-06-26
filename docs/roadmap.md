# Nexus OS Roadmap

Nexus OS is now planned as a personalized workflow/config/control layer around GBrain, not a standalone memory engine.

The current CLI/search/ingest code remains available as prototype/fallback workflow helpers. Do not remove it until GBrain is installed, tested, and Nexus workflows no longer depend on it.

## Phase 0: Architecture Reset

Status: current.

- Record the final architecture decision.
- Make GBrain the core memory/search/MCP/skills engine.
- Reclassify existing Nexus OS CLI/search/ingest code as prototype/fallback helpers.
- Preserve the public repo/private brain boundary.
- Avoid building duplicate GBrain features in Nexus OS.
- Document what belongs in Obsidian/Markdown, GBrain, Nexus OS, and agent clients.

## Phase 1: Local Brain + GBrain Setup

Goal: establish the local brain and connect it to GBrain safely.

- Install and configure GBrain after architecture docs are settled.
- Point GBrain at the private Markdown/Obsidian brain folder.
- Verify local indexing and search.
- Confirm private brain files are not copied into this public repo.
- Decide how the existing prototype helpers should coexist with GBrain during transition.
- Keep a rollback path until GBrain is proven against real workflows.

## Phase 2: Agent Connections

Goal: connect coding and writing agents to the same GBrain-backed memory.

- Phase 2A status: verified. Codex uses local GBrain MCP over stdio without copying private brain files into Nexus OS.
- Phase 2B status: verified (superseded by 2E). ChatGPT originally used the `Nexus GBrain Readonly Memory` connector through Secure MCP Tunnel + the read-only wrapper at `/Users/ssavan99/MCPs/nexus-gbrain-readonly-mcp`; raw GBrain MCP is not safe for ChatGPT.
- Phase 2C status: verified. Claude Code uses raw local GBrain MCP at user scope in `~/.claude.json` (global, all projects); a restarted session loaded all 89 `mcp__gbrain__*` tools and `get_brain_identity` returned the local brain. Operating instructions at `docs/claude-code-gbrain-operating-instructions.md`.
- Phase 2D status: 2D.2 DONE. claude.ai is connected to GBrain's native `serve --http` (OAuth 2.1, manual `read`-scoped public PKCE client, DCR off) over a **permanent ngrok static URL**, always-on under launchd. The brain was **migrated PGLite → local Postgres** (crash-safe, concurrent) after an unclean PGLite `serve --http` stop corrupted the data dir (recovered via `pg_resetwal -f`). End-to-end verified: read works, write refused. Helpers: `scripts/claude-chat-gbrain-serve.sh`, `scripts/com.nexus.claude-chat-gbrain.plist`. Plan + ops at `docs/claude-chat-gbrain-plan.md`. Future: 2D.3 (move to an always-on host for 24/7).
- Phase 2E status: DONE. ChatGPT unified onto the same always-on native HTTP MCP as claude.ai, using its own `read`-scoped public PKCE client (DCR off) and a Developer-Mode "User-Defined OAuth Client" connector at the permanent ngrok URL. Read verified from ChatGPT; write refused server-side. Retires the per-session tunnel-client/wrapper ritual (kept as fallback). See `docs/chatgpt-readonly-connector.md`.
- Verify shared memory means shared Markdown brain files plus GBrain index, not shared chat histories.
- Document agent-specific operating instructions.

## Phase 3: Nexus Workflows

Goal: build personalized workflows on top of GBrain.

- Job-search workflows.
- Startup and business workflows.
- Weekly planning and review workflows.
- Personal knowledge maintenance workflows.
- Research and learning workflows.
- Ingestion instructions for raw captures and source summaries.
- Prompt packs and schemas that tell agents how to operate.

## Phase 4: Capture Pipelines

Goal: make it easier to capture useful material into the brain without overbuilding infrastructure.

- Instagram saved-link and pasted-post workflow.
- YouTube link/transcript workflow.
- Articles, documents, meeting notes, Slack-style discussions, and customer research.
- Source metadata conventions.
- Human review points before important generated updates become durable brain knowledge.
- Prefer GBrain-compatible capture patterns over custom memory engines.

## Phase 5: Agent/Dream Cycle

Goal: add scheduled or background intelligence once the core brain is stable.

- Use GBrain's future dream-cycle, cron, or scheduled workflow capabilities where possible.
- Periodically lint stale claims, contradictions, open loops, and missing links.
- Suggest new questions, areas, and source-gathering tasks.
- Maintain dashboards or review queues for the user.
- Avoid building a custom background automation engine in Nexus OS unless explicitly requested later.

## Phase 6: PA / Cofounder OS

Goal: evolve Nexus OS into a personal assistant and cofounder operating system.

- Use the shared GBrain-backed brain as the memory layer for personal, career, startup, and project work.
- Add higher-level workflows for planning, prioritization, outreach, product thinking, customer research, and execution tracking.
- Support future clients such as Hermes/OpenClaw through the same memory layer.
- Build custom UI or skills only where they personalize and orchestrate the GBrain-backed system.

## Design Principles

- Markdown/Obsidian brain files are the human-readable source of truth.
- GBrain owns indexing, search, MCP, skills, and memory infrastructure.
- Nexus OS owns personal schemas, prompts, workflow docs, roadmaps, and control logic.
- Agents are clients/operators that use the shared GBrain-backed brain.
- Do not duplicate GBrain features in Nexus OS.
- Do not store private brain files in this public repo.
