#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

WHEEL_PATH="$(ls -1 "$ROOT_DIR"/dist/*.whl 2>/dev/null | sort -V | tail -n 1 || true)"
if [[ -z "$WHEEL_PATH" ]]; then
  echo "[smoke-wheel] no wheel found in dist/. Run: python -m build"
  exit 1
fi

tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

venv_dir="$tmp_dir/venv"
workspace_dir="$tmp_dir/workspace"

python3 -m venv "$venv_dir"
"$venv_dir/bin/python" -m pip install --upgrade pip >/dev/null
"$venv_dir/bin/pip" install "$WHEEL_PATH" >/dev/null

mkdir -p "$workspace_dir"
cd "$workspace_dir"

echo "[smoke-wheel] checking CLI version"
if "$venv_dir/bin/neksus-jobspec" --version >/dev/null 2>&1; then
  :
else
  "$venv_dir/bin/neksus-jobspec" version >/dev/null
fi

echo "[smoke-wheel] initializing project"
"$venv_dir/bin/neksus-jobspec" init >/dev/null

echo "[smoke-wheel] generating jobspec"
"$venv_dir/bin/neksus-jobspec" spec new backend-engineer >/dev/null

echo "[smoke-wheel] validating jobspec"
"$venv_dir/bin/neksus-jobspec" spec validate jobspecs/backend-engineer.jobspec.yaml >/dev/null

echo "[smoke-wheel] rendering web"
"$venv_dir/bin/neksus-jobspec" spec render jobspecs/backend-engineer.jobspec.yaml --format web --theme soft-professional >/dev/null

echo "[smoke-wheel] rendering json-ld"
"$venv_dir/bin/neksus-jobspec" spec render jobspecs/backend-engineer.jobspec.yaml --format json-ld >/dev/null

echo "[smoke-wheel] checking public Python API import"
"$venv_dir/bin/python" -c "from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec; print('ok')" >/dev/null

echo "[smoke-wheel] wheel smoke checks passed"
