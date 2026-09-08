# Analytics Release Gate

**Catch analytics-engineering defects before they become release defects.**

Analytics Release Gate is an open-source CLI for auditing analytics and Power BI repositories. It focuses on release readiness that is easy to miss in manual review: repository hygiene, PBIP/PBIR/TMDL integrity, risky DAX literals, machine-specific paths, documentation links, security signals and reproducibility controls.

> **Status:** v0.1 is an alpha foundation. Rules are intentionally conservative and every heuristic is documented. The tool does not claim to prove analytical truth, business correctness or Power BI Desktop runtime validity.

## Quick start

```bash
pip install -e .
argate audit .
```

Machine-readable output:

```bash
argate audit . --format json --output release-gate.json
```

## Current rules

| Rule | Purpose | Default result |
|---|---|---|
| `REP001` | README exists | FAIL if missing |
| `REP002` | License exists | WARNING if missing |
| `REP003` | Tests detected | WARNING if missing |
| `REP004` | GitHub Actions workflow detected | WARNING if missing |
| `PBI001` | PBIP manifest parses | FAIL on invalid manifest |
| `PBI002` | PBIR JSON parses | FAIL on invalid JSON |
| `PBI003` | TMDL semantic model present for PBIP | FAIL if missing |
| `PBI004` | No machine-specific absolute paths | FAIL on match |
| `DAX001` | Suspicious hard-coded comparator heuristic | WARNING |
| `DAX002` | TMDL measure descriptions | WARNING |
| `SEC001` | High-confidence credential patterns | FAIL |
| `SEC002` | User home paths in tracked text | WARNING |
| `DOC001` | Local Markdown links resolve | WARNING |
| `BLD001` | Build/config entry point exists | WARNING |
| `BLD002` | Generated-output drift | MANUAL in v0.1 |

See [docs/rules.md](docs/rules.md) for semantics, limitations and examples.

## Configuration

Rules can be excluded in `pyproject.toml`:

```toml
[tool.analytics-release-gate]
exclude = ["DAX002"]
```

Rule suppression is explicit by ID so exceptions remain reviewable. See [docs/configuration.md](docs/configuration.md).

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Audit completed with no FAIL findings |
| `1` | One or more release-blocking FAIL findings |
| `2` | Invalid path or configuration/input error |
| `3` | Internal tool failure |

## What this tool does not do

Analytics Release Gate does **not**:

- prove that a business metric is factually correct;
- replace source/provenance review;
- execute arbitrary repository build commands in v0.1;
- claim that a PBIP project opens successfully in Power BI Desktop;
- replace secret-management or full static-analysis products.

These boundaries are deliberate. A green gate means the supported checks passed, not that the analytics product is universally correct.

## Development

```bash
python -m venv .venv
# activate the environment
pip install -e ".[dev]"
pytest
ruff check .
mypy src
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contributor workflow.

## Roadmap

- v0.1: core CLI and first release rules
- v0.2: deeper DAX and semantic-model validation
- v0.3: configurable severity and richer suppression metadata
- v0.4: GitHub Actions annotations and Markdown reporting improvements
- v0.5: SARIF output
- v0.6: deterministic-build framework
- v0.7: plugin architecture
- v0.8+: governance rules informed by external users

## License

MIT. See [LICENSE](LICENSE).
