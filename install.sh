#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install --upgrade pip >/dev/null
python3 -m pip install git+https://github.com/kasimmj/ai-commit
echo "✓ ai-commit installed. Run: ai-commit --help"
