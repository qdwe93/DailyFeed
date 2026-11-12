"""Duplicate index must only read published channel files (T08)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _helpers import day, gn, write

import run
from pipeline import digest
from pipeline.util import canonical, existing_urls


class TestDedupeIndex(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_T08_digest_and_docs_urls_are_not_article_sources(self):
        yesterday, today = day("2026-11-11"), day("2026-11-12")
        published = write(self.root, "geeknews", yesterday, gn(2))
        digest.write_digest(yesterday, self.root, now=day("2026-11-11", 12))
        only_in_digest = "https://only-in-digest.example/post"
        (self.root / "daily" / "2026-11-10.md").write_text(f"- [x]({only_in_digest})\n", encoding="utf-8")
        (self.root / "today.md").write_text(f"- [x]({only_in_digest}/today)\n", encoding="utf-8")
        (self.root / "README.md").write_text("| 1 | Src | https://readme.example/feed | | RSS |\n", encoding="utf-8")
        (self.root / "notes").mkdir()
        (self.root / "notes" / "memo.md").write_text("https://memo.example/a\n", encoding="utf-8")
        (self.root / "log").mkdir()
        (self.root / "log" / "2026-11-11.md").write_text("https://log.example/a\n", encoding="utf-8")

        for index in (run._existing_index(today, self.root), existing_urls(self.root)):
            rels = set(index.values())
            self.assertEqual(rels, {published.relative_to(self.root).as_posix()})
            self.assertIn(canonical("https://news.hada.io/topic?id=9001"), index)
            for url in (only_in_digest, f"{only_in_digest}/today", "https://readme.example/feed",
                        "https://memo.example/a", "https://log.example/a"):
                self.assertNotIn(canonical(url), index)

    def test_same_date_files_still_excluded(self):
        today = day("2026-11-12")
        write(self.root, "geeknews", today, gn(1))
        self.assertEqual(run._existing_index(today, self.root), {})
        self.assertEqual(len(run._existing_index(day("2026-11-13"), self.root)), 1)


if __name__ == "__main__":
    unittest.main()
