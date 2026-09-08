from pathlib import Path

from analytics_release_gate.checks.powerbi import check_absolute_paths, check_pbip_manifest
from analytics_release_gate.models import Status


def test_invalid_pbip_fails(tmp_path: Path) -> None:
    (tmp_path / "Demo.pbip").write_text("{not-json", encoding="utf-8")
    assert check_pbip_manifest(tmp_path)[0].status is Status.FAIL


def test_absolute_windows_path_fails(tmp_path: Path) -> None:
    path = tmp_path / "model.tmdl"
    path.write_text('source = "C:\\\\Users\\\\alice\\\\Desktop\\\\data.csv"', encoding="utf-8")
    findings = check_absolute_paths(tmp_path)
    assert any(item.status is Status.FAIL for item in findings)
