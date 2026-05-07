#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "[smoke-ci] checking CLI version"
if ./.venv/bin/neksus-jobspec --version >/dev/null 2>&1; then
  :
else
  ./.venv/bin/neksus-jobspec version >/dev/null
fi

echo "[smoke-ci] validating known-valid fixture"
./.venv/bin/neksus-jobspec spec validate fixtures/valid/minimal-valid.jobspec.yaml >/dev/null

echo "[smoke-ci] validating known-invalid fixture (expect failure)"
if ./.venv/bin/neksus-jobspec spec validate fixtures/invalid/missing-title.jobspec.yaml >/dev/null 2>&1; then
  echo "[smoke-ci] expected invalid fixture to fail validation"
  exit 1
fi

tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

echo "[smoke-ci] init + generate + validate + render"
cd "$tmp_dir"
"$ROOT_DIR/.venv/bin/neksus-jobspec" init --empty >/dev/null
"$ROOT_DIR/.venv/bin/neksus-jobspec" spec new backend-engineer >/dev/null
"$ROOT_DIR/.venv/bin/neksus-jobspec" spec validate jobspecs/backend-engineer.jobspec.yaml >/dev/null
"$ROOT_DIR/.venv/bin/neksus-jobspec" spec render jobspecs/backend-engineer.jobspec.yaml --format web --output dist/backend-engineer.html >/dev/null
"$ROOT_DIR/.venv/bin/neksus-jobspec" spec render jobspecs/backend-engineer.jobspec.yaml --format web --theme "$ROOT_DIR/fixtures/themes/custom-basic" --output dist/backend-engineer-custom.html >/dev/null
"$ROOT_DIR/.venv/bin/neksus-jobspec" spec render jobspecs/backend-engineer.jobspec.yaml --format json-ld --output dist/backend-engineer.json >/dev/null
"$ROOT_DIR/.venv/bin/neksus-jobspec" check >/dev/null

cd "$ROOT_DIR"
echo "[smoke-ci] checking public Python API import"
./.venv/bin/python -c "from neksus_jobspec import load_jobspec, render_jobspec; print('ok')" >/dev/null

echo "[smoke-ci] building docs in strict mode"
./.venv/bin/mkdocs build --strict >/dev/null

echo "[smoke-ci] all smoke checks passed"
