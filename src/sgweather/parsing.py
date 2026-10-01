"""Parse daily weather records.

Mirrors the cleaning rule used in the Snowflake weather starter
(``TRY_TO_DOUBLE(NULLIF(x, 'na'))``): the literal string ``na`` (and blanks or
non-numeric junk) become ``None`` instead of crashing the pipeline.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from pathlib import Path

NUMERIC_FIELDS = (
    "daily_rainfall_total",
    "highest_30_min_rainfall",
    "highest_60_min_rainfall",
    "highest_120_min_rainfall",
    "mean_temperature",
    "maximum_temperature",
    "minimum_temperature",
    "mean_wind_speed",
    "max_wind_speed",
)


@dataclass(frozen=True)
class DailyRecord:
    """One station-day of observations. Missing values are ``None``."""

    date: date
    station: str
    daily_rainfall_total: float | None = None
    highest_30_min_rainfall: float | None = None
    highest_60_min_rainfall: float | None = None
    highest_120_min_rainfall: float | None = None
    mean_temperature: float | None = None
    maximum_temperature: float | None = None
    minimum_temperature: float | None = None
    mean_wind_speed: float | None = None
    max_wind_speed: float | None = None


def to_float(raw: str | None) -> float | None:
    """Convert a raw cell to float; ``'na'``, blanks and junk become ``None``."""
    if raw is None:
        return None
    text = raw.strip()
    if text == "" or text.lower() == "na":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_rows(rows: Iterable[dict[str, str]]) -> list[DailyRecord]:
    """Parse dict rows (case-insensitive headers) into ``DailyRecord`` objects."""
    records: list[DailyRecord] = []
    for row in rows:
        norm = {k.strip().lower(): v for k, v in row.items() if k is not None}
        values = {field: to_float(norm.get(field)) for field in NUMERIC_FIELDS}
        records.append(
            DailyRecord(
                date=date.fromisoformat(norm["date"].strip()),
                station=norm.get("station", "").strip(),
                **values,
            )
        )
    return records


def load_csv(path: str | Path) -> list[DailyRecord]:
    """Load a daily weather CSV (same columns as WEATHER.PUBLIC.DAILY_WEATHER)."""
    with open(path, newline="", encoding="utf-8") as handle:
        lines = (line for line in handle if not line.startswith("#"))
        return parse_rows(csv.DictReader(lines))
