# Architecture

## 1. Code: data flow inside `sgweather`

```mermaid
flowchart LR
    subgraph Inputs
        CSV["Daily CSV<br/>(same columns as WEATHER.PUBLIC.DAILY_WEATHER)<br/>fixtures = SYNTHETIC"]
        API["data.gov.sg v2 real-time<br/>air-temperature API<br/>(Open Data Licence)"]
    end
    CSV --> P["parsing.py<br/>'na' -> None"]
    P --> Q["quality.py<br/>missing values, date gaps,<br/>duplicates, sanity rules"]
    P --> F["features.py<br/>tomorrow's max temp target,<br/>chronological split"]
    F --> B["baseline.py<br/>persistence forecast,<br/>MAE / RMSE"]
    API -. "injectable fetcher<br/>(tests: JSON fixture, no network)" .-> R["realtime.py<br/>stations + readings"]
    Q --> CLI["cli.py<br/>python -m sgweather report / realtime"]
    B --> CLI
    R --> CLI
```

## 2. Process: the agent harness around the code

```mermaid
flowchart TD
    T["Task brief<br/>tasks/NNN.md<br/>(acceptance criteria, data = synthetic)"] --> A["AI coding agent<br/>follows AGENTS.md / CLAUDE.md"]
    A --> L["scripts/ci_local.sh<br/>(same gates as CI)"]
    L -->|red| A
    L -->|green| PR["Pull request<br/>+ AI-disclosure section<br/>+ commit trailers"]
    PR --> CI{"GitHub Actions gates<br/>1 ruff lint · 2 ruff format<br/>3 pytest cov>=90% · 4 PDPA guard<br/>5 gitleaks · 6 licence allow-list"}
    CI -->|red| A
    CI -->|green| H{"Human review<br/>harness/review-checklist.md"}
    H -->|changes requested| A
    H -->|approve| D["Done = CI green + human sign-off<br/>logged in docs/review-log.md<br/>& docs/ai-disclosure-log.md"]
    D --> M["Merge to main"]
    D -.-> CT["docs/cycle-time-template.md<br/>(measure, don't guess)"]
```

## Design choices
- **Stdlib-only runtime.** This keeps the dependency and licence surface small, so the
  gates have little to check and SMEs can audit it quickly.
- **Injectable I/O.** The network sits behind a function argument, which keeps
  tests deterministic and lets CI run offline.
- **Generated synthetic fixtures.** Anyone can rerun `scripts/make_fixtures.py` to
  regenerate them, and their defects are deliberate and documented.
- **Gates are cheap and local-first.** If a gate cannot run on a laptop in seconds,
  people stop running it.
