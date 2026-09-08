# Configuration

Analytics Release Gate reads configuration from the audited repository's `pyproject.toml`.

```toml
[tool.analytics-release-gate]
exclude = ["DAX002"]
```

## Design principles

- Suppression is explicit by stable rule ID.
- A missing configuration section uses safe defaults.
- Invalid configuration produces exit code `2` rather than silently ignoring errors.
- v0.1 intentionally keeps configuration small while real users establish which controls are necessary.
