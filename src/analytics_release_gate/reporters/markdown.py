from __future__ import annotations

from analytics_release_gate.models import AuditReport, Status


def render(report: AuditReport) -> str:
    lines = ["# Analytics Release Gate", "", "| Status | Rule | Finding | Location |", "|---|---|---|---|"]
    for item in report.findings:
        location = item.path or ""
        if item.line:
            location += f":{item.line}"
        lines.append(f"| {item.status.value} | {item.rule_id} | {item.title} | {location} |")
    lines.extend([
        "",
        "## Summary",
        "",
        f"- PASS: {report.count(Status.PASS)}",
        f"- WARNING: {report.count(Status.WARNING)}",
        f"- FAIL: {report.count(Status.FAIL)}",
        f"- MANUAL: {report.count(Status.MANUAL)}",
        f"- Release result: **{'FAIL' if report.has_failures else 'PASS'}**",
    ])
    return "\n".join(lines)
