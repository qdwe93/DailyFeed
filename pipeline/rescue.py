"""Failure diagnosis and fallback fetching.

When a direct request fails, the cause is classified first (DNS, Cloudflare block, 404, parse
error...) and then the fetch is retried with progressively heavier tools:

    feed autodiscovery (404/parse only) -> crawl4ai -> Apify web-fetch -> Playwright -> opencode agent

Every attempt is recorded so the run log shows what was tried and why it failed.
"""

from __future__ import annotations

import asyncio
import os
import re
import time
from datetime import datetime
from urllib.parse import urljoin, urlsplit

import httpx

from . import llm
from .fetch import get, parse_feed
from .util import canonical, in_window

os.environ.setdefault("CRAWL4AI_NO_CLOUD_NOTICE", "1")

APIFY_MAX_CALLS = 20  # per run; web-fetch costs about $0.0016 a call on the free plan
_apify_calls = 0

CAUSES = {
    "dns": "DNS 조회 실패 (도메인 소멸 또는 네트워크 문제)",
    "connect": "연결 실패 (네트워크 또는 서버 다운)",
    "timeout": "응답 시간 초과",
    "tls": "TLS/인증서 오류",
    "blocked-cloudflare": "Cloudflare 봇 차단 (403/503 challenge)",
    "forbidden": "접근 거부 (403)",
    "not-found": "피드 주소 없음 (404/410) — 피드 URL 변경 가능성",
    "rate-limited": "요청 제한 (429)",
    "server-error": "서버 오류 (5xx)",
    "parse-error": "응답은 왔지만 RSS/Atom으로 해석 불가 (HTML 반환 등)",
    "empty-feed": "피드에 항목이 없음",
    "unknown": "원인 미상",
}


def diagnose(result: dict) -> str:
    """Classify a fetch_feed result into one of CAUSES."""
    error = (result.get("error") or "").lower()
    status = result.get("status")
    if result.get("blocked_by") == "cloudflare" and status in (403, 503, None):
        return "blocked-cloudflare"
    if status == 403:
        return "forbidden"
    if status in (404, 410):
        return "not-found"
    if status == 429:
        return "rate-limited"
    if status and status >= 500:
        return "server-error"
    if "getaddrinfo" in error or "name or service" in error or "nodename" in error:
        return "dns"
    if "timeout" in error:
        return "timeout"
    if "ssl" in error or "certificate" in error:
        return "tls"
    if "connecterror" in error or "connection" in error:
        return "connect"
    if error.startswith("parse"):
        return "parse-error"
    if "empty feed" in error:
        return "empty-feed"
    return "unknown"


# ------------------------------------------------------------------ raw fetchers


def _unwrap_browser_text(page: str) -> str:
    """Chrome shows XML/plain text inside a viewer; recover the original document."""
    if re.search(r"<(rss|feed|rdf:RDF)[\s>]", page[:5000]) and "xml-viewer-style" not in page[:3000]:
        return page
    match = re.search(r"<pre[^>]*>(.*?)</pre>", page, flags=re.S)
    if match:
        import html as htmlmod

        return htmlmod.unescape(match.group(1))
    return page


def via_crawl4ai(url: str, markdown: bool = False) -> str:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

    async def go():
        async with AsyncWebCrawler(config=BrowserConfig(headless=True, verbose=False)) as crawler:
            res = await crawler.arun(url, config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS, verbose=False))
            if not res.success:
                raise RuntimeError(f"crawl4ai: {res.error_message or res.status_code}")
            if markdown:
                md = res.markdown
                return str(getattr(md, "raw_markdown", md) or "")
            return res.html or ""

    page = asyncio.run(go())
    return page if markdown else _unwrap_browser_text(page)


def via_apify(url: str, markdown: bool = False) -> str:
    global _apify_calls
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise RuntimeError("APIFY_TOKEN not set")
    if _apify_calls >= APIFY_MAX_CALLS:
        raise RuntimeError(f"apify call budget ({APIFY_MAX_CALLS}/run) used up")
    _apify_calls += 1
    fmt = "markdown" if markdown else "raw"
    resp = httpx.post(
        "https://api.apify.com/v2/acts/apify~web-fetch/run-sync-get-dataset-items?timeout=150",
        headers={"Authorization": f"Bearer {token}"},
        json={"url": url, "formats": [fmt]},
        timeout=180,
    )
    resp.raise_for_status()
    items = resp.json()
    item = items[0] if isinstance(items, list) and items else {}
    status = (item.get("fetch") or {}).get("httpStatusCode")
    if status and status >= 400:
        raise RuntimeError(f"apify: target returned {status}")
    content = item.get(fmt) or ""
    if not content:
        raise RuntimeError("apify: empty result")
    return content


def via_playwright(url: str, markdown: bool = False) -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(locale="ko-KR")
            resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
            if "just a moment" in (page.title() or "").lower():
                page.wait_for_timeout(8000)  # let a JS challenge settle, then re-read
                resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
            if resp is None or resp.status >= 400:
                raise RuntimeError(f"playwright: HTTP {resp.status if resp else '?'}")
            if markdown:
                return page.inner_text("body")
            return resp.body().decode("utf-8", errors="replace")
        finally:
            browser.close()


FETCHERS = [("crawl4ai", via_crawl4ai), ("apify", via_apify), ("playwright", via_playwright)]


