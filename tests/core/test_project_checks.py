from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()


def test_check_succeeds_in_initialized_project() -> None:
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init"])
        assert init_result.exit_code == 0

        check_result = runner.invoke(app, ["check"])
        assert check_result.exit_code == 0
        assert "Project check passed." in check_result.stdout


def test_duplicate_jobspec_ids_fail_project_check() -> None:
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init"])
        assert init_result.exit_code == 0

        base = Path("jobspecs/example.jobspec.yaml").read_text(encoding="utf-8")
        Path("jobspecs/another.jobspec.yaml").write_text(base, encoding="utf-8")

        check_result = runner.invoke(app, ["check"])
        assert check_result.exit_code == 1
        assert "duplicate" in check_result.output.lower()
