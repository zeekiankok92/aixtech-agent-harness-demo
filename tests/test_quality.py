from datetime import date

from sgweather.parsing import DailyRecord, load_csv
from sgweather.quality import build_report, missing_dates, sanity_issues


def test_fixture_defects_are_all_detected(daily_csv):
    report = build_report(load_csv(daily_csv))
    assert report.rows == 28
    assert report.first_date == date(2016, 12, 18)
    assert report.last_date == date(2017, 1, 14)
    assert report.missing_dates == [date(2016, 12, 25)]
    assert report.duplicate_dates == [date(2016, 12, 24)]
    assert report.missing_by_column["highest_30_min_rainfall"] == 1
    assert report.missing_by_column["maximum_temperature"] == 1
    assert any("minimum_temperature > maximum_temperature" in s for s in report.sanity_issues)
    assert not report.ok


def test_clean_data_is_ok():
    recs = [
        DailyRecord(
            date(2017, 1, d),
            "S",
            mean_temperature=28,
            maximum_temperature=31,
            minimum_temperature=25,
            mean_wind_speed=5,
            max_wind_speed=20,
        )
        for d in (1, 2, 3)
    ]
    report = build_report(recs)
    assert report.ok
    assert report.sanity_issues == []


def test_empty_input():
    report = build_report([])
    assert report.rows == 0 and report.first_date is None
    assert missing_dates([]) == []


def test_each_sanity_rule():
    bad = DailyRecord(
        date(2017, 1, 1),
        "S",
        daily_rainfall_total=-1,
        mean_temperature=35,
        maximum_temperature=30,
        minimum_temperature=36,
        mean_wind_speed=10,
        max_wind_speed=-2,
    )
    issues = sanity_issues([bad])
    for fragment in (
        "minimum_temperature > maximum_temperature",
        "minimum_temperature > mean_temperature",
        "mean_temperature > maximum_temperature",
        "mean_wind_speed > max_wind_speed",
        "negative daily_rainfall_total",
        "negative max_wind_speed",
    ):
        assert any(fragment in i for i in issues), fragment
