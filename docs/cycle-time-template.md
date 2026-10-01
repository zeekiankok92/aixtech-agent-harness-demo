# Before/after cycle-time - TEMPLATE

> **TEMPLATE. This page contains no measured data.** Every cell is blank on purpose.
> Fill it in only with times you actually measured on your own team's work. Do not
> estimate them or copy numbers from vendor marketing.

## What we measure
| Metric | Definition | Source |
|---|---|---|
| Lead time | Task brief created -> change merged to `main` | brief date and merge commit time |
| Coding time | First commit on branch -> PR opened | `git log` / PR timestamps |
| Review wait | PR opened -> first human review | PR timeline |
| Review time | Minutes the reviewer spent (self-reported) | `docs/review-log.md` |
| Rework loops | Number of "request changes" rounds | PR reviews |
| Escaped defects | Bugs found after merge that trace back to the change | issue tracker |

## Baseline (before the harness): same task types, done the usual way
| Task ID | Type | Lead time | Coding time | Review wait | Review time | Rework loops | Escaped defects |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |

## With the harness (AI agent plus gates plus human review)
| Task ID | Type | Lead time | Coding time | Review wait | Review time | Rework loops | Escaped defects |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |

## Comparison (fill in only once you have at least 5 tasks on each side)
| Metric | Before (median) | After (median) | Change | Notes / confounders |
|---|---|---|---|---|
| Lead time | | | | |
| Review time | | | | |
| Rework loops | | | | |
| Escaped defects | | | | |

### Honesty rules
- Compare similar task types and sizes. Write down anything that differs between the
  two sides (team, season, task mix).
- Report medians and the number of tasks (n). If n < 5, say "not enough data".
- Count escaped defects and review time as well as speed. If the change is faster
  but breaks more, it is not an improvement.

### Helper: pull commit timestamps
```bash
git log --reverse --format='%h %ad %s' --date=iso-strict main
```
