# Human review checklist (AI-assisted changes)

Copy this into the PR review or `docs/review-log.md` and tick each item.

## Intent
- [ ] The change does what the task brief asked: no more, no less (no scope creep).
- [ ] I can explain the change in my own words without the AI summary.

## Correctness
- [ ] I read every changed line, not just the summary.
- [ ] Edge cases are covered: missing values (`na`), empty input, date gaps, duplicates.
- [ ] Tests assert behaviour, not implementation. A test that only mirrors the code is not a test.
- [ ] No hallucinated APIs, parameters or library functions. I checked docs for anything unfamiliar.

## Safety and compliance
- [ ] No personal data or production data in code, fixtures, prompts or logs (PDPA).
- [ ] No secrets. Config comes from the environment.
- [ ] No new dependencies, or each new one is justified and passes the licence gate.
- [ ] CI gates, thresholds and harness files were not weakened.

## Honesty
- [ ] Numbers in docs or README trace to a recorded command, or are marked TEMPLATE/TBD.
- [ ] The AI-disclosure entry matches what actually happened.

## Decision
- [ ] Approve  - [ ] Request changes  - Reviewer: ______  Date: ______
