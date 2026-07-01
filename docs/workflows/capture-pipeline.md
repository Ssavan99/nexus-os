# Capture Pipeline

Status: Phase 4 / Nexus v1 #2 — spec.

Make capturing a source (Instagram reel, YouTube, article, idea, meeting) **fast and repeatable**, so it lands in the vault in the right place with a consistent shape and flows into the brain via the 5-minute sync. Builds directly on the existing convention in `inbox/how-to-add-notes.md` — it does not invent a new format.

It's a **prompt-pack any agent runs** (convention, not new infra). GBrain indexes; the vault holds the files; agents write them on user approval.

## Scope: assisted capture, not fully-automatic ingestion

There is **no reliable/safe way to auto-pull the user's *saved* Instagram collection** (no official API; scraping needs the user's login, breaks ToS, is fragile). So capture is **assisted**: the user hands over the raw material in whatever form is easiest, and the pipeline extracts, **summarizes**, formats, and files it. It handles **every content type** as long as *some* form of the content is provided.

## Input modes (cover all post/reel types)

Provide any one (or more) of these per source:

- **Caption / pasted text** — caption-only posts or reels.
- **Transcript** — audio reels (user's tool: https://wayin.ai/wayinvideo/, or any transcript).
- **Screenshot / image** — text-in-video reels (no audio) and photo posts/carousels: the agent reads on-screen text/visuals with vision/OCR.
- **URL** — always include if available (provenance; public caption may be readable from it).

Other fields:
- **Type**: `instagram` | `youtube` | `article` | `idea` | `journal` | `meeting` | `document`
- **Connection hints** (optional): Startup / Job / AI learning / Personal.

**Always produce a `summary`** (see below) regardless of input mode — so agents can reference the content and the user can verify it without re-watching.

## Routing (from `how-to-add-notes.md`)

| Type | Folder |
|---|---|
| Instagram saved/pasted | `raw/sources/instagram/` |
| YouTube transcript | `raw/sources/youtube/` |
| Article | `raw/sources/articles/` |
| Startup idea | `raw/sources/ideas/` |
| Job/career doc | `raw/sources/documents/` |
| Journal/self | `raw/sources/journals/` |
| Meeting | `raw/sources/meetings/` |
| Loose idea | `inbox/loose-notes/` |

## File shape

Filename: short kebab-case title. Frontmatter makes captures queryable by the checklist engine + coverage:

```markdown
---
type: note
source: instagram            # instagram|youtube|article|idea|meeting|...
area: [career]               # startups|career|ai-learning|personal|system (list ok)
captured: 2026-07-01
status: raw                  # raw -> (later) integrated
url: <source url>
creator: <handle/author>
input_mode: caption|transcript|screenshot|url   # how content was provided
---

# <Short Title>

Summary:
- <2-4 line concise summary of what the reel/post actually says — ALWAYS filled, whatever the input mode. This is what agents reference and the user verifies.>

Raw capture:
- <caption / transcript / text read from the screenshot — preserve meaning, don't rewrite. If from an image, note "(read from screenshot)".>

Why I saved it:
- <one line>

Useful ideas:
- <optional>

Possible connection:
- Startup:
- Job search:
- AI learning:
- Personal:
```

## The `capture` operation (what an agent does)

1. Pick the folder by `type`; generate a kebab-case slug.
2. Fill the frontmatter + template from the input; set `status: raw`, `captured: <today>`, tag `area` from the connection hints.
3. **Write to the vault on user approval** (per boundary rules). Preserve provenance; never silently rewrite the raw content.
4. The 5-min brain-sync ingests it (or run `launchctl kickstart -k gui/$(id -u)/com.nexus.brain-sync` to ingest now).
5. Report the path + that it's queued for later synthesis.

## After capture (connects to the rest of the system)

- Captured items are `status: raw`. A later **synthesis** pass (or the checklist engine) folds them into the durable wiki playbooks and flips `status: integrated`, updating the area's `source-coverage`/backlog. This is how the raw→wiki coverage gap gets closed over time.
- A capture tagged `area: career` seeds the **Job system** backlog once that area is built.

## Boundaries

- Vault writes only on explicit user approval.
- `raw/` is source-of-truth: preserve original meaning + provenance; do not rewrite (per `raw/README.md`).
- Sensitive/credential-like raw material: flag, do not copy tokens into wiki/prompts.
- No new capture infrastructure — this is a convention + prompt-pack over GBrain + the vault.
