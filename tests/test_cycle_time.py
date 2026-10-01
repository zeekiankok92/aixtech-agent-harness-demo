import importlib.util
from datetime import datetime, timedelta
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "cycle_time", Path(__file__).resolve().parents[1] / "scripts" / "cycle_time_from_git.py"
)
cycle_time = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cycle_time)


def test_fmt_delta():
    assert cycle_time.fmt_delta(None) == "-"
    assert cycle_time.fmt_delta(timedelta(minutes=7)) == "7 min"
    assert cycle_time.fmt_delta(timedelta(hours=2, minutes=5)) == "2 h 05 min"


def test_render_uses_only_given_rows():
    t0 = datetime.fromisoformat("2026-10-01T17:36:00+08:00")
    rows = [
        {"sha": "aaa", "when": t0, "subject": "a | b", "ai": "yes"},
        {"sha": "bbb", "when": t0 + timedelta(minutes=20), "subject": "c", "ai": ""},
    ]
    md = cycle_time.render(rows)
    assert "| 2 | `bbb` | 2026-10-01 17:56 | 20 min | - | c |" in md
    assert "a / b" in md and "20 min across 2 commits" in md


def test_git_log_reads_this_repo():
    rows = cycle_time.git_log()
    assert rows and all({"sha", "when", "subject", "ai"} <= r.keys() for r in rows)
