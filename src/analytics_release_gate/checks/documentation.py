from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from analytics_release_gate.models import Finding, Status

_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check_local_markdown_links(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    checked = 0
    for path in root.rglob("*.md"):
        if any(part in {".git", ".venv", "venv", "node_modules"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for raw_target in _LINK.findall(line):
                target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = unquote(target.split("#", 1)[0])
                if not target:
                    continue
                checked += 1
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    findings.append(Finding.for_path(root=root, rule_id="DOC001", status=Status.WARNING,
                        title="Broken local documentation link", message=f"Local Markdown target does not exist: {target}",
                        path=path, line=line_number,
                        recommendation="Fix or remove the stale local link."))
    if findings:
        return findings
    return [Finding.for_path(root=root, rule_id="DOC001", status=Status.PASS,
        title="Local documentation links valid", message=f"Checked {checked} local Markdown link(s) without missing targets.")]
