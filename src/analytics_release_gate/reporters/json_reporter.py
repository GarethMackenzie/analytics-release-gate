from __future__ import annotations

import json

from analytics_release_gate.models import AuditReport


def render(report: AuditReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True)