def _attempt(method: str, fn, *args) -> tuple[object, dict]:
    started = time.monotonic()
    record = {"method": method, "ok": False, "error": None, "seconds": 0.0}
    try:
        value = fn(*args)
        record["ok"] = True
        return value, record
    except Exception as exc:  # noqa: BLE001 - every failure is data for the log
        record["error"] = f"{type(exc).__name__}: {exc}"[:200]
        return None, record
    finally:
        record["seconds"] = round(time.monotonic() - started, 1)


# ------------------------------------------------------------------ feed rescue


def discover_feed(url: str) -> str | None:
    """Look for <link rel=alternate type=rss/atom> on the site home page."""
    parts = urlsplit(url)
    home = f"{parts.scheme}://{parts.netloc}/"
    page = get(home, retries=1).text
    for match in re.finditer(r"<link[^>]+>", page, flags=re.I):
        tag = match.group(0)
        if "alternate" in tag.lower() and re.search(r"(rss|atom)\+xml", tag, flags=re.I):
            href = re.search(r'href=["\']([^"\']+)', tag)
            if href:
                found = urljoin(home, href.group(1))
                if canonical(found) != canonical(url):
                    return found
    return None


def _base_domain(url: str) -> str:
    host = urlsplit(url).netloc.lower().split(":")[0]
    return ".".join(host.split(".")[-2:])


def via_agent(source: dict, start: datetime, end: datetime, models: list[str]) -> list[dict]:
    """Last resort: let an opencode agent search the web (and its MCP tools) for the posts."""
    if not models:
        raise RuntimeError("no working model for agent search")
    prompt = (
        "웹 검색 도구(websearch/webfetch, 가능하면 playwright·apify MCP)를 사용해 아래 소스에 "
        "기간 내 게시된 글을 찾아라. 직접 RSS 요청은 차단되어 있다.\n"
        f"소스: {source['name']}\n피드/사이트: {source['url']}\n"
        f"기간: {start.isoformat()} 초과 ~ {end.isoformat()} 이하 (KST)\n"
        "게시 시각을 원문 페이지에서 확인한 글만 넣는다. 확인 못 한 글은 넣지 않는다. 없으면 빈 배열.\n"
        '설명 없이 JSON 하나만 출력: {"items": [{"title": "...", "url": "원문 URL", '
        '"published": "2026-01-01T10:00:00+09:00", "summary": "본문 핵심 3~5문장"}]}'
    )
    reply = llm.run(models[0], prompt, timeout=420, agent=True)
    if reply["error"]:
        raise RuntimeError(f"agent: {reply['error']}")
    data = llm.extract_json(reply["text"])
    rows = data.get("items", []) if isinstance(data, dict) else []
    medium = "medium.com" in source["url"]
    entries = []
    for row in rows:
        url = str(row.get("url") or "")
        if not url.startswith("http"):
            continue
        if not medium and _base_domain(url) != _base_domain(source["url"]):
            continue  # agent wandered to another site
        if not in_window(row.get("published"), start, end):
            continue
        entries.append(
            {
                "title": str(row.get("title") or "").strip(),
                "url": url,
                "canonical": canonical(url),
                "published": row.get("published"),
                "summary": str(row.get("summary") or "")[:3000],
                "author": "",
                "rescued_by": "agent-websearch",
            }
        )
    return entries


def rescue_feed(result: dict, start: datetime, end: datetime, models: list[str], allow_agent: bool = True) -> dict:
    """Try every fallback for a failed feed. Returns {entries, cause, attempts, method, discovered_url}."""
    source = {"name": result["source"], "url": result["url"]}
    cause = diagnose(result)
    out = {"cause": cause, "cause_ko": CAUSES[cause], "attempts": [], "entries": [], "method": None, "discovered_url": None}

    targets = [result["url"]]
    if cause in ("not-found", "parse-error", "empty-feed"):
        found, record = _attempt("autodiscover", discover_feed, result["url"])
        record["ok"] = bool(found)
        if found:
            record["found"] = found
            targets.insert(0, found)
        out["attempts"].append(record)

    for target in targets:
        for method, fn in FETCHERS:
            raw, record = _attempt(method, fn, target)
            record["url"] = target
            if raw:
                entries, err = parse_feed(raw)
                if err:
                    record.update(ok=False, error=err)
                else:
                    record["entries"] = len(entries)
                    out.update(entries=entries, method=method)
                    if target != result["url"]:
                        out["discovered_url"] = target
                    out["attempts"].append(record)
                    return out
            out["attempts"].append(record)

    if allow_agent:
        entries, record = _attempt("agent-websearch", via_agent, source, start, end, models)
        if entries is not None:
            record["entries"] = len(entries)
            out.update(entries=entries, method="agent-websearch")
        out["attempts"].append(record)
    return out


def rescue_html(url: str) -> tuple[str | None, list[dict]]:
    """Fetch an HTML page (e.g. GitHub Trending) through the browser-based fetchers."""
    attempts = []
    for method, fn in FETCHERS:
        page, record = _attempt(method, fn, url)
        attempts.append(record)
        if page:
            return page, attempts
    return None, attempts


def rescue_body(url: str) -> tuple[str, str | None, list[dict]]:
    """Article text when trafilatura got nothing (JS shell, block). Returns (text, method, attempts)."""
    attempts = []
    for method, fn in FETCHERS:
        text, record = _attempt(method, fn, url, True)
        text = re.sub(r"\n{3,}", "\n\n", text or "").strip()
        if text and len(text) >= 300:
            attempts.append(record)
            return text, method, attempts
        if record["ok"]:
            record.update(ok=False, error=f"too short ({len(text)} chars)")
        attempts.append(record)
    return "", None, attempts
