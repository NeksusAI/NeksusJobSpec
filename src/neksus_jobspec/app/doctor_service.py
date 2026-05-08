"""Environment and repository health checks for the CLI doctor command."""

from __future__ import annotations

import importlib
import platform
import tempfile
from pathlib import Path

from neksus_jobspec import __version__
from neksus_jobspec.app.spec_service import SpecUseCase
from neksus_jobspec.jobspec.rendering import list_theme_names


class DoctorService:
    """Run local health checks without requiring remote services."""

    def __init__(self) -> None:
        self._spec_use_case = SpecUseCase()

    def run(self) -> dict[str, object]:
        checks: list[dict[str, str]] = []

        def add(name: str, status: str, detail: str) -> None:
            checks.append({"name": name, "status": status, "detail": detail})

        py = platform.python_version()
        add("Python version", "OK", py)

        add("Installed package version", "OK", __version__)

        try:
            importlib.import_module("neksus_jobspec_cli.main")
            add("CLI importability", "OK", "neksus_jobspec_cli.main import works")
        except Exception as exc:  # noqa: BLE001
            add("CLI importability", "FAIL", str(exc))

        try:
            importlib.import_module("neksus_jobspec")
            add("Core package importability", "OK", "neksus_jobspec import works")
        except Exception as exc:  # noqa: BLE001
            add("Core package importability", "FAIL", str(exc))

        try:
            importlib.import_module("mcp.server.fastmcp")
            add("Optional MCP availability", "OK", "mcp extra available")
        except Exception:
            add(
                "Optional MCP availability",
                "WARN",
                'Install with pip install "neksus-jobspec[mcp]"',
            )

        try:
            theme_names = list_theme_names()
            add("Built-in themes", "OK", ", ".join(theme_names))
        except Exception as exc:  # noqa: BLE001
            add("Built-in themes", "FAIL", str(exc))

        try:
            importlib.import_module("neksus_jobspec.jobspec.models")
            add("Schema/model importability", "OK", "jobspec models import works")
        except Exception as exc:  # noqa: BLE001
            add("Schema/model importability", "FAIL", str(exc))

        repo_root = Path.cwd()
        example_candidates = [
            repo_root / "examples" / "startup-engineer.jobspec.yaml",
            repo_root / "jobspecs" / "example.jobspec.yaml",
        ]
        example = next((path for path in example_candidates if path.exists()), None)
        if example is None:
            add("Example JobSpec availability", "WARN", "No built-in example file found")
        else:
            add("Example JobSpec availability", "OK", str(example))
            try:
                with tempfile.TemporaryDirectory(prefix="neksus-doctor-") as tmp_dir:
                    out = Path(tmp_dir) / "doctor-preview.html"
                    self._spec_use_case.render_file(
                        example,
                        format="web",
                        theme="soft-professional",
                        no_validate=False,
                        asset_base_url=None,
                        output=out,
                    )
                    add("Example render smoke", "OK", str(out))
            except Exception as exc:  # noqa: BLE001
                add("Example render smoke", "FAIL", str(exc))

        expected_repo_paths = [
            repo_root / "README.md",
            repo_root / "CHANGELOG.md",
            repo_root / "AGENTS.MD",
            repo_root / "docs",
        ]
        llms_path = repo_root / "llms.txt"
        if llms_path.exists():
            expected_repo_paths.append(llms_path)

        for path in expected_repo_paths:
            if path.exists():
                add(f"Repo file: {path.name}", "OK", str(path))
            else:
                add(f"Repo file: {path.name}", "WARN", f"Missing {path}")

        failed = any(check["status"] == "FAIL" for check in checks)
        return {"ok": not failed, "checks": checks}
