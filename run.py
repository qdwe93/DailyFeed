#!/usr/bin/env python3
"""DailyFeed orchestrator.

    python run.py auto                         # scheduled entry point (Windows Task Scheduler, 12:00 KST)
    python run.py models                       # probe opencode free models -> models/available.md
    python run.py doctor
    python run.py collect  [--date 2026-10-20]
    python run.py summarize [--date 2026-10-21]
    python run.py render   [--date 2026-10-21] [--publish]
    python run.py weekly   [--date YYYY-MM-DD] [--publish]

`auto` does everything: model check -> collect everything newer than the previous run ->
rescue failed sources -> summarize with opencode free models -> render -> GitHub weekly when
due -> commit/push -> Discord/Slack notification. Output files are named by run date (KST).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

from pipeline import classify, extract, fetch, models, notify, pages, publish, render, rescue, state, summarize
from pipeline.util import (
    KST,
    ROOT,
    canonical,
    in_window,
    month_dir,
    now_kst,
    parse_date,
    parse_iso,
    parse_readme,
    read_json,
    urls_in_markdown,
    write_json,
)

WORK = ROOT / "work"
REPO_URL = "https://github.com/qdwe93/DailyFeed"
DAILY = list(state.DAILY_CHANNELS)

CHANNEL_LABEL = {
    "geeknews": "GeekNews",
    "tech": "Tech Feeds",
    "youtube": "YouTube Tech",
    "github": "GitHub Trending Weekly",
}


class NetworkDown(RuntimeError):
    pass


# --------------------------------------------------------------------- helpers


def _existing_index(target: datetime) -> dict[str, str]:
    """URLs already recorded anywhere except the target date's own files."""
    stamp = target.strftime("%Y-%m-%d")
    compact = target.strftime("%Y%m%d")
    index: dict[str, str] = {}
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("pipeline/", "work/", "docs/", "log/", "models/", ".venv/")) or rel.startswith("."):
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


def _same_date_files(channel: str, target: datetime) -> list[Path]:
    folder = ROOT / channel / month_dir(target)
    return sorted(folder.glob(f"{target:%Y-%m-%d}_*.md")) if folder.exists() else []


def _drop_stale_files(channel: str, target: datetime, keep: Path | None = None) -> list[Path]:
    removed = []
    for path in _same_date_files(channel, target):
        if keep and path.resolve() == keep.resolve():
            continue
        path.unlink()
        removed.append(path)
    return removed


def _midnight(d: datetime) -> datetime:
    return d.astimezone(KST).replace(hour=0, minute=0, second=0, microsecond=0)


def _fmt(d: datetime) -> str:
    return d.astimezone(KST).strftime("%m-%d %H:%M")


# --------------------------------------------------------------------- collect


def merge_with_previous(payload: dict, date_dir: Path) -> dict:
    """Union this run with an earlier collect of the same file date.

    A second run on the same day must not lose what the first run already published, and
    keeping the old ids lets summaries.json be reused. Previous items keep their ids.
    """
    previous = read_json(date_dir / "candidates.json")
    if not previous:
        return payload
    for channel, block in payload["channels"].items():
        old_block = previous.get("channels", {}).get(channel)
        if not old_block:
            continue
        old_items = old_block.get("items", [])
        if not old_items:
            continue
        seen = {item.get("canonical") for item in old_items}
        merged = list(old_items)
        for item in block["items"]:
            if item.get("canonical") in seen:
                continue
            merged.append(item)
        for i, item in enumerate(merged, start=1):
            item["id"] = f"{channel}-{i}"
        block["items"] = merged
        block["count"] = len(merged)
        snaps = payload.setdefault("merged_snapshots", [])
        if previous.get("collected_at") not in snaps:
            snaps.append(previous.get("collected_at"))
    return payload


def _apply_override(name: str, url: str) -> None:
    path = ROOT / "pipeline" / "overrides.json"
    data = read_json(path, default={}) or {}
    data.setdefault("feed_overrides", {})[name] = url
    write_json(path, data)


