"""Client for the public data.gov.sg real-time air-temperature API.

Endpoint: https://api-open.data.gov.sg/v2/real-time/api/air-temperature
Data is published under the Singapore Open Data Licence. An API key is
optional; if you use one, read it from the environment (``DATA_GOV_SG_API_KEY``)
- never hard-code it, and never paste it into an agent prompt.

The HTTP call is injectable so tests (and CI) never touch the network.
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

BASE_URL = "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"

Fetcher = Callable[[str, dict[str, str]], dict]


@dataclass(frozen=True)
class StationReading:
    station_id: str
    station_name: str
    latitude: float
    longitude: float
    timestamp: str
    value: float
    unit: str


class ApiError(RuntimeError):
    """Raised when the API returns a non-zero ``code``."""


def build_url(date: str | None = None, pagination_token: str | None = None) -> str:
    params = {}
    if date:
        params["date"] = date
    if pagination_token:
        params["paginationToken"] = pagination_token
    return BASE_URL + ("?" + urllib.parse.urlencode(params) if params else "")


def default_headers(env: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ if env is None else env
    headers = {"Accept": "application/json", "User-Agent": "sgweather-demo/0.1"}
    key = env.get("DATA_GOV_SG_API_KEY")
    if key:
        headers["x-api-key"] = key
    return headers


def urllib_fetcher(url: str, headers: dict[str, str]) -> dict:  # pragma: no cover - network
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def parse_payload(payload: dict) -> list[StationReading]:
    """Flatten the API payload into one ``StationReading`` per station/timestamp."""
    if payload.get("code", 0) != 0:
        raise ApiError(payload.get("errorMsg") or f"API error code {payload.get('code')}")
    data = payload.get("data") or {}
    unit = data.get("readingUnit", "")
    stations = {s["id"]: s for s in data.get("stations", [])}
    readings: list[StationReading] = []
    for block in data.get("readings", []):
        for item in block.get("data", []):
            station = stations.get(item["stationId"], {})
            location = station.get("location", {})
            readings.append(
                StationReading(
                    station_id=item["stationId"],
                    station_name=station.get("name", "unknown"),
                    latitude=float(location.get("latitude", "nan")),
                    longitude=float(location.get("longitude", "nan")),
                    timestamp=block.get("timestamp", ""),
                    value=float(item["value"]),
                    unit=unit,
                )
            )
    return readings


def fetch_air_temperature(
    date: str | None = None, fetcher: Fetcher = urllib_fetcher
) -> list[StationReading]:
    return parse_payload(fetcher(build_url(date), default_headers()))


def summarise(readings: list[StationReading]) -> dict[str, float]:
    if not readings:
        return {"stations": 0.0}
    values = [r.value for r in readings]
    return {
        "stations": float(len({r.station_id for r in readings})),
        "min": min(values),
        "max": max(values),
        "mean": round(sum(values) / len(values), 2),
    }
