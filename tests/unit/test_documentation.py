from pathlib import Path

from analytics_release_gate.checks.documentation import check_local_markdown_links
from analytics_release_gate.models import Status


def test_missing_local_markdown_target_warns(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("[missing](docs/missing.md)", encoding="utf-8")
    assert check_local_markdown_links(tmp_path)[0].status is Status.WARNING


def test_existing_local_markdown_target_passes(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "ok.md").write_text("ok", encoding="utf-8")
    (tmp_path / "README.md").write_text("[ok](docs/ok.md)", encoding="utf-8")
    assert check_local_markdown_links(tmp_path)[0].status is Status.PASS
