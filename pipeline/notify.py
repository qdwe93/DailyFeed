"""Run result notification via Discord/Slack incoming webhooks (both free).

The webhook URL is a secret and this repo is public, so it lives outside the repo:
env DAILYFEED_DISCORD_WEBHOOK / DAILYFEED_SLACK_WEBHOOK, or %USERPROFILE%/.dailyfeed/config.json
{"discord_webhook": "...", "slack_webhook": "..."}.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx

CONFIG_PATH = Path.home() / ".dailyfeed" / "config.json"


def _config() -> dict:
    data = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
    return {
        "discord": os.environ.get("DAILYFEED_DISCORD_WEBHOOK") or data.get("discord_webhook"),
        "slack": os.environ.get("DAILYFEED_SLACK_WEBHOOK") or data.get("slack_webhook"),
    }


def _chunks(text: str, size: int) -> list[str]:
    out, current = [], ""
    for line in text.splitlines():
        if len(current) + len(line) + 1 > size and current:
            out.append(current)
            current = ""
        current += line + "\n"
    if current.strip():
        out.append(current)
    return out


def _safe_error(exc: Exception) -> str:
    """Never echo the exception text: httpx puts the secret webhook URL in it."""
    status = getattr(getattr(exc, "response", None), "status_code", None)
    return f"{type(exc).__name__}" + (f" HTTP {status}" if status else "")


def send(text: str) -> dict:
    """Post to every configured webhook. Returns {target: 'ok' | error | 'not configured'}."""
    cfg = _config()
    result = {}
    if cfg["discord"]:
        try:
            for chunk in _chunks(text, 1900):  # Discord content limit is 2000
                httpx.post(cfg["discord"], json={"content": chunk}, timeout=20).raise_for_status()
            result["discord"] = "ok"
        except Exception as exc:  # noqa: BLE001
            result["discord"] = _safe_error(exc)
    if cfg["slack"]:
        try:
            httpx.post(cfg["slack"], json={"text": text}, timeout=20).raise_for_status()
            result["slack"] = "ok"
        except Exception as exc:  # noqa: BLE001
            result["slack"] = _safe_error(exc)
    return result or {"webhook": "not configured"}
