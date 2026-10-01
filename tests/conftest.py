from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture
def daily_csv() -> Path:
    return FIXTURES / "daily_weather_synthetic.csv"


@pytest.fixture
def realtime_json() -> Path:
    return FIXTURES / "realtime_air_temperature_synthetic.json"
