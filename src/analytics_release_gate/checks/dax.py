from __future__ import annotations

import re
from pathlib import Path

from analytics_release_gate.models import Finding, Status
from analytics_release_gate.parsers import iter_measure_blocks

_NUMERIC_LITERAL = re.compile(r"(?<![A-Za-z0-9_])(?:\d{8,}|\d+\.\d{4,})(?![A-Za-z0-9_])")


def _measure_sources(root: Path) -> list[Path]:
    return [*root.rglob("*.dax"), *root.glob("*.SemanticModel/definition/**/*.tmdl")]


def check_hardcoded_comparators(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _measure_sources(root):
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue
            match = _NUMERIC_LITERAL.search(stripped)
            if match and any(token in stripped.upper() for token in ("CALCULATE", "DIVIDE", "VAR", "RETURN", "=")):
                findings.append(Finding.for_path(root=root, rule_id="DAX001", status=Status.WARNING,
                    title="Possible hard-coded analytical comparator",
                    message="A large or high-precision numeric literal appears in DAX/TMDL logic. Review whether it should come from model data.",
                    path=path, line=number, evidence=stripped[:240],
                    recommendation="Prefer dynamic period/value resolution when the literal represents business data rather than a true constant."))
    if findings:
        return findings
    return [Finding.for_path(root=root, rule_id="DAX001", status=Status.PASS,
        title="No suspicious DAX comparators detected", message="No high-risk numeric literals were detected in DAX/TMDL measure logic.")]


def check_measure_descriptions(root: Path) -> list[Finding]:
    tmdl_files = list(root.glob("*.SemanticModel/definition/**/*.tmdl"))
    if not tmdl_files:
        return [Finding.for_path(root=root, rule_id="DAX002", status=Status.PASS,
            title="Measure descriptions not applicable", message="No TMDL semantic model was detected.")]

    missing: list[Finding] = []
    measure_count = 0
    for path in tmdl_files:
        for block in iter_measure_blocks(path):
            measure_count += 1
            if "description =" not in block.text.lower():
                missing.append(Finding.for_path(root=root, rule_id="DAX002", status=Status.WARNING,
                    title="Measure description missing", message=f"Measure '{block.name}' has no description in its TMDL block.",
                    path=path, line=block.start_line,
                    recommendation="Document business meaning, units and important filter semantics for public measures."))
    if missing:
        return missing
    return [Finding.for_path(root=root, rule_id="DAX002", status=Status.PASS,
        title="Measure descriptions present", message=f"All {measure_count} detected TMDL measure(s) include descriptions.")]
