#!/usr/bin/env bash
# Run exactly the same gates as .github/workflows/ci.yml, locally.
# Usage: scripts/ci_local.sh            (expects tools on PATH or in .venv)
#        GITLEAKS=/path/to/gitleaks scripts/ci_local.sh
set -euo pipefail
cd "$(dirname "$0")/.."
[ -d .venv ] && export PATH="$PWD/.venv/bin:$PATH"
GITLEAKS="${GITLEAKS:-gitleaks}"
ALLOWED="MIT;BSD;Apache;ISC;Python Software Foundation;PSF;MPL-2.0;Mozilla Public License 2.0"

step() { printf '\n=== %s ===\n' "$1"; }

step "1/6 ruff lint";            ruff check .
step "2/6 ruff format check";    ruff format --check .
step "3/6 pytest + coverage>=90"; pytest
step "4/6 PDPA personal-data guard"; python scripts/check_pdpa.py
step "5/6 secret scan (gitleaks)"
if command -v "$GITLEAKS" >/dev/null 2>&1; then
  if git rev-parse --git-dir >/dev/null 2>&1; then
    "$GITLEAKS" git --redact --no-banner .
  fi
  "$GITLEAKS" dir --redact --no-banner .
else
  echo "gitleaks not found - install from https://github.com/gitleaks/gitleaks/releases" >&2
  exit 1
fi
step "6/6 dependency licence allow-list (pip-licenses)"
pip-licenses --partial-match --ignore-packages sgweather --allow-only="$ALLOWED"

printf '\nALL GATES PASSED - remember: Definition of Done also needs a human review sign-off.\n'