def _rescue_failed(results: list[dict], channel_of, starts, end, order, payload) -> None:
    """Diagnose each failed source and run the fallback chain; patch results in place."""
    for result in results:
        if not result["error"]:
            continue
        channel = channel_of(result)
        target = dict(result)
        if channel == "youtube":
            if not result.get("feed_url"):
                continue  # channel id unresolved; recorded as-is
            target["url"] = result["feed_url"]
        print(f"  rescue {result['source']}: {result['error'][:80]}")
        outcome = rescue.rescue_feed(target, starts[channel], end, order, allow_agent=channel != "youtube")
        record = {
            "source": result["source"],
            "channel": channel,
            "error": result["error"],
            "cause": outcome["cause"],
            "cause_ko": outcome["cause_ko"],
            "method": outcome["method"],
            "entries": len(outcome["entries"]),
            "attempts": outcome["attempts"],
        }
        if outcome["discovered_url"] and channel == "tech":
            _apply_override(result["source"], outcome["discovered_url"])
            record["override"] = outcome["discovered_url"]
        payload["rescues"].append(record)
        if outcome["method"]:
            result["entries"] = outcome["entries"]
            result["error"] = None
            result["rescued_by"] = outcome["method"]


def _geeknews_gap(entries: list[dict], start: datetime, end: datetime) -> tuple[list[dict], dict | None]:
    """RSS keeps ~50 items; if it does not reach back to `start`, read the day archives."""
    dated = [e for e in entries if e.get("published")]
    oldest = min((datetime.fromisoformat(e["published"]) for e in dated), default=None)
    if oldest is not None and oldest <= start:
        return entries, None
    have = {e["canonical"] for e in entries}
    added, days, error = 0, [], None
    day = _midnight(start)
    last_day = _midnight(oldest or end)
    while day <= last_day:
        try:
            for entry in pages.geeknews_past(day):
                if entry["canonical"] not in have:
                    entries.append(entry)
                    have.add(entry["canonical"])
                    added += 1
        except Exception as exc:  # noqa: BLE001
            error = f"{day:%Y-%m-%d}: {type(exc).__name__}: {exc}"[:200]
        days.append(f"{day:%Y-%m-%d}")
        day += timedelta(days=1)
    return entries, {"days": days, "added": added, "error": error}


