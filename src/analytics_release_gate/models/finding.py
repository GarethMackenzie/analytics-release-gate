from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any


class Status(StrEnum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    MANUAL = "MANUAL"


@dataclass(frozen=True, slots=True)
class Finding:
    rule_id: str
    status: Status
    title: str
    message: str
    path: str | None = None
    line: int | None = None
    evidence: str | None = None
    recommendation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def for_path(
        cls,
        *,
        root: Path,
        rule_id: str,
        status: Status,
        title: str,
        message: str,
        path: Path | None = None,
        line: int | None = None,
        evidence: str | None = None,
        recommendation: str | None = None,
    ) -> Finding:
        relative = None
        if path is not None:
            try:
                relative = path.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                relative = path.as_posix()
        return cls(
            rule_id=rule_id,
            status=status,
            title=title,
            message=message,
            path=relative,
            line=line,
            evidence=evidence,
            recommendation=recommendation,
        )
