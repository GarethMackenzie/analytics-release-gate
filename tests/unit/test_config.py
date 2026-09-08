from pathlib import Path

import pytest

from analytics_release_gate.config import load_config


def test_config_loads_exclusions(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[tool.analytics-release-gate]\nexclude = ["DAX002"]\n', encoding="utf-8"
    )
    assert load_config(tmp_path).exclude == frozenset({"DAX002"})


def test_invalid_exclusion_config_fails(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[tool.analytics-release-gate]\nexclude = "DAX002"\n', encoding="utf-8"
    )
    with pytest.raises(ValueError):
        load_config(tmp_path)
