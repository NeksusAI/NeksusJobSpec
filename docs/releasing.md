# Releasing Neksus to PyPI

This document defines a minimal, repeatable release flow for `neksus-jobspec`.

## Prerequisites

- Python 3.11+
- A clean working tree (`git status` shows no pending changes)
- PyPI account and project permissions
- TestPyPI account (recommended for dry runs)
- Trusted publishing or API tokens configured

## 1. Choose the next version

Update the version in:

- `pyproject.toml` (`[project].version`)
- `neksus/__init__.py` (`__version__`)

Use semantic versioning:

- Patch: bug fixes (`0.1.0` -> `0.1.1`)
- Minor: backward-compatible features (`0.1.0` -> `0.2.0`)
- Major: breaking changes (`0.x` -> `1.0.0`)

## 2. Verify quality gates

Run all checks before building artifacts:

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run neksus-jobspec version
```

CI status must be green on the branch before tagging or publishing.

## 3. Build distribution artifacts

Install build tools if needed:

```bash
python -m pip install --upgrade build twine
```

Build sdist and wheel:

```bash
python -m build
```

Expected outputs:

- `dist/*.tar.gz`
- `dist/*.whl`

## 4. Validate artifacts locally

Run Twine checks:

```bash
twine check dist/*
```

Optional smoke test in a clean virtual environment:

```bash
python -m venv /tmp/neksus-release-venv
source /tmp/neksus-release-venv/bin/activate
pip install dist/*.whl
neksus-jobspec version
deactivate
```

## 5. Publish to TestPyPI first (recommended)

```bash
twine upload --repository testpypi dist/*
```

Install from TestPyPI and verify:

```bash
python -m venv /tmp/neksus-testpypi-venv
source /tmp/neksus-testpypi-venv/bin/activate
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple neksus-jobspec==<VERSION>
neksus-jobspec version
deactivate
```

## 6. Publish to PyPI

```bash
twine upload dist/*
```

## 7. Post-release verification

- Confirm package page on PyPI
- Install from PyPI in a clean venv
- Run a quick CLI smoke flow:

```bash
python -m venv /tmp/neksus-pypi-venv
source /tmp/neksus-pypi-venv/bin/activate
pip install neksus-jobspec==<VERSION>
neksus-jobspec version
neksus-jobspec init --empty
deactivate
```

## 8. Tag and announce

Create and push a git tag after successful publish:

```bash
git tag v<VERSION>
git push origin v<VERSION>
```

Then publish release notes in GitHub Releases.

## Branch protection expectations

Set branch protection so merges require the `CI` workflow to pass.

## Troubleshooting

- `File already exists` on upload: version already published. Bump version and rebuild.
- `twine check` failures: fix metadata/readme and rebuild.
- Install failures from TestPyPI: ensure `--extra-index-url https://pypi.org/simple` is present for dependencies.
