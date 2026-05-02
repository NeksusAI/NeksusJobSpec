from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()


def test_init_creates_project_structure() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "Initialized Neksus project." in result.stdout
        assert Path(".neksus/config.yaml").exists()
        assert Path("jobspecs").exists()
        assert Path("dist").exists()
        assert Path("jobspecs/example.jobspec.yaml").exists()


def test_init_empty_skips_example_file() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--empty"])
        assert result.exit_code == 0
        assert Path("jobspecs/example.jobspec.yaml").exists() is False


def test_init_refuses_overwrite_without_force() -> None:
    with runner.isolated_filesystem():
        first = runner.invoke(app, ["init"])
        assert first.exit_code == 0
        second = runner.invoke(app, ["init"])
        assert second.exit_code == 3
        assert "Use --force" in second.output
