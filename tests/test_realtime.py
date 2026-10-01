import json

import pytest

from sgweather.realtime import (
    BASE_URL,
    ApiError,
    build_url,
    default_headers,
    fetch_air_temperature,
    parse_payload,
    summarise,
)


def test_build_url():
    assert build_url() == BASE_URL
    assert build_url("2026-01-15") == BASE_URL + "?date=2026-01-15"
    assert "paginationToken=abc" in build_url(pagination_token="abc")


def test_api_key_only_from_env():
    assert "x-api-key" not in default_headers({})
    assert default_headers({"DATA_GOV_SG_API_KEY": "dummy"})["x-api-key"] == "dummy"


def test_parse_fixture(realtime_json):
    readings = parse_payload(json.loads(realtime_json.read_text()))
    assert len(readings) == 5
    first = readings[0]
    assert (first.station_id, first.value, first.unit) == ("SYN01", 31.2, "deg C")
    assert summarise(readings) == {"stations": 3.0, "min": 30.4, "max": 32.0, "mean": 31.08}


def test_fetch_uses_injected_fetcher_no_network(realtime_json, monkeypatch):
    monkeypatch.delenv("DATA_GOV_SG_API_KEY", raising=False)
    calls = []

    def fake(url, headers):
        calls.append((url, headers))
        return json.loads(realtime_json.read_text())

    readings = fetch_air_temperature("2026-01-15", fetcher=fake)
    assert len(readings) == 5
    assert calls[0][0].endswith("date=2026-01-15")


def test_api_error_and_unknown_station():
    with pytest.raises(ApiError, match="bad"):
        parse_payload({"code": 4, "errorMsg": "bad"})
    readings = parse_payload(
        {
            "code": 0,
            "data": {"readings": [{"timestamp": "t", "data": [{"stationId": "X", "value": 1}]}]},
        }
    )
    assert readings[0].station_name == "unknown"
    assert summarise([]) == {"stations": 0.0}
