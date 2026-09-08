# Architecture

The v0.1 architecture separates rule execution, parsers, finding models and output renderers.

```text
CLI
 |
 v
configuration -> audit engine -> checks -> Finding objects -> AuditReport
                             |                         |
                             v                         v
                           parsers          console / JSON / Markdown
```

## Constraints

1. Checks inspect a user-supplied repository path and should not mutate it.
2. Rules return structured findings with stable IDs.
3. Release failure is determined by FAIL findings, not warning count.
4. Power BI parsers validate source files without claiming Desktop runtime behavior.
5. New rules require regression tests and rule-reference documentation.
