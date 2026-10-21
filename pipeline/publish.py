"""Git sync, commit and push with verification against origin."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .util import NO_WINDOW, ROOT

# Everything the pipeline writes. Staged with -A so renamed/removed daily files are committed too.
OUTPUT_PATHS = ["geeknews", "tech", "youtube", "github", "models", "state", "log", "pipeline/overrides.json"]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        creationflags=NO_WINDOW,
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


def sync() -> dict:
    """Pull before a run so edits made on GitHub (e.g. models/priority.txt) take effect."""
    try:
        _run(["pull", "--rebase", "--autostash", "origin", current_branch()])
        return {"error": None}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)[:300]}


def publish(paths: list[Path | str], message: str, push: bool = True) -> dict:
    """Stage the given paths (additions, edits and deletions), commit, push, verify the remote ref."""
    out = {"committed": False, "pushed": False, "commit": None, "branch": None, "error": None}
    try:
        rel = [str(Path(p).relative_to(ROOT)) if Path(p).is_absolute() else str(p) for p in paths]
        rel = [p for p in rel if (ROOT / p).exists() or git("ls-files", "--", p).stdout.strip()]
        if not rel:
            out["error"] = "no files to publish"
            return out
        _run(["add", "-A", "--", *rel])
        staged = git("diff", "--cached", "--name-only").stdout.strip()
        if not staged:
            out["note"] = "no changes to commit (content identical)"
            return out
        _run(["commit", "-m", message])
        commit = _run(["rev-parse", "HEAD"])
        branch = current_branch()
        out.update(committed=True, commit=commit, branch=branch)
        if push:
            if git("push", "origin", branch).returncode != 0:
                # Someone pushed meanwhile (e.g. a priority.txt edit on GitHub): rebase once and retry.
                _run(["pull", "--rebase", "origin", branch])
                _run(["push", "origin", branch])
                commit = _run(["rev-parse", "HEAD"])
                out["commit"] = commit
            remote = _run(["ls-remote", "origin", f"refs/heads/{branch}"]).split()[0]
            if remote != commit:
                raise RuntimeError(f"remote mismatch: local {commit[:8]} remote {remote[:8]}")
            out["pushed"] = True
        return out
    except Exception as exc:  # noqa: BLE001
        out["error"] = str(exc)[:500]
        return out


def publish_outputs(message: str, push: bool = True) -> dict:
    return publish(OUTPUT_PATHS, message, push=push)


def status() -> dict:
    return {
        "is_repo": is_repo(),
        "branch": current_branch() if is_repo() else None,
        "dirty": git("status", "--porcelain").stdout.strip().splitlines(),
        "remote": git("remote", "get-url", "origin").stdout.strip(),
    }
