from __future__ import annotations

import re
from pathlib import Path

from analytics_release_gate.models import Finding, Status

_SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("generic credential assignment", re.compile(r"(?i)\b(?:password|passwd|api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"'\n]{8,}[\"']")),
]
_TEXT_SUFFIXES = {".py", ".toml", ".yaml", ".yml", ".json", ".md", ".txt", ".env", ".ini", ".cfg", ".tmdl", ".dax", ".sql"}


def check_secrets(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skip_parts = {".git", ".venv", "venv", "node_modules", "dist", "build"}
    for path in root.rglob("*"):
        if not path.is_file() or (path.suffix.lower() not in _TEXT_SUFFIXES and path.name != ".env"):
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, start=1):
            for label, pattern in _SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(Finding.for_path(root=root, rule_id="SEC001", status=Status.FAIL,
                        title="Potential credential detected", message=f"Detected pattern consistent with {label}.",
                        path=path, line=number,
                        recommendation="Remove the credential from tracked content and rotate it if it was ever valid."))
                    break
    if findings:
        return findings
    return [Finding.for_path(root=root, rule_id="SEC001", status=Status.PASS,
        title="No high-confidence credentials detected", message="No supported high-confidence secret patterns were found.")]


def check_sensitive_home_paths(root: Path) -> list[Finding]:
    pattern = re.compile(r"(?:[A-Za-z]:[\\/]Users[\\/][^\\/\s]+|/(?:Users|home)/[^/\s]+)")
    findings: list[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in _TEXT_SUFFIXES:
            continue
        if any(part in {".git", ".venv", "venv", "node_modules"} for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, start=1):
            if pattern.search(line):
                findings.append(Finding.for_path(root=root, rule_id="SEC002", status=Status.WARNING,
                    title="User home path disclosed", message="A user-specific local home path appears in tracked text.",
                    path=path, line=number, evidence=line.strip()[:240],
                    recommendation="Use relative paths or neutral placeholders in public repositories."))
    if findings:
        return findings
    return [Finding.for_path(root=root, rule_id="SEC002", status=Status.PASS,
        title="No user home paths detected", message="No common user-specific home path patterns were found.")]
