from pathlib import Path

from analytics_release_gate.checks.repository import check_readme
from analytics_release_gate.models import Status


def test_readme_missing_is_failure(tmp_path: Path) -> None:
    finding = check_readme(tmp_path)[0]
    assert finding.rule_id == "REP001"
    assert finding.status is Status.FAIL


def test_readme_present_passes(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# project", encoding="utf-8")
    assert check_readme(tmp_path)[0].status is Status.PASS
