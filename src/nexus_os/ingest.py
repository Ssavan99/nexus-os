from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .vault import VaultPaths


TEXT_EXTENSIONS = {".md", ".markdown", ".txt"}
DEFAULT_SOURCE_TYPES = {
    "instagram",
    "youtube",
    "articles",
    "meetings",
    "journals",
    "documents",
}
CONTROL_WIKI_FILES = {"index.md", "log.md", "_schema.md"}


@dataclass(frozen=True)
class SourceInfo:
    path: Path
    relative_path: Path
    source_type: str
    title: str
    text: str
    suggested_summary_path: Path
    likely_areas: list[str]
    likely_concepts: list[str]
    likely_people: list[str]
    likely_organizations: list[str]
    likely_decisions: list[str]
    likely_questions: list[str]


def resolve_raw_source(paths: VaultPaths, source_arg: Path) -> Path:
    source_path = source_arg.expanduser()
    if not source_path.is_absolute():
        source_path = paths.vault_root / source_path
    source_path = source_path.resolve()

    if not _is_relative_to(source_path, paths.vault_root):
        raise ValueError(f"Source path must be inside VAULT_PATH: {source_path}")
    if not _is_relative_to(source_path, paths.raw_root):
        raise ValueError(f"Source path must be under raw/: {source_path}")
    if not source_path.exists():
        raise FileNotFoundError(f"Source does not exist: {source_path}")
    if not source_path.is_file():
        raise ValueError(f"Source is not a file: {source_path}")
    if source_path.suffix.lower() not in TEXT_EXTENSIONS:
        raise ValueError("Only Markdown and text raw sources are supported.")
    return source_path


def collect_source_info(paths: VaultPaths, source_arg: Path) -> SourceInfo:
    source_path = resolve_raw_source(paths, source_arg)
    text = source_path.read_text(encoding="utf-8")
    title = detect_title(text, source_path)
    source_type = infer_source_type(paths, source_path)
    summary_name = f"{slugify(title or source_path.stem)}.md"
    suggested_summary_path = paths.wiki_root / "summaries" / summary_name

    return SourceInfo(
        path=source_path,
        relative_path=source_path.relative_to(paths.vault_root),
        source_type=source_type,
        title=title,
        text=text,
        suggested_summary_path=suggested_summary_path,
        likely_areas=infer_areas(text, source_type),
        likely_concepts=extract_concepts(text),
        likely_people=extract_people(text),
        likely_organizations=extract_organizations(text),
        likely_decisions=extract_decision_checks(text),
        likely_questions=extract_questions(text),
    )


def render_ingest_plan(info: SourceInfo, paths: VaultPaths) -> str:
    summary_rel = info.suggested_summary_path.relative_to(paths.vault_root)
    return "\n".join(
        [
            "# Nexus OS Ingest Plan",
            "",
            f"- Detected source title: {info.title}",
            f"- Source path: `{info.relative_path}`",
            f"- Source type: {info.source_type}",
            f"- Suggested summary file: `{summary_rel}`",
            "",
            "## Likely Wiki Areas To Update",
            _bullet_list(info.likely_areas),
            "",
            "## Likely Concepts To Check",
            _bullet_list(info.likely_concepts),
            "",
            "## Likely People To Check",
            _bullet_list(info.likely_people),
            "",
            "## Likely Organizations To Check",
            _bullet_list(info.likely_organizations),
            "",
            "## Likely Decisions To Check",
            _bullet_list(info.likely_decisions),
            "",
            "## Likely Questions To Check",
            _bullet_list(info.likely_questions),
            "",
            "## Manual LLM Checklist",
            "1. Read the raw source and keep it immutable.",
            f"2. Draft or complete `{summary_rel}` using `templates/source_summary.md`.",
            "3. Update relevant pages under `wiki/areas/`.",
            "4. Update or create related concept, decision, question, people, and organization pages.",
            "5. Cite the raw source path when making factual claims.",
            "6. Note uncertainty and contradictions explicitly.",
            "7. Run `nexus-os rebuild-index`.",
            f"8. Run `nexus-os append-log --type ingest --title \"{info.title}\" --path \"{info.relative_path}\"`.",
        ]
    )


def render_summary_draft(info: SourceInfo, paths: VaultPaths) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    template = template_path(paths.repo_root, "source_summary.md").read_text(
        encoding="utf-8"
    )
    replacements = {
        "title": info.title,
        "created": today,
        "updated": today,
        "source_path": str(info.relative_path),
        "source_type": info.source_type,
        "summary_placeholder": "TODO: Complete this summary from the raw source.",
        "raw_excerpt": excerpt_text(info.text),
    }
    return render_template(template, replacements)


