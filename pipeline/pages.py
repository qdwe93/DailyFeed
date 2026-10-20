"""Page sources without a feed (e.g. Anthropic Newsroom) via sitemap lastmod."""

from __future__ import annotations

import re
from datetime import datetime

from .fetch import get
from .util import KST


def sitemap_dated_links(site: str, path_contains: str, date: datetime) -> list[dict]:
    """Return [[name, url]] for sitemap entries whose lastmod falls on `date` (KST)."""
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
        if stamp.astimezone(KST).date() != date.date():
            continue
        slug = url.rstrip("/").split("/")[-1]
        found.append({"title": slug.replace("-", " ").strip().capitalize(), "url": url})
    return found
