from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()


def test_spec_templates_lists_stable_names() -> None:
    result = runner.invoke(app, ["spec", "templates", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["templates"] == ["basic", "engineering", "product", "sales"]


def test_spec_new_templates_generate_valid_specs() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        cases = [
            ("backend-engineer", "engineering"),
            ("product-manager", "product"),
            ("account-executive", "sales"),
            ("general-role", "basic"),
        ]
        for name, template in cases:
            create_result = runner.invoke(app, ["spec", "new", name, "--template", template])
            assert create_result.exit_code == 0
            target = Path(f"jobspecs/{name}.jobspec.yaml")
            validate_result = runner.invoke(app, ["spec", "validate", str(target)])
            assert validate_result.exit_code == 0


def test_spec_new_unknown_template_is_controlled_error() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        result = runner.invoke(app, ["spec", "new", "role", "--template", "unknown", "--json"])
        assert result.exit_code == 2
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
