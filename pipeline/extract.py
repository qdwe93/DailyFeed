"""Article body extraction (trafilatura) with RSS-summary fallback."""

from __future__ import annotations

import concurrent.futures as cf
import re

from .fetch import get
from .util import youtube_id


def extract_article(url: str, rss_summary: str = "", max_chars: int = 4000) -> dict:
    """Return {text, chars, method}. Never raises."""
    result = {"text": "", "chars": 0, "method": "none"}
    try:
        resp = get(url, retries=1)
        if "text/html" not in resp.headers.get("content-type", ""):
            raise ValueError("not html")
        import trafilatura

        text = trafilatura.extract(
            resp.text,
            include_comments=False,
            include_tables=True,
            favor_precision=True,
            deduplicate=True,
        )
        if text:
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
            if len(text) >= 200:
                result.update(text=text[:max_chars], chars=len(text), method="trafilatura")
                return result
            # Too thin (paywall / JS shell): prefer the feed body when available.
            if rss_summary and len(rss_summary) > len(text):
                result.update(text=rss_summary[:max_chars], chars=len(rss_summary), method="rss-fallback")
                return result
            result.update(text=text[:max_chars], chars=len(text), method="trafilatura-short")
            return result
    except Exception:  # noqa: BLE001 - fall back to RSS body
        pass
    if rss_summary and len(rss_summary) > 80:
        result.update(text=rss_summary[:max_chars], chars=len(rss_summary), method="rss")
    return result


def extract_many(items: list[dict], workers: int = 8, max_chars: int = 4000) -> list[dict]:
    def one(item: dict) -> dict:
        if youtube_id(item.get("url", "")):
            item = dict(item)
            item.setdefault("body", item.get("summary", "")[:max_chars])
            item["extract"] = {"method": "youtube-description", "chars": len(item["body"])}
            return item
        fetched = extract_article(item["url"], item.get("summary", ""), max_chars=max_chars)
        item = dict(item)
        item["body"] = fetched["text"]
        item["extract"] = {"method": fetched["method"], "chars": fetched["chars"]}
        return item

    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(one, items))
