from pathlib import Path

from analytics_release_gate.cli import main


def _healthy_repo(root: Path) -> None:
    (root / "README.md").write_text("# Demo", encoding="utf-8")
    (root / "LICENSE").write_text("MIT", encoding="utf-8")
    tests = root / "tests"
    tests.mkdir()
    (tests / "test_demo.py").write_text("def test_demo(): assert True", encoding="utf-8")
    workflows = root / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: CI", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname='demo'", encoding="utf-8")


def test_cli_returns_zero_without_fail_findings(tmp_path: Path, capsys: object) -> None:
    _healthy_repo(tmp_path)
    assert main(["audit", str(tmp_path)]) == 0


def test_cli_returns_one_for_release_blocker(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'", encoding="utf-8")
    assert main(["audit", str(tmp_path)]) == 1


def test_json_output_written(tmp_path: Path) -> None:
    _healthy_repo(tmp_path)
    output = tmp_path / "report.json"
    assert main(["audit", str(tmp_path), "--format", "json", "--output", str(output)]) == 0
    assert '"release_result": "PASS"' in output.read_text(encoding="utf-8")
