"""Simple forecasters that must beat the persistence baseline to be worth using.

All are standard-library only and fully transparent:

- ``persistence``: tomorrow's max = today's max (the baseline)
- ``climatology``: tomorrow's max = mean max temperature of the training period
- ``rolling_mean_k``: tomorrow's max = mean of the last *k* observed daily maxima
- ``linear``: least-squares line, tomorrow's max ~ a + b * today's max, fitted on train only

Every model is fitted on the training split and scored on the later test split.
Nothing from the test period leaks into fitting.
"""

from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import dataclass

from .baseline import mae, persistence_forecast, rmse
from .features import TrainingRow


@dataclass(frozen=True)
class ModelScore:
    model: str
    n: int
    mae: float
    rmse: float
    mae_skill_vs_persistence: float  # 1 - MAE/MAE_persistence; > 0 means better than baseline


def climatology_forecast(train: Sequence[TrainingRow], test: Sequence[TrainingRow]) -> list[float]:
    if not train:
        raise ValueError("climatology needs a non-empty training set")
    mean = statistics.fmean(r.tomorrows_maximum_temperature for r in train)
    return [mean] * len(test)


def rolling_mean_forecast(
    train: Sequence[TrainingRow], test: Sequence[TrainingRow], window: int = 3
) -> list[float]:
    """Mean of today's and the previous ``window - 1`` observed maxima.

    History comes from rows in date order, so a forecast made on day *d* only uses
    values that were known on day *d*. Early test rows borrow history from the end
    of the training period.
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    history = [r.maximum_temperature for r in train]
    preds = []
    for row in test:
        history.append(row.maximum_temperature)
        recent = history[-window:]
        preds.append(sum(recent) / len(recent))
    return preds


def fit_linear(train: Sequence[TrainingRow]) -> tuple[float, float]:
    """Return (intercept, slope) for tomorrow_max ~ today_max, fitted on train only."""
    if len(train) < 2:
        raise ValueError("linear model needs at least 2 training rows")
    x = [r.maximum_temperature for r in train]
    y = [r.tomorrows_maximum_temperature for r in train]
    if len(set(x)) < 2:
        raise ValueError("linear model needs variation in today's max temperature")
    slope, intercept = statistics.linear_regression(x, y)
    return intercept, slope


def linear_forecast(train: Sequence[TrainingRow], test: Sequence[TrainingRow]) -> list[float]:
    intercept, slope = fit_linear(train)
    return [intercept + slope * r.maximum_temperature for r in test]


def compare_models(
    train: Sequence[TrainingRow], test: Sequence[TrainingRow], window: int = 3
) -> list[ModelScore]:
    """Score every model on ``test``. The persistence baseline comes first."""
    if not test:
        raise ValueError("test split is empty - choose an earlier cutoff")
    actual = [r.tomorrows_maximum_temperature for r in test]
    candidates = {
        "persistence (baseline)": persistence_forecast(test),
        "climatology (train mean)": climatology_forecast(train, test),
        f"rolling_mean_{window}": rolling_mean_forecast(train, test, window),
        "linear (today's max)": linear_forecast(train, test),
    }
    base_mae = mae(actual, candidates["persistence (baseline)"])
    scores = []
    for name, preds in candidates.items():
        m = mae(actual, preds)
        skill = 0.0 if base_mae == 0 else 1 - m / base_mae
        scores.append(ModelScore(name, len(test), m, rmse(actual, preds), skill))
    return scores
