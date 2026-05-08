from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from neksus_jobspec_cli.main import app
from tests.spec_builders import write_export_spec

runner = CliRunner()


def test_spec_lint_warning_only_is_zero() -> None:
    with runner.isolated_filesystem():
        target = Path("role.jobspec.yaml")
        write_export_spec(target)
        result = runner.invoke(app, ["spec", "lint", str(target), "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert isinstance(payload["warnings"], list)


def test_spec_lint_invalid_is_nonzero() -> None:
    with runner.isolated_filesystem():
        target = Path("broken.jobspec.yaml")
        target.write_text("id: missing-required-fields\n", encoding="utf-8")
        result = runner.invoke(app, ["spec", "lint", str(target), "--json"])
        assert result.exit_code != 0


def test_spec_preview_renders_and_prints_url(monkeypatch: pytest.MonkeyPatch) -> None:
    with runner.isolated_filesystem():
        target = Path("role.jobspec.yaml")
        write_export_spec(target)

        import neksus_jobspec_cli.commands.spec as spec_cmd

        monkeypatch.setattr(spec_cmd.webbrowser, "open", lambda _url: True)

        def _stop_forever(self) -> None:  # pragma: no cover - test hook
            raise KeyboardInterrupt

        monkeypatch.setattr(spec_cmd.socketserver.TCPServer, "serve_forever", _stop_forever)

        result = runner.invoke(app, ["spec", "preview", str(target), "--no-open", "--port", "8766"])
        assert result.exit_code == 0
        assert "Preview available at:" in result.stdout
