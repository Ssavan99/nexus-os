from __future__ import annotations

import io
import os
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.cli import main


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.old_vault_path = os.environ.get("VAULT_PATH")
        self.vault_dir = tempfile.TemporaryDirectory()
        self.vault = Path(self.vault_dir.name)
        os.environ["VAULT_PATH"] = str(self.vault)

    def tearDown(self) -> None:
        if self.old_vault_path is None:
            os.environ.pop("VAULT_PATH", None)
        else:
            os.environ["VAULT_PATH"] = self.old_vault_path
        self.vault_dir.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def init_vault(self) -> None:
        code, _stdout, stderr = self.run_cli("init")
        self.assertEqual(code, 0, stderr)

    def write_raw_source(self, relative_path: str, content: str) -> Path:
        path = self.vault / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_plan_ingest_rejects_paths_outside_vault(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
            handle.write("# Outside\n")
            outside_path = Path(handle.name)
        try:
            code, _stdout, stderr = self.run_cli("plan-ingest", str(outside_path))
        finally:
            outside_path.unlink(missing_ok=True)

        self.assertEqual(code, 1)
        self.assertIn("inside VAULT_PATH", stderr)

    def test_plan_ingest_rejects_non_raw_paths(self) -> None:
        self.init_vault()
        wiki_page = self.vault / "wiki" / "summaries" / "note.md"
        wiki_page.write_text("# Not Raw\n", encoding="utf-8")

        code, _stdout, stderr = self.run_cli("plan-ingest", "wiki/summaries/note.md")

        self.assertEqual(code, 1)
        self.assertIn("under raw", stderr)

    def test_draft_summary_creates_file(self) -> None:
        self.init_vault()
        self.write_raw_source(
            "raw/sources/documents/manual-ingest.md",
            "# Manual Ingest\n\nStartup customer research notes.\n",
        )

        code, stdout, stderr = self.run_cli(
            "draft-summary", "raw/sources/documents/manual-ingest.md"
        )

        self.assertEqual(code, 0, stderr)
        self.assertIn("Draft summary:", stdout)
        summary = self.vault / "wiki" / "summaries" / "manual-ingest.md"
        self.assertTrue(summary.exists())
        content = summary.read_text(encoding="utf-8")
        self.assertIn("type: source-summary", content)
        self.assertIn('title: "Manual Ingest"', content)
        self.assertIn("raw/sources/documents/manual-ingest.md", content)

    def test_draft_summary_refuses_overwrite(self) -> None:
        self.init_vault()
        self.write_raw_source("raw/sources/documents/note.md", "# Note\n")
        first_code, _stdout, stderr = self.run_cli(
            "draft-summary", "raw/sources/documents/note.md"
        )
        self.assertEqual(first_code, 0, stderr)

        second_code, _stdout, stderr = self.run_cli(
            "draft-summary", "raw/sources/documents/note.md"
        )

        self.assertEqual(second_code, 1)
        self.assertIn("will not be overwritten", stderr)

    def test_append_log_creates_consistent_heading(self) -> None:
        self.init_vault()
        code, _stdout, stderr = self.run_cli(
            "append-log",
            "--type",
            "ingest",
            "--title",
            "Manual Ingest",
            "--path",
            "raw/sources/documents/manual-ingest.md",
            "--page",
            "wiki/summaries/manual-ingest.md",
        )

        self.assertEqual(code, 0, stderr)
        today = datetime.now(timezone.utc).date().isoformat()
        log = (self.vault / "wiki" / "log.md").read_text(encoding="utf-8")
        self.assertIn(f"## [{today}] ingest | Manual Ingest", log)
        self.assertIn("raw/sources/documents/manual-ingest.md", log)
        self.assertIn("wiki/summaries/manual-ingest.md", log)

    def test_rebuild_index_finds_generated_wiki_pages(self) -> None:
        self.init_vault()
        page = self.vault / "wiki" / "concepts" / "llm-wiki.md"
        page.write_text(
            "---\n"
            'title: "LLM Wiki"\n'
            "type: concept\n"
            "status: draft\n"
            'summary: "Persistent generated knowledge layer."\n'
            "---\n\n"
            "# LLM Wiki\n",
            encoding="utf-8",
        )

        code, _stdout, stderr = self.run_cli("rebuild-index")

        self.assertEqual(code, 0, stderr)
        index = (self.vault / "wiki" / "index.md").read_text(encoding="utf-8")
        self.assertIn("[[concepts/llm-wiki]]", index)
        self.assertIn("LLM Wiki", index)
        self.assertIn("concept", index)
        self.assertRegex(index, re.compile(r"Persistent generated knowledge layer\."))


if __name__ == "__main__":
    unittest.main()
