"""HTTP + feed collection with retries, UA fallback, and per-source error capture."""

from __future__ import annotations

import concurrent.futures as cf
import html
import re
import time
from datetime import datetime, timezone

import feedparser
import httpx

from .util import HEADERS, KST, UA, UA_FEED, canonical, youtube_id

TIMEOUT = httpx.Timeout(25.0, connect=15.0)


def _client() -> httpx.Client:
    return httpx.Client(headers=HEADERS, timeout=TIMEOUT, follow_redirects=True, http2=False)


def get(url: str, ua: str | None = None, retries: int = 2) -> httpx.Response:
    last: Exception | None = None
    with _client() as client:
        for attempt in range(retries + 1):
            headers = {"User-Agent": ua or UA}
            try:
                resp = client.get(url, headers=headers)
                if resp.status_code in (403, 429) and attempt == 0:
                    time.sleep(1.0)
                    continue
                resp.raise_for_status()
                return resp
            except Exception as exc:  # noqa: BLE001 - surfaced by caller
                last = exc
                time.sleep(0.6 * (attempt + 1))
    raise last if last else RuntimeError("request failed")


def _strip_html(raw: str) -> str:
    if not raw:
        return ""
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"<br\s*/?>|</p>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()


def entry_datetime(entry) -> datetime | None:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        value = entry.get(key)
        if value:
            try:
                return datetime(*value[:6], tzinfo=timezone.utc).astimezone(KST)
            except (TypeError, ValueError):
                continue
    return None


def _blocked_by(resp: httpx.Response | None) -> str | None:
    if resp is None:
        return None
    server = resp.headers.get("server", "").lower()
    if "cf-ray" in resp.headers or "cloudflare" in server or "just a moment" in resp.text[:2000].lower():
        return "cloudflare"
    return server or None


def fetch_feed(source: dict) -> dict:
    """Return {entries: [...], error: str|None, status, blocked_by}. Never raises."""
    out = {"source": source["name"], "url": source["url"], "entries": [], "error": None}
    content = None
    err = None
    for ua in (UA, UA_FEED):
        try:
            content = get(source["url"], ua=ua).content
            break
        except Exception as exc:  # noqa: BLE001
            err = f"{type(exc).__name__}: {exc}"[:200]
            resp = getattr(exc, "response", None)
            if resp is not None:
                out["status"] = resp.status_code
                out["blocked_by"] = _blocked_by(resp)
    if content is None:
        out["error"] = err or "no content"
        return out
    out["entries"], out["error"] = parse_feed(content)
    return out


def parse_feed(content: bytes | str) -> tuple[list[dict], str | None]:
    """Feed bytes -> normalized entries. Shared by the direct fetch and the rescue fetchers."""
    feed = feedparser.parse(content)
    if not feed.entries and feed.bozo:
        return [], f"parse: {type(feed.get('bozo_exception')).__name__}"
    if not feed.entries:
        return [], "empty feed"
    entries = []
    for entry in feed.entries:
        raw_link = entry.get("link") or ""
        vid = youtube_id(raw_link) or entry.get("yt_videoid")
        link = f"https://www.youtube.com/watch?v={vid}" if vid else raw_link
        summary = _strip_html(entry.get("summary") or "")
        body = ""
        if entry.get("content"):
            body = _strip_html(" ".join(c.get("value", "") for c in entry["content"]))
        entries.append(
            {
                "title": _strip_html(entry.get("title") or "").strip(),
                "url": link,
                "canonical": canonical(link),
                "published": entry_datetime(entry).isoformat() if entry_datetime(entry) else None,
                "summary": (body or summary)[:6000],
                "author": entry.get("author") or "",
            }
        )
    return entries, None


def fetch_all(sources: list[dict], workers: int = 10) -> list[dict]:
    if not sources:
        return []
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(fetch_feed, sources))


# ---------------------------------------------------------------- YouTube


def resolve_channel_id(url: str) -> str | None:
    if "/channel/" in url:
        return url.split("/channel/")[-1].split("/")[0].split("?")[0]
    resp = get(url)
    for pattern in (r'"channelId":"(UC[\w-]{22})"', r'channel/(UC[\w-]{22})'):
        match = re.search(pattern, resp.text)
        if match:
            return match.group(1)
    return None


def fetch_youtube(channels: list[dict]) -> list[dict]:
    def one(channel: dict) -> dict:
        out = {"source": channel["name"], "url": channel["url"], "entries": [], "error": None}
        try:
            cid = resolve_channel_id(channel["url"])
            if not cid:
                out["error"] = "channel id not found"
                return out
            feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
            out.update(fetch_feed({"name": channel["name"], "url": feed_url}))
            out["url"] = channel["url"]
            out["feed_url"] = feed_url
            out["channel_id"] = cid
        except Exception as exc:  # noqa: BLE001
            out["error"] = f"{type(exc).__name__}: {exc}"[:200]
        return out

    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(one, channels))


# ---------------------------------------------------------------- GitHub trending


def fetch_trending(limit: int = 10) -> dict:
    """Parse https://github.com/trending?since=weekly (official page only)."""
    out = {"entries": [], "error": None, "source": TRENDING_URL}
    try:
        resp = get(TRENDING_URL)
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"[:200]
        return out
    out["entries"] = parse_trending(resp.text, limit)
    if not out["entries"]:
        out["error"] = "no rows parsed"
    return out


TRENDING_URL = "https://github.com/trending?since=weekly"


def parse_trending(page: str, limit: int = 10) -> list[dict]:
    import lxml.html

    entries = []
    doc = lxml.html.fromstring(page)
    for article in doc.cssselect("article.Box-row")[:limit]:
        links = article.cssselect("h2 a")
        if not links:
            continue
        href = (links[0].get("href") or "").strip("/")
        if "/" not in href:
            continue
        language = article.cssselect("span[itemprop='programmingLanguage']")
        stars = article.cssselect("span.d-inline-block.float-sm-right")
        star_text = stars[0].text_content().strip() if stars else ""
        desc = article.cssselect("p")
        entries.append(
            {
                "repo": href,
                "url": f"https://github.com/{href}",
                "description": desc[0].text_content().strip() if desc else "",
                "language": language[0].text_content().strip() if language else "",
                "stars": re.sub(r"\s+", " ", star_text).strip(),
            }
        )
    return entries


def readme_excerpt(repo: str, limit: int = 1800) -> str:
    """README head for the weekly summarizer (AGENT.md 6: describe what it really does)."""
    for branch in ("HEAD", "main", "master"):
        try:
            text = get(f"https://raw.githubusercontent.com/{repo}/{branch}/README.md", retries=0).text
        except Exception:  # noqa: BLE001
            continue
        text = re.sub(r"<[^>]+>|!\[[^\]]*\]\([^)]*\)", " ", text)
        return re.sub(r"\n{2,}", "\n", text).strip()[:limit]
    return ""
