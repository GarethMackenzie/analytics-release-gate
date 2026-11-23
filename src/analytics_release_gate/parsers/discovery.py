from __future__ import annotations

import os
from pathlib import Path

_SKIP = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def discover(root: Path) -> list[Path]:
    paths: list[Path] = []

    def failed(error: OSError) -> None:
        raise ValueError("Project discovery incomplete: directory cannot be read") from error

    for directory, dirs, files in os.walk(root, onerror=failed, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in _SKIP)
        for name in [*dirs, *sorted(files)]:
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError("Project discovery incomplete: symlink entries are unsupported")
            paths.append(path)
            if len(paths) > 100_000:
                raise ValueError("Project discovery exceeds 100000 entries")
    return paths


def model_files(root: Path) -> list[Path]:
    return [p for p in discover(root) if p.suffix.lower() == ".tmdl"
            and any(part.endswith(".SemanticModel") for part in p.relative_to(root).parts)
            and "definition" in p.relative_to(root).parts]
