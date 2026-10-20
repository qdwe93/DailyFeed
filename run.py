#!/usr/bin/env python3
"""DailyFeed orchestrator.

    python run.py doctor
    python run.py collect  --date 2026-10-20
    python run.py render   --date 2026-10-20 --publish
    python run.py weekly   [--date YYYY-MM-DD] [--publish]

`collect` is deterministic: RSS/YouTube/Trending -> work/<date>/candidates.json
plus a prompt bundle for the summarizing agent. The agent writes
work/<date>/summaries.json; `render` turns both into markdown and publishes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from pipeline import classify, extract, fetch, pages, publish, render
from pipeline.util import (
    CHANNELS,
    KST,
    ROOT,
    canonical,
    channel_priority,
    default_target_date,
    existing_urls,
    month_dir,
    now_kst,
    parse_date,
    parse_readme,
    urls_in_markdown,
    write_json,
)

WORK = ROOT / "work"

CHANNEL_LABEL = {
    "geeknews": "GeekNews",
    "tech": "Tech Feeds",
    "youtube": "YouTube Tech",
    "github": "GitHub Trending Weekly",
}


# --------------------------------------------------------------------- helpers


def _same_day(published: str | None, target: datetime) -> bool:
    if not published:
        return False
    try:
        return datetime.fromisoformat(published).astimezone(KST).date() == target.date()
    except ValueError:
        return False


def _existing_index(target: datetime) -> dict[str, str]:
    """URLs already recorded anywhere except the target date's own files."""
    stamp = target.strftime("%Y-%m-%d")
    compact = target.strftime("%Y%m%d")
    index: dict[str, str] = {}
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("pipeline/", "work/", "docs/")) or rel.startswith("."):
            continue
        if path.name.startswith((stamp, compact)):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for url in urls_in_markdown(text):
            key = canonical(url)
            if key:
                index.setdefault(key, rel)
    return index


def _dedupe(items: list[dict], index: dict[str, str]) -> tuple[list[dict], list[dict]]:
    seen: dict[str, str] = {}
    kept, dropped = [], []
    for item in items:
        key = item.get("canonical") or canonical(item.get("url", ""))
        if not key:
            dropped.append({"title": item.get("title", ""), "reason": "no-url"})
            continue
        if key in index:
            dropped.append({"title": item.get("title", ""), "reason": f"already in {index[key]}"})
            continue
        if key in seen:
            dropped.append({"title": item.get("title", ""), "reason": f"duplicate in run ({seen[key]})"})
            continue
        # Same source + same title = re-upload/short pair; keep the first.
        title_key = f"{item.get('source','')}|{' '.join(item.get('title','').lower().split())}"
        if title_key in seen:
            dropped.append({"title": item.get("title", ""), "reason": f"same title in run ({seen[title_key]})"})
            continue
        seen[key] = item.get("source", "")
        seen[title_key] = item.get("id", item.get("source", ""))
        kept.append(item)
    return kept, dropped


def _drop_stale_files(channel: str, target: datetime, keep: Path | None = None) -> list[Path]:
    folder = ROOT / channel / month_dir(target)
    if not folder.exists():
        return []
    removed = []
    stamp = target.strftime("%Y-%m-%d")
    for path in folder.glob(f"{stamp}_*.md"):
        if keep and path.resolve() == keep.resolve():
            continue
        path.unlink()
        removed.append(path)
    return removed


# --------------------------------------------------------------------- collect


