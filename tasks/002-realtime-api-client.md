# Task 002 - data.gov.sg real-time air-temperature client

**Owner (human):** Anthony Zee  **Agent/tool:** Grok Bot (AI coding agent)  **Risk:** Medium

## Goal
A thin client for `https://api-open.data.gov.sg/v2/real-time/api/air-temperature`
that parses stations and readings into flat records.

## Acceptance criteria
- [x] Injectable fetcher; tests and CI never call the network
- [x] Optional API key read only from `DATA_GOV_SG_API_KEY`, never hard-coded
- [x] Non-zero `code` raises `ApiError`
- [x] Fixture in the same shape as the live response (shape checked manually 2026-10-01), synthetic values

## Data
Synthetic only: `fixtures/realtime_air_temperature_synthetic.json`.