def collect_window(
    channels: list[str],
    starts: dict[str, datetime],
    end: datetime,
    file_date: datetime,
    workers: int = 8,
    fresh: bool = False,
    order: list[str] | None = None,
    rescue_on: bool = True,
    source_starts: dict[str, datetime] | None = None,
) -> dict:
    """Collect items published in (starts[channel], end] into work/<file_date>/.

    source_starts lets a source that failed in earlier runs reach back to when it first failed.
    """
    source_starts = source_starts or {}

    def start_for(key: str, channel: str) -> datetime:
        return min(starts[channel], source_starts.get(key, starts[channel]))

    readme = parse_readme()
    index = _existing_index(file_date)
    date_dir = WORK / file_date.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    payload: dict = {
        "target_date": file_date.strftime("%Y-%m-%d"),
        "collected_at": now_kst().isoformat(timespec="seconds"),
        "window": {c: [starts[c].isoformat(), end.isoformat()] for c in channels},
        "channels": {},
        "sources": {},
        "dropped": {},
        "rescues": [],
    }

    feeds = [s for s in readme["tech"] if s["type"] == "feed"]
    feeds = [s for s in feeds if ("geeknews" in channels if s["name"] == "GeekNews" else "tech" in channels)]
    results = fetch.fetch_all(feeds)
    yt_results = fetch.fetch_youtube(readme["youtube"]) if "youtube" in channels else []

    everything = results + yt_results
    failed = [r for r in everything if r["error"]]
    network = [r for r in failed if rescue.diagnose(r) in ("dns", "connect", "timeout")]
    if len(everything) >= 5 and len(network) > len(everything) * 0.6:
        raise NetworkDown(f"{len(network)}/{len(everything)} sources unreachable (dns/connect) — network down?")

    def channel_of(result: dict) -> str:
        if result in yt_results:
            return "youtube"
        return "geeknews" if result["source"] == "GeekNews" else "tech"

    if rescue_on and failed:
        _rescue_failed(everything, channel_of, starts, end, order or [], payload)

    for result in everything:
        key = f"YouTube:{result['source']}" if result in yt_results else result["source"]
        payload["sources"][key] = {
            "error": result["error"],
            "entries": len(result["entries"]),
            **({"rescued_by": result["rescued_by"]} if result.get("rescued_by") else {}),
        }

    counts: dict[str, int] = {}

    # ---- GeekNews
    if "geeknews" in channels:
        gn = next((r for r in results if r["source"] == "GeekNews"), {"entries": []})
        entries, gap = _geeknews_gap(list(gn["entries"]), starts["geeknews"], end)
        if gap:
            payload["sources"]["GeekNews (지난 소식 페이지)"] = {"error": gap["error"], "entries": gap["added"], "days": gap["days"]}
        items = [
            {**e, "source": "GeekNews", "channel": "geeknews"}
            for e in entries
            if in_window(e["published"], starts["geeknews"], end)
        ]
        items, dup_dropped = _dedupe(items, index)
        items, non_tech = classify.filter_items(items)
        items.sort(key=lambda i: i.get("published") or "")
        payload["channels"]["geeknews"] = {"items": items, "count": len(items)}
        payload["dropped"]["geeknews"] = dup_dropped + non_tech
        counts["geeknews"] = len(items)

    # ---- Tech feeds (all README sources except GeekNews)
    if "tech" in channels:
        start = starts["tech"]
        items = []
        for result in results:
            if result["source"] == "GeekNews":
                continue
            for entry in result["entries"]:
                if in_window(entry["published"], start_for(result["source"], "tech"), end):
                    items.append({**entry, "source": result["source"], "channel": "tech"})
        for page_source in [s for s in readme["tech"] if s["type"] == "page"]:
            links = pages.sitemap_dated_links(page_source["url"], "/news/", start, end)
            payload["sources"][page_source["name"]] = {"error": None, "entries": len(links)}
            for link in links:
                items.append(
                    {
                        "title": link["title"],
                        "url": link["url"],
                        "canonical": canonical(link["url"]),
                        "published": link["published"],
                        "summary": "",
                        "source": page_source["name"],
                        "channel": "tech",
                    }
                )
        items, dropped = _dedupe(items, index)
        order_idx = {s["name"]: i for i, s in enumerate(readme["tech"])}
        items.sort(key=lambda i: (order_idx.get(i["source"], 999), i.get("published") or ""))
        items = extract.extract_many(items, workers=workers)
        for item in items:
            # trafilatura got nothing usable (JS shell / block): try the browser-based fetchers.
            if item["extract"]["chars"] >= 200 or item["extract"]["method"].startswith("rss"):
                continue
            text, method, attempts = rescue.rescue_body(item["url"])
            if text:
                item["body"] = text[:4000]
                item["extract"] = {"method": method, "chars": len(text)}
            payload["rescues"].append(
                {"source": item["source"], "channel": "tech", "error": f"본문 추출 실패: {item['url']}",
                 "cause": "body", "cause_ko": "본문 추출 실패 (JS 렌더링/차단)", "method": method,
                 "entries": 1 if text else 0, "attempts": attempts}
            )
        payload["channels"]["tech"] = {"items": items, "count": len(items)}
        payload["dropped"]["tech"] = dropped
        counts["tech"] = len(items)

    # ---- YouTube
    if "youtube" in channels:
        items = []
        for result in yt_results:
            for entry in result["entries"]:
                if in_window(entry["published"], start_for(f"YouTube:{result['source']}", "youtube"), end):
                    items.append({**entry, "source": result["source"], "channel": "youtube"})
        items, dropped = _dedupe(items, index)
        items.sort(key=lambda i: i.get("published") or "")
        items = extract.extract_many(items, workers=workers, max_chars=3000)
        payload["channels"]["youtube"] = {"items": items, "count": len(items)}
        payload["dropped"]["youtube"] = dropped
        counts["youtube"] = len(items)

    for channel, block in payload["channels"].items():
        for i, item in enumerate(block["items"], start=1):
            item["id"] = f"{channel}-{i}"

    if not fresh:
        payload = merge_with_previous(payload, date_dir)

    write_json(date_dir / "candidates.json", payload)
    write_json(date_dir / "stats.json", {"counts": counts, "sources": payload["sources"], "rescues": payload["rescues"]})
    write_prompt_bundle(date_dir, payload, file_date)
    print_summary(payload, file_date)
    return payload


