#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI_BIN="$ROOT_DIR/.venv/bin/neksus-jobspec"
MKDOCS_BIN="$ROOT_DIR/.venv/bin/mkdocs"

if [[ ! -x "$CLI_BIN" ]]; then
  echo "[smoke] CLI binary not found at $CLI_BIN. Run: uv sync"
  exit 1
fi

cd "$ROOT_DIR"

echo "[smoke] checking CLI version"
if "$CLI_BIN" --version >/dev/null 2>&1; then
  :
else
  "$CLI_BIN" version >/dev/null
fi

echo "[smoke] validating known-valid fixture"
"$CLI_BIN" spec validate fixtures/valid/backend-engineer.jobspec.yaml >/dev/null

echo "[smoke] validating known-invalid fixture (expect failure)"
if "$CLI_BIN" spec validate fixtures/invalid/missing-title.jobspec.yaml >/dev/null 2>&1; then
  echo "[smoke] expected invalid fixture to fail validation"
  exit 1
fi

tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

echo "[smoke] initializing temporary project"
cd "$tmp_dir"
"$CLI_BIN" init --empty >/dev/null
"$CLI_BIN" spec new backend-engineer >/dev/null

echo "[smoke] validating generated jobspec"
"$CLI_BIN" spec validate jobspecs/backend-engineer.jobspec.yaml >/dev/null

echo "[smoke] rendering markdown output"
"$CLI_BIN" spec render jobspecs/backend-engineer.jobspec.yaml \
  --format markdown \
  --output dist/backend-engineer.md >/dev/null

echo "[smoke] rendering fixture with custom CSS"
"$CLI_BIN" spec render jobspecs/backend-engineer.jobspec.yaml \
  --format html \
  --theme modern \
  --css "$ROOT_DIR/examples/jobspec.css" \
  --output dist/backend-engineer.html >/dev/null

echo "[smoke] running project check"
"$CLI_BIN" check >/dev/null

cd "$ROOT_DIR"

echo "[smoke] checking public Python API import"
"$ROOT_DIR/.venv/bin/python" -c "from neksus_jobspec import load_jobspec, render_jobspec; print('ok')" >/dev/null

echo "[smoke] building docs in strict mode"
if [[ -x "$MKDOCS_BIN" ]]; then
  "$MKDOCS_BIN" build --strict >/dev/null
else
  echo "[smoke] mkdocs not found in .venv. Install docs dependencies first: pip install -r requirements-docs.txt"
  exit 1
fi

echo "[smoke] all smoke checks passed"
