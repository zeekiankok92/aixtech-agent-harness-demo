from datetime import date

import pytest

from sgweather.baseline import evaluate_persistence, mae, rmse
from sgweather.features import TrainingRow, add_tomorrow_target, time_split
from sgweather.parsing import DailyRecord, load_csv


def _rec(day, tmax):
    return DailyRecord(date(2017, 1, day), "S", maximum_temperature=tmax)


def test_target_alignment_skips_gaps_and_missing():
    rows = add_tomorrow_target([_rec(1, 30), _rec(2, 31), _rec(4, 33), _rec(5, None), _rec(6, 32)])
    assert rows == [TrainingRow(date(2017, 1, 1), "S", 30, 31)]


def test_time_split_is_chronological(daily_csv):
    rows = add_tomorrow_target(load_csv(daily_csv))
    train, test = time_split(rows, date(2017, 1, 1))
    assert train and test
    assert max(r.date for r in train) < date(2017, 1, 1) <= min(r.date for r in test)


def test_metrics():
    assert mae([1, 2, 3], [1, 2, 5]) == pytest.approx(2 / 3)
    assert rmse([0, 0], [3, 4]) == pytest.approx((12.5) ** 0.5)


@pytest.mark.parametrize(("a", "p"), [([], []), ([1], [1, 2])])
def test_metric_input_validation(a, p):
    with pytest.raises(ValueError):
        mae(a, p)


def test_persistence_on_toy_series():
    rows = [TrainingRow(date(2017, 1, 1), "S", 30, 31), TrainingRow(date(2017, 1, 2), "S", 31, 31)]
    result = evaluate_persistence(rows)
    assert result == {"n": 2.0, "mae": 0.5, "rmse": pytest.approx(0.5**0.5)}
