"""CLI entrypoint."""

import argparse
import sys
from . import __version__
from .git_io import staged_diff, staged_files, is_git_repo, commit
from .redact import redact
from .prompts import SYSTEM_EN, SYSTEM_AR, build_user_message
from .providers import ProviderConfig, call, detect_provider


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="ai-commit",
        description="Generate conventional git commit messages with AI.",
    )
    p.add_argument("--model", default="gpt-4o-mini", help="Model name (e.g. gpt-4o-mini, claude-haiku-4, llama3.2)")
    p.add_argument("--lang", default="en", choices=["en", "ar"], help="Output language")
    p.add_argument("--dry-run", action="store_true", help="Print message without committing")
    p.add_argument("--yes", "-y", action="store_true", help="Auto-accept the generated message")
    p.add_argument("--max-diff-lines", type=int, default=500, help="Cap diff size sent to model")
    p.add_argument("--regen", action="store_true", help="Skip cache, regenerate")
    p.add_argument("--version", action="version", version=f"ai-commit {__version__}")
    return p.parse_args(argv)


def confirm_loop(message: str) -> tuple[str, str]:
    """Ask user. Returns (action, message). action ∈ accept/edit/regen/cancel."""
    while True:
        sys.stderr.write("\nAccept this message? [Y/n/edit/regen]: ")
        sys.stderr.flush()
        choice = (sys.stdin.readline() or "").strip().lower()
        if choice in ("", "y", "yes"):
            return "accept", message
        if choice in ("n", "no", "cancel"):
            return "cancel", message
        if choice in ("e", "edit"):
            sys.stderr.write("Enter new message (end with empty line):\n")
            sys.stderr.flush()
            lines = []
            while True:
                line = sys.stdin.readline()
                if not line or line.strip() == "":
                    break
                lines.append(line.rstrip())
            return "accept", "\n".join(lines)
        if choice in ("r", "regen"):
            return "regen", message


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if not is_git_repo():
        print("✗ Not inside a git repository.", file=sys.stderr)
        return 2

    files = staged_files()
    if not files:
        print("✗ No staged changes. Run `git add` first.", file=sys.stderr)
        return 1

    diff = staged_diff(max_lines=args.max_diff_lines)
    diff = redact(diff)

    system = SYSTEM_AR if args.lang == "ar" else SYSTEM_EN
    user = build_user_message(diff, files)
    cfg = ProviderConfig(name=detect_provider(args.model), model=args.model)

    while True:
        try:
            print("→ Generating commit message...", file=sys.stderr)
            message = call(system, user, cfg)
        except Exception as e:
            print(f"✗ Generation failed: {e}", file=sys.stderr)
            return 3

        print("\n" + "─" * 60)
        print(message)
        print("─" * 60)

        if args.dry_run:
            return 0

        if args.yes:
            action, final = "accept", message
        else:
            action, final = confirm_loop(message)

        if action == "accept":
            return commit(final)
        if action == "cancel":
            print("Aborted.", file=sys.stderr)
            return 1
        # action == "regen" → loop


if __name__ == "__main__":
    raise SystemExit(main())
