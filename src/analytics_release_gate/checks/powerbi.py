from __future__ import annotations

import re
from pathlib import Path

from analytics_release_gate.models import Finding, Status
from analytics_release_gate.parsers import parse_json, parse_pbip
from analytics_release_gate.parsers.discovery import discover, model_files

_TEXT_SUFFIXES = {".json", ".tmdl", ".dax", ".m", ".pq", ".txt", ".md", ".yaml", ".yml"}
_ABSOLUTE_PATTERNS = [
    re.compile(r"[A-Za-z]:[\\/]+(?:Users|Documents|Desktop|Downloads)[\\/]+", re.IGNORECASE),
    re.compile(r"/(?:Users|home)/[^/\s]+/"),
    re.compile(r"File\.Contents\s*\(\s*[\"'][A-Za-z]:[\\/]", re.IGNORECASE),
]


def check_pbip_manifest(root: Path) -> list[Finding]:
    files = [p for p in discover(root) if p.suffix.lower() == ".pbip" and p.is_file()]
    if not files:
        return [Finding.for_path(root=root, rule_id="PBI001", status=Status.PASS,
            title="PBIP not applicable", message="No PBIP project was detected; rule is not applicable.")]

    findings: list[Finding] = []
    for path in files:
        try:
            parse_pbip(path)
        except (OSError, ValueError) as exc:
            findings.append(Finding.for_path(root=root, rule_id="PBI001", status=Status.FAIL,
                title="Invalid PBIP manifest", message=str(exc), path=path))
        else:
            findings.append(Finding.for_path(root=root, rule_id="PBI001", status=Status.PASS,
                title="PBIP manifest valid", message="PBIP manifest parsed successfully.", path=path))
    return findings


def check_pbir_json(root: Path) -> list[Finding]:
    report_dirs = [path for path in discover(root) if path.name.endswith(".Report") and path.is_dir()]
    if not report_dirs:
        return [Finding.for_path(root=root, rule_id="PBI002", status=Status.PASS,
            title="PBIR not applicable", message="No source-controlled Power BI report directory was detected.")]

    json_files = [path for report in report_dirs for path in discover(report)
                  if path.is_file() and (path.suffix.lower() == ".json" or path.name == "definition.pbir")]
    empty = [report for report in report_dirs if not any(report in p.parents for p in json_files)]
    if empty:
        return [Finding.for_path(root=root, rule_id="PBI002", status=Status.FAIL,
            title="PBIR JSON missing", message="Report directory contains no supported JSON metadata.", path=p) for p in empty]
    if not json_files:
        return [Finding.for_path(root=root, rule_id="PBI002", status=Status.FAIL,
            title="PBIR JSON missing", message="A report directory exists but contains no JSON files.", path=report_dirs[0])]

    failures = []
    for path in json_files:
        try:
            parse_json(path)
        except (OSError, ValueError) as exc:
            failures.append((path, str(exc)))
    if failures:
        return [Finding.for_path(root=root, rule_id="PBI002", status=Status.FAIL,
            title="Invalid PBIR JSON", message=message, path=path) for path, message in failures]
    return [Finding.for_path(root=root, rule_id="PBI002", status=Status.PASS,
        title="PBIR JSON valid", message=f"Parsed {len(json_files)} PBIR JSON file(s).", path=report_dirs[0])]


def check_tmdl_model(root: Path) -> list[Finding]:
    pbip_files = [p for p in discover(root) if p.suffix.lower() == ".pbip" and p.is_file()]
    tmdl_files = model_files(root)
    if not pbip_files:
        return [Finding.for_path(root=root, rule_id="PBI003", status=Status.PASS,
            title="TMDL not applicable", message="No PBIP project was detected; rule is not applicable.")]
    if tmdl_files:
        return [Finding.for_path(root=root, rule_id="PBI003", status=Status.PASS,
            title="TMDL semantic model detected", message=f"Detected {len(tmdl_files)} TMDL file(s).", path=tmdl_files[0].parent)]
    return [Finding.for_path(root=root, rule_id="PBI003", status=Status.FAIL,
        title="TMDL semantic model missing", message="PBIP project detected without source-controlled TMDL model.",
        recommendation="Commit the editable semantic-model source rather than relying on an opaque binary artifact.")]


def check_absolute_paths(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skip_parts = {".git", ".venv", "venv", "node_modules", "dist", "build"}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in _TEXT_SUFFIXES:
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError as exc:
            raise ValueError(f"Scan incomplete: cannot read {path.relative_to(root)}") from exc
        for line_number, line in enumerate(lines, start=1):
            if any(pattern.search(line) for pattern in _ABSOLUTE_PATTERNS):
                findings.append(Finding.for_path(root=root, rule_id="PBI004", status=Status.FAIL,
                    title="Absolute local path detected", message="Repository contains a machine-specific local path.",
                    path=path, line=line_number, evidence=line.strip()[:240],
                    recommendation="Replace the path with a relative, parameterized or portable source reference."))
    if findings:
        return findings
    return [Finding.for_path(root=root, rule_id="PBI004", status=Status.PASS,
        title="No machine-specific paths detected", message="No common absolute local-path patterns were found.")]