def collect(args) -> int:
    target = parse_date(args.date) if args.date else default_target_date()
    channels = [c.strip() for c in args.channels.split(",")] if args.channels else ["geeknews", "tech", "youtube"]
    readme = parse_readme()
    index = _existing_index(target)
    date_dir = WORK / target.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)

    payload: dict = {
        "target_date": target.strftime("%Y-%m-%d"),
        "collected_at": now_kst().isoformat(),
        "channels": {},
        "sources": {},
        "dropped": {},
    }
    counts: dict[str, int] = {}

    # ---- GeekNews (feed #6 in README)
    if "geeknews" in channels:
        gn_src = next((s for s in readme["tech"] if s["name"] == "GeekNews"), None)
        items, dropped = [], []
        if gn_src:
            result = fetch.fetch_feed(gn_src)
            payload["sources"]["GeekNews"] = {"error": result["error"], "entries": len(result["entries"])}
            for entry in result["entries"]:
                if not _same_day(entry["published"], target):
                    continue
                items.append({**entry, "source": "GeekNews", "channel": "geeknews"})
            items, dup_dropped = _dedupe(items, index)
            items, non_tech = classify.filter_items(items)
            dropped += dup_dropped + non_tech
        items.sort(key=lambda i: i.get("published") or "")
        payload["channels"]["geeknews"] = {"items": items, "count": len(items)}
        payload["dropped"]["geeknews"] = dropped
        counts["geeknews"] = len(items)

    # ---- Tech feeds (all README sources except GeekNews)
    if "tech" in channels:
        sources = [s for s in readme["tech"] if s["name"] != "GeekNews"]
        feed_sources = [s for s in sources if s["type"] == "feed"]
        results = fetch.fetch_all(feed_sources)
        items, dropped = [], []
        for result in results:
            payload["sources"][result["source"]] = {
                "error": result["error"],
                "entries": len(result["entries"]),
            }
            for entry in result["entries"]:
                if not _same_day(entry["published"], target):
                    continue
                items.append({**entry, "source": result["source"], "channel": "tech"})
        for page_source in [s for s in sources if s["type"] == "page"]:
            links = pages.sitemap_dated_links(page_source["url"], "/news/", target)
            payload["sources"][page_source["name"]] = {"error": None, "entries": len(links)}
            for link in links:
                items.append(
                    {
                        "title": link["title"],
                        "url": link["url"],
                        "canonical": canonical(link["url"]),
                        "published": target.isoformat(),
                        "summary": "",
                        "source": page_source["name"],
                        "channel": "tech",
                    }
                )
        items, dup_dropped = _dedupe(items, index)
        dropped += dup_dropped
        if args.include_undated:
            undated = [i for i in items if not i.get("published")]
        order = {s["name"]: i for i, s in enumerate(readme["tech"])}
        items.sort(key=lambda i: (order.get(i["source"], 999), i.get("published") or ""))
        items = extract.extract_many(items, workers=args.workers)
        payload["channels"]["tech"] = {"items": items, "count": len(items)}
        payload["dropped"]["tech"] = dropped
        counts["tech"] = len(items)

    # ---- YouTube
    if "youtube" in channels:
        results = fetch.fetch_youtube(readme["youtube"])
        items, dropped = [], []
        for result in results:
            payload["sources"][f"YouTube:{result['source']}"] = {
                "error": result["error"],
                "entries": len(result["entries"]),
            }
            for entry in result["entries"]:
                if not _same_day(entry["published"], target):
                    continue
                items.append({**entry, "source": result["source"], "channel": "youtube"})
        items, dup_dropped = _dedupe(items, index)
        dropped += dup_dropped
        items.sort(key=lambda i: i.get("published") or "")
        items = extract.extract_many(items, workers=args.workers, max_chars=3000)
        payload["channels"]["youtube"] = {"items": items, "count": len(items)}
        payload["dropped"]["youtube"] = dropped
        counts["youtube"] = len(items)

    # ---- stable ids for the summarizer
    for channel, block in payload["channels"].items():
        for i, item in enumerate(block["items"], start=1):
            item["id"] = f"{channel}-{i}"

    write_json(date_dir / "candidates.json", payload)
    write_json(date_dir / "stats.json", {"counts": counts, "sources": payload["sources"]})
    write_prompt_bundle(date_dir, payload, target)
    print_summary(payload, target)
    return 0