def collect(args) -> int:
    channels = [c.strip() for c in args.channels.split(",")]
    if args.date:
        # Legacy calendar-day mode: items published on that KST day, file named by that day.
        day = parse_date(args.date)
        starts = {c: day - timedelta(microseconds=1) for c in channels}
        end, file_date = day + timedelta(days=1) - timedelta(microseconds=1), day
    else:
        st = state.load()
        end = now_kst().replace(microsecond=0)
        starts = {c: state.window_start(st, c, end) for c in channels}
        file_date = _midnight(end)
    collect_window(channels, starts, end, file_date, workers=args.workers, fresh=args.fresh, rescue_on=not args.no_rescue)
    return 0


def write_prompt_bundle(date_dir: Path, payload: dict, target: datetime) -> None:
    """Human-readable view of the candidates (the automated path builds its own prompts)."""
    lines = [f"# 수집 후보 — {target.strftime('%Y-%m-%d')} (KST)", ""]
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
    print(f"file_date={target.strftime('%Y-%m-%d')}  kst_now={now_kst():%Y-%m-%d %H:%M}")
    for channel, block in payload["channels"].items():
        dropped = payload["dropped"].get(channel, [])
        print(f"- {channel:9} new={block['count']:3}  dropped={len(dropped):3}")
    for rec in payload.get("rescues", []):
        print(f"    ! {rec['source']}: {rec['cause']} -> {rec['method'] or 'unrecovered'}")
    print(f"work dir: {WORK / target.strftime('%Y-%m-%d')}")


# ---------------------------------------------------------------------- render


def load_summaries(date_dir: Path) -> dict:
    data = {}
    path = date_dir / "summaries.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("items", data if isinstance(data, dict) else {})


def render_channels(date_dir: Path, file_date: datetime, channels: list[str]) -> tuple[list[Path], list[Path], list[str]]:
    """Write markdown for `channels`. Returns (written, removed, warnings)."""
    candidates = json.loads((date_dir / "candidates.json").read_text(encoding="utf-8"))
    summaries = load_summaries(date_dir)
    written, removed, warnings = [], [], []
    for channel in channels:
        block = candidates["channels"].get(channel)
        if block is None:
            continue
        items = []
        for item in block["items"]:
            summary = summaries.get(item["id"], {})
            if summary.get("skip"):
                continue
            merged = dict(item)
            merged["title_ko"] = summary.get("title_ko") or item.get("title")
            merged["bullets"] = summary.get("bullets") or []
            items.append(merged)
        # Guard: never let a rerun silently drop links an earlier run already published today.
        new_urls = {canonical(i["url"]) for i in items}
        lost = set()
        for path in _same_date_files(channel, file_date):
            lost |= {canonical(u) for u in urls_in_markdown(path.read_text(encoding="utf-8"))} - new_urls
        lost.discard("")
        if lost:
            warnings.append(f"{channel}: 기존 {file_date:%Y-%m-%d} 파일의 링크 {len(lost)}개가 새 결과에 없어 덮어쓰지 않음")
            continue
        path = render.write_channel(channel, file_date, {"items": items})
        removed += _drop_stale_files(channel, file_date, keep=path)
        written.append(path)
        print(f"wrote {path.relative_to(ROOT)}  items={len(items)}")
    return written, removed, warnings


def render_cmd(args) -> int:
    file_date = parse_date(args.date) if args.date else _midnight(now_kst())
    date_dir = WORK / file_date.strftime("%Y-%m-%d")
    candidates = read_json(date_dir / "candidates.json")
    written, removed, warnings = render_channels(date_dir, file_date, list(candidates["channels"]))
    for warning in warnings:
        print(f"! {warning}")
    if args.publish:
        message = args.message or f"daily: {file_date:%Y-%m-%d} " + ", ".join(
            f"{c} {candidates['channels'][c]['count']}" for c in candidates["channels"]
        )
        result = publish.publish_outputs(message, push=not args.no_push)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("error"):
            return 1
    return 0


