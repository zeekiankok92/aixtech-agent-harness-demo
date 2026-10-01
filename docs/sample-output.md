# Sample output: `python -m sgweather demo`

> Captured verbatim from a local run on 2026-10-01 (SGT). **All inputs are synthetic fixtures.** The scores describe the fixture generator (AR(1) anomalies around a seasonal curve), not real Singapore weather or any model's real-world accuracy.

```text
$ python -m sgweather demo
sgweather demo - ALL INPUTS ARE SYNTHETIC FIXTURES (not real observations)

[1] Data-quality checks on daily_weather_synthetic.csv (28 rows)
    missing dates:   ['2016-12-25']
    duplicate dates: ['2016-12-24']
    sanity issues:   3
      - 2017-01-03 Synthetic Station A: minimum_temperature > maximum_temperature
      - 2017-01-03 Synthetic Station A: minimum_temperature > mean_temperature
      - 2017-01-03 Synthetic Station A: mean_temperature > maximum_temperature

[2] Model comparison on daily_weather_synthetic_long.csv (cutoff 2017-01-01)
    train rows: 731 (< 2017-01-01)   test rows: 180 (>= 2017-01-01)
    model                          MAE    RMSE   skill vs baseline
    persistence (baseline)       0.853   1.075              +0.0%
    climatology (train mean)     0.949   1.168             -11.2%
    rolling_mean_3               0.870   1.118              -2.0%
    linear (today's max)         0.751   0.956             +12.0%

[3] data.gov.sg air-temperature payload (realtime_air_temperature_synthetic.json, offline)
    {"stations": 3.0, "min": 30.4, "max": 32.0, "mean": 31.08}

Note: scores on synthetic data show the pipeline works, not real-world accuracy.
```

## Reading the comparison
- **skill vs baseline** = 1 - MAE(model) / MAE(persistence). Positive means the model beats "tomorrow = today".
- On this synthetic series, only the linear model beats the baseline. Climatology and the 3-day rolling mean do worse. That is useful: a simpler-looking idea is not automatically better, and the baseline catches it.
- Reproduce: `python scripts/make_fixtures.py && python -m sgweather demo`.
