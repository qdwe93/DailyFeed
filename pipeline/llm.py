"""Thin wrapper over the model CLIs: send a prompt on stdin, collect the reply text.

Model ids starting with `agy/` go to Antigravity CLI (`agy`, default since 2026-11-13);
anything else goes to `opencode run` (kept only for manual use / rollback).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from .util import NO_WINDOW, ROOT

# Runs outside the repo so the CLI does not pick up project files as context.
SCRATCH = ROOT / "work" / ".opencode"
AGY_SCRATCH = ROOT / "work" / ".agy"


def opencode_bin() -> str:
    return shutil.which("opencode") or "opencode"


def agy_bin() -> str:
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "agy" / "bin" / "agy.exe"
    return str(local) if local.exists() else (shutil.which("agy") or "agy")


def run_agy(model: str, prompt: str, timeout: int = 300, agent: bool = False) -> dict:
    """agy headless, plan mode, sandboxed. The prompt goes in on stdin (stream-json), so size is not
    limited by the Windows command line. Returns {text, error, seconds}. Never raises."""
    AGY_SCRATCH.mkdir(parents=True, exist_ok=True)
    # Always plan mode + sandbox. Headless agy auto-denies tools that need permission (shell, writes, MCP);
    # the only web tool it offers there is search_web (2026-11-13 check), so agent prompts are told to use it.
    cmd = [agy_bin(), "--model", model, "--sandbox", "--mode", "plan", "--disable-slash-commands",
           "--print-timeout", f"{max(30, timeout - 15)}s",
           "--input-format", "stream-json", "--output-format", "stream-json", "--print="]
    if agent:
        prompt = ("도구 제한: MCP·브라우저·셸 도구는 쓸 수 없다. 웹 검색(search_web)만 사용하라. "
                  "검색 결과로 확인되지 않는 항목은 넣지 않는다.\n\n" + prompt)
    message = json.dumps({"event": "user", "message": {"content": prompt}}, ensure_ascii=False) + "\n"
    started = time.monotonic()
    out = {"text": "", "error": None, "seconds": 0.0}
    try:
        proc = subprocess.run(
            cmd,
            input=message,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=AGY_SCRATCH,
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

    result = None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("event") == "result":
            result = event.get("result") or {}
    if result and result.get("status") == "SUCCESS" and (result.get("response") or "").strip():
        out["text"] = result["response"].strip()
    else:
        stderr = re.sub(r"\x1b\[[0-9;]*m", "", proc.stderr or "").strip()
        out["error"] = ((result or {}).get("error") or stderr[-300:] or f"empty output (exit {proc.returncode})")[:300]
    return out


def run(model: str, prompt: str, timeout: int = 300, agent: bool = False) -> dict:
    """Return {text, error, seconds}. Never raises.

    agent=True lets the model use its tools (websearch, playwright/apify MCP) without prompts.
    """
    if model.startswith("agy/"):
        return run_agy(model[len("agy/"):], prompt, timeout=timeout, agent=agent)
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
