from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from .ingest import (
    collect_source_info,
    rebuild_index_content,
    render_ingest_plan,
    render_summary_draft,
)
from .vault import VaultConfigError, VaultPaths, resolve_vault_paths


SEARCH_EXTENSIONS = {".md", ".markdown", ".txt"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexus-os",
        description="Operate safely on the external Nexus OS Obsidian vault.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="Validate VAULT_PATH and show vault locations.")
    subparsers.add_parser("init", help="Initialize the external vault structure.")

    add_note = subparsers.add_parser(
        "add-note",
        help="Copy a note into raw/sources without overwriting an existing raw file.",
    )
    add_note.add_argument("path", type=Path, help="Markdown or text file to add.")
    add_note.add_argument(
        "--source-type",
        default="documents",
        help="Raw source type folder under raw/sources/. Defaults to documents.",
    )

    plan_ingest = subparsers.add_parser(
        "plan-ingest",
        help="Print a manual ingest plan for a raw source without modifying the wiki.",
    )
    plan_ingest.add_argument("path", type=Path, help="Raw source path inside the vault.")

    draft_summary = subparsers.add_parser(
        "draft-summary",
        help="Create a structured draft summary for a raw source.",
    )
    draft_summary.add_argument("path", type=Path, help="Raw source path inside the vault.")
    draft_summary.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing draft summary.",
    )

    append_log = subparsers.add_parser(
        "append-log",
        help="Append a structured entry to wiki/log.md.",
    )
    append_log.add_argument("--type", required=True, help="Log entry type, e.g. ingest.")
    append_log.add_argument("--title", required=True, help="Log entry title.")
    append_log.add_argument("--path", required=True, help="Related source or wiki path.")
    append_log.add_argument(
        "--page",
        action="append",
        default=[],
        help="Generated or updated wiki page. Can be repeated.",
    )

    subparsers.add_parser(
        "rebuild-index",
        help="Rebuild wiki/index.md from generated wiki Markdown pages.",
    )

    search = subparsers.add_parser("search", help="Search raw and wiki Markdown files.")
    search.add_argument("query", help="Case-insensitive query text.")
    search.add_argument(
        "--layer",
        choices=("all", "wiki", "raw"),
        default="all",
        help="Vault layer to search. Defaults to all.",
    )
    search.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum matching lines to print. Defaults to 20.",
    )

    return parser


def cmd_check(paths: VaultPaths) -> int:
    print(f"Repository: {paths.repo_root}")
    print(f"Vault:      {paths.vault_root}")
    print(f"Raw:        {paths.raw_root}")
    print(f"Wiki:       {paths.wiki_root}")
    return 0


def cmd_init(paths: VaultPaths) -> int:
    for directory in (
        paths.raw_root / "sources" / "instagram",
        paths.raw_root / "sources" / "youtube",
        paths.raw_root / "sources" / "articles",
        paths.raw_root / "sources" / "meetings",
        paths.raw_root / "sources" / "journals",
        paths.raw_root / "sources" / "documents",
        paths.raw_root / "assets",
        paths.wiki_root / "areas" / "personal",
        paths.wiki_root / "areas" / "career",
        paths.wiki_root / "areas" / "ai-learning",
        paths.wiki_root / "areas" / "startups",
        paths.wiki_root / "areas" / "projects",
        paths.wiki_root / "concepts",
        paths.wiki_root / "decisions",
        paths.wiki_root / "questions",
        paths.wiki_root / "summaries",
        paths.wiki_root / "people",
        paths.wiki_root / "organizations",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    _write_if_missing(
        paths.wiki_root / "index.md",
        "# Nexus OS Wiki Index\n\n"
        "Catalog generated wiki pages here. Keep entries short and link to pages.\n\n"
        "## Areas\n\n"
        "- [[areas/personal/]]\n"
        "- [[areas/career/]]\n"
        "- [[areas/ai-learning/]]\n"
        "- [[areas/startups/]]\n"
        "- [[areas/projects/]]\n\n"
        "## Summaries\n\n"
        "## Concepts\n\n"
        "## Decisions\n\n"
        "## Questions\n\n"
        "## People\n\n"
        "## Organizations\n",
    )
    _write_if_missing(
        paths.wiki_root / "log.md",
        "# Nexus OS Wiki Log\n\n"
        "Append ingest, query, and lint events below.\n\n",
    )
    _write_if_missing(paths.wiki_root / "_schema.md", _schema_template())

    print(f"Initialized external vault at {paths.vault_root}")
    return 0


def cmd_add_note(paths: VaultPaths, source_path: Path, source_type: str) -> int:
    source = source_path.expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Source note does not exist: {source}")
    if not source.is_file():
        raise ValueError(f"Source note is not a file: {source}")
    if source.suffix.lower() not in SEARCH_EXTENSIONS:
        raise ValueError("Only Markdown and text notes are supported in this first CLI.")

    source_type = _validate_source_type(source_type)
    target_dir = paths.raw_root / "sources" / source_type
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    if target.exists():
        raise FileExistsError(
            f"Raw source already exists and will not be overwritten: {target}"
        )

    shutil.copy2(source, target)
    _append_log(
        paths,
        f"add-note | {source.name}",
        f"Copied external source into raw/sources/{source_type}/{source.name}.",
    )
    print(f"Added raw source: {target}")
    return 0


def cmd_plan_ingest(paths: VaultPaths, source_path: Path) -> int:
    info = collect_source_info(paths, source_path)
    print(render_ingest_plan(info, paths))
    return 0


def cmd_draft_summary(paths: VaultPaths, source_path: Path, overwrite: bool) -> int:
    info = collect_source_info(paths, source_path)
    target = info.suggested_summary_path
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"Summary already exists and will not be overwritten: {target}"
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_summary_draft(info, paths), encoding="utf-8")
    print(f"Draft summary: {target}")
    return 0


