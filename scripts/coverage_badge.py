"""Write (or check) docs/badges/coverage.svg from coverage.xml. No third-party service.

python scripts/coverage_badge.py            # regenerate the badge
python scripts/coverage_badge.py --check    # fail if the badge is > 1 point off
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET  # noqa: S405 - parsing our own coverage.xml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BADGE = ROOT / "docs" / "badges" / "coverage.svg"
TOLERANCE = 1.0  # Python versions can count branches slightly differently

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="104" height="20" role="img" \
aria-label="coverage: {pct}%"><title>coverage: {pct}%</title>
<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/>\
<stop offset="1" stop-opacity=".1"/></linearGradient>
<clipPath id="r"><rect width="104" height="20" rx="3" fill="#fff"/></clipPath>
<g clip-path="url(#r)"><rect width="61" height="20" fill="#555"/>\
<rect x="61" width="43" height="20" fill="{color}"/>\
<rect width="104" height="20" fill="url(#s)"/></g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" \
font-size="11"><text x="31" y="14">coverage</text><text x="81.5" y="14">{pct}%</text></g>
</svg>
"""


def total_percent(xml_path: Path) -> float:
    root = ET.parse(xml_path).getroot()  # noqa: S314 - trusted local file
    covered = int(root.get("lines-covered", 0)) + int(root.get("branches-covered", 0))
    valid = int(root.get("lines-valid", 0)) + int(root.get("branches-valid", 0))
    return 100.0 * covered / valid if valid else 0.0


def color(pct: float) -> str:
    return "#4c1" if pct >= 90 else "#dfb317" if pct >= 75 else "#e05d44"


def main(argv: list[str]) -> int:
    pct = total_percent(ROOT / "coverage.xml")
    shown = str(int(pct))  # floor, so 99.75 % shows as 99 %, never rounded up to 100
    if "--check" in argv:
        match = re.search(r"coverage: (\d+)%", BADGE.read_text(encoding="utf-8"))
        badge = float(match.group(1)) if match else -1.0
        ok = abs(badge - pct) <= TOLERANCE
        print(f"coverage badge {badge:.0f}% vs measured {pct:.2f}% -> {'ok' if ok else 'STALE'}")
        return 0 if ok else 1
    BADGE.parent.mkdir(parents=True, exist_ok=True)
    BADGE.write_text(SVG.format(pct=shown, color=color(pct)), encoding="utf-8")
    print(f"wrote {BADGE.relative_to(ROOT)} ({shown}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
