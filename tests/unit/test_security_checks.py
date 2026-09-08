from pathlib import Path

from analytics_release_gate.checks.security import check_secrets
from analytics_release_gate.models import Status


def test_github_token_pattern_fails(tmp_path: Path) -> None:
    fake = "ghp_" + "A" * 40
    (tmp_path / "config.py").write_text(f'TOKEN = "{fake}"', encoding="utf-8")
    findings = check_secrets(tmp_path)
    assert findings[0].status is Status.FAIL


def test_clean_repository_passes_secret_check(tmp_path: Path) -> None:
    (tmp_path / "config.py").write_text('TOKEN_ENV = "GITHUB_TOKEN"', encoding="utf-8")
    assert check_secrets(tmp_path)[0].status is Status.PASS
