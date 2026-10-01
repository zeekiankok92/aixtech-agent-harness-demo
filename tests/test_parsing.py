from datetime import date

import pytest

from sgweather.parsing import load_csv, parse_rows, to_float


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("31.2", 31.2),
        (" 0 ", 0.0),
        ("na", None),
        ("NA", None),
        ("", None),
        (None, None),
        ("x", None),
    ],
)
def test_to_float_mirrors_sql_cleaning(raw, expected):
    assert to_float(raw) == expected


def test_parse_rows_is_case_insensitive():
    [rec] = parse_rows([{"Date": "2017-01-01", "Station": "S", "Maximum_Temperature": "32"}])
    assert rec.date == date(2017, 1, 1)
    assert rec.maximum_temperature == 32.0
    assert rec.mean_wind_speed is None


def test_load_fixture_skips_comment_banner(daily_csv):
    records = load_csv(daily_csv)
    assert len(records) == 28
    assert records[3].highest_30_min_rainfall is None
