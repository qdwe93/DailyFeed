"""Shared helpers: KST dates, URL canonicalization, README parsing, slugs."""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
KST = timezone(timedelta(hours=9))

KST_WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]

TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {
    "fbclid", "gclid", "dclid", "msclkid", "igshid", "mc_cid", "mc_eid",
    "ref", "ref_src", "source", "spm", "yclid", "_hsenc", "_hsmi", "trk",
}

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)
UA_FEED = "DailyFeedBot/1.0 (+https://github.com/qdwe93/DailyFeed; RSS reader)"

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,ja;q=0.8,en;q=0.7,zh;q=0.6",
}

CHANNELS = ("geeknews", "tech", "youtube", "github")


def now_kst() -> datetime:
    return datetime.now(KST)


def parse_date(value: str) -> datetime:
    """Accept YYYY-MM-DD or YYYYMMDD, return midnight KST."""
    value = value.strip()
    if re.fullmatch(r"\d{8}", value):
        value = f"{value[:4]}-{value[4:6]}-{value[6:8]}"
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=KST)


def default_target_date() -> datetime:
    """Daily target = yesterday in KST (AGENT.md section 1)."""
    return (now_kst() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


def month_dir(d: datetime) -> str:
    """Folder name used under each channel: e.g. 2026년10월."""
    return f"{d.year}년{d.month}월"


def canonical(url: str) -> str:
    """Canonical form for duplicate detection across runs."""
    if not url:
        return ""
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    parts = urlsplit(url)
    host = parts.netloc.lower()
    for prefix in ("www.", "m.", "amp."):
        if host.startswith(prefix):
            host = host[len(prefix):]
    path = re.sub(r"/+$", "", parts.path) or "/"

    yt = youtube_id(url)
    if yt:
        return f"youtube:{yt}"

    query = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith(TRACKING_PREFIXES) and k.lower() not in TRACKING_KEYS
    ]
    query.sort()
    return urlunsplit(("https", host, path, urlencode(query), ""))


def youtube_id(url: str) -> str | None:
    if not url:
        return None
    parts = urlsplit(url)
    host = parts.netloc.lower()
    if host.endswith("youtu.be"):
        return parts.path.strip("/").split("/")[0] or None
    if "youtube.com" in host:
        if parts.path == "/watch":
            q = dict(parse_qsl(parts.query))
            return q.get("v")
        m = re.match(r"^/(?:shorts|embed|live)/([A-Za-z0-9_-]{6,})", parts.path)
        if m:
            return m.group(1)
    return None


_URL_RE = re.compile(r"https?://[^\s<>\"'\)\]]+")


def urls_in_markdown(text: str) -> list[str]:
    return _URL_RE.findall(text)


def slug(text: str, limit: int = 20) -> str:
    """Filesystem-safe slug, <= limit characters (Korean counts as one char)."""
    text = unicodedata.normalize("NFC", text or "")
    text = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", text)
    text = re.sub(r"[\\/:*?\"<>|#%&{}$!'@+`=~^]", " ", text)
    text = text.replace("·", "-").replace("—", "-").replace("–", "-")
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-{2,}", "-", text).strip("-.")
    if len(text) > limit:
        text = text[:limit].rstrip("-.")
    return text or "feed"


def read_json(path: Path, default=None):
    import json

    if not path.exists():
        return default
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data) -> None:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


# ---------------------------------------------------------------- README parsing


def _table_rows(section: str, need_url: bool = True):
    rows = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if any(set(c) <= set("-: ") for c in cells if c):
            continue
        rows.append(cells)
    if need_url:
        return [r for r in rows if any(c.startswith("http") for c in r)]
    return rows


def parse_readme(root: Path = ROOT) -> dict:
    """Sources come from README.md, which AGENT.md designates as canonical."""
    text = (root / "README.md").read_text(encoding="utf-8")

    tech_part = text.split("# Tech Feed 구독 소스", 1)[1]
    tech_part = tech_part.split("# YouTube Tech 모니터링 소스", 1)[0]
    tech = []
    for cells in _table_rows(tech_part):
        if len(cells) < 4:
            continue
        name, url = cells[1], cells[2]
        kind = cells[4].lower() if len(cells) > 4 else "rss"
        tech.append({"name": name, "url": url, "type": "page" if "웹페이지" in kind else "feed"})

    yt_part = text.split("# YouTube Tech 모니터링 소스", 1)[1]
    yt_part = yt_part.split("### YouTube 제외 원칙", 1)[0]
    channels = []
    for cells in _table_rows(yt_part):
        if len(cells) < 2:
            continue
        name, url = cells[0], cells[1]
        if name in ("채널", "Feed / Source"):
            continue
        channels.append({"name": name, "url": url})

    overrides_path = root / "pipeline" / "overrides.json"
    if overrides_path.exists():
        import json

        overrides = json.loads(overrides_path.read_text(encoding="utf-8")).get("feed_overrides", {})
        for source in tech:
            if source["name"] in overrides:
                source["url"] = overrides[source["name"]]
                source["overridden"] = True

    return {"tech": tech, "youtube": channels}


def existing_urls(root: Path = ROOT) -> dict[str, str]:
    """Map canonical URL -> file that already contains it."""
    index: dict[str, str] = {}
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(("pipeline/", "work/", "docs/")) or rel.startswith("."):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for url in urls_in_markdown(text):
            key = canonical(url)
            if key:
                index.setdefault(key, rel)
    return index


def channel_priority(name: str, tech_names: list[str]) -> int:
    """Lower is more important; used to pick the file's headline article."""
    official_first = ["OpenAI", "Anthropic", "Google DeepMind", "Google Official Blog"]
    for i, key in enumerate(official_first):
        if name.startswith(key):
            return i
    if name in tech_names:
        return 100 + tech_names.index(name)
    return 1000
