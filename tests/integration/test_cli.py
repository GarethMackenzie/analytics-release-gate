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
    repository = tmp_path / "repository"
    repository.mkdir()
    _healthy_repo(repository)
    output = tmp_path / "report.json"
    assert main(["audit", str(repository), "--format", "json", "--output", str(output)]) == 0
    assert '"release_result": "PASS"' in output.read_text(encoding="utf-8")


def test_output_inside_audited_repository_is_rejected(tmp_path: Path) -> None:
    _healthy_repo(tmp_path)
    output = tmp_path / "report.json"

    assert main(["audit", str(tmp_path), "--format", "json", "--output", str(output)]) == 2
    assert not output.exists()


def test_symlinked_output_cannot_overwrite_target(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _healthy_repo(repository)
    target = tmp_path / "sensitive.txt"
    target.write_text("do not replace", encoding="utf-8")
    output = repository / "report.json"
    output.symlink_to(target)

    assert main(["audit", str(repository), "--format", "json", "--output", str(output)]) == 2
    assert target.read_text(encoding="utf-8") == "do not replace"


def test_repository_symlink_cannot_redirect_output(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _healthy_repo(repository)
    trusted = tmp_path / "trusted"
    trusted.mkdir()
    (repository / "escape").symlink_to(trusted, target_is_directory=True)
    alias = tmp_path / "repository-alias"
    alias.symlink_to(repository, target_is_directory=True)
    output = alias / "escape" / "report.json"

    assert main(["audit", str(repository), "--format", "json", "--output", str(output)]) == 2
    assert not output.exists()