def summarize_cmd(args) -> int:
    file_date = parse_date(args.date) if args.date else _midnight(now_kst())
    date_dir = WORK / file_date.strftime("%Y-%m-%d")
    st = state.load()
    order = models.check(st.get("last_model"))["order"]
    report = summarize.summarize(date_dir, DAILY, order, {})
    print(json.dumps({k: report[k] for k in ("model_counts", "failed")}, ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------------- weekly


def weekly_collect(run_date: datetime) -> tuple[Path, dict]:
    date_dir = WORK / f"weekly-{run_date.strftime('%Y-%m-%d')}"
    date_dir.mkdir(parents=True, exist_ok=True)
    result = fetch.fetch_trending()
    attempts = []
    if result["error"]:
        page, attempts = rescue.rescue_html(fetch.TRENDING_URL)
        if page:
            result["entries"] = fetch.parse_trending(page)
            result["error"] = None if result["entries"] else "no rows parsed (rescue)"
    for i, item in enumerate(result["entries"], start=1):
        item["id"] = f"github-{i}"
        item["channel"] = "github"
        item["body"] = fetch.readme_excerpt(item["repo"])
    payload = {
        "target_date": run_date.strftime("%Y-%m-%d"),
        "collected_at": now_kst().isoformat(timespec="seconds"),
        "source": result["source"],
        "error": result["error"],
        "rescue_attempts": attempts,
        "channels": {"github": {"items": result["entries"], "count": len(result["entries"])}},
        "sources": {"github.com/trending": {"error": result["error"], "entries": len(result["entries"])}},
        "dropped": {},
    }
    write_json(date_dir / "candidates.json", payload)
    print(f"trending entries={len(result['entries'])} error={result['error']}")
    return date_dir, payload


def weekly(args) -> int:
    run_date = parse_date(args.date) if args.date else _midnight(now_kst())
    date_dir, payload = weekly_collect(run_date)
    if args.summarize:
        order = models.check(state.load().get("last_model"))["order"]
        summarize.summarize(date_dir, ["github"], order, {})
    written, _, _ = render_channels(date_dir, run_date, ["github"])
    if args.publish and written:
        result = publish.publish_outputs(f"weekly: add {run_date:%Y%m%d} GitHub trending", push=not args.no_push)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("error") else 0
    return 0


# ------------------------------------------------------------------------ auto


def _github_link(path: Path) -> str:
    return f"{REPO_URL}/blob/main/{quote(path.relative_to(ROOT).as_posix())}"


def write_run_log(run: dict) -> Path:
    """Append this run to log/<run date>.md. Failures and their causes are never hidden."""
    path = ROOT / "log" / f"{run['started'][:10]}.md"
    lines = []
    if not path.exists():
        lines += [f"# DailyFeed 실행 로그 — {run['started'][:10]}", ""]
    lines += [f"## 실행 {run['started'][11:16]} KST — {run['status_ko']}", ""]
    if run.get("windows"):
        for channel, (start, end) in run["windows"].items():
            lines.append(f"- 수집 구간 `{channel}`: {start[:16]} → {end[:16]}")
    m = run.get("models") or {}
    if m:
        ok = sum(1 for p in m.get("probes", []) if p["ok"])
        lines.append(f"- 무료 모델 점검: {ok}/{len(m.get('probes', []))} 정상 (상세: `models/available.md`)")
        if m.get("disappeared"):
            lines.append(f"- 사라진 모델: {', '.join(m['disappeared'])}")
    if run.get("model_counts"):
        lines.append("- 요약 모델: " + ", ".join(f"`{k}` {v}건" for k, v in run["model_counts"].items()))
    lines.append("")
    if run.get("counts"):
        lines += ["| 채널 | 수록 |", "|---|---:|"]
        lines += [f"| {CHANNEL_LABEL[c]} | {n} |" for c, n in run["counts"].items()]
        lines.append("")
    if run.get("rescues"):
        lines += ["### 수집 실패와 대체 시도", "", "| 소스 | 원인 | 시도 | 결과 |", "|---|---|---|---|"]
        for rec in run["rescues"]:
            tried = " → ".join(
                f"{a['method']}{'✅' if a['ok'] else '❌'}" for a in rec["attempts"]
            ) or "-"
            outcome = f"{rec['method']}로 복구 ({rec['entries']}건)" if rec["method"] else "복구 실패"
            if rec.get("override"):
                outcome += f", 새 피드 주소 적용: {rec['override']}"
            lines.append(f"| {rec['source']} | {rec['cause_ko']} | {tried} | {outcome} |")
        lines.append("")
        details = [
            f"  - {rec['source']} / {a['method']}: {a['error']}"
            for rec in run["rescues"] for a in rec["attempts"] if a.get("error")
        ]
        if details:
            lines += ["<details><summary>시도별 오류</summary>", "", *details, "", "</details>", ""]
    if run.get("summary_failed"):
        lines += ["### 요약 실패 (제목만 기록)", ""]
        lines += [f"- {f['channel']} `{f['id']}`: {f['title']}" for f in run["summary_failed"]]
        lines.append("")
    if run.get("held"):
        lines += [f"- ⚠️ 사용 가능한 모델이 없어 보류: {', '.join(run['held'])} (다음 실행에서 같은 구간을 다시 처리)", ""]
    for warning in run.get("warnings", []):
        lines.append(f"- ⚠️ {warning}")
    for note in run.get("notes", []):
        lines.append(f"- {note}")
    if run.get("files"):
        lines += ["### 생성 파일", ""] + [f"- `{f}`" for f in run["files"]] + [""]
    if run.get("error"):
        lines += ["### 오류", "", "```", run["error"][-1500:], "```", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def notification_text(run: dict) -> str:
    icon = {"ok": "✅", "partial": "⚠️", "failed": "❌"}[run["status"]]
    lines = [f"{icon} DailyFeed {run['started'][:16].replace('T', ' ')} {run['status_ko']} ({run.get('seconds', 0)//60}분 {run.get('seconds', 0)%60}초)"]
    if run.get("windows"):
        start, end = next(iter(run["windows"].values()))
        lines.append(f"구간: {start[5:16].replace('T', ' ')} → {end[5:16].replace('T', ' ')}")
    if run.get("counts"):
        lines.append(" · ".join(f"{CHANNEL_LABEL[c]} {n}건" for c, n in run["counts"].items()))
    m = run.get("models") or {}
    if m:
        ok = sum(1 for p in m.get("probes", []) if p["ok"])
        used = ", ".join(f"{k.split('/')[-1]}({v})" for k, v in (run.get("model_counts") or {}).items()) or "-"
        lines.append(f"모델: {used} | 무료 모델 {ok}/{len(m.get('probes', []))} 정상")
        if m.get("disappeared"):
            lines.append(f"사라진 모델: {', '.join(m['disappeared'])}")
        if m.get("appeared"):
            lines.append(f"새 모델: {', '.join(m['appeared'])}")
    for rec in run.get("rescues", []):
        result = f"{rec['method']}로 복구" if rec["method"] else "복구 실패"
        lines.append(f"• {rec['source']}: {rec['cause_ko']} → {result}")
    if run.get("summary_failed"):
        lines.append(f"요약 실패 {len(run['summary_failed'])}건 (제목만 기록)")
    if run.get("held"):
        lines.append(f"보류: {', '.join(run['held'])} (모델 없음)")
    for warning in run.get("warnings", []):
        lines.append(f"⚠️ {warning}")
    lines += run.get("notes", [])
    if run.get("publish"):
        pub = run["publish"]
        if pub.get("error"):
            lines.append(f"push 실패: {pub['error'][:200]}")
        elif pub.get("pushed"):
            lines.append(f"커밋 {pub['commit'][:7]} push 완료")
        elif pub.get("note"):
            lines.append(pub["note"])
    for path in run.get("file_paths", []):
        lines.append(_github_link(path))
    if run.get("error"):
        lines.append(f"오류: {run['error'].strip().splitlines()[-1][:300]}")
    return "\n".join(lines)


def auto(args) -> int:
    started = now_kst().replace(microsecond=0)
    clock = time.monotonic()
    lock = WORK / ".auto.lock"
    WORK.mkdir(exist_ok=True)
    if lock.exists() and time.time() - lock.stat().st_mtime < 3 * 3600:
        print("another auto run is in progress (work/.auto.lock)")
        return 1
    lock.write_text(started.isoformat(), encoding="utf-8")

    run: dict = {"started": started.isoformat(), "status": "ok", "warnings": [], "notes": [], "files": [], "file_paths": []}
    st = state.load()
    try:
        sync = publish.sync()
        if sync.get("error"):
            run["warnings"].append(f"git pull 실패: {sync['error'][:150]}")

        # 1. free models (also refreshes models/available.md for the user to set priorities)
        mreport = models.check(st.get("last_model"))
        run["models"] = mreport
        order = mreport["order"]
        print(f"models: {len(order)} usable, order={order[:3]}")

        # 2. daily collect — everything newer than each channel's previous run
        end = now_kst().replace(microsecond=0)
        file_date = _midnight(end)
        starts = {c: state.window_start(st, c, end) for c in DAILY}
        run["windows"] = {c: [starts[c].isoformat(), end.isoformat()] for c in DAILY}
        failed_since = {k: v for k, v in ((k, parse_iso(v)) for k, v in st["failed_since"].items()) if v}
        payload = collect_window(
            DAILY, starts, end, file_date, order=order, rescue_on=not args.no_rescue, source_starts=failed_since
        )
        run["rescues"] = payload["rescues"]
        for key, info in payload["sources"].items():
            if key.startswith("GeekNews") or key == "Anthropic Newsroom":
                continue
            channel = "youtube" if key.startswith("YouTube:") else "tech"
            if info["error"]:
                st["failed_since"].setdefault(key, starts[channel].isoformat())
            elif key in st["failed_since"]:
                run["notes"].append(f"{key}: 복구됨, {st['failed_since'].pop(key)[:16]} 이후 놓친 글까지 다시 수집")
        date_dir = WORK / file_date.strftime("%Y-%m-%d")

        # 3. summarize
        srep = summarize.summarize(date_dir, DAILY, order, {})
        run["model_counts"] = srep["model_counts"]
        run["summary_failed"] = srep["failed"]
        cov = summarize.coverage(date_dir, DAILY)

        # No model at all: publish GeekNews (titles are Korean already), keep tech/youtube for the next run.
        ready = [c for c in DAILY if not (c != "geeknews" and cov[c]["items"] and cov[c]["ok"] == 0 and not order)]
        run["held"] = [c for c in DAILY if c not in ready]

        # 4. render
        written, removed, warnings = render_channels(date_dir, file_date, ready)
        run["warnings"] += warnings
        run["counts"] = {}
        summaries = load_summaries(date_dir)
        for c in ready:
            run["counts"][c] = sum(1 for i in payload["channels"][c]["items"] if not summaries.get(i["id"], {}).get("skip"))
            st["last_run"][c] = end.isoformat()
        run["file_paths"] += written

        # 5. GitHub weekly on Monday, or as a catch-up once a week has passed
        if state.weekly_due(st, end):
            wdir, wpayload = weekly_collect(file_date)
            wrep = summarize.summarize(wdir, ["github"], order, {})
            for model, n in wrep["model_counts"].items():
                run["model_counts"][model] = run["model_counts"].get(model, 0) + n
            run["summary_failed"] += wrep["failed"]
            if wpayload["channels"]["github"]["items"]:
                wwritten, _, wwarn = render_channels(wdir, file_date, ["github"])
                run["warnings"] += wwarn
                run["file_paths"] += wwritten
                run["counts"]["github"] = len(wpayload["channels"]["github"]["items"])
                st["last_weekly_at"] = end.isoformat()
            else:
                run["warnings"].append(f"GitHub Trending 수집 실패: {wpayload['error']}")
                run["rescues"].append({
                    "source": "GitHub Trending", "channel": "github", "error": wpayload["error"],
                    "cause": "trending", "cause_ko": "Trending 페이지 수집 실패", "method": None,
                    "entries": 0, "attempts": wpayload["rescue_attempts"],
                })

        st["last_model"] = srep.get("last_model") or st.get("last_model")
        state.save(st)
        run["files"] = [p.relative_to(ROOT).as_posix() for p in run["file_paths"]]
        failed_sources = [r for r in run["rescues"] if not r["method"]]
        if failed_sources or run["summary_failed"] or run["held"] or run["warnings"]:
            run["status"] = "partial"
    except Exception as exc:  # noqa: BLE001 - reported, logged, and notified below
        run["status"] = "failed"
        run["error"] = "".join(traceback.format_exception(exc))
        print(run["error"])

    run["status_ko"] = {"ok": "완료", "partial": "부분 완료", "failed": "실패"}[run["status"]]
    run["seconds"] = int(time.monotonic() - clock)
    try:
        write_run_log(run)
        counts = ", ".join(f"{c} {n}" for c, n in (run.get("counts") or {}).items()) or "no items"
        run["publish"] = publish.publish_outputs(f"daily: {started:%Y-%m-%d %H:%M} ({counts})", push=not args.no_push)
        if run["publish"].get("error") and run["status"] == "ok":
            run["status"], run["status_ko"] = "partial", "부분 완료"
    except Exception as exc:  # noqa: BLE001
        run["publish"] = {"error": f"{type(exc).__name__}: {exc}"}
    finally:
        lock.unlink(missing_ok=True)

    text = notification_text(run)
    print(text)
    sent = notify.send(text) if not args.no_notify else {"notify": "skipped"}
    print(f"notify: {sent}")
    return 0 if run["status"] != "failed" else 1


# ---------------------------------------------------------------------- doctor


def doctor(_args) -> int:
    readme = parse_readme()
    info = publish.status()
    print(f"repo={info['is_repo']} branch={info['branch']} remote={info['remote']}")
    print(f"dirty_files={len(info['dirty'])}")
    print(f"tech_sources={len(readme['tech'])} youtube_channels={len(readme['youtube'])}")
    results = fetch.fetch_all([s for s in readme["tech"] if s["type"] == "feed"], workers=10)
    bad = [(r["source"], r["error"], rescue.diagnose(r)) for r in results if r["error"] or not r["entries"]]
    print(f"feed_ok={len(results) - len(bad)} feed_bad={len(bad)}")
    for name, err, cause in bad:
        print(f"  ! {name}: [{cause}] {err}")
    print(f"notify targets: {notify._config()['discord'] is not None and 'discord' or ''} {notify._config()['slack'] is not None and 'slack' or ''}".strip())
    return 0


def models_cmd(_args) -> int:
    report = models.check(state.load().get("last_model"))
    print(f"order: {report['order']}")
    print(f"wrote {models.AVAILABLE_MD.relative_to(ROOT)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DailyFeed pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_auto = sub.add_parser("auto", help="scheduled run: models, collect, summarize, render, publish, notify")
    p_auto.add_argument("--no-push", action="store_true")
    p_auto.add_argument("--no-notify", action="store_true")
    p_auto.add_argument("--no-rescue", action="store_true")
    p_auto.set_defaults(func=auto)

    p_models = sub.add_parser("models", help="probe opencode free models -> models/available.md")
    p_models.set_defaults(func=models_cmd)

    p_collect = sub.add_parser("collect", help="fetch sources into work/<date>/")
    p_collect.add_argument("--date", help="calendar-day mode; default is 'since the previous run'")
    p_collect.add_argument("--channels", default="geeknews,tech,youtube")
    p_collect.add_argument("--workers", type=int, default=8)
    p_collect.add_argument("--fresh", action="store_true", help="ignore the earlier collect for this date")
    p_collect.add_argument("--no-rescue", action="store_true")
    p_collect.set_defaults(func=collect)

    p_sum = sub.add_parser("summarize", help="summarize work/<date>/ with opencode free models")
    p_sum.add_argument("--date")
    p_sum.set_defaults(func=summarize_cmd)

    p_render = sub.add_parser("render", help="write markdown from candidates + summaries")
    p_render.add_argument("--date")
    p_render.add_argument("--publish", action="store_true")
    p_render.add_argument("--no-push", action="store_true")
    p_render.add_argument("--message")
    p_render.set_defaults(func=render_cmd)

    p_weekly = sub.add_parser("weekly", help="GitHub weekly trending")
    p_weekly.add_argument("--date")
    p_weekly.add_argument("--summarize", action="store_true")
    p_weekly.add_argument("--publish", action="store_true")
    p_weekly.add_argument("--no-push", action="store_true")
    p_weekly.set_defaults(func=weekly)

    p_doctor = sub.add_parser("doctor", help="check repo + source reachability")
    p_doctor.set_defaults(func=doctor)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    if sys.stdout is None:  # pythonw (Task Scheduler): keep a local log of the run
        log_dir = WORK / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        sys.stdout = sys.stderr = open(log_dir / f"{datetime.now():%Y%m%d-%H%M%S}.log", "w", encoding="utf-8")
    sys.exit(main())
