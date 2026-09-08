# Releasing Analytics Release Gate

Releases are published to PyPI with GitHub Actions Trusted Publishing. The release workflow does not use a long-lived PyPI API token.

## Trusted Publisher configuration

Configure a PyPI GitHub Actions publisher with these exact values:

- PyPI project: `analytics-release-gate`
- GitHub owner: `GarethMackenzie`
- Repository: `analytics-release-gate`
- Workflow filename: `release.yml`
- Environment: `pypi`

For the first release, use PyPI's pending Trusted Publisher flow if the project does not yet exist on PyPI. The project name is not reserved until the first successful publish.

## Release process

1. Confirm `main` is green in hosted CI.
2. Confirm `pyproject.toml` contains the intended version.
3. Confirm `CHANGELOG.md` describes the release scope and known limitations.
4. Create a GitHub release from a tag matching the package version exactly, for example `v0.1.0` for package version `0.1.0`.
5. Publishing the GitHub release triggers `.github/workflows/release.yml`.
6. The workflow builds the sdist and wheel once, validates metadata, smoke-tests the built wheel on Python 3.11, 3.12 and 3.13, then publishes the same artifacts to PyPI through OIDC Trusted Publishing.
7. After publication, verify from a clean environment:

```bash
python -m venv .venv-release-check
# activate the environment
python -m pip install --upgrade pip
python -m pip install analytics-release-gate
argate --version
argate audit .
```

## Safety controls

- The publish job has only `id-token: write`; repository contents remain read-only.
- Publication is tied to the `release.yml` workflow identity and `pypi` GitHub environment.
- No PyPI password or API token should be stored in repository secrets for the normal release path.
- The release tag must match `project.version` in `pyproject.toml` or the build fails.
- Publishing happens only after the built wheel passes the supported Python smoke-test matrix.

## First-release manual setup

Before publishing `v0.1.0`, configure the pending Trusted Publisher in PyPI using the exact values above. On GitHub, the `pypi` environment can be configured with deployment protection rules if available. No secret is required in that environment.

Do not publish a release to test the workflow. Validate changes through a pull request and ordinary CI first; publishing a GitHub release is the production distribution action.
