"""Run state committed to the repo: per-channel window start, weekly run, last model."""

from __future__ import annotations

from datetime import datetime, timedelta

from .util import ROOT, parse_iso, read_json, write_json

STATE_PATH = ROOT / "state" / "run_state.json"
DAILY_CHANNELS = ("geeknews", "tech", "youtube")


def load() -> dict:
    data = read_json(STATE_PATH, default={}) or {}
    data.setdefault("last_run", {})
    data.setdefault("last_weekly_at", None)
    data.setdefault("last_model", None)
    data.setdefault("failed_since", {})  # source -> window start of its first failed run
    return data


def save(state: dict) -> None:
    write_json(STATE_PATH, state)


def window_start(state: dict, channel: str, now: datetime) -> datetime:
    """Items newer than the channel's last successful run; a first run looks back one day."""
    return parse_iso(state["last_run"].get(channel)) or (now - timedelta(days=1))


def weekly_due(state: dict, now: datetime) -> bool:
    """Monday run, or a catch-up when the last snapshot is a week old (the PC may have been off)."""
    last = parse_iso(state.get("last_weekly_at"))
    if last is None:
        return True
    if (now.date() - last.date()).days >= 7:
        return True
    return now.weekday() == 0 and last.date() != now.date()
