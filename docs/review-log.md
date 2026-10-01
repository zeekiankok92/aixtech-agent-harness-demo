# Review log

One entry per reviewed PR or change set. Each entry uses
[`harness/review-checklist.md`](../harness/review-checklist.md).

---

## Entry format (copy this)

```text
### R-NNN - <PR/commit> - <short title>
Reviewer: <name>          Date (SGT): <YYYY-MM-DD>
AI-assisted: yes/no (<tool>)   Risk: low/medium/high
CI: green/red (<run link or ci_local output>)
Checklist: intent [ ] correctness [ ] safety/PDPA [ ] honesty [ ]
Findings:
  1. <file:line> - <issue> - <severity> - <resolved how>
Decision: Approve / Request changes
Time spent reviewing: <minutes, measured, or leave blank>
```

---

## R-000 - ILLUSTRATIVE EXAMPLE (not a real review)

> This entry shows the level of detail we expect. It is a **worked example** written
> to illustrate the format. It does not record a review that actually happened.

```text
### R-000 - example PR - "add duplicate-date check"
Reviewer: <example reviewer>   Date (SGT): <example>
AI-assisted: yes (coding agent)  Risk: medium
CI: green
Checklist: intent [x] correctness [x] safety/PDPA [x] honesty [x]
Findings:
  1. quality.py - duplicates were keyed on date only, so two stations on the
     same day were reported as duplicates - major - agent re-keyed on
     (station, date) and added a test
  2. test_quality.py - a test asserted the internal Counter, not behaviour -
     minor - rewritten to assert the public report
Decision: Request changes -> Approve after fix
```

---

## R-001 - commits a8d81bc..HEAD (initial demo build) - approved for publication

```text
Reviewer: Anthony Zee      Date (SGT): 2026-10-01
AI-assisted: yes (Grok Bot AI coding agent)   Risk: high (includes CI/harness)
CI: scripts/ci_local.sh green on 2026-10-01 (see previews/02_ci_local_output.png);
    GitHub Actions: first run happens on publication
Checklist: not recorded. This entry records the publish approval only.
Findings: none recorded
Decision: Approved for publication by Anthony Zee, 2026-10-01
```
