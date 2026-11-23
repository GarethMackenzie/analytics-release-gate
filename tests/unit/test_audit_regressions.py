from pathlib import Path
from unittest.mock import patch

import pytest

from analytics_release_gate.audit import audit_repository
from analytics_release_gate.checks.dax import check_measure_descriptions
from analytics_release_gate.checks.powerbi import check_pbip_manifest, check_pbir_json
from analytics_release_gate.cli import main
from analytics_release_gate.config import load_config
from analytics_release_gate.models import Status
from analytics_release_gate.reporters import console, json_reporter, markdown


def test_multirule_evidence_never_copies_source(tmp_path):
    token = "ghp_" + "a" * 36
    (tmp_path / "config.json").write_text('{"token":"' + token + '","path":"C:/Users/test/data"}')
    report = audit_repository(tmp_path, load_config(tmp_path))
    assert any(f.rule_id == "SEC001" and f.status == Status.FAIL for f in report.findings)
    assert any(f.rule_id == "PBI004" for f in report.findings)
    for renderer in (console, json_reporter, markdown):
        assert token not in renderer.render(report)
    assert all(f.evidence is None for f in report.findings)


@pytest.mark.parametrize("suffix", [".json", ".dax", ".md", ".tmdl"])
def test_unreadable_supported_file_is_not_a_clean_pass(tmp_path, suffix, capsys):
    target = tmp_path / ("unreadable" + suffix)
    target.write_text("content")
    original = Path.read_text

    def read(path, *args, **kwargs):
        if path == target:
            raise PermissionError("injected")
        return original(path, *args, **kwargs)

    with patch.object(Path, "read_text", read):
        assert main(["audit", str(tmp_path)]) == 2
    assert "error" in capsys.readouterr().err


def test_nested_manifest_and_definition_pbir_are_checked(tmp_path):
    nested = tmp_path / "projects"
    nested.mkdir()
    (nested / "broken.pbip").write_text("{invalid")
    assert check_pbip_manifest(tmp_path)[0].status == Status.FAIL
    report = nested / "Demo.Report"
    report.mkdir()
    (report / "report.json").write_text("{}")
    (report / "definition.pbir").write_text("{invalid")
    assert check_pbir_json(tmp_path)[0].status == Status.FAIL
    (report / "definition.pbir").write_text("{}")
    assert check_pbir_json(tmp_path)[0].status == Status.PASS
    (nested / "Empty.Report").mkdir()
    assert check_pbir_json(tmp_path)[0].status == Status.FAIL


def test_descriptions_attach_to_measure_not_later_column(tmp_path):
    model = tmp_path / "nested" / "Demo.SemanticModel" / "definition"
    model.mkdir(parents=True)
    (model / "table.tmdl").write_text("""table Sales
    /// Business meaning
    /// Units and filters
    measure 'Customer''s total' =
        SUM(Sales[Amount])
    measure Missing = 1
    column Other
        description = 'not a measure description'
""")
    findings = check_measure_descriptions(tmp_path)
    assert len(findings) == 1
    assert findings[0].status == Status.WARNING
    assert "Missing" in findings[0].message


def test_explicit_missing_and_invalid_config(tmp_path):
    assert not load_config(tmp_path).exclude
    assert main(["audit", str(tmp_path), "--config", str(tmp_path / "missing.toml")]) == 2
    config = tmp_path / "bad.toml"
    config.write_text('[tool]\nanalytics-release-gate = "invalid"')
    assert main(["audit", str(tmp_path), "--config", str(config)]) == 2


@pytest.mark.parametrize("method", ["mkdir", "write_text"])
def test_output_failure_is_controlled(tmp_path, capsys, method):
    with patch.object(Path, method, side_effect=PermissionError("injected")):
        assert main(["audit", str(tmp_path), "--output", str(tmp_path / "report.json")]) == 2
    assert "Traceback" not in capsys.readouterr().err
