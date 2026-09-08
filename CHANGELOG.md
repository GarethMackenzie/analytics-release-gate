# Changelog

All notable project changes will be documented here.

The project follows semantic versioning once public releases begin.

## [Unreleased]

## [0.1.0] - 2026-09-08

### Added
- Initial `argate audit` CLI.
- Structured PASS/WARNING/FAIL/MANUAL findings.
- Fifteen initial repository, Power BI, DAX, documentation, security and reproducibility rules.
- Console, JSON and Markdown reporters.
- Stable rule IDs and `pyproject.toml` exclusions.
- Contributor, security and architecture documentation.
- CI matrix for Python 3.11-3.13.
- Trusted PyPI release workflow using GitHub Actions OIDC.

### Notes
- This is an alpha release.
- A green audit means the supported checks passed; it does not prove analytical truth, business correctness, source provenance, or Power BI Desktop runtime validity.
