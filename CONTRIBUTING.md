# Contributing

Thank you for helping improve Analytics Release Gate.

## Development setup

```bash
git clone https://github.com/GarethMackenzie/analytics-release-gate.git
cd analytics-release-gate
python -m venv .venv
pip install -e ".[dev]"
pytest
```

Before opening a pull request, run:

```bash
ruff check .
ruff format --check .
mypy src
pytest
```

## Adding a rule

1. Choose the correct rule family and next stable ID.
2. Implement the check without mutating the audited repository.
3. Return structured `Finding` objects.
4. Add positive and negative fixtures/tests.
5. Document the rule in `docs/rules.md`.
6. Explain known false-positive/false-negative tradeoffs in the PR.

Please do not weaken a rule or test merely to make a fixture pass. Fix the underlying logic or document the legitimate exception.
