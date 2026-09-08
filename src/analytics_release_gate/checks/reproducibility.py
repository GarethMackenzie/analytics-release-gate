from __future__ import annotations

from pathlib import Path

from analytics_release_gate.models import Finding, Status


def check_build_entrypoint(root: Path) -> list[Finding]:
    candidates = [
        root / "pyproject.toml",
        root / "Makefile",
        root / "justfile",
        root / "scripts" / "build.py",
        root / "scripts" / "build_project.py",
    ]
    found = next((path for path in candidates if path.exists()), None)
    if found:
        return [Finding.for_path(root=root, rule_id="BLD001", status=Status.PASS,
            title="Build/config entry point detected", message="A conventional build or project configuration entry point exists.", path=found)]
    return [Finding.for_path(root=root, rule_id="BLD001", status=Status.WARNING,
        title="Build entry point not detected", message="No conventional project/build entry point was found.",
        recommendation="Document a deterministic build command or add a standard project configuration file.")]


def check_generated_drift(root: Path) -> list[Finding]:
    return [Finding.for_path(root=root, rule_id="BLD002", status=Status.MANUAL,
        title="Generated-output drift requires configured build",
        message="v0.1 does not execute arbitrary repository build commands automatically.",
        recommendation="Run the documented build in CI and fail when generated tracked artifacts change unexpectedly.")]
