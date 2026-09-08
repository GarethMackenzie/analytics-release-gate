from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .finding import Finding, Status


@dataclass(slots=True)
class AuditReport:
    root: Path
    findings: list[Finding] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    @property
    def has_failures(self) -> bool:
        return any(item.status is Status.FAIL for item in self.findings)

    def count(self, status: Status) -> int:
        return sum(item.status is status for item in self.findings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": str(self.root),
            "summary": {status.value: self.count(status) for status in Status},
            "release_result": "FAIL" if self.has_failures else "PASS",
            "findings": [item.to_dict() for item in self.findings],
        }
