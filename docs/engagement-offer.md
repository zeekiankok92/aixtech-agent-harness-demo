# Engagement offer (1 page)

**Anthony Zee: AI-assisted software delivery for Singapore SMEs**

This repository shows how I work. AI coding agents do the drafting inside a harness
of rules, automatic quality gates, human review and a written AI-disclosure trail.
You get the speed of AI-assisted development, plus an audit pack you can show your
customers, auditors or board.

---

## Option 1: Build Sprint, **S$4,000 fixed price**
*For a small, well-defined piece of software: an internal tool, an integration, a
data pipeline, a prototype that has to become real.*

- **Scope:** agreed up front in a written statement of work (SOW), sized to about 40 hours of delivery
- **You receive:**
  - working code in your repository;
  - tests and the CI gates from this repo (lint, tests with a coverage threshold, secret scan, licence check, personal-data guard);
  - an AI-disclosure log and a review log for every change;
  - a short handover walkthrough.
- **Acceptance:** against acceptance tests written into the SOW. Done = CI green + your sign-off
- **Optional:** a care retainer of **S$1,000/month**, about 10 hours: maintenance, small changes and dependency updates, through the same gates

## Option 2: Harness Setup, **S$2,500**
*For teams that already write code and want to use AI coding assistants safely.*

- **About 20 hours.** I install and tailor this harness in *your* repositories:
  - `AGENTS.md` rules;
  - task-brief and PR templates with an AI-disclosure section;
  - the six CI gates;
  - CODEOWNERS and the review checklist;
  - Dependabot.
- **Includes:** a working session with your developers, plus a cycle-time template so you can measure before/after on your own work
- **Optional:** care at **S$300/month**, about 3 hours: gate and rule updates as tools change

---

## How every engagement handles data (PDPA)
- No production or personal data goes into AI tools' context. Development uses synthetic or masked data that you approve.
- The data-handling, data-intermediary and AI-use terms are written into the SOW.
- Secrets stay in your secret store and are never committed or pasted into prompts.

## What this offer is *not*
- **No guaranteed speed-ups or savings.** This repo makes no client claims and shows no results from client projects. If you want to know whether it helps your team, the
  cycle-time template measures that on your own work.
- Not legal advice, not a compliance certification, not a substitute for your own DPO.

## Terms (summary)
Prices are in SGD and indicative until confirmed in a signed SOW. That SOW covers scope,
acceptance tests, IP, liability cap, payment schedule and any GST.
Contact via GitHub: [@zeekiankok92](https://github.com/zeekiankok92).
