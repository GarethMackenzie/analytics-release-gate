from __future__ import annotations

from pathlib import Path

from analytics_release_gate.models import Finding, Status


def check_readme(root: Path) -> list[Finding]:
    candidates = [root / "README.md", root / "README.rst", root / "README.txt"]
    found = next((path for path in candidates if path.is_file()), None)
    if found:
        return [Finding.for_path(root=root, rule_id="REP001", status=Status.PASS,
            title="README detected", message="Repository documentation entry point exists.", path=found)]
    return [Finding.for_path(root=root, rule_id="REP001", status=Status.FAIL,
        title="README missing", message="No README file was found.",
        recommendation="Add a concise README with install, usage, limitations and contribution guidance.")]


def check_license(root: Path) -> list[Finding]:
    candidates = [root / "LICENSE", root / "LICENSE.md", root / "COPYING"]
    found = next((path for path in candidates if path.is_file()), None)
    if found:
        return [Finding.for_path(root=root, rule_id="REP002", status=Status.PASS,
            title="License detected", message="A repository license file exists.", path=found)]
    return [Finding.for_path(root=root, rule_id="REP002", status=Status.WARNING,
        title="License missing", message="No repository license file was found.",
        recommendation="Choose and add an explicit open-source license before public distribution.")]


def check_tests(root: Path) -> list[Finding]:
    test_dir = root / "tests"
    tests = list(test_dir.rglob("test_*.py")) if test_dir.is_dir() else []
    if tests:
        return [Finding.for_path(root=root, rule_id="REP003", status=Status.PASS,
            title="Tests detected", message=f"Detected {len(tests)} Python test file(s).", path=test_dir)]
    return [Finding.for_path(root=root, rule_id="REP003", status=Status.WARNING,
        title="Tests not detected", message="No Python test files were found under tests/.",
        recommendation="Add automated tests for release-critical behavior.")]


def check_ci(root: Path) -> list[Finding]:
    workflow_dir = root / ".github" / "workflows"
    workflows = []
    if workflow_dir.is_dir():
        workflows = [*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")]
    if workflows:
        return [Finding.for_path(root=root, rule_id="REP004", status=Status.PASS,
            title="CI workflow detected", message=f"Detected {len(workflows)} GitHub Actions workflow(s).", path=workflow_dir)]
    return [Finding.for_path(root=root, rule_id="REP004", status=Status.WARNING,
        title="CI workflow missing", message="No GitHub Actions workflow was found.",
        recommendation="Add CI that runs linting, tests and package/build validation.")]
