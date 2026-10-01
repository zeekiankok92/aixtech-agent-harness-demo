# Task 004 - Simple models beyond the persistence baseline, plus a CLI demo

**Owner (human):** Anthony Zee  **Agent/tool:** Grok Bot (AI coding agent)  **Risk:** Medium

## Goal
Add light, stdlib-only forecasters and compare their MAE/RMSE against the
persistence baseline on synthetic data, clearly labelled. Add a one-command CLI demo.

## Acceptance criteria
- [x] `models.py`: climatology (train mean), rolling mean (k days), linear regression on today's max (`statistics.linear_regression`)
- [x] Fit on train only; rolling history uses only past values (no look-ahead)
- [x] `sgweather compare <csv> --cutoff` prints MAE, RMSE and skill vs the baseline
- [x] `sgweather demo` runs quality checks, model comparison and API parsing on the bundled fixtures, offline
- [x] A longer clean synthetic fixture (2015-01 to 2017-06) from the existing generator; the small fixture is byte-identical
- [x] All 6 gates green, coverage >= 90 %

## Out of scope
Heavy ML dependencies (scikit-learn, statsmodels); real-world accuracy claims.

## Data
Synthetic only. Results describe the generator (AR(1) anomalies around a seasonal curve), not Singapore's climate.
