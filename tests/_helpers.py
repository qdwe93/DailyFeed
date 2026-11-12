"""Shared fixtures for the offline tests: no network, no LLM, no git push, no webhooks."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from pipeline import render  # noqa: E402
from pipeline.util import KST  # noqa: E402


def day(value: str, hour: int = 0, minute: int = 0) -> datetime:
    y, m, d = (int(x) for x in value.split("-"))
    return datetime(y, m, d, hour, minute, tzinfo=KST)


def gn(n: int, start: int = 1) -> list[dict]:
    return [{"title": f"GN 기사 {i}", "url": f"https://news.hada.io/topic?id={9000 + i}"} for i in range(start, start + n)]


def tech(n: int, start: int = 1, source: str = "NAVER D2") -> list[dict]:
    return [
        {
            "source": source,
            "title_ko": f"테크 글 {i}",
            "url": f"https://d2.naver.com/helloworld/{1000 + i}",
            "bullets": [f"요약 {i}-{b}" for b in range(1, 6)],
        }
        for i in range(start, start + n)
    ]


def yt(n: int, start: int = 1) -> list[dict]:
    return [
        {
            "source": "Fireship",
            "title_ko": f"영상 {i}",
            "url": f"https://www.youtube.com/watch?v=vid{i:08d}",
            "bullets": [f"영상 요약 {i}-1", f"영상 요약 {i}-2"],
        }
        for i in range(start, start + n)
    ]


def gh(n: int) -> list[dict]:
    return [
        {"repo": f"owner/repo{i}", "url": f"https://github.com/owner/repo{i}", "language": "Python",
         "stars": f"{i * 100} stars this week", "bullets": [f"레포 설명 {i}"]}
        for i in range(1, n + 1)
    ]


def write(root: Path, channel: str, date: datetime, items: list[dict]) -> Path:
    return render.write_channel(channel, date, {"items": items}, root=root)


def work_dir(root: Path, date: datetime, channels: dict[str, list[dict]], summaries: dict) -> Path:
    """work/<date>/candidates.json + summaries.json as collect/summarize would leave them."""
    date_dir = root / "work" / f"{date:%Y-%m-%d}"
    date_dir.mkdir(parents=True, exist_ok=True)
    payload = {"channels": {c: {"items": items, "count": len(items)} for c, items in channels.items()}}
    (date_dir / "candidates.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    (date_dir / "summaries.json").write_text(json.dumps({"items": summaries}, ensure_ascii=False), encoding="utf-8")
    return date_dir
