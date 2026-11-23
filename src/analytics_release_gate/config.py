from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Config:
    exclude: frozenset[str] = field(default_factory=frozenset)


def load_config(root: Path, explicit: Path | None = None) -> Config:
    path = explicit or (root / "pyproject.toml")
    if not path.exists():
        if explicit is not None:
            raise ValueError(f"Explicit configuration does not exist: {path}")
        return Config()
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    tool = data.get("tool", {})
    if not isinstance(tool, dict):
        raise ValueError("tool must be a TOML table")
    section = tool.get("analytics-release-gate", {})
    if not isinstance(section, dict):
        raise ValueError("tool.analytics-release-gate must be a TOML table")
    exclude = section.get("exclude", [])
    if not isinstance(exclude, list) or not all(isinstance(item, str) for item in exclude):
        raise ValueError("tool.analytics-release-gate.exclude must be a list of rule IDs")
    return Config(exclude=frozenset(item.upper() for item in exclude))
