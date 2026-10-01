"""Data-quality checks (ported from the 030202 data-exploration notebook)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta

from .parsing import NUMERIC_FIELDS, DailyRecord


@dataclass
class QualityReport:
    rows: int
    first_date: date | None
    last_date: date | None
    missing_by_column: dict[str, int]
    missing_dates: list[date]
    duplicate_dates: list[date]
    sanity_issues: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when there are no gaps, duplicates or sanity violations."""
        return not (self.missing_dates or self.duplicate_dates or self.sanity_issues)


def missing_by_column(records: list[DailyRecord]) -> dict[str, int]:
    return {f: sum(1 for r in records if getattr(r, f) is None) for f in NUMERIC_FIELDS}


def missing_dates(records: list[DailyRecord]) -> list[date]:
    """Calendar dates between the first and last record that have no row."""
    if not records:
        return []
    present = {r.date for r in records}
    start, end = min(present), max(present)
    gaps = []
    day = start
    while day <= end:
        if day not in present:
            gaps.append(day)
        day += timedelta(days=1)
    return gaps


def duplicate_dates(records: list[DailyRecord]) -> list[date]:
    counts = Counter((r.station, r.date) for r in records)
    return sorted({d for (_, d), n in counts.items() if n > 1})


def sanity_issues(records: list[DailyRecord]) -> list[str]:
    """Physically impossible combinations, e.g. min temperature above max."""
    issues: list[str] = []
    for r in records:
        tag = f"{r.date.isoformat()} {r.station}"
        lo, mean, hi = r.minimum_temperature, r.mean_temperature, r.maximum_temperature
        if lo is not None and hi is not None and lo > hi:
            issues.append(f"{tag}: minimum_temperature > maximum_temperature")
        if lo is not None and mean is not None and lo > mean:
            issues.append(f"{tag}: minimum_temperature > mean_temperature")
        if mean is not None and hi is not None and mean > hi:
            issues.append(f"{tag}: mean_temperature > maximum_temperature")
        if (
            r.mean_wind_speed is not None
            and r.max_wind_speed is not None
            and r.mean_wind_speed > r.max_wind_speed
        ):
            issues.append(f"{tag}: mean_wind_speed > max_wind_speed")
        for name in ("daily_rainfall_total", "mean_wind_speed", "max_wind_speed"):
            value = getattr(r, name)
            if value is not None and value < 0:
                issues.append(f"{tag}: negative {name}")
    return issues


def build_report(records: list[DailyRecord]) -> QualityReport:
    dates = [r.date for r in records]
    return QualityReport(
        rows=len(records),
        first_date=min(dates) if dates else None,
        last_date=max(dates) if dates else None,
        missing_by_column=missing_by_column(records),
        missing_dates=missing_dates(records),
        duplicate_dates=duplicate_dates(records),
        sanity_issues=sanity_issues(records),
    )
