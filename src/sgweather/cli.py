"""Command line: ``python -m sgweather report <csv>`` / ``python -m sgweather realtime <json>``."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from .baseline import evaluate_persistence
from .features import add_tomorrow_target, time_split
from .parsing import load_csv
from .quality import build_report
from .realtime import parse_payload, summarise


def _report(args: argparse.Namespace) -> int:
    records = load_csv(args.csv)
    quality = build_report(records)
    rows = add_tomorrow_target(records)
    out: dict = {
        "rows": quality.rows,
        "date_range": [str(quality.first_date), str(quality.last_date)],
        "missing_by_column": {k: v for k, v in quality.missing_by_column.items() if v},
        "missing_dates": [str(d) for d in quality.missing_dates],
        "duplicate_dates": [str(d) for d in quality.duplicate_dates],
        "sanity_issues": quality.sanity_issues,
        "training_rows": len(rows),
    }
    if args.cutoff:
        _, test = time_split(rows, date.fromisoformat(args.cutoff))
        rows = test
    if rows:
        out["persistence_baseline"] = {
            k: round(v, 3) for k, v in evaluate_persistence(rows).items()
        }
    print(json.dumps(out, indent=2))
    return 0 if quality.ok or not args.strict else 1


def _realtime(args: argparse.Namespace) -> int:
    with open(args.json, encoding="utf-8") as handle:
        readings = parse_payload(json.load(handle))
    print(json.dumps(summarise(readings), indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sgweather", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rep = sub.add_parser("report", help="data-quality + baseline report for a daily CSV")
    rep.add_argument("csv")
    rep.add_argument("--cutoff", help="evaluate baseline only on dates >= YYYY-MM-DD")
    rep.add_argument("--strict", action="store_true", help="exit 1 on any quality issue")
    rep.set_defaults(func=_report)
    rt = sub.add_parser("realtime", help="summarise a saved data.gov.sg air-temperature JSON")
    rt.add_argument("json")
    rt.set_defaults(func=_realtime)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
