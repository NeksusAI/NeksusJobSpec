"""Architecture boundary checks for layering contracts."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_cli_commands_use_app_use_cases() -> None:
    spec = _read("src/neksus_jobspec_cli/commands/spec.py")
    feed = _read("src/neksus_jobspec_cli/commands/feed.py")
    check = _read("src/neksus_jobspec_cli/commands/check.py")
    config = _read("src/neksus_jobspec_cli/commands/config.py")
    render = _read("src/neksus_jobspec_cli/commands/render.py")

    assert "from neksus_jobspec.app import SpecUseCase" in spec
    assert "from neksus_jobspec.app import FeedUseCase" in feed
    assert "from neksus_jobspec.app import ProjectUseCase" in check
    assert "from neksus_jobspec.app import ProjectUseCase" in config
    assert "from neksus_jobspec.app import RenderUseCase" in render
    assert "from neksus_jobspec.project." not in spec


def test_mcp_service_uses_app_use_cases() -> None:
    service = _read("src/neksus_jobspec_mcp/service.py")
    assert "from neksus_jobspec.app import FeedUseCase, ProjectUseCase, SpecUseCase" in service
