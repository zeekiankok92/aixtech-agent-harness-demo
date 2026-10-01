# Security policy

## Supported versions
Only the latest commit on `main` gets fixes. This is a demonstration repository.

## Reporting a vulnerability
Please **do not open a public issue**. Use GitHub's private
[**Report a vulnerability**](../../security/advisories/new) form on this repository
(Security tab, then Advisories). Include steps to reproduce, and use synthetic data only.

You should get an acknowledgement within 7 days. This is a best-effort personal project with no SLA.

## What is in scope
- The `sgweather` package and the scripts in `scripts/`
- The CI workflow and the agent harness, for example a way to bypass a gate

## Built-in protections
- **gitleaks** scans the working tree and full git history on every push and PR
- **ruff** security rules (`S`, bandit-style) run as part of lint
- **Licence allow-list** on dependencies; **Dependabot** sends weekly update PRs
- **PDPA guard**: a tripwire for personal-data patterns in fixtures and docs
- Runtime has **no third-party dependencies**; the API key is optional and read from the environment only

If you find a secret in this repo, report it privately. It will be rotated and purged.
