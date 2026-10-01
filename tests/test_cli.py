import json

from sgweather.cli import main


def test_report(daily_csv, capsys):
    assert main(["report", str(daily_csv), "--cutoff", "2017-01-01"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["missing_dates"] == ["2016-12-25"]
    assert out["persistence_baseline"]["n"] > 0


def test_report_strict_fails_on_defects(daily_csv, capsys):
    assert main(["report", str(daily_csv), "--strict"]) == 1


def test_realtime(realtime_json, capsys):
    assert main(["realtime", str(realtime_json)]) == 0
    assert json.loads(capsys.readouterr().out)["stations"] == 3.0
