from __future__ import annotations

import argparse
from pathlib import Path
import sys

from analytics_release_gate import __version__
from analytics_release_gate.audit import audit_repository
from analytics_release_gate.config import load_config
from analytics_release_gate.models import AuditReport
from analytics_release_gate.reporters import console, json_reporter, markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="argate", description="Audit analytics repositories before release.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit = subparsers.add_parser("audit", help="Audit a repository path")
    audit.add_argument("path", nargs="?", default=".", help="Repository root (default: current directory)")
    audit.add_argument("--format", choices=("console", "json", "markdown"), default="console")
    audit.add_argument("--output", type=Path, help="Write report to a file instead of stdout")
    audit.add_argument("--config", type=Path, help="Explicit pyproject.toml/config path")
    return parser


def _render(format_name: str, report: AuditReport) -> str:
    if format_name == "json":
        return json_reporter.render(report)
    if format_name == "markdown":
        return markdown.render(report)
    return console.render(report)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.path)
    if not root.exists() or not root.is_dir():
        print(f"argate: repository path does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    try:
        config = load_config(root.resolve(), args.config)
        report = audit_repository(root, config)
        rendered = _render(args.format, report)
    except (OSError, ValueError) as exc:
        print(f"argate: configuration/input error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # defensive boundary for CLI consumers
        print(f"argate: internal error: {exc}", file=sys.stderr)
        return 3

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 1 if report.has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
