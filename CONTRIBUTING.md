# Contributing

Contributions from people and from AI coding agents go through the same process.

1. **Start from a task brief.** Copy `harness/templates/task-brief.md` to `tasks/NNN-name.md`,
   or open an issue with the *Agent task* template. Acceptance criteria must be testable.
2. **Branch and keep it small.** One task, one branch, one PR, ideally under 300 changed lines.
3. **AI agents follow [`AGENTS.md`](AGENTS.md).** Humans should read it too; the rules on data and secrets apply to everyone.
4. **Run the gates locally.**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements-dev.txt && pip install -e .
   scripts/ci_local.sh   # needs the gitleaks binary on PATH
   ```
   This also refreshes `docs/badges/coverage.svg`. Commit the badge if it changed.
5. **Disclose AI use.** Add these commit trailers:
   ```text
   AI-Assisted: yes (<tool/model>) | no
   Human-Review: pending | approved by <name>, <date>
   ```
   Then add a row to [`docs/ai-disclosure-log.md`](docs/ai-disclosure-log.md) and fill in the PR template's AI section.
6. **Review.** A CODEOWNER goes through [`harness/review-checklist.md`](harness/review-checklist.md)
   and logs the outcome in [`docs/review-log.md`](docs/review-log.md).
7. **Done = CI green + human review.** See [`harness/definition-of-done.md`](harness/definition-of-done.md).

### Data rules (PDPA)
Use synthetic fixtures (`scripts/make_fixtures.py`) or public open data only. Never put
personal or production data in code, fixtures, issues, PRs or AI prompts.

### Licence
By contributing you agree that your contribution is licensed under the [MIT licence](LICENSE).
