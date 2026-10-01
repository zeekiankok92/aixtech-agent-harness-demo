# AI-disclosure log

Every change that an AI tool generated or substantially drafted is listed here.
Commits also carry `AI-Assisted:` and `Human-Review:` trailers, so you can
check this log against `git log`:

```bash
git log --format='%h %ad %s%n   %(trailers:key=AI-Assisted,key=Human-Review,separator=%x20|%x20)' --date=short
```

| Date (SGT) | Commit / PR | Change | AI tool | AI share | Human reviewer | Sign-off |
|---|---|---|---|---|---|---|
| 2026-10-01 | `a8d81bc` (`sgweather` core) | Parsing, quality checks, target alignment, baseline, synthetic fixture generator, tests (task 001) | Grok Bot (AI coding agent) | Drafted all of it | Anthony Zee | Approved for publication - Anthony Zee, 2026-10-01 |
| 2026-10-01 | `b702e41` (real-time client) | data.gov.sg air-temperature client, fixture, tests, CLI (task 002) | Grok Bot (AI coding agent) | Drafted all of it | Anthony Zee | Approved for publication - Anthony Zee, 2026-10-01 |
| 2026-10-01 | `37a0e64` (harness + CI) | AGENTS.md, CLAUDE.md, templates, checklist, DoD, CI workflow, local CI script, PDPA guard, gitleaks config (task 003) | Grok Bot (AI coding agent) | Drafted all of it | Anthony Zee | Approved for publication - Anthony Zee, 2026-10-01 |
| 2026-10-01 | docs commit (README + docs) | README, docs/, previews | Grok Bot (AI coding agent) | Drafted all of it | Anthony Zee | Approved for publication - Anthony Zee, 2026-10-01 |
| 2026-10-01 | `4639c56` (models) | Climatology, rolling-mean and linear forecasters, `compare` and `demo` CLI commands, long synthetic fixture, tests | Grok Bot (AI coding agent) | Drafted all of it | Anthony Zee | Approved for publication - Anthony Zee, 2026-10-01 |
| 2026-10-01 | `7a3a281` (repo hygiene) | Dependabot, CODEOWNERS, SECURITY.md, CONTRIBUTING.md, self-hosted coverage badge plus a CI staleness check | Grok Bot (AI coding agent) | Drafted all of it | Anthony Zee | Approved for publication - Anthony Zee, 2026-10-01 |
| 2026-10-01 | enhancement-docs commit | Build walkthrough, engagement offer, sample output, cycle-time evidence generator and page, README badges and updates | Grok Bot (AI coding agent) | Drafted all of it | Anthony Zee | Approved for publication - Anthony Zee, 2026-10-01 |

**Status:** Anthony Zee approved these changes **for publication** on 2026-10-01.
That approval covers publishing the repo. It is not a recorded line-by-line code
review: no checklist findings have been logged yet (see R-001 in
[review-log.md](review-log.md)). Later changes follow the full process, which means
a checklist review is logged before sign-off.

### How to fill a row
- **AI share:** "Drafted all", "Drafted most, human edited", "Suggestions only" or "None".
  Describe the share in words. Do not make up percentages.
- **Sign-off:** only the named human edits this cell.
