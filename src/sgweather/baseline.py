"""A transparent persistence baseline and error metrics.

"Tomorrow's max = today's max" is the yardstick any fancier model (the course
uses KNN imputation + ARIMAX) must beat before it earns its complexity.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from .features import TrainingRow


def persistence_forecast(rows: Sequence[TrainingRow]) -> list[float]:
    return [r.maximum_temperature for r in rows]


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _check(actual, predicted)
    return sum(abs(a - p) for a, p in zip(actual, predicted, strict=True)) / len(actual)


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _check(actual, predicted)
    squared = sum((a - p) ** 2 for a, p in zip(actual, predicted, strict=True))
    return math.sqrt(squared / len(actual))


def evaluate_persistence(rows: Sequence[TrainingRow]) -> dict[str, float]:
    actual = [r.tomorrows_maximum_temperature for r in rows]
    predicted = persistence_forecast(rows)
    return {"n": float(len(rows)), "mae": mae(actual, predicted), "rmse": rmse(actual, predicted)}


def _check(actual: Sequence[float], predicted: Sequence[float]) -> None:
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    if not actual:
        raise ValueError("cannot score an empty series")
