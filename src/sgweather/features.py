"""Feature engineering: align each day with tomorrow's maximum temperature.

Equivalent to the notebook's self-join on ``DATE + 1`` that creates
``TOMORROWS_MAXIMUM_TEMPERATURE``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .parsing import DailyRecord


@dataclass(frozen=True)
class TrainingRow:
    date: date
    station: str
    maximum_temperature: float
    tomorrows_maximum_temperature: float


def add_tomorrow_target(records: list[DailyRecord]) -> list[TrainingRow]:
    """Pair each record with the next calendar day's max temperature.

    Rows are dropped when either today's or tomorrow's value is missing, or
    when tomorrow has no record (a date gap) - we never invent a target.
    """
    lookup = {
        (r.station, r.date): r.maximum_temperature
        for r in records
        if r.maximum_temperature is not None
    }
    rows: list[TrainingRow] = []
    for (station, day), today in sorted(lookup.items(), key=lambda kv: kv[0][1]):
        tomorrow = lookup.get((station, day + timedelta(days=1)))
        if tomorrow is not None:
            rows.append(TrainingRow(day, station, today, tomorrow))
    return rows


def time_split(
    rows: list[TrainingRow], cutoff: date
) -> tuple[list[TrainingRow], list[TrainingRow]]:
    """Chronological split (no shuffling - avoids look-ahead leakage)."""
    train = [r for r in rows if r.date < cutoff]
    test = [r for r in rows if r.date >= cutoff]
    return train, test
