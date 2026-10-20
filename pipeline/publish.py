"""Git commit and push with verification against origin."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .util import ROOT


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _run(args: list[str]) -> str:
    result = git(*args)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {(result.stderr or result.stdout).strip()[:500]}")
    return result.stdout.strip()


def is_repo() -> bool:
    return git("rev-parse", "--is-inside-work-tree").returncode == 0


def current_branch() -> str:
    return _run(["rev-parse", "--abbrev-ref", "HEAD"])


def publish(paths: list[Path], message: str, push: bool = True) -> dict:
    """Stage only the given files, commit, push, and verify the remote ref."""
    out = {"committed": False, "pushed": False, "commit": None, "branch": None, "error": None}
    try:
        rel = [str(p.relative_to(ROOT)) for p in paths if p.exists()]
        if not rel:
            out["error"] = "no files to publish"
            return out
        _run(["add", "--", *rel])
        staged = git("diff", "--cached", "--name-only").stdout.strip()
        if not staged:
            out["error"] = "nothing staged (content unchanged)"
            return out
        _run(["commit", "-m", message])
        commit = _run(["rev-parse", "HEAD"])
        branch = current_branch()
        out.update(committed=True, commit=commit, branch=branch)
        if push:
            _run(["push", "origin", branch])
            remote = _run(["ls-remote", "origin", f"refs/heads/{branch}"]).split()[0]
            if remote != commit:
                raise RuntimeError(f"remote mismatch: local {commit[:8]} remote {remote[:8]}")
            out["pushed"] = True
        return out
    except Exception as exc:  # noqa: BLE001
        out["error"] = str(exc)[:500]
        return out


def status() -> dict:
    return {
        "is_repo": is_repo(),
        "branch": current_branch() if is_repo() else None,
        "dirty": git("status", "--porcelain").stdout.strip().splitlines(),
        "remote": git("remote", "get-url", "origin").stdout.strip(),
    }
