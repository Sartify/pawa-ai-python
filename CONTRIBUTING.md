# Contributing to pawa-ai-python

Thanks for helping improve the official Pawa AI Python SDK.

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

1. Update the version in `pyproject.toml` and `src/pawa_ai/__init__.py`
2. Create a GitHub Release with a tag like `v0.2.0`
3. The **Publish to PyPI** workflow uploads the package automatically

Configure the `pypi` environment in GitHub with [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) for `pawa-ai`.
