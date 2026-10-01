# Task 003 - Agent harness, CI gates and evidence docs

**Owner (human):** Anthony Zee  **Agent/tool:** Grok Bot (AI coding agent)  **Risk:** High (CI/security). Needs a human reviewer.

## Goal
Add AGENTS.md/CLAUDE.md rules, task templates, review checklist, Definition of Done,
a GitHub Actions workflow (ruff, pytest+coverage, PDPA guard, gitleaks, licence
allow-list) mirrored by `scripts/ci_local.sh`, and the docs/ evidence trail.

## Acceptance criteria
- [x] `scripts/ci_local.sh` passes locally
- [x] Disclosure log, review log, cycle-time TEMPLATE (no fabricated metrics), architecture diagram
- [ ] Workflow observed green on GitHub. **Not done: the repo is not published yet (needs owner approval).**
