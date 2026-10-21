"""Thin wrapper over `opencode run`: send a prompt on stdin, collect the text parts."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time

from .util import NO_WINDOW, ROOT

# Runs outside the repo so opencode does not pick up project files as context.
SCRATCH = ROOT / "work" / ".opencode"


def opencode_bin() -> str:
    return shutil.which("opencode") or "opencode"


def run(model: str, prompt: str, timeout: int = 300, agent: bool = False) -> dict:
    """Return {text, error, seconds}. Never raises.

    agent=True lets the model use its tools (websearch, playwright/apify MCP) without prompts.
    """
    SCRATCH.mkdir(parents=True, exist_ok=True)
    cmd = [opencode_bin(), "run", "-m", model, "--format", "json"]
    if agent:
        cmd.append("--auto")
    started = time.monotonic()
    out = {"text": "", "error": None, "seconds": 0.0}
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=SCRATCH,
            creationflags=NO_WINDOW,
        )
    except subprocess.TimeoutExpired:
        out["error"] = f"timeout after {timeout}s"
        out["seconds"] = round(time.monotonic() - started, 1)
        return out
    except OSError as exc:
        out["error"] = f"{type(exc).__name__}: {exc}"[:300]
        return out
    out["seconds"] = round(time.monotonic() - started, 1)

    texts, errors = [], []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        part = event.get("part") or {}
        if event.get("type") == "text" and part.get("text"):
            texts.append(part["text"])
        elif event.get("type") == "error" or "error" in event:
            errors.append(json.dumps(event.get("error") or event, ensure_ascii=False)[:300])
    out["text"] = "\n".join(texts).strip()
    if not out["text"]:
        stderr = re.sub(r"\x1b\[[0-9;]*m", "", proc.stderr or "").strip()
        out["error"] = (errors[0] if errors else stderr[-300:]) or f"empty output (exit {proc.returncode})"
    return out


def extract_json(text: str):
    """First JSON object or array in a model reply (tolerates code fences and prose)."""
    if not text:
        return None
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.S)
    candidates = [fenced.group(1)] if fenced else []
    candidates.append(text)
    decoder = json.JSONDecoder()
    for chunk in candidates:
        for match in re.finditer(r"[\[{]", chunk):
            try:
                value, _ = decoder.raw_decode(chunk[match.start():])
                return value
            except json.JSONDecodeError:
                continue
    return None
