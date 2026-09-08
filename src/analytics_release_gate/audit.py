from __future__ import annotations

from pathlib import Path

from analytics_release_gate.checks import CHECKS
from analytics_release_gate.config import Config
from analytics_release_gate.models import AuditReport


def audit_repository(root: Path, config: Config) -> AuditReport:
    root = root.resolve()
    report = AuditReport(root=root)
    for check in CHECKS:
        for finding in check(root):
            if finding.rule_id.upper() not in config.exclude:
                report.add(finding)
    return report
