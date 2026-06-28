# Weekly Checklist Engine

Status: Phase 3 foundation — spec (the heart of Nexus OS workflows).

This is the unifying primitive both the Startup and Job systems plug into. It turns the brain's *resources* (raw captures + synthesized wiki pages) into a **prioritized implementation backlog per area**, and rolls the top items into a **single weekly checklist** the user reviews once a week.

It is a **convention + prompt-pack**, not new infrastructure. GBrain stays the memory/index engine; the generated lists are Markdown in the **private vault**; agents (Claude Code, claude.ai, ChatGPT, Codex) run the prompts against the shared brain.

## Source of the idea

`inbox/loose-notes/Future directions - Nexus-GBrain.md`: per-area priority lists → done/archive; an auto-generated weekly combined checklist ("I will only look at this each week"); recurring tasks (e.g. apply to N jobs/week); later exportable to a Jira/Trello/Notion board.

## Two kinds of list items (in priority order of when we build them)

1. **PRIMARY — implementation backlog** (build first): concrete setup/build items derived from resources. Examples: "run an LLM council on the startup idea", "set up the automated job-application system", "revise LinkedIn using [[resource]]", "set up automated social posts", "build a reach-out system", "find agencies / investors / VCs / founders / startups to research or contact".
2. **SECONDARY — recurring operations** (later): "apply X jobs/week", "reach out to N people/week".

Not every resource becomes a task. Item **types**:

- `task` — something to do/build/set up (goes on checklists).
- `recurring` — repeats on a cadence (weekly/…); regenerated each period.
- `note` — knowledge to remember (not a checklist item; lives in the backlog as reference).
- `reminder` — surface at a critical moment (e.g. "get legal review before fundraising").

## Files (in the private vault)

```
wiki/areas/<area>/backlog.md      # per-area prioritized backlog (+ a ## Done section)
wiki/weekly/<YYYY>-W<WW>.md        # the week's combined checklist (the only page user opens weekly)
wiki/weekly/index.md              # links to current + past weeks
```

Areas today: `startups`, `career` (job), `ai-learning`, `personal`, `projects`, plus a `system` (Nexus/GBrain) area.

## Item line format (export-friendly Markdown)

```
- [ ] (P1) [task] Set up automated job-application system — src: [[Startup job apply strategy and list]] — area: career
- [ ] (P2) [recurring:weekly] Apply to 10 Greenhouse roles opened in last 24h — area: career
- [ ] (P2) [task] Run LLM council on AI story-game idea — src: [[customer-discovery-playbook]] — area: startups
- [n] [note] Bottom-up market sizing beats top-down in pitches — src: [[Why VCs check out during a pitch]] — area: startups
- [!] [reminder] Get legal review before signing any term sheet — src: [[VC Legal Traps]] — area: startups
```

- Priority: `P1` (now) > `P2` (soon) > `P3` (later).
- Plain `- [ ]` checkboxes so a future exporter maps cleanly to Notion/Jira/Trello.
- Every actionable item cites its `src:` wiki/raw page (traceability; no raw content copied).

## The three operations (prompt-pack any agent runs)

### 1. `refresh-backlog <area>`
Read the area's wiki pages + their linked/cited raw sources via GBrain → extract actionable implementation items → write/update `wiki/areas/<area>/backlog.md`, priority-ordered, typed, source-linked. De-duplicate against existing items; never drop a `## Done` entry. **Human review before save** (per boundary rules; vault writes only on explicit user action).

### 2. `generate-week`
Pull the top undone `task` items per area (by priority, tailored to the week) + any due `recurring` items → write `wiki/weekly/<YYYY>-W<WW>.md` as one combined checklist grouped by area. This is the page the user opens weekly.

### 3. `complete <item>` / `roll-over`
Move a checked item to the area backlog's `## Done` section (with date). Unfinished weekly items roll into next week's `generate-week`. Eventually everything in an area's backlog reaches `## Done` → area is "worked through".

## How the two goal-systems use it

- **Startup (Category 1):** `refresh-backlog startups` turns the existing playbooks (`founder-operating-system`, `customer-discovery-playbook`, `app-build-and-launch-playbook`, …) + the 18 un-integrated startup raw notes into a backlog; weekly checklist drives the founder weekly evidence loop.
- **Job (Category 2):** after job reels are captured, `refresh-backlog career` builds the job backlog (tracking board setup, resume revision, auto-apply system, referral outreach), plus `recurring:weekly` apply/networking quotas.

## Export path (future)

Markdown checkboxes → a small exporter → Notion (team layer) / Jira / Trello board running as a sprint. The personal vault stays private; the board is the shareable surface.

## Boundaries

- Spec + prompts live here (public Nexus OS). Generated lists live in the **private vault** — never committed to this repo.
- Vault writes happen only on explicit user approval (create/update backlog or weekly pages).
- Do not copy raw note contents into checklists; cite `src:` links instead.
- This is a convention over GBrain, not a parallel task engine. If GBrain later ships native tasks/cron, prefer it.
