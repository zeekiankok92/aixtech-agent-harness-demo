"""PDPA guard: fail if fixtures/docs look like they contain personal data.

A cheap, deliberately conservative pattern scan (NRIC/FIN-like IDs, SG phone
numbers, email addresses). It is a tripwire, not a DLP product: it exists so
that "no production personal data in the repo or agent context" is enforced
by CI rather than by memory.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = {
    "NRIC/FIN-like": re.compile(r"\b[STFGM]\d{7}[A-Z]\b"),
    "SG phone-like": re.compile(r"(?<![\d.])(?:\+65[ -]?)?[689]\d{3}[ -]?\d{4}(?![\d.])"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
}
ALLOWED_EMAILS = {"noreply@example.invalid"}
DEFAULT_PATHS = ["fixtures", "docs", "tasks", "harness", "README.md", "AGENTS.md", "CLAUDE.md"]
SUFFIXES = {".csv", ".json", ".md", ".txt", ".yml", ".yaml"}


def scan_file(path: Path) -> list[tuple[str, str]]:
    hits = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for kind, pattern in PATTERNS.items():
            for match in pattern.findall(line):
                if kind == "email" and match in ALLOWED_EMAILS:
                    continue
                hits.append((f"{path}:{lineno}", kind))
    return hits


def scan_paths(paths: list[Path]) -> list[tuple[str, str]]:
    hits = []
    for base in paths:
        files = [base] if base.is_file() else sorted(base.rglob("*"))
        for f in files:
            if f.is_file() and f.suffix in SUFFIXES:
                hits.extend(scan_file(f))
    return hits


def main(argv: list[str]) -> int:
    paths = [Path(p) for p in (argv or DEFAULT_PATHS) if Path(p).exists()]
    hits = scan_paths(paths)
    for where, kind in hits:
        print(f"PDPA guard: possible {kind} at {where}")
    print(f"PDPA guard: scanned {', '.join(map(str, paths))} - {len(hits)} finding(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
