# Rule reference

Rules use stable IDs so findings can be discussed, tested and intentionally suppressed.

## Status model

- **PASS**: supported check completed without a defect.
- **WARNING**: review recommended; does not fail the release gate.
- **FAIL**: release-blocking defect detected by the supported rule.
- **MANUAL**: tool cannot verify the requirement automatically yet.

## Heuristic rules

`DAX001`, `DAX002`, `SEC001`, `SEC002` and some path/link checks are heuristic. A heuristic finding is evidence to review, not a claim about intent. False positives should be reported with a minimal reproducible fixture.

## Power BI scope

PBIP/PBIR/TMDL checks validate source-controlled structure and parseability. They do not perform Power BI Desktop runtime validation and do not guarantee DAX semantic correctness.

## Rule catalogue

### REP001 - README exists
Release-blocking when no common README file exists.

### REP002 - License exists
Warns when no common license file exists.

### REP003 - Tests detected
Warns when no `tests/test_*.py` files are found.

### REP004 - CI workflow detected
Warns when `.github/workflows/*.yml|yaml` is absent.

### PBI001 - PBIP manifest parses
Fails when a detected `.pbip` manifest is not valid JSON.

### PBI002 - PBIR JSON parses
Fails when source-controlled report JSON is malformed.

### PBI003 - TMDL model present
Fails when a PBIP project is present without source-controlled TMDL under a `*.SemanticModel/definition/` tree.

### PBI004 - No absolute machine path
Fails on common Windows/macOS/Linux user-path patterns in supported text files.

### DAX001 - Possible hard-coded analytical comparator
Warns on large/high-precision numeric literals in likely measure logic. It intentionally does not auto-fix values.

### DAX002 - TMDL measure descriptions
Warns when a detected TMDL measure block lacks a description.

### SEC001 - Potential credential
Fails on a small set of high-confidence token/key/credential patterns.

### SEC002 - User home path disclosed
Warns when public tracked text contains common user-home path patterns.

### DOC001 - Local Markdown links
Warns when a relative Markdown target cannot be resolved on disk.

### BLD001 - Build/config entry point
Warns when no conventional build/project configuration entry point is detected.

### BLD002 - Generated-output drift
MANUAL in v0.1. Future releases will support an opt-in deterministic build contract rather than executing arbitrary commands by default.
