"""Markdown rendering in AGENT.md format, plus filename selection."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .util import CHANNELS, ROOT, month_dir, slug

HEADERS = {
    "geeknews": "GeekNews",
    "tech": "Tech Feeds",
    "youtube": "YouTube Tech",
    "github": "GitHub Trending Weekly",
}


def output_path(channel: str, date: datetime, headline: str, root: Path = ROOT) -> Path:
    stamp = date.strftime("%Y-%m-%d")
    name = f"{stamp}_{slug(headline or HEADERS[channel], 20)}.md"
    return root / channel / month_dir(date) / name


def _clean(text: str) -> str:
    return " ".join((text or "").split())


def _bullets(bullets) -> str:
    lines = []
    for bullet in bullets or []:
        text = _clean(str(bullet)).lstrip("-• ").strip()
        if text:
            lines.append(f"- {text}")
    return "\n".join(lines)


def pick_headline(items: list[dict]) -> str:
    if not items:
        return ""
    first = items[0]
    return first.get("title_ko") or first.get("title") or first.get("repo", "")


def render(channel: str, date: datetime, payload: dict) -> tuple[str, str]:
    """Return (markdown, headline used for the filename)."""
    stamp = date.strftime("%Y-%m-%d")
    items = payload.get("items", [])
    headline = pick_headline(items)
    lines = [f"# {HEADERS[channel]} — {stamp}", ""]

    if channel == "geeknews":
        if not items:
            lines.append("해당 날짜에 확인된 신규 기술 항목 없음.")
        for item in items:
            title = _clean(item.get("title_ko") or item.get("title", ""))
            lines.append(f"- [{title}]({item['url']})")

    elif channel == "tech":
        if not items:
            lines.append("해당 날짜에 확인된 신규 글 없음.")
        current = None
        for item in items:
            if item.get("source") != current:
                current = item.get("source")
                lines += [f"## {current}", ""]
            title = _clean(item.get("title_ko") or item.get("title", ""))
            lines.append(f"### {title}")
            lines.append(f"원문: {item['url']}")
            lines.append("")
            lines.append(_bullets(item.get("bullets")))
            lines.append("")

    elif channel == "youtube":
        if not items:
            lines.append("해당 날짜에 확인된 신규 기술 영상 없음.")
        current = None
        for item in items:
            if item.get("source") != current:
                current = item.get("source")
                lines += [f"## {current}", ""]
            title = _clean(item.get("title_ko") or item.get("title", ""))
            lines.append(f"### {title}")
            lines.append(item["url"])
            lines.append("")
            lines.append(_bullets(item.get("bullets")))
            lines.append("")

    elif channel == "github":
        if not items:
            lines.append("해당 날짜에 확인된 Trending 스냅샷 없음.")
        for i, item in enumerate(items, start=1):
            if i > 1:
                lines.append("")
            lines += [f"## {i}. {item['repo']}", "", item["url"], ""]
            if item.get("language"):
                lines.append(f"- 언어: {item['language']}")
            if item.get("stars"):
                lines.append(f"- 이번 주 증가: {item['stars']}")
            lines.append(_bullets(item.get("bullets")))

    text = "\n".join(lines).rstrip() + "\n"
    return text, (headline or HEADERS[channel])


def write_channel(channel: str, date: datetime, payload: dict, root: Path = ROOT) -> Path:
    text, headline = render(channel, date, payload)
    path = output_path(channel, date, headline, root=root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path