def cmd_append_log(
    paths: VaultPaths, entry_type: str, title: str, path: str, pages: list[str]
) -> int:
    log_path = paths.wiki_root / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text("# Nexus OS Wiki Log\n\n", encoding="utf-8")

    today = datetime.now(timezone.utc).date().isoformat()
    updated_pages = pages or ["TODO: list generated or updated wiki pages"]
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## [{today}] {entry_type} | {title}\n\n")
        handle.write(f"- Source path: `{path}`\n")
        handle.write("- Generated/updated pages:\n")
        for page in updated_pages:
            handle.write(f"  - `{page}`\n")
    print(f"Appended log entry: {log_path}")
    return 0


def cmd_rebuild_index(paths: VaultPaths) -> int:
    paths.wiki_root.mkdir(parents=True, exist_ok=True)
    index_path = paths.wiki_root / "index.md"
    index_path.write_text(rebuild_index_content(paths), encoding="utf-8")
    print(f"Rebuilt index: {index_path}")
    return 0


def cmd_search(paths: VaultPaths, query: str, layer: str, limit: int) -> int:
    if limit < 1:
        raise ValueError("--limit must be at least 1")

    roots = []
    if layer in ("all", "wiki"):
        roots.append(paths.wiki_root)
    if layer in ("all", "raw"):
        roots.append(paths.raw_root)

    needle = query.casefold()
    count = 0
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SEARCH_EXTENSIONS:
                continue
            for line_number, line in _iter_text_lines(path):
                if needle not in line.casefold():
                    continue
                print(
                    f"{path.relative_to(paths.vault_root)}:{line_number}: "
                    f"{line.strip()}"
                )
                count += 1
                if count >= limit:
                    return 0

    if count == 0:
        print("No matches.")
    return 0


def _write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _validate_source_type(source_type: str) -> str:
    normalized = source_type.strip().casefold()
    if not normalized:
        raise ValueError("--source-type cannot be empty")
    if "/" in normalized or "\\" in normalized or normalized in {".", ".."}:
        raise ValueError("--source-type must be a single folder name")
    if not all(char.isalnum() or char in {"-", "_"} for char in normalized):
        raise ValueError("--source-type may only contain letters, numbers, hyphens, and underscores")
    return normalized


def _append_log(paths: VaultPaths, title: str, body: str) -> None:
    log_path = paths.wiki_root / "log.md"
    if not log_path.exists():
        return
    today = datetime.now(timezone.utc).date().isoformat()
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## [{today}] {title}\n\n{body}\n")


def _iter_text_lines(path: Path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            for index, line in enumerate(handle, start=1):
                yield index, line
    except UnicodeDecodeError:
        return


def _schema_template() -> str:
    return """# Nexus OS Wiki Schema

This file describes how LLM sessions should maintain this vault.

## Layers

- `raw/` is immutable source material organized by source type, not knowledge domain.
- `raw/sources/instagram/` is for Instagram links, exports, or pasted post contents.
- `raw/sources/youtube/` is for YouTube links, transcripts, and captured metadata.
- `raw/sources/articles/` is for web articles, papers, and saved posts.
- `raw/sources/meetings/` is for meeting transcripts and call notes.
- `raw/sources/journals/` is for journal entries and personal reflections.
- `raw/sources/documents/` is for project docs, converted PDFs, and miscellaneous notes.
- `raw/assets/` is for local images and attachments.
- `wiki/` is generated Markdown. The LLM may create and update pages here.
- `wiki/areas/` is organized by knowledge domain and can change over time.
- Default areas include personal, career, AI learning, startups, and projects.
- General wiki folders include concepts, decisions, questions, summaries, people, and organizations.
- `wiki/index.md` is the content catalog.
- `wiki/log.md` is the chronological append-only activity log.

## Flexibility

Do not overfit the wiki to today's categories. Add new source-type folders only when a new
capture workflow needs them. Add new `wiki/areas/` pages or folders when sources reveal a
durable domain that deserves its own home.

## Ingest Workflow

1. Process one raw source at a time unless the user asks for a batch.
2. Identify both the source type and the knowledge domains it touches.
3. Create or update a source summary in `wiki/summaries/`.
4. Update relevant area, concept, decision, question, people, and organization pages.
5. Add cross-links using Obsidian wiki links where helpful.
6. Update `wiki/index.md`.
7. Append an entry to `wiki/log.md` with a `## [YYYY-MM-DD] ...` heading.

## Query Workflow

1. Read `wiki/index.md` first.
2. Search relevant wiki pages before raw sources.
3. Cite source summaries or raw files when making factual claims.
4. Offer to file durable answers back into `wiki/areas/`, `wiki/summaries/`, `wiki/questions/`, or `wiki/decisions/`.

## Lint Workflow

Look for stale claims, contradictions, orphan pages, missing links, missing entity pages,
and useful future source-gathering questions.
"""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        paths = resolve_vault_paths()
        if args.command == "check":
            return cmd_check(paths)
        if args.command == "init":
            return cmd_init(paths)
        if args.command == "add-note":
            return cmd_add_note(paths, args.path, args.source_type)
        if args.command == "plan-ingest":
            return cmd_plan_ingest(paths, args.path)
        if args.command == "draft-summary":
            return cmd_draft_summary(paths, args.path, args.overwrite)
        if args.command == "append-log":
            return cmd_append_log(paths, args.type, args.title, args.path, args.page)
        if args.command == "rebuild-index":
            return cmd_rebuild_index(paths)
        if args.command == "search":
            return cmd_search(paths, args.query, args.layer, args.limit)
    except (VaultConfigError, FileExistsError, FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    parser.error(f"Unhandled command: {args.command}")
    return 2
