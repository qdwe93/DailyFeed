"""Page sources without a usable feed: sitemap lastmod (Anthropic) and GeekNews day archives."""

from __future__ import annotations

import html
import re
from datetime import datetime

from .fetch import get
from .util import KST


def sitemap_dated_links(site: str, path_contains: str, start: datetime, end: datetime) -> list[dict]:
    """Sitemap entries under `path_contains` whose lastmod falls in (start, end]."""
    found: list[dict] = []
    try:
        resp = get(site.rstrip("/") + "/sitemap.xml")
    except Exception:  # noqa: BLE001
        return found

    for match in re.finditer(
        r"<url>\s*<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]+)</lastmod>)?",
        resp.text,
    ):
        url, lastmod = match.group(1), match.group(2)
        if path_contains not in url or not lastmod:
            continue
        try:
            stamp = datetime.fromisoformat(lastmod.replace("Z", "+00:00"))
        except ValueError:
            continue
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=KST)
        if not (start < stamp <= end):
            continue
        slug = url.rstrip("/").split("/")[-1]
        found.append({"title": slug.replace("-", " ").strip().capitalize(), "url": url, "published": stamp.isoformat()})
    return found


_TOPIC_RE = re.compile(
    r"<div class='topic_row'.*?<h2 class='topic-title-heading'>(?P<title>.*?)</h2>"
    r".*?<a href='topic\?id=(?P<id>\d+)'[^>]*>(?P<desc>.*?)</a>"
    r".*?<time[^>]*datetime=\"(?P<when>[^\"]+)\"",
    flags=re.S,
)


def geeknews_past(day: datetime, max_pages: int = 10) -> list[dict]:
    """All topics GeekNews lists for one day (news.hada.io/past). Fills gaps the 50-item RSS lost."""
    entries: dict[str, dict] = {}
    for page in range(1, max_pages + 1):
        url = f"https://news.hada.io/past?day={day:%Y-%m-%d}" + (f"&page={page}" if page > 1 else "")
        text = get(url).text
        rows = list(_TOPIC_RE.finditer(text))
        new = 0
        for row in rows:
            link = f"https://news.hada.io/topic?id={row.group('id')}"
            if link in entries:
                continue
            new += 1
            entries[link] = {
                "title": html.unescape(re.sub(r"<[^>]+>", "", row.group("title"))).strip(),
                "url": link,
                "canonical": link,
                "published": row.group("when"),
                "summary": html.unescape(re.sub(r"<[^>]+>", "", row.group("desc"))).strip(),
                "author": "",
            }
        if not rows or not new:
            break
    return list(entries.values())
