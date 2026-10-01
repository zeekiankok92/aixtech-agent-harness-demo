# Definition of Done

A change is **done** only when **all** of the following are true:

| # | Criterion | Evidence |
|---|-----------|----------|
| 1 | CI is green: ruff lint and format, pytest with coverage >= 90 %, PDPA guard, gitleaks, licence allow-list | GitHub Actions run link (or `scripts/ci_local.sh` output pasted in the PR before CI exists) |
| 2 | Every behaviour change has a test | Diff shows tests next to the code |
| 3 | A **human reviewer** has gone through `harness/review-checklist.md` and signed off | Entry in `docs/review-log.md` and an approving PR review |
| 4 | AI involvement is disclosed | Commit trailers plus a row in `docs/ai-disclosure-log.md` |
| 5 | Docs and README are updated if behaviour or usage changed | Diff |
| 6 | No personal data, no secrets, no new unapproved dependencies | Gates 4-6 plus reviewer check |

CI green alone is **not** done. Human review alone is **not** done. You need both.