def rebuild_index_content(paths: VaultPaths) -> str:
    entries = []
    if paths.wiki_root.exists():
        for page in sorted(paths.wiki_root.rglob("*.md")):
            if page.name in CONTROL_WIKI_FILES:
                continue
            rel = page.relative_to(paths.wiki_root)
            metadata = read_page_metadata(page)
            title = metadata.get("title") or first_heading(page) or page.stem
            page_type = metadata.get("type", "")
            status = metadata.get("status", "")
            summary = metadata.get("summary") or first_section_line(page, "Summary")
            entries.append((rel, title, page_type, status, summary))

    lines = [
        "# Nexus OS Wiki Index",
        "",
        "Catalog of generated wiki pages. Rebuilt by `nexus-os rebuild-index`.",
        "",
        "| Page | Title | Type | Status | Summary |",
        "| --- | --- | --- | --- | --- |",
    ]
    for rel, title, page_type, status, summary in entries:
        link = rel.with_suffix("").as_posix()
        lines.append(
            f"| [[{link}]] | {escape_table(title)} | {escape_table(page_type)} | "
            f"{escape_table(status)} | {escape_table(summary)} |"
        )
    lines.append("")
    return "\n".join(lines)


def read_page_metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def first_section_line(path: Path, section: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            in_section = stripped[3:].strip().casefold() == section.casefold()
            continue
        if in_section and stripped and not stripped.startswith("#"):
            return stripped.removeprefix("- ").strip()
    return ""


def template_path(repo_root: Path, name: str) -> Path:
    path = repo_root / "templates" / name
    if not path.exists():
        raise FileNotFoundError(f"Missing template: {path}")
    return path


def render_template(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def detect_title(text: str, path: Path) -> str:
    metadata_title = _frontmatter_value(text, "title")
    if metadata_title:
        return metadata_title

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:80]

    return path.stem.replace("-", " ").replace("_", " ").title()


def infer_source_type(paths: VaultPaths, path: Path) -> str:
    try:
        rel = path.relative_to(paths.raw_root / "sources")
    except ValueError:
        return "raw"
    if len(rel.parts) >= 2:
        return rel.parts[0]
    return "uncategorized"


def infer_areas(text: str, source_type: str) -> list[str]:
    lower = text.casefold()
    areas = []
    keyword_map = {
        "personal": [
            "goal",
            "health",
            "psychology",
            "journal",
            "habit",
            "self-improvement",
            "reflection",
        ],
        "career": ["career", "job", "resume", "interview", "manager", "promotion"],
        "ai-learning": [
            "ai",
            "llm",
            "model",
            "prompt",
            "agent",
            "implementation",
            "machine learning",
        ],
        "startups": [
            "startup",
            "business",
            "customer",
            "market",
            "sales",
            "revenue",
            "founder",
        ],
        "projects": ["project", "roadmap", "technical", "architecture", "build", "ship"],
    }
    for area, keywords in keyword_map.items():
        if any(keyword in lower for keyword in keywords):
            areas.append(area)

    if not areas:
        if source_type == "journals":
            areas.append("personal")
        elif source_type in {"meetings", "documents"}:
            areas.append("projects")

    return areas or ["TODO: choose or propose area"]


def extract_concepts(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z-]{4,}", text)
    stop = {
        "about",
        "after",
        "before",
        "could",
        "should",
        "their",
        "there",
        "these",
        "those",
        "through",
        "would",
        "notes",
        "source",
        "summary",
    }
    counts: dict[str, int] = {}
    for word in words:
        key = word.casefold()
        if key in stop:
            continue
        counts[key] = counts.get(key, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _count in ranked[:8]] or ["TODO: identify concepts"]


def extract_people(text: str) -> list[str]:
    names = _unique_matches(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", text)
    return names[:8] or ["TODO: check people mentioned"]


def extract_organizations(text: str) -> list[str]:
    orgs = _unique_matches(
        r"\b[A-Z][A-Za-z0-9&.-]+(?: [A-Z][A-Za-z0-9&.-]+)* "
        r"(?:Inc|LLC|Labs|AI|Systems|University|Company|Corp|Corporation)\b",
        text,
    )
    return orgs[:8] or ["TODO: check organizations mentioned"]


def extract_decision_checks(text: str) -> list[str]:
    lower = text.casefold()
    if any(word in lower for word in ("decision", "decide", "option", "tradeoff")):
        return ["TODO: check whether this source implies a decision page"]
    return ["None obvious; verify during ingest"]


def extract_questions(text: str) -> list[str]:
    questions = []
    for line in text.splitlines():
        stripped = line.strip("- ").strip()
        if stripped.endswith("?"):
            questions.append(stripped)
    return questions[:8] or ["TODO: identify open questions"]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "untitled-source"


def excerpt_text(text: str, limit: int = 2000) -> str:
    cleaned = text.strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit].rstrip() + "\n\n[Excerpt truncated. Read raw source for full context.]"


def escape_table(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ")


def _frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end == -1:
        return ""
    for line in text[4:end].splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def _bullet_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def _unique_matches(pattern: str, text: str) -> list[str]:
    seen = set()
    values = []
    for match in re.findall(pattern, text):
        if match in seen:
            continue
        seen.add(match)
        values.append(match)
    return values


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True
