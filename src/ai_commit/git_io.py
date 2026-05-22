"""Git interaction helpers."""

import subprocess
from pathlib import Path


def staged_diff(max_lines: int = 500) -> str:
    """Return the staged diff, capped to max_lines."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--no-color"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git diff failed: {result.stderr.strip()}")

    lines = result.stdout.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines.append(f"... [truncated to {max_lines} lines]")
    return "\n".join(lines)


def staged_files() -> list[str]:
    """List files in the index."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=False,
    )
    return [f for f in result.stdout.splitlines() if f.strip()]


def is_git_repo() -> bool:
    return Path(".git").exists() or _in_git_tree()


def _in_git_tree() -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def commit(message: str) -> int:
    """Run `git commit -m <message>`. Returns exit code."""
    return subprocess.run(["git", "commit", "-m", message]).returncode
