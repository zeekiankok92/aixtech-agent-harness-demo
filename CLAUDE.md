# CLAUDE.md

Follow **[AGENTS.md](AGENTS.md)**. It is the single source of truth for every AI agent in
this repo. Quick reminders for Claude Code sessions:

- Read the task brief in `tasks/` first and restate it in one paragraph before you edit.
- Plan, then make small diffs. Run `scripts/ci_local.sh` before you say "done".
- Synthetic fixtures only. No personal data and no secrets in context or code (PDPA).
- Add the `AI-Assisted:` / `Human-Review:` commit trailers and a row in
  `docs/ai-disclosure-log.md`.
- Never edit CI gates, thresholds or harness files unless the task says so explicitly.
