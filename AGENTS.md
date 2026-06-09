# Nexus OS Agent Instructions

Nexus OS is the public code engine for an external private Obsidian vault. The repository must not contain private notes, raw sources, generated wiki pages, or personal vault files.

## Vault Boundary

- Read the vault path from `VAULT_PATH`.
- Refuse to operate if `VAULT_PATH` is missing.
- Refuse to operate if `VAULT_PATH` resolves inside this repository.
- Do not expose private `.env` values in responses.
- Raw sources in the vault are immutable. Never overwrite or delete raw files automatically.

## Architecture

Separate source type from knowledge domain.

Raw source types live under:

```text
raw/sources/
  instagram/
  youtube/
  articles/
  meetings/
  journals/
  documents/
raw/assets/
```

Generated wiki knowledge lives under:

```text
wiki/
  areas/
    personal/
    career/
    ai-learning/
    startups/
    projects/
  concepts/
  decisions/
  questions/
  summaries/
  people/
  organizations/
  index.md
  log.md
  _schema.md
```

The default areas are starting points, not a closed taxonomy. Add or suggest new areas when sources reveal durable domains that deserve their own home.

## Main Use Cases

- Personal knowledge wiki: goals, health, psychology, self-improvement, journal entries, articles, podcasts, saved posts, and a structured picture of the user over time.
- Startup, business, and team wiki: project notes, technical notes, business notes, customer research, meeting transcripts, Slack-style discussions, project documents, and decisions.

## Ingest Rules

1. Identify the raw source type separately from the wiki knowledge domains it affects.
2. Preserve raw files exactly as source material.
3. Write source summaries under `wiki/summaries/`.
4. Update relevant area pages under `wiki/areas/`.
5. Update general pages under `wiki/concepts/`, `wiki/decisions/`, `wiki/questions/`, `wiki/people/`, or `wiki/organizations/` when appropriate.
6. Update `wiki/index.md`.
7. Append to `wiki/log.md` using headings like `## [YYYY-MM-DD] ingest | Source Title`.

## Manual Ingest Workflow

Use this workflow when the user asks Codex to process a raw source manually.

1. Run `nexus-os plan-ingest <raw-source-path>` to inspect the source and produce a checklist.
2. Run `nexus-os draft-summary <raw-source-path>` if a summary page does not exist yet.
3. Read the raw source and complete the draft summary. Do not pretend the CLI summarized it automatically.
4. Update relevant `wiki/areas/` pages with durable synthesis, not just copied notes.
5. Update or create supporting pages in `wiki/concepts/`, `wiki/decisions/`, `wiki/questions/`, `wiki/people/`, or `wiki/organizations/`.
6. Run `nexus-os rebuild-index`.
7. Run `nexus-os append-log --type ingest --title "Source Title" --path "<raw-source-path>"`, including `--page` for generated or updated pages when practical.

Every ingest must update `wiki/index.md` and `wiki/log.md`.

## Command Guidance

- Use `plan-ingest` before editing wiki pages when processing a new raw source.
- Use `draft-summary` to create the initial source-summary structure.
- Use `draft-summary --overwrite` only when the user explicitly confirms replacing an existing draft.
- Use `rebuild-index` after creating or editing generated wiki pages.
- Use `append-log` after the ingest is complete.

## Updating Wiki Pages

- Area pages should capture evolving understanding for a durable domain such as personal, career, AI learning, startups, or projects.
- Concept pages should define reusable ideas and link to the areas or sources where they matter.
- Decision pages should record the decision, context, options, rationale, consequences, sources, and revisit trigger.
- Question pages should track open questions, why they matter, current evidence, possible answers, and next actions.
- Person and organization pages should be created when an entity appears repeatedly or matters to decisions, projects, customer research, or relationships.
- Prefer updating existing pages over creating duplicates with slightly different names.

## Citations And Source Handling

- Cite raw sources with vault-relative paths such as `raw/sources/documents/example.md`.
- Cite source summaries when using synthesized claims, and raw sources when grounding factual claims.
- Never silently delete, move, rename, or overwrite raw sources.
- Never treat generated wiki pages as more authoritative than raw sources.

## Uncertainty And Contradictions

- Mark uncertain claims explicitly with phrases like "Unclear", "Needs verification", or "Source only implies".
- When a new source contradicts an older wiki claim, do not erase the contradiction silently. Note both claims, cite both sources, and explain what changed.
- If the contradiction affects a decision or important understanding, add or update a question page.

## Taxonomy Changes

- The default areas are flexible, but ask before major taxonomy changes.
- Propose new areas when multiple sources point to a durable domain that does not fit the current structure.
- Do not create a new area for a one-off topic if a concept, project, question, or summary page is enough.

## Future Work Placeholders

- Instagram links may initially be pasted into `raw/sources/instagram/instagram_saved_links.md`. Future tooling should process links or pasted post contents into career/job notes, AI learning/implementation notes, and startup/business notes.
- YouTube links and transcripts should eventually become source summaries with video title, channel, URL, date captured, transcript source, key ideas, implementation notes, and related wiki pages.
