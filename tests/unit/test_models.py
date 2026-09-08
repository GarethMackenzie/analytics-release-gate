from pathlib import Path

from analytics_release_gate.models import AuditReport, Finding, Status


def test_report_marks_failures() -> None:
    report = AuditReport(root=Path("."))
    report.add(Finding("REP001", Status.PASS, "ok", "ok"))
    assert not report.has_failures
    report.add(Finding("SEC001", Status.FAIL, "bad", "bad"))
    assert report.has_failures
    assert report.count(Status.FAIL) == 1
