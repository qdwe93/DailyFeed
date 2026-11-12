"""today.md / daily/YYYY-MM-DD.md: one page with everything published for a collection date.

The digest is assembled only from the per-channel Markdown files that were actually written
(geeknews/ tech/ youtube/ github/). It never reads candidates.json and never calls an LLM, so the
render guard in run.render_channels() (refuse to drop links already published today) carries over:
whatever the channel file holds is exactly what the digest shows.

The date is the collection (run) date in KST — the same `file_date` the channel files use — not
the article's publication date.
"""

from __future__ import annotations

import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from .util import CHANNELS, KST, ROOT, month_dir, now_kst

LABELS = {
    "geeknews": "GeekNews",
    "tech": "Tech Feeds",
    "youtube": "YouTube Tech",
    "github": "GitHub Trending Weekly",
}
DAILY_CHANNELS = ("geeknews", "tech", "youtube")
TODAY = "today.md"
DAILY_DIR = "daily"

_HEADING = re.compile(r"^(#{1,5}) ")
_HELD_MARK = re.compile(r"<!-- dailyfeed-digest held=([a-z,]*) -->")


class DigestError(RuntimeError):
    """The published files for the date are inconsistent; the digest is not written."""


def _anchor(label: str) -> str:
    """GitHub heading anchor for the simple ASCII labels above."""
    return re.sub(r"[^a-z0-9 -]", "", label.lower()).replace(" ", "-")


def repo_link(path: Path, root: Path) -> str:
    """Repository-root link ('/geeknews/2026%EB%85%8411%EC%9B%94/...'). GitHub resolves a leading
    '/' against the repository root, so the same link works from today.md and daily/<date>.md."""
    return "/" + quote(path.relative_to(root).as_posix())


def channel_file(root: Path, channel: str, date: datetime) -> Path | None:
    folder = root / channel / month_dir(date)
    found = sorted(folder.glob(f"{date:%Y-%m-%d}_*.md")) if folder.is_dir() else []
    if len(found) > 1:
        names = ", ".join(p.name for p in found)
        raise DigestError(f"{channel}: {date:%Y-%m-%d} 발행 파일이 {len(found)}개 ({names}) — 하나만 있어야 함")
    return found[0] if found else None


def _count(channel: str, text: str) -> int:
    lines = text.splitlines()
    if channel == "geeknews":
        return sum(1 for line in lines if line.startswith("- ["))
    if channel == "github":
        return sum(1 for line in lines if re.match(r"^## \d+\. ", line))
    return sum(1 for line in lines if line.startswith("### "))


def _body(text: str) -> str:
    """Channel file minus its '# Channel — date' title, every heading one level deeper."""
    lines = text.rstrip("\n").splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(_HEADING.sub(lambda m: "#" + m.group(1) + " ", line) for line in lines)


def previous_held(root: Path, date: datetime) -> list[str]:
    """Held channels recorded by an earlier digest of the same date (for weekly/manual rebuilds)."""
    path = root / DAILY_DIR / f"{date:%Y-%m-%d}.md"
    if not path.exists():
        return []
    m = _HELD_MARK.search(path.read_text(encoding="utf-8", errors="replace"))
    return [c for c in (m.group(1).split(",") if m else []) if c]


def build_digest(
    date: datetime,
    root: Path = ROOT,
    held: list[str] | tuple[str, ...] = (),
    generated_at: datetime | None = None,
    link_log: bool | None = None,
) -> str:
    """Markdown for `date` (KST collection date). Raises DigestError on inconsistent inputs."""
    generated_at = (generated_at or now_kst()).astimezone(KST)
    held = [c for c in held if c in CHANNELS]
    stamp = f"{date:%Y-%m-%d}"

    sections: list[tuple[str, Path | None, str]] = []
    for channel in CHANNELS:
        path = channel_file(root, channel, date)
        if channel == "github" and path is None:
            continue  # weekly snapshot only on the days it ran
        text = path.read_text(encoding="utf-8") if path else ""
        sections.append((channel, path, text))

    log_path = root / "log" / f"{stamp}.md"
    if link_log is None:
        link_log = log_path.exists()

    lines = [
        f"# DailyFeed — {stamp} (KST)",
        "",
        f"<!-- dailyfeed-digest held={','.join(held)} -->",
        "",
        f"- 수집일: {stamp}",
        f"- 통합 생성: {generated_at:%Y-%m-%d %H:%M} KST",
        "- 구분: 수집일(실행일) 기준. 기사 게시일과 다를 수 있음",
    ]
    if link_log:
        lines.append(f"- 실행 로그: [log/{stamp}.md]({repo_link(log_path, root)})")
    lines += ["", "## 빠른 이동", ""]
    for channel, path, text in sections:
        if path:
            note = f" — {_count(channel, text)}건"
        elif channel in held:
            note = " — 보류"
        else:
            note = " — 발행 파일 없음"
        lines.append(f"- [{LABELS[channel]}](#{_anchor(LABELS[channel])}){note}")
    lines.append("")

    for channel, path, text in sections:
        lines += [f"## {LABELS[channel]}", ""]
        if channel in held:
            if path:
                lines += ["> ⚠️ 이번 실행의 신규 항목은 사용 가능한 요약 모델이 없어 요약/발행 보류. 아래는 이미 발행된 내용이며, 보류분은 다음 실행에서 처리됨.", ""]
            else:
                lines += ["> ⚠️ 요약/발행 보류: 사용 가능한 요약 모델이 없음. 다음 실행에서 같은 구간을 다시 처리함.", ""]
        if not path:
            if channel not in held:
                lines += ["> 이 수집일의 발행 파일이 없음 (수집 미실행 또는 실패일 수 있음 — 실행 로그 참고).", ""]
            continue
        lines += [f"[채널별 원본]({repo_link(path, root)})", "", _body(text), ""]

    return "\n".join(lines).rstrip() + "\n"


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def write_digest(
    date: datetime,
    root: Path = ROOT,
    held: list[str] | None = None,
    update_today: bool = True,
    now: datetime | None = None,
    link_log: bool | None = None,
) -> list[Path]:
    """Write daily/<date>.md, and today.md with identical content when `date` is today (KST).

    held=None keeps the held channels recorded by an earlier digest of the same date.
    Nothing is written if building fails, so the previous today.md survives.
    """
    now = (now or now_kst()).astimezone(KST)
    if held is None:
        held = previous_held(root, date)
    text = build_digest(date, root, held=held, generated_at=now, link_log=link_log)
    daily = root / DAILY_DIR / f"{date:%Y-%m-%d}.md"
    _atomic_write(daily, text)
    written = [daily]
    if update_today and date.astimezone(KST).date() == now.date():
        today = root / TODAY
        _atomic_write(today, text)
        written.insert(0, today)
    return written
