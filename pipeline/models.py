"""Free-model discovery, probing, and ordering.

opencode's free lineup changes without notice, so every run lists what opencode offers,
probes each free model with the same small summarizing task, and publishes the result
to models/available.md. models/priority.txt (edited by hand) decides the order; with no
priority the last model that worked goes first, then the rest by probe score.
OpenRouter `:free` models are only a last resort when no opencode free model answers.
"""

from __future__ import annotations

import concurrent.futures as cf
import subprocess
import time

import httpx

from . import llm
from .util import HANGUL_RE, NO_WINDOW, ROOT, now_kst, read_json, write_json

MODELS_DIR = ROOT / "models"
PRIORITY_PATH = MODELS_DIR / "priority.txt"
AVAILABLE_JSON = MODELS_DIR / "available.json"
AVAILABLE_MD = MODELS_DIR / "available.md"

PROBE_TIMEOUT = 120
PROBE_PROMPT = """다음 영어 글을 한국어로 요약하라. 설명 없이 JSON 객체 하나만 출력한다.
형식: {"title_ko": "한국어 제목", "bullets": ["1줄", "2줄", "3줄", "4줄", "5줄"]}
bullets는 정확히 5개, 각각 한 문장.

Title: PostgreSQL 18 adds asynchronous I/O
Body: PostgreSQL 18 introduces an asynchronous I/O subsystem that lets sequential scans,
bitmap heap scans and vacuum issue multiple reads at once instead of waiting for each block.
On Linux it can use io_uring; elsewhere it falls back to a pool of worker processes. Benchmarks
from the release notes show up to 3x faster cold-cache scans on cloud block storage. The release
also adds virtual generated columns by default, OAuth authentication, and uuidv7() for
time-ordered identifiers. Upgrades keep planner statistics, which shortens post-upgrade warmup.
"""


def list_models() -> tuple[list[str], str | None]:
    try:
        proc = subprocess.run(
            [llm.opencode_bin(), "models"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            creationflags=NO_WINDOW,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], f"{type(exc).__name__}: {exc}"[:200]
    models = [line.strip() for line in proc.stdout.splitlines() if "/" in line and " " not in line.strip()]
    return models, None if models else (proc.stderr or "no models listed").strip()[:200]


def _zero_cost_ids() -> set[str]:
    """opencode model ids that models.dev prices at zero (catches free models without '-free')."""
    try:
        data = httpx.get("https://models.dev/api.json", timeout=20).json()
    except Exception:  # noqa: BLE001 - name heuristic still works
        return set()
    free = set()
    for model_id, info in (data.get("opencode", {}).get("models") or {}).items():
        cost = info.get("cost") or {}
        if cost.get("input") == 0 and cost.get("output") == 0:
            free.add(f"opencode/{model_id}")
    return free


def free_models(models: list[str]) -> tuple[list[str], list[str]]:
    zero = _zero_cost_ids()
    opencode_free = [m for m in models if m.startswith("opencode/") and (m.endswith("-free") or m in zero)]
    openrouter_free = [m for m in models if m.startswith("openrouter/") and m.endswith(":free")]
    return opencode_free, openrouter_free


def probe(model: str) -> dict:
    result = {"model": model, "ok": False, "score": 0, "seconds": None, "error": None}
    reply = llm.run(model, PROBE_PROMPT, timeout=PROBE_TIMEOUT)
    result["seconds"] = reply["seconds"]
    if reply["error"]:
        result["error"] = reply["error"]
        return result
    data = llm.extract_json(reply["text"])
    score = 40  # answered
    notes = []
    if isinstance(data, dict):
        score += 20
        bullets = data.get("bullets") or []
        if isinstance(bullets, list) and len(bullets) == 5:
            score += 15
        else:
            notes.append(f"bullets={len(bullets) if isinstance(bullets, list) else '?'}")
        text = f"{data.get('title_ko', '')} {' '.join(map(str, bullets if isinstance(bullets, list) else []))}"
        if len(HANGUL_RE.findall(text)) >= 40:
            score += 15
        else:
            notes.append("한국어 부족")
    else:
        notes.append("JSON 아님")
    if reply["seconds"] <= 15:
        score += 10
    elif reply["seconds"] <= 45:
        score += 5
    result.update(ok=isinstance(data, dict), score=score, error="; ".join(notes) or None)
    return result


def probe_all(models: list[str], workers: int = 4) -> list[dict]:
    if not models:
        return []
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(probe, models))