def write_prompt_bundle(date_dir: Path, payload: dict, target: datetime) -> None:
    """One file the summarizing agent reads; keeps its context bounded."""
    lines = [
        f"# 요약 작업 — {target.strftime('%Y-%m-%d')} (KST)",
        "",
        f"candidates: {date_dir / 'candidates.json'}",
        f"출력 파일: {date_dir / 'summaries.json'}",
        "",
        "## 작성 규칙",
        "",
        "- tech/youtube: `title_ko`는 자연스러운 한국어 제목, `bullets`는 정확히 3줄(사실 위주, 마케팅 문구 금지).",
        "- geeknews: `title_ko`만 필요(불릿 없음). 이미 한국어면 그대로 둔다.",
        "- `id`는 아래 항목의 id를 그대로 쓴다. 항목을 임의로 추가/삭제하지 않는다.",
        "- 본문이 부실해 요약할 수 없으면 `\"skip\": true`와 `\"reason\"`을 넣는다.",
        "- 출력은 UTF-8 JSON만. 코드블록 없이 파일로 저장.",
        "",
        "## 출력 스키마",
        "",
        "```json",
        '{"date": "YYYY-MM-DD", "items": {"tech-1": {"title_ko": "...", "bullets": ["...","...","..."]}, '
        '"geeknews-1": {"title_ko": "..."}}}',
        "```",
        "",
    ]
    for channel in ("geeknews", "tech", "youtube"):
        block = payload["channels"].get(channel)
        if not block:
            continue
        lines += [f"## {CHANNEL_LABEL[channel]} ({block['count']}건)", ""]
        if not block["items"]:
            lines += ["(신규 항목 없음)", ""]
            continue
        for item in block["items"]:
            lines.append(f"### {item['id']} | {item['source']}")
            lines.append(f"제목: {item['title']}")
            if item.get("published"):
                lines.append(f"게시: {item['published']}")
            lines.append(f"URL: {item['url']}")
            body = (item.get("body") or item.get("summary") or "").strip()
            body = re.sub(r"\n{2,}", "\n", body)[:1500]
            if body:
                lines += ["본문:", body]
            lines.append("")
    (date_dir / "prompt.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def print_summary(payload: dict, target: datetime) -> None:
    print(f"target={target.strftime('%Y-%m-%d')}  kst_now={now_kst():%Y-%m-%d %H:%M}")
    for channel, block in payload["channels"].items():
        dropped = payload["dropped"].get(channel, [])
        errors = [
            f"{name}: {info['error']}"
            for name, info in payload["sources"].items()
            if info["error"] and (channel == "geeknews" or name.startswith("YouTube:") == (channel == "youtube"))
        ]
        print(f"- {channel:9} new={block['count']:3}  dropped={len(dropped):3}  source_errors={len(errors)}")
        for err in errors[:6]:
            print(f"    ! {err}")
    print(f"work dir: {WORK / target.strftime('%Y-%m-%d')}")


# ---------------------------------------------------------------------- render


def load_summaries(date_dir: Path) -> dict:
    data = {}
    path = date_dir / "summaries.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("items", data if isinstance(data, dict) else {})


def render_cmd(args) -> int:
    target = parse_date(args.date) if args.date else default_target_date()
    date_dir = WORK / target.strftime("%Y-%m-%d")
    candidates = json.loads((date_dir / "candidates.json").read_text(encoding="utf-8"))
    summaries = load_summaries(date_dir)
    published_paths: list[Path] = []
    stamp = target.strftime("%Y-%m-%d")

    for channel in candidates["channels"]:
        block = candidates["channels"][channel]
        items = []
        for item in block["items"]:
            summary = summaries.get(item["id"], {})
            if summary.get("skip"):
                continue
            merged = dict(item)
            merged["title_ko"] = summary.get("title_ko") or item.get("title")
            merged["bullets"] = summary.get("bullets") or []
            items.append(merged)
        path = render.write_channel(channel, target, {"items": items})
        _drop_stale_files(channel, target, keep=path)
        published_paths.append(path)
        print(f"wrote {path.relative_to(ROOT)}  items={len(items)}")

    if args.publish:
        messages = {
            "geeknews": f"daily: add {stamp} GeekNews",
            "tech": f"daily: add {stamp} tech feeds",
            "youtube": f"daily: add {stamp.replace('-', '')} YouTube tech",
            "github": f"weekly: add {stamp.replace('-', '')} GitHub trending",
        }
        message = args.message or "; ".join(messages[c] for c in candidates["channels"] if c in messages)
        result = publish.publish(published_paths, message, push=not args.no_push)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("error"):
            return 1
    return 0


# ---------------------------------------------------------------------- weekly


def weekly(args) -> int:
    target = parse_date(args.date) if args.date else now_kst().replace(hour=0, minute=0, second=0, microsecond=0)
    date_dir = WORK / f"weekly-{target.strftime('%Y-%m-%d')}"
    date_dir.mkdir(parents=True, exist_ok=True)
    result = fetch.fetch_trending(limit=args.limit)
    payload = {
        "target_date": target.strftime("%Y-%m-%d"),
        "collected_at": now_kst().isoformat(),
        "source": result["source"],
        "error": result["error"],
        "channels": {"github": {"items": result["entries"], "count": len(result["entries"])}},
        "sources": {"github.com/trending": {"error": result["error"], "entries": len(result["entries"])}},
        "dropped": {},
    }
    for i, item in enumerate(result["entries"], start=1):
        item["id"] = f"github-{i}"
        item["channel"] = "github"
    write_json(date_dir / "candidates.json", payload)
    write_weekly_prompt(date_dir, result["entries"], target)
    print(f"trending entries={len(result['entries'])} error={result['error']}")
    print(f"work dir: {date_dir}")
    return 0


def write_weekly_prompt(date_dir: Path, entries: list[dict], target: datetime) -> None:
    lines = [
        f"# GitHub Trending Weekly 요약 — {target.strftime('%Y-%m-%d')}",
        "",
        f"출력 파일: {date_dir / 'summaries.json'}",
        "",
        "규칙: 각 항목마다 `title_ko`(없어도 됨), `bullets` 2줄 — 무엇을 하는 프로젝트인지, 핵심 특징.",
        "README/Description을 확인해 실제 용도를 파악한다. 확인되지 않은 유행 이유는 쓰지 않는다.",
        "",
        "```json",
        '{"date": "YYYY-MM-DD", "items": {"github-1": {"bullets": ["...", "..."]}}}',
        "```",
        "",
    ]
    for item in entries:
        lines += [
            f"### {item['id']} | {item['repo']}",
            f"URL: {item['url']}",
            f"언어: {item.get('language') or '-'} | 증가: {item.get('stars') or '-'}",
            f"설명: {item.get('description') or '-'}",
            "",
        ]
    (date_dir / "prompt.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def render_weekly(args) -> int:
    target = parse_date(args.date) if args.date else now_kst().replace(hour=0, minute=0, second=0, microsecond=0)
    date_dir = WORK / f"weekly-{target.strftime('%Y-%m-%d')}"
    candidates = json.loads((date_dir / "candidates.json").read_text(encoding="utf-8"))
    summaries = load_summaries(date_dir)
    items = []
    for item in candidates["channels"]["github"]["items"]:
        merged = dict(item)
        summary = summaries.get(item["id"], {})
        merged["bullets"] = summary.get("bullets") or []
        items.append(merged)
    path = render.write_channel("github", target, {"items": items})
    _drop_stale_files("github", target, keep=path)
    print(f"wrote {path.relative_to(ROOT)} items={len(items)}")
    if args.publish:
        message = f"weekly: add {target.strftime('%Y%m%d')} GitHub trending"
        result = publish.publish([path], message, push=not args.no_push)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("error"):
            return 1
    return 0


# ---------------------------------------------------------------------- doctor


def doctor(_args) -> int:
    readme = parse_readme()
    info = publish.status()
    print(f"repo={info['is_repo']} branch={info['branch']} remote={info['remote']}")
    print(f"dirty_files={len(info['dirty'])}")
    print(f"tech_sources={len(readme['tech'])} youtube_channels={len(readme['youtube'])}")
    results = fetch.fetch_all(readme["tech"], workers=10)
    bad = [(r["source"], r["error"]) for r in results if r["error"] or not r["entries"]]
    print(f"feed_ok={len(results) - len(bad)} feed_bad={len(bad)}")
    for name, err in bad:
        print(f"  ! {name}: {err}")
    return 0


def daily_lite(args) -> int:
    """No-LLM daily path: GeekNews titles are already Korean, so publish without summaries."""
    target = parse_date(args.date) if args.date else default_target_date()
    existing = list((ROOT / "geeknews" / month_dir(target)).glob(f"{target:%Y-%m-%d}_*.md"))
    if existing:
        print(f"skip: {existing[0].relative_to(ROOT)} already exists (lite mode never overwrites curated files)")
        return 0
    collect_args = argparse.Namespace(
        date=target.strftime("%Y-%m-%d"),
        channels="geeknews",
        workers=args.workers,
        include_undated=False,
    )
    collect(collect_args)
    render_args = argparse.Namespace(
        date=target.strftime("%Y-%m-%d"),
        publish=not args.no_publish,
        no_push=False,
        message=f"daily: add {target:%Y-%m-%d} GeekNews",
    )
    return render_cmd(render_args)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DailyFeed pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_collect = sub.add_parser("collect", help="fetch sources into work/<date>/")
    p_collect.add_argument("--date")
    p_collect.add_argument("--channels", default="geeknews,tech,youtube")
    p_collect.add_argument("--workers", type=int, default=8)
    p_collect.add_argument("--include-undated", action="store_true")
    p_collect.set_defaults(func=collect)

    p_render = sub.add_parser("render", help="write markdown from candidates + summaries")
    p_render.add_argument("--date")
    p_render.add_argument("--publish", action="store_true")
    p_render.add_argument("--no-push", action="store_true")
    p_render.add_argument("--message")
    p_render.set_defaults(func=render_cmd)

    p_weekly = sub.add_parser("weekly", help="collect GitHub weekly trending")
    p_weekly.add_argument("--date")
    p_weekly.add_argument("--limit", type=int, default=10)
    p_weekly.set_defaults(func=weekly)

    p_render_weekly = sub.add_parser("render-weekly", help="write weekly markdown and publish")
    p_render_weekly.add_argument("--date")
    p_render_weekly.add_argument("--publish", action="store_true")
    p_render_weekly.add_argument("--no-push", action="store_true")
    p_render_weekly.set_defaults(func=render_weekly)

    p_doctor = sub.add_parser("doctor", help="check repo + source reachability")
    p_doctor.set_defaults(func=doctor)

    p_lite = sub.add_parser("daily-lite", help="GeekNews only, no LLM needed")
    p_lite.add_argument("--date")
    p_lite.add_argument("--workers", type=int, default=8)
    p_lite.add_argument("--no-publish", action="store_true")
    p_lite.set_defaults(func=daily_lite)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
