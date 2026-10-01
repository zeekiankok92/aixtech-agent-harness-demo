# AIxTech demo: an AI-agent harness on a Singapore weather starter

> **What this is:** a small, public reference repo that shows *how* a team can let
> AI coding agents write code **safely**: rules for the agent, automatic quality
> gates, a human sign-off and a written trail of what the AI did.
> The weather code is deliberately small. The process around it is what the repo demonstrates.

[![CI](https://img.shields.io/badge/CI-ruff%20%7C%20pytest%E2%89%A590%25%20%7C%20gitleaks%20%7C%20licences-informational)](.github/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Licence](https://img.shields.io/badge/licence-MIT-green)

## Who it is for
Singapore SMEs and small tech teams who want to use AI coding assistants
(Claude Code, Cursor, Copilot and others) but need answers to:

- *How do we stop the AI shipping broken or insecure code?* Six automatic CI gates.
- *How do we keep customer data out of AI tools (PDPA)?* Agent rules, synthetic fixtures and a CI tripwire.
- *Who is accountable?* A named human reviewer signs off every change. That review is part of the Definition of Done.
- *Can we prove what the AI did?* Commit trailers, an AI-disclosure log and a review log.
- *Is it actually faster?* A before/after cycle-time **template**, so you can measure that on your own work.

## What it demonstrates

| Harness piece | File(s) |
|---|---|
| Agent rules (one source of truth) | [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md) |
| Task briefs with testable acceptance criteria | [`harness/templates/`](harness/templates), [`tasks/`](tasks), [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE) |
| Human review checklist | [`harness/review-checklist.md`](harness/review-checklist.md) |
| **Definition of Done = CI green + human review** | [`harness/definition-of-done.md`](harness/definition-of-done.md) |
| CI gates (GitHub Actions) | [`.github/workflows/ci.yml`](.github/workflows/ci.yml) |
| Same gates, run locally | [`scripts/ci_local.sh`](scripts/ci_local.sh) |
| PR template with AI-disclosure section | [`.github/pull_request_template.md`](.github/pull_request_template.md) |
| AI-disclosure trail | [`docs/ai-disclosure-log.md`](docs/ai-disclosure-log.md) plus `AI-Assisted:` commit trailers |
| Review log | [`docs/review-log.md`](docs/review-log.md) |
| Cycle-time measurement (template) | [`docs/cycle-time-template.md`](docs/cycle-time-template.md) |
| Architecture (mermaid) | [`docs/architecture.md`](docs/architecture.md) |

### The six gates
1. **ruff lint**: style, bugs and security lint rules (`S` = bandit-style checks)
2. **ruff format**: one formatting style, so diffs only show real changes
3. **pytest with coverage of 90 % or more**: the build fails below the threshold
4. **PDPA guard** (`scripts/check_pdpa.py`): fails on NRIC/FIN-like IDs, SG phone numbers or emails in fixtures and docs
5. **gitleaks**: secret scan of the working tree and the full git history
6. **Licence allow-list** (`pip-licenses`): only permissive licences (MIT, BSD, Apache, ISC, PSF, MPL-2.0)

```mermaid
flowchart LR
    T[Task brief] --> A[AI agent<br/>AGENTS.md] --> G{6 CI gates} -->|green| H{Human review} -->|approve| D[Done + logged]
    G -->|red| A
    H -->|changes| A
```

## The work product: `sgweather`
This is a stdlib-only Python package. It is adapted from a Snowflake ML course weather starter
(data exploration and model-training notebooks):

- `parsing.py`: loads daily station records and turns `'na'` into missing values (mirrors `TRY_TO_DOUBLE(NULLIF(x,'na'))`)
- `quality.py`: missing values per column, missing dates, duplicate dates and physical sanity rules (min > max, mean wind > max wind, negative rain)
- `features.py`: builds the "tomorrow's maximum temperature" target without inventing values across gaps, plus a chronological train/test split
- `baseline.py`: persistence forecast (tomorrow = today) with MAE/RMSE. A fancier model has to beat this yardstick to be worth its complexity
- `realtime.py`: client for the public [data.gov.sg](https://data.gov.sg) v2 real-time **air-temperature** API (Singapore Open Data Licence). Network access sits behind an injectable fetcher, so tests run offline

## Run it (about 2 minutes)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt && pip install -e .

# the demo
python -m sgweather report fixtures/daily_weather_synthetic.csv --cutoff 2017-01-01
python -m sgweather realtime fixtures/realtime_air_temperature_synthetic.json

# all CI gates, locally (needs the gitleaks binary on PATH)
scripts/ci_local.sh
```

Optional, live data: the code below calls the public API directly. An API key is optional. If you
have one, export `DATA_GOV_SG_API_KEY` and never commit it.
```python
from sgweather.realtime import fetch_air_temperature, summarise

print(summarise(fetch_air_temperature()))
```

Sample output on the **synthetic** fixture. The fixture has injected defects, and the baseline numbers
say nothing about real Singapore weather:
```text
"missing_dates": ["2016-12-25"], "duplicate_dates": ["2016-12-24"],
"sanity_issues": ["2017-01-03 Synthetic Station A: minimum_temperature > maximum_temperature", ...],
"persistence_baseline": {"n": 13.0, "mae": 2.285, "rmse": 3.403}
```

## PDPA note: no production personal data in agent context
- The repo contains **only synthetic data**, generated by `scripts/make_fixtures.py` and labelled as such, plus
  references to **public open data**. It holds no customer, employee or personal data.
- `AGENTS.md` forbids pasting or loading production or personal data (names, NRIC/FIN, phone numbers, emails,
  addresses, customer records) into prompts, code, logs or fixtures. Whatever an AI tool sees may leave your
  environment, depending on the vendor's terms.
- CI gate 4 is a **tripwire**, not a data-loss-prevention product. Real client projects also need access
  controls, vendor due diligence (data residency and retention), a data-protection impact view, and
  the client's own DPO sign-off.
- This repo is a demonstration and is not legal advice.

## Honesty notes
- **No client claims or performance numbers.** This repo has not been used on a client engagement. The
  cycle-time page is an empty **template**, to be filled with your own measured data.
- **Built with AI assistance:** the initial code and docs were drafted by an AI coding agent. Anthony Zee approved
  them **for publication** on 2026-10-01. See [`docs/ai-disclosure-log.md`](docs/ai-disclosure-log.md) and
  [`docs/review-log.md`](docs/review-log.md). Line-by-line checklist reviews are logged separately for later changes.
- **Status:** `scripts/ci_local.sh` passes locally, and the same gates are defined for GitHub Actions in `.github/workflows/ci.yml`.

## Licence
[MIT](LICENSE) © 2026 Anthony Zee. Weather data from data.gov.sg is under the
[Singapore Open Data Licence](https://data.gov.sg/open-data-licence).
