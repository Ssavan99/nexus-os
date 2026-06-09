# Nexus OS Roadmap

This roadmap preserves the useful ideas from the LLM Wiki pattern while keeping implementation phased and reviewable.

## Phase 0: Public Code, Private Vault

Status: started.

- Keep this repository limited to code, templates, and documentation.
- Read the private vault path from `VAULT_PATH`.
- Refuse to operate when `VAULT_PATH` is missing or points inside this repo.
- Initialize a safe external vault layout.
- Preserve raw sources as immutable files.
- Provide basic local search.
- Separate raw source type folders from generated wiki knowledge areas.

## Phase 1: Manual LLM Wiki Workflow

Status: started.

Goal: make the LLM a disciplined wiki maintainer while the user stays in the loop.

- Provide page templates for summaries, areas, concepts, projects, decisions, questions, people, and organizations.
- Plan ingests with `nexus-os plan-ingest` before wiki edits.
- Draft structured source summaries with `nexus-os draft-summary`.
- Ingest one source at a time.
- Generate source summary pages under `wiki/summaries/`.
- Update area pages, concept pages, decision pages, question pages, people pages, and organization pages.
- Keep source type separate from knowledge domain so one source can affect many wiki areas.
- Keep `wiki/index.md` as the first navigation surface.
- Keep `wiki/log.md` as an append-only timeline.
- Rebuild the index and append log entries with deterministic helper commands.
- Use Obsidian to review graph structure, links, and generated pages.

## Phase 2: Query-To-Wiki Memory

Goal: make useful answers durable instead of leaving them in chat history.

- Search `wiki/index.md` before raw sources.
- Answer questions from the generated wiki with citations.
- Save durable comparisons, analyses, and discoveries into the appropriate wiki area or general folder.
- Add source-aware frontmatter for future Dataview queries.

## Phase 3: Wiki Linting And Maintenance

Goal: keep the wiki healthy as it grows.

- Detect stale claims superseded by newer sources.
- Flag contradictions between pages.
- Find orphan pages and missing inbound links.
- Suggest entity or concept pages that should exist.
- Identify important unanswered questions and source gaps.

## Phase 4: Better Search And Agent Tools

Goal: support larger vaults without forcing every query through raw retrieval.

- Add a stronger local search backend, such as `qmd`, BM25, vector search, or hybrid search.
- Expose search and ingest operations through MCP tools.
- Add structured command outputs that agent sessions can consume reliably.
- Preserve fully local/on-device options where possible.

## Phase 5: Instagram And Saved-Post Workflows

Goal: turn saved social posts into durable wiki knowledge without locking the system to one platform.

- Start manually with saved links in `raw/sources/instagram/instagram_saved_links.md`.
- Later support pasted post contents, exports, or fetched content when available.
- Process useful items into career/job notes, AI learning/implementation notes, startup/business notes, and any other areas the source requires.
- Preserve the original links and captures as immutable raw sources.
- Let the LLM suggest new areas or pages when saved posts do not fit existing categories.

## Phase 6: YouTube Workflows

Goal: turn videos and transcripts into source summaries and connected wiki pages.

- Store YouTube links, transcripts, or captured metadata under `raw/sources/youtube/`.
- Generate source summaries with video title, channel, URL, date captured, transcript source, key ideas, implementation notes, and related wiki pages.
- Update relevant areas such as career, AI learning, startups, projects, or new areas as needed.
- Keep transcript provenance clear so claims can be traced back to the source.

## Phase 7: Rich Outputs

Goal: let wiki knowledge become artifacts.

- Generate Marp slide decks from wiki syntheses.
- Produce charts or notebooks from structured notes.
- Support canvases or maps for relationship-heavy domains.
- Optionally store image assets locally under `raw/assets/` when the user chooses.

## Phase 8: Team And Workflow Engine

Goal: evolve from personal wiki to reviewed, multi-step agent workflows.

- Support human review before generated wiki updates are accepted.
- Track pending ingest tasks and review status.
- Integrate meeting transcripts, Slack exports, customer calls, and project docs.
- Add workflow runs for recurring lint, research, and summarization tasks.

## Design Principles

- Raw sources are source of truth and immutable.
- Generated wiki pages are editable by the LLM.
- The user curates sources, asks questions, and reviews direction.
- The LLM handles summarizing, cross-linking, filing, contradiction checks, and upkeep.
- Future automation should extend the current structure instead of replacing it.
