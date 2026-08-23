# Contributing to pawa-ai-python

Thanks for helping improve the official Pawa AI Python SDK.

> **Access control:** This is a public repo, but merges and releases are restricted. See [docs/GOVERNANCE.md](docs/GOVERNANCE.md) for branch protection, CODEOWNERS, and PyPI publish controls.

## How to contribute

1. **Fork** the repository (if you are not a maintainer)
2. Create a feature branch from `main`
3. Make changes and run the checks below
4. Open a **Pull Request** — CI must pass and a code owner must approve before merge

Direct pushes to `main` are blocked for non-maintainers.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Checks before opening a PR

```bash
ruff check src tests
pytest -q
python -m build
```

## CI

GitHub Actions runs on every push and pull request to `main`:

- **Lint** — `ruff check`
- **Test** — `pytest` on Python 3.9–3.13
- **Build** — validates the package builds cleanly

## Releases

Releases are **maintainer-only** and require approval via the protected `pypi` GitHub Environment.

1. A maintainer updates the version in `pyproject.toml` and `src/pawa_ai/__init__.py` (via PR)
2. After merge, a maintainer creates a GitHub Release with a semver tag like `v0.2.0`
3. The **Publish to PyPI** workflow runs after required environment approval
4. Configure Trusted Publishing on PyPI for `Sartify/pawa-ai-python` → `publish.yml` → environment `pypi`

See [docs/GOVERNANCE.md](docs/GOVERNANCE.md) for the full access-control checklist.
