"""Summaries via opencode free models: small batches, validated, retried on the next model.

Writes work/<dir>/summaries.json incrementally in the format `render` already reads, so a
crashed run resumes where it stopped and a same-day rerun only summarizes new ids.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import llm
from .util import HANGUL_RE, read_json, write_json

BULLETS = {"tech": 5, "youtube": 5, "github": 2}
BATCH = {"geeknews": 25, "tech": 4, "youtube": 4, "github": 5}
BODY_CHARS = {"tech": 2500, "youtube": 2000, "github": 1800}
CALL_TIMEOUT = 360

RULES = {
    "tech": "기술 블로그 글이다. 본문에 있는 사실만 근거로 핵심을 요약한다.",
    "youtube": (
        "YouTube 영상이다. 설명란·메타데이터에 있는 사실만 근거로 요약한다. "
        "Shorts, 회사 홍보, 채용, 행사 티저, 기술 내용이 없는 영상, 설명이 부족해 내용을 알 수 없는 영상은 skip한다."
    ),
    "github": "GitHub Weekly Trending 저장소다. 무엇을 하는 프로젝트인지, 핵심 특징을 README/설명 근거로 쓴다. 유행 이유를 지어내지 않는다.",
}


def _has_hangul(text: str, minimum: int = 2) -> bool:
    return len(HANGUL_RE.findall(text or "")) >= minimum


def validate(channel: str, entry) -> str | None:
    """None when usable, else the reason it is rejected."""
    if not isinstance(entry, dict):
        return "not an object"
    if entry.get("skip"):
        return None if str(entry.get("reason", "")).strip() else "skip without reason"
    title = str(entry.get("title_ko", "")).strip()
    if channel != "github" and not _has_hangul(title):
        return "title_ko missing or not Korean"
    if channel == "geeknews":
        return None
    bullets = entry.get("bullets")
    need = BULLETS[channel]
    if not isinstance(bullets, list) or len([b for b in bullets if str(b).strip()]) != need:
        return f"need exactly {need} bullets"
    if not all(_has_hangul(str(b), 4) for b in bullets):
        return "bullet not Korean"
    return None


def _item_block(channel: str, item: dict) -> str:
    lines = [f"### id: {item['id']}"]
    if channel == "github":
        lines += [
            f"저장소: {item.get('repo')}",
            f"언어: {item.get('language') or '-'} | 증가: {item.get('stars') or '-'}",
            f"설명: {item.get('description') or '-'}",
        ]
    else:
        lines += [f"출처: {item.get('source')}", f"제목: {item.get('title')}", f"URL: {item.get('url')}"]
    body = re.sub(r"\n{2,}", "\n", (item.get("body") or item.get("summary") or "").strip())
    limit = BODY_CHARS.get(channel, 0)
    if body and limit:
        lines += ["본문:", body[:limit]]
    return "\n".join(lines)


def build_prompt(channel: str, items: list[dict]) -> str:
    ids = ", ".join(item["id"] for item in items)
    if channel == "geeknews":
        head = (
            "다음 GeekNews 글 제목을 자연스러운 한국어 제목으로 옮겨라. 고유명사·제품명은 원문 표기를 유지한다.\n"
            'JSON 객체 하나만 출력한다: {"items": {"<id>": {"title_ko": "..."}}}\n'
        )
    else:
        need = BULLETS[channel]
        head = (
            f"{RULES[channel]}\n"
            "규칙:\n"
            "- title_ko: 자연스러운 한국어 제목. 원제가 한국어면 거의 그대로 둔다.\n"
            f"- bullets: 정확히 {need}개. 각 항목은 한국어 한 문장, 사실 위주. 마케팅 문구·추측·본문에 없는 내용 금지.\n"
            '- 요약할 수 없으면 {"skip": true, "reason": "이유"}.\n'
            "- 도구를 쓰지 말고 아래 내용만으로 답한다. 설명 없이 JSON 객체 하나만 출력한다.\n"
            f'형식: {{"items": {{"<id>": {{"title_ko": "...", "bullets": [{", ".join(chr(34) + "..." + chr(34) for _ in range(need))}]}}}}}}\n'
        )
    blocks = "\n\n".join(_item_block(channel, item) for item in items)
    return f"{head}반드시 다음 id를 모두 포함한다: {ids}\n\n{blocks}\n"


def _pending(channel: str, items: list[dict], done: dict) -> list[dict]:
    pending = []
    for item in items:
        if validate(channel, done.get(item["id"])) is None:
            continue
        # GeekNews titles are already Korean; only foreign titles need a model.
        if channel == "geeknews" and _has_hangul(item.get("title", "")):
            continue
        pending.append(item)
    return pending


def summarize(date_dir: Path, channels: list[str], order: list[str], report: dict) -> dict:
    """Fill summaries.json for `channels`. Returns updated report with per-model counts and failures."""
    candidates = read_json(date_dir / "candidates.json")
    path = date_dir / "summaries.json"
    data = read_json(path, default={}) or {}
    done: dict = data.get("items", {})
    data.setdefault("date", candidates.get("target_date"))
    report.setdefault("model_counts", {})
    report.setdefault("failed", [])
    report.setdefault("calls", [])
    pointer = 0  # sticky: a model that errored is not tried first again in this run

    for channel in channels:
        block = candidates["channels"].get(channel)
        if not block:
            continue
        pending = _pending(channel, block["items"], done)
        size = BATCH[channel]
        for start in range(0, len(pending), size):
            batch = pending[start:start + size]
            left = {item["id"]: item for item in batch}
            tries = [order[(pointer + k) % len(order)] for k in range(min(len(order), 4))]
            for attempt, model in enumerate(tries):
                if not left:
                    break
                reply = llm.run(model, build_prompt(channel, list(left.values())), timeout=CALL_TIMEOUT)
                call = {"channel": channel, "model": model, "ids": list(left), "seconds": reply["seconds"]}
                if reply["error"]:
                    call["error"] = reply["error"][:200]
                    report["calls"].append(call)
                    if attempt == 0:
                        pointer = (pointer + 1) % len(order)
                    continue
                parsed = llm.extract_json(reply["text"])
                got = parsed.get("items", parsed) if isinstance(parsed, dict) else {}
                accepted, rejected = [], {}
                for item_id in list(left):
                    entry = got.get(item_id) if isinstance(got, dict) else None
                    problem = validate(channel, entry)
                    if problem:
                        rejected[item_id] = problem
                        continue
                    entry = dict(entry)
                    if entry.get("bullets"):
                        entry["bullets"] = [str(b).strip() for b in entry["bullets"]]
                    entry["model"] = model
                    done[item_id] = entry
                    accepted.append(item_id)
                    left.pop(item_id)
                call.update(accepted=len(accepted), rejected=rejected)
                report["calls"].append(call)
                report["model_counts"][model] = report["model_counts"].get(model, 0) + len(accepted)
                if accepted:
                    report["last_model"] = model
                data["items"] = done
                write_json(path, data)
            for item_id, item in left.items():
                report["failed"].append({"id": item_id, "title": item.get("title") or item.get("repo"), "channel": channel})
    data["items"] = done
    write_json(path, data)
    return report


def coverage(date_dir: Path, channels: list[str]) -> dict:
    """Per channel: (items, summarized) — a channel with items but nothing usable needs a model."""
    candidates = read_json(date_dir / "candidates.json")
    done = (read_json(date_dir / "summaries.json", default={}) or {}).get("items", {})
    out = {}
    for channel in channels:
        items = (candidates["channels"].get(channel) or {}).get("items", [])
        ok = sum(1 for i in items if validate(channel, done.get(i["id"])) is None or (
            channel == "geeknews" and _has_hangul(i.get("title", ""))))
        out[channel] = {"items": len(items), "ok": ok}
    return out
