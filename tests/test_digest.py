"""today.md / daily/ digest tests (T01–T07, T09–T14). Offline only."""

from __future__ import annotations

import io
import re
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock
from urllib.parse import unquote

from _helpers import REPO, day, gh, gn, tech, write, work_dir, yt

import run
from pipeline import digest, publish
from pipeline.util import urls_in_markdown

D = day("2026-11-12")
NOW = day("2026-11-12", 12, 34)
MONDAY = day("2026-11-09")


def urls(text: str) -> set[str]:
    return set(urls_in_markdown(text))


class DigestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def digest(self, date=D, now=NOW, **kw) -> str:
        paths = digest.write_digest(date, self.root, now=now, **kw)
        return paths[0].read_text(encoding="utf-8")

    def quiet(self, fn, *a, **kw):
        with redirect_stdout(io.StringIO()):
            return fn(*a, **kw)


class TestDigest(DigestBase):
    def test_T01_all_daily_articles_with_links_and_summaries(self):
        files = [write(self.root, "geeknews", D, gn(2)), write(self.root, "tech", D, tech(3)), write(self.root, "youtube", D, yt(1))]
        text = self.digest()
        for path in files:
            self.assertTrue(urls(path.read_text(encoding="utf-8")) <= urls(text), path)
        self.assertEqual(len(urls(text)), 6)
        for i in range(1, 4):
            for b in range(1, 6):
                self.assertIn(f"- 요약 {i}-{b}", text)
        self.assertIn("- 영상 요약 1-2", text)
        self.assertIn("- [GN 기사 2](https://news.hada.io/topic?id=9002)", text)
        # heading hierarchy: channel ##, source ###, article ####
        self.assertIn("\n## Tech Feeds\n", text)
        self.assertIn("\n### NAVER D2\n", text)
        self.assertIn("\n#### 테크 글 1\n", text)
        self.assertEqual(len(re.findall(r"^# ", text, flags=re.M)), 1)
        self.assertIn("- [GeekNews](#geeknews) — 2건", text)
        self.assertIn("- [Tech Feeds](#tech-feeds) — 3건", text)
        self.assertIn("- [YouTube Tech](#youtube-tech) — 1건", text)
        # today.md and daily/<date>.md are identical
        self.assertEqual(text, (self.root / "daily" / "2026-11-12.md").read_text(encoding="utf-8"))
        self.assertIn("수집일: 2026-11-12", text)
        self.assertIn("통합 생성: 2026-11-12 12:34 KST", text)

    def test_T02_weekly_trending_added_on_monday(self):
        now = day("2026-11-09", 12, 30)
        write(self.root, "geeknews", MONDAY, gn(2))
        write(self.root, "tech", MONDAY, tech(3))
        write(self.root, "youtube", MONDAY, yt(1))
        write(self.root, "github", MONDAY, gh(10))
        text = self.digest(MONDAY, now)
        self.assertEqual(len(urls(text)), 16)
        self.assertIn("\n## GitHub Trending Weekly\n", text)
        self.assertIn("\n### 10. owner/repo10\n", text)
        self.assertIn("- [GitHub Trending Weekly](#github-trending-weekly) — 10건", text)

    def test_T03_no_weekly_section_on_other_days(self):
        write(self.root, "github", MONDAY, gh(10))  # last Monday's snapshot exists
        write(self.root, "geeknews", D, gn(2))
        text = self.digest()
        self.assertNotIn("GitHub Trending", text)
        self.assertNotIn("github.com/owner", text)

    def test_T04_same_day_rerun_accumulates_without_duplicates(self):
        items = {"geeknews": [{"id": f"geeknews-{i}", **g} for i, g in enumerate(gn(2), 1)]}
        date_dir = work_dir(self.root, D, items, {})
        self.quiet(run.render_channels, date_dir, D, ["geeknews"], root=self.root)
        first = self.digest()
        items = {"geeknews": [{"id": f"geeknews-{i}", **g} for i, g in enumerate(gn(4), 1)]}  # merged rerun
        date_dir = work_dir(self.root, D, items, {})
        written, _, warnings = self.quiet(run.render_channels, date_dir, D, ["geeknews"], root=self.root)
        self.assertEqual(warnings, [])
        second = self.digest(now=day("2026-11-12", 18))
        self.assertTrue(urls(first) <= urls(second))
        self.assertEqual(len(urls(second)), 4)
        self.assertEqual(len(re.findall(r"topic\?id=9001\)", second)), 1)
        self.assertEqual(len(list((self.root / "geeknews").rglob("2026-11-12_*.md"))), 1)

    def test_T05_skip_and_failed_summary_match_published_file(self):
        cands = [
            {"id": "tech-1", "source": "NAVER D2", "title": "A", "url": "https://d2.naver.com/a"},
            {"id": "tech-2", "source": "NAVER D2", "title": "B (skip)", "url": "https://d2.naver.com/b"},
            {"id": "tech-3", "source": "NAVER D2", "title": "C original", "url": "https://d2.naver.com/c"},
        ]
        summaries = {
            "tech-1": {"title_ko": "가", "bullets": ["가 요약"]},
            "tech-2": {"skip": True},
            # tech-3: summary failed -> title only
        }
        date_dir = work_dir(self.root, D, {"tech": cands}, summaries)
        (path,), _, _ = self.quiet(run.render_channels, date_dir, D, ["tech"], root=self.root)
        text = self.digest()
        self.assertEqual(urls(text), urls(path.read_text(encoding="utf-8")))
        self.assertNotIn("https://d2.naver.com/b", text)
        section = text.split("#### C original", 1)[1]
        self.assertTrue(section.lstrip("\n").startswith("원문: https://d2.naver.com/c"))
        self.assertNotRegex(section, r"\n- ")  # no invented summary for the failed item
        self.assertEqual(digest._body(path.read_text(encoding="utf-8")) in text, True)

    def test_T06_held_channels_marked_and_existing_output_kept(self):
        tech_file = write(self.root, "tech", D, tech(2))  # published by an earlier run today
        write(self.root, "geeknews", D, gn(3))
        text = self.digest(held=["tech", "youtube"])
        self.assertTrue(urls(tech_file.read_text(encoding="utf-8")) <= urls(text))
        self.assertIn("- [Tech Feeds](#tech-feeds) — 2건", text)
        self.assertIn("이번 실행의 신규 항목은 사용 가능한 요약 모델이 없어 요약/발행 보류", text)
        self.assertIn("- [YouTube Tech](#youtube-tech) — 보류", text)
        yt_section = text.split("## YouTube Tech", 1)[1]
        self.assertIn("요약/발행 보류", yt_section)
        self.assertNotIn("발행 파일 없음", yt_section)
        self.assertTrue(tech_file.exists())
        # a later weekly/manual rebuild (held=None) keeps the recorded held state
        self.assertEqual(digest.previous_held(self.root, D), ["tech", "youtube"])
        again = self.digest(held=None)
        self.assertIn("- [YouTube Tech](#youtube-tech) — 보류", again)

    def test_T07_guard_refusal_keeps_previous_output_in_digest(self):
        published = [{"id": f"geeknews-{i}", **g} for i, g in enumerate(gn(3), 1)]
        date_dir = work_dir(self.root, D, {"geeknews": published}, {})
        self.quiet(run.render_channels, date_dir, D, ["geeknews"], root=self.root)
        # a rerun without the earlier candidates (e.g. another PC): fewer links -> guard refuses
        date_dir = work_dir(self.root, D, {"geeknews": [published[0]]}, {})
        written, _, warnings = self.quiet(run.render_channels, date_dir, D, ["geeknews"], root=self.root)
        self.assertEqual(written, [])
        self.assertTrue(warnings)
        text = self.digest()
        self.assertEqual(len(urls(text)), 3)

    def test_T09_past_date_render_keeps_today(self):
        write(self.root, "geeknews", D, gn(2))
        today_before = self.digest()
        past = day("2026-11-01")
        write(self.root, "geeknews", past, gn(5, start=50))
        paths = digest.write_digest(past, self.root, now=day("2026-11-12", 15), held=[])
        self.assertEqual(paths, [self.root / "daily" / "2026-11-01.md"])
        self.assertEqual((self.root / "today.md").read_text(encoding="utf-8"), today_before)
        self.assertIn("topic?id=9050", paths[0].read_text(encoding="utf-8"))

    def test_T10_missing_outputs_are_not_reported_as_zero(self):
        text = self.digest()
        self.assertNotRegex(text, r"0건")
        for label in ("GeekNews", "Tech Feeds", "YouTube Tech"):
            self.assertIn(f"- [{label}](#{label.lower().replace(' ', '-')}) — 발행 파일 없음", text)
        self.assertIn("이 수집일의 발행 파일이 없음", text)
        self.assertNotIn("GitHub Trending", text)

    def test_T11_digest_error_keeps_existing_today_and_warns(self):
        write(self.root, "geeknews", D, gn(2))
        before = self.digest()
        extra = self.root / "geeknews" / "2026년11월" / "2026-11-12_중복-파일.md"
        extra.write_text("# GeekNews — 2026-11-12\n\n- [x](https://x.example/1)\n", encoding="utf-8")
        with self.assertRaises(digest.DigestError):
            digest.write_digest(D, self.root, now=day("2026-11-12", 18))
        warnings: list[str] = []
        paths = self.quiet(run.write_digest_safe, D, [], warnings, root=self.root)
        self.assertEqual(paths, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("통합 문서", warnings[0])
        self.assertEqual((self.root / "today.md").read_text(encoding="utf-8"), before)
        self.assertEqual(list(self.root.glob("**/*.tmp")), [])
        # the warning reaches the run log and the notification text like any other warning
        run_info = {"started": "2026-11-12T12:00:00+09:00", "status": "partial", "status_ko": "부분 완료", "warnings": warnings}
        self.assertIn("통합 문서", run.notification_text(run_info))

    def test_T13_korean_paths_are_encoded_repo_links(self):
        path = write(self.root, "tech", D, tech(1))
        text = self.digest()
        links = re.findall(r"\[채널별 원본\]\(([^)]+)\)", text)
        self.assertEqual(len(links), 1)
        link = links[0]
        self.assertTrue(link.startswith("/tech/"))
        self.assertRegex(link, r"^[A-Za-z0-9/%._~-]+$")  # no raw Korean or spaces
        self.assertEqual(self.root / unquote(link).lstrip("/"), path)


class TestPublishAndOps(DigestBase):
    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, encoding="utf-8", check=True).stdout

    def test_T12_publish_stages_today_and_daily(self):
        self.assertIn("today.md", publish.OUTPUT_PATHS)
        self.assertIn("daily", publish.OUTPUT_PATHS)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "test")
        (self.root / "seed.txt").write_text("x", encoding="utf-8")
        self.git("add", "seed.txt")
        self.git("commit", "-q", "-m", "seed")
        write(self.root, "geeknews", D, gn(1))
        self.digest()
        with mock.patch.object(publish, "ROOT", self.root):
            result = publish.publish_outputs("test", push=False)
        self.assertIsNone(result["error"], result)
        self.assertTrue(result["committed"])
        files = set(self.git("show", "--name-only", "--format=", "HEAD").splitlines())
        self.assertIn("today.md", files)
        self.assertIn("daily/2026-11-12.md", files)

    def test_T14_scheduler_and_branch_untouched(self):
        script = (REPO / "scripts" / "register_task.ps1").read_text(encoding="utf-8")
        self.assertIn('-TaskName "DailyFeed"', script)
        self.assertIn("-Daily -At 12:00", script)
        self.assertIn('run.py`" auto', script)
        # publishing follows whatever branch is checked out; nothing pins a feature branch
        source = (REPO / "pipeline" / "publish.py").read_text(encoding="utf-8")
        self.assertIn("current_branch()", source)
        self.assertNotIn("today-digest", source)
        digest_src = (REPO / "pipeline" / "digest.py").read_text(encoding="utf-8")
        self.assertNotIn("subprocess", digest_src)  # digest never touches git
        self.assertNotIn("summarize", digest_src)  # and never calls an LLM


if __name__ == "__main__":
    unittest.main()