def read_priority() -> list[str]:
    if not PRIORITY_PATH.exists():
        return []
    lines = PRIORITY_PATH.read_text(encoding="utf-8").splitlines()
    return [line.split("#", 1)[0].strip() for line in lines if line.split("#", 1)[0].strip()]


def order(probes: list[dict], last_model: str | None) -> list[str]:
    """priority.txt first, else the last model that worked, then the rest by score."""
    ok = {p["model"]: p for p in probes if p["ok"]}
    ordered: list[str] = []
    for model in read_priority():
        if model in ok and model not in ordered:
            ordered.append(model)
    if last_model in ok and last_model not in ordered:
        ordered.append(last_model)
    for p in sorted(ok.values(), key=lambda p: (-p["score"], p["seconds"] or 999)):
        if p["model"] not in ordered:
            ordered.append(p["model"])
    return ordered


def check(last_model: str | None) -> dict:
    """Discover + probe; fall back to OpenRouter free only when no opencode free model works."""
    started = time.monotonic()
    models, error = list_models()
    opencode_free, openrouter_free = free_models(models)
    probes = probe_all(opencode_free)
    used_fallback = False
    if not any(p["ok"] for p in probes) and openrouter_free:
        used_fallback = True
        probes += probe_all(openrouter_free)
    report = {
        "checked_at": now_kst().isoformat(timespec="seconds"),
        "list_error": error,
        "opencode_free": opencode_free,
        "openrouter_fallback_used": used_fallback,
        "probes": probes,
        "order": order(probes, last_model),
        "seconds": round(time.monotonic() - started, 1),
    }
    previous = read_json(AVAILABLE_JSON, default={}) or {}
    report["disappeared"] = sorted(set(previous.get("opencode_free", [])) - set(opencode_free))
    report["appeared"] = sorted(set(opencode_free) - set(previous.get("opencode_free", []))) if previous else []
    write_json(AVAILABLE_JSON, report)
    write_available_md(report)
    ensure_priority_file()
    return report


def write_available_md(report: dict) -> None:
    lines = [
        "# 사용 가능한 무료 모델",
        "",
        f"- 점검 시각: {report['checked_at']} (KST)",
        f"- opencode 무료 모델 {len(report['opencode_free'])}개 발견, "
        f"정상 응답 {sum(1 for p in report['probes'] if p['ok'] and p['model'].startswith('opencode/'))}개",
        f"- 이번 실행 사용 순서: {' → '.join(f'`{m}`' for m in report['order'][:5]) or '없음'}",
    ]
    if report.get("openrouter_fallback_used"):
        lines.append("- ⚠️ opencode 무료 모델이 모두 실패해 OpenRouter `:free` 모델을 점검했다.")
    if report.get("appeared"):
        lines.append(f"- 새로 생김: {', '.join(f'`{m}`' for m in report['appeared'])}")
    if report.get("disappeared"):
        lines.append(f"- 사라짐: {', '.join(f'`{m}`' for m in report['disappeared'])}")
    lines += [
        "",
        "우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.",
        "",
        "점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).",
        "",
        "| 모델 | 상태 | 점수 | 응답(초) | 비고 |",
        "|---|---|---:|---:|---|",
    ]
    for p in sorted(report["probes"], key=lambda p: (not p["ok"], -p["score"], p["seconds"] or 999)):
        status = "✅" if p["ok"] else "❌"
        note = (p.get("error") or "").replace("|", "/").replace("\n", " ")[:120]
        lines.append(f"| `{p['model']}` | {status} | {p['score']} | {p['seconds'] if p['seconds'] is not None else '-'} | {note} |")
    AVAILABLE_MD.parent.mkdir(parents=True, exist_ok=True)
    AVAILABLE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def ensure_priority_file() -> None:
    if PRIORITY_PATH.exists():
        return
    PRIORITY_PATH.write_text(
        "# 요약에 쓸 모델 우선순위. 한 줄에 하나, 위에 있을수록 먼저 쓴다. '#' 뒤는 주석.\n"
        "# 후보는 available.md 표를 참고한다. 목록의 모델이 모두 실패하면 마지막 성공 모델 → 점수순으로 넘어간다.\n"
        "# 예) opencode/deepseek-v4.1-flash-free\n",
        encoding="utf-8",
        newline="\n",
    )
