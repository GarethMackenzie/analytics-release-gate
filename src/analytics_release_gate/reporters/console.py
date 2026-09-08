from __future__ import annotations

from analytics_release_gate.models import AuditReport, Status

_SYMBOLS = {
    Status.PASS: "PASS",
    Status.WARNING: "WARN",
    Status.FAIL: "FAIL",
    Status.MANUAL: "MANUAL",
}


def render(report: AuditReport) -> str:
    lines = ["Analytics Release Gate", "=" * 72]
    for item in report.findings:
        location = ""
        if item.path:
            location = f" [{item.path}{':' + str(item.line) if item.line else ''}]"
        lines.append(f"{_SYMBOLS[item.status]:<6} {item.rule_id:<7} {item.title}{location}")
        lines.append(f"       {item.message}")
        if item.recommendation:
            lines.append(f"       Fix: {item.recommendation}")
    lines.extend([
        "",
        "Summary",
        "-" * 72,
        f"PASS={report.count(Status.PASS)}  WARNING={report.count(Status.WARNING)}  "
        f"FAIL={report.count(Status.FAIL)}  MANUAL={report.count(Status.MANUAL)}",
        f"RELEASE RESULT: {'FAIL' if report.has_failures else 'PASS'}",
    ])
    return "\n".join(lines)
