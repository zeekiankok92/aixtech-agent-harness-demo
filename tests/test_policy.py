"""The PDPA guard itself is tested, so the gate cannot silently rot."""

import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "check_pdpa", Path(__file__).resolve().parents[1] / "scripts" / "check_pdpa.py"
)
check_pdpa = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_pdpa)


def test_flags_nric_phone_email(tmp_path):
    f = tmp_path / "leak.csv"
    f.write_text("name,id\nx," + "S" + "1234567" + "D\ncall 9" + "123 4567\nme@" + "corp.com.sg\n")
    kinds = {k for _, k in check_pdpa.scan_file(f)}
    assert kinds == {"NRIC/FIN-like", "SG phone-like", "email"}


def test_repo_fixtures_are_clean():
    root = Path(__file__).resolve().parents[1]
    assert check_pdpa.scan_paths([root / "fixtures"]) == []
