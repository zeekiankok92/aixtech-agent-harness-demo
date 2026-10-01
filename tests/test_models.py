from datetime import date, timedelta

import pytest

from sgweather.features import TrainingRow, add_tomorrow_target, time_split
from sgweather.models import (
    climatology_forecast,
    compare_models,
    fit_linear,
    linear_forecast,
    rolling_mean_forecast,
)
from sgweather.parsing import load_csv


def _rows(values, start=date(2017, 1, 1)):
    return [
        TrainingRow(start + timedelta(days=i), "S", values[i], values[i + 1])
        for i in range(len(values) - 1)
    ]


def test_climatology_uses_train_targets_only():
    train, test = _rows([30, 31, 32]), _rows([40, 41])
    assert climatology_forecast(train, test) == [31.5]


def test_rolling_mean_uses_only_past_values():
    train, test = _rows([30, 31, 32]), _rows([33, 34, 35], start=date(2017, 2, 1))
    # history: train today-values 30, 31 then test 33, 34
    assert rolling_mean_forecast(train, test, window=3) == [
        pytest.approx(94 / 3),
        pytest.approx(98 / 3),
    ]


def test_rolling_mean_window_validation():
    with pytest.raises(ValueError):
        rolling_mean_forecast([], _rows([1, 2]), window=0)


def test_linear_recovers_exact_line():
    # tomorrow = 2 + 0.9 * today for every pair
    train = [
        TrainingRow(date(2017, 1, i), "S", t, 2 + 0.9 * t) for i, t in enumerate([28, 30, 33], 1)
    ]
    intercept, slope = fit_linear(train)
    assert (intercept, slope) == (pytest.approx(2), pytest.approx(0.9))
    assert linear_forecast(train, _rows([31, 0]))[0] == pytest.approx(29.9)


@pytest.mark.parametrize("train", [[], _rows([30, 31]), _rows([30, 30, 30])])
def test_linear_needs_enough_varied_data(train):
    with pytest.raises(ValueError):
        fit_linear(train)


def test_empty_inputs_rejected():
    with pytest.raises(ValueError):
        climatology_forecast([], _rows([1, 2]))
    with pytest.raises(ValueError):
        compare_models(_rows([1, 2, 3]), [])


def test_compare_on_long_synthetic_fixture():
    path = "fixtures/daily_weather_synthetic_long.csv"
    train, test = time_split(add_tomorrow_target(load_csv(path)), date(2017, 1, 1))
    scores = compare_models(train, test)
    names = [s.model for s in scores]
    assert names[0] == "persistence (baseline)" and scores[0].mae_skill_vs_persistence == 0
    assert len(names) == 4 and all(s.n == len(test) for s in scores)
    linear = next(s for s in scores if s.model.startswith("linear"))
    # the generator has mean-reverting (AR) anomalies, so a fitted line beats persistence
    assert linear.mae < scores[0].mae


def test_zero_baseline_error_gives_zero_skill():
    flat = _rows([30, 30, 30, 30])
    train = _rows([29, 30, 31])
    scores = compare_models(train, flat)
    assert scores[0].mae == 0 and all(s.mae_skill_vs_persistence == 0 for s in scores)
