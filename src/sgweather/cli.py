"""sgweather command line.

python -m sgweather report   <daily.csv>  [--cutoff YYYY-MM-DD] [--strict]
python -m sgweather compare  <daily.csv>  --cutoff YYYY-MM-DD [--window K]
python -m sgweather realtime <saved_api_response.json>
python -m sgweather demo     [--fixtures DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .baseline import evaluate_persistence
from .features import add_tomorrow_target, time_split
from .models import compare_models
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


def comparison_table(csv_path: str, cutoff: str, window: int = 3) -> str:
    rows = add_tomorrow_target(load_csv(csv_path))
    train, test = time_split(rows, date.fromisoformat(cutoff))
    scores = compare_models(train, test, window)
    lines = [
        f"train rows: {len(train)} (< {cutoff})   test rows: {len(test)} (>= {cutoff})",
        f"{'model':<26}{'MAE':>8}{'RMSE':>8}{'skill vs baseline':>20}",
    ]
    for s in scores:
        lines.append(
            f"{s.model:<26}{s.mae:>8.3f}{s.rmse:>8.3f}{s.mae_skill_vs_persistence:>+19.1%}"
        )
    return "\n".join(lines)


def _compare(args: argparse.Namespace) -> int:
    print(comparison_table(args.csv, args.cutoff, args.window))
    return 0


def _demo(args: argparse.Namespace) -> int:
    base = Path(args.fixtures)
    small = base / "daily_weather_synthetic.csv"
    long = base / "daily_weather_synthetic_long.csv"
    api = base / "realtime_air_temperature_synthetic.json"
    print("sgweather demo - ALL INPUTS ARE SYNTHETIC FIXTURES (not real observations)\n")
    quality = build_report(load_csv(small))
    print(f"[1] Data-quality checks on {small.name} ({quality.rows} rows)")
    print(f"    missing dates:   {[str(d) for d in quality.missing_dates]}")
    print(f"    duplicate dates: {[str(d) for d in quality.duplicate_dates]}")
    print(f"    sanity issues:   {len(quality.sanity_issues)}")
    for issue in quality.sanity_issues:
        print(f"      - {issue}")
    print(f"\n[2] Model comparison on {long.name} (cutoff 2017-01-01)")
    for line in comparison_table(str(long), "2017-01-01").splitlines():
        print(f"    {line}")
    with open(api, encoding="utf-8") as handle:
        summary = summarise(parse_payload(json.load(handle)))
    print(f"\n[3] data.gov.sg air-temperature payload ({api.name}, offline)")
    print(f"    {json.dumps(summary)}")
    print("\nNote: scores on synthetic data show the pipeline works, not real-world accuracy.")
    return 0


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
    cmp_ = sub.add_parser("compare", help="compare simple models against the persistence baseline")
    cmp_.add_argument("csv")
    cmp_.add_argument("--cutoff", required=True, help="test split starts at YYYY-MM-DD")
    cmp_.add_argument("--window", type=int, default=3, help="rolling-mean window (days)")
    cmp_.set_defaults(func=_compare)
    demo = sub.add_parser("demo", help="run the end-to-end demo on the bundled synthetic fixtures")
    demo.add_argument("--fixtures", default="fixtures", help="fixtures directory")
    demo.set_defaults(func=_demo)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
