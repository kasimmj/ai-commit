"""Redact secrets in diffs before sending to a model."""

import re


SECRET_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"sk-[A-Za-z0-9]{32,}"), "<OPENAI_KEY>"),
    (re.compile(r"sk-ant-[A-Za-z0-9-_]{40,}"), "<ANTHROPIC_KEY>"),
    (re.compile(r"ghp_[A-Za-z0-9]{36,}"), "<GITHUB_TOKEN>"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{80,}"), "<GITHUB_PAT>"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "<AWS_ACCESS_KEY>"),
    (re.compile(r"(?i)aws_secret[^=]*=\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?"), "AWS_SECRET=<REDACTED>"),
    (re.compile(r"(?i)(password|passwd|pwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]{6,}['\"]"), r"\1=<REDACTED>"),
    (re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+PRIVATE KEY-----"), "<PRIVATE_KEY>"),
]


def redact(text: str) -> str:
    """Replace secret-looking strings with placeholders."""
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text
