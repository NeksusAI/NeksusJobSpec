"""Local stdio MCP server for Neksus JobSpec."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from neksus_jobspec_mcp.service import JobspecMcpService

SERVER_NAME = "neksus-jobspec-local"


def build_tool_map(service: JobspecMcpService) -> dict[str, Callable[..., dict[str, Any]]]:
    """Build MCP tool map from service methods."""
    return {
        "version": lambda: service.safe_call("version"),
        "init": lambda root=None, empty=False, force=False: service.safe_call(
            "init", root=root, empty=empty, force=force
        ),
        "check": lambda root=None, strict=False: service.safe_call(
            "check", root=root, strict=strict
        ),
        "config_get": lambda key=None, root=None: service.safe_call(
            "config_get", key=key, root=root
        ),
        "config_set": lambda key, value, root=None: service.safe_call(
            "config_set", key=key, value=value, root=root
        ),
        "themes_list": lambda: service.safe_call("themes_list"),
        "themes_show": lambda name: service.safe_call("themes_show", name=name),
        "spec_schema": lambda output=None: service.safe_call("spec_schema", output=output),
        "spec_templates": lambda: service.safe_call("spec_templates"),
        "spec_new": lambda name, template="basic", output=None, force=False: service.safe_call(
            "spec_new", name=name, template=template, output=output, force=force
        ),
        "spec_validate": lambda path, strict=False: service.safe_call(
            "spec_validate", path=path, strict=strict
        ),
        "spec_render": lambda path, format="web", theme=None, asset_base_url=None, output=None, no_validate=False: (
            service.safe_call(  # noqa: E501
                "spec_render",
                path=path,
                format=format,
                theme=theme,
                asset_base_url=asset_base_url,
                output=output,
                no_validate=no_validate,
            )
        ),
        "spec_inspect": lambda path: service.safe_call("spec_inspect", path=path),
        "spec_status": lambda path: service.safe_call("spec_status", path=path),
        "spec_migrate": lambda path, write=False: service.safe_call(
            "spec_migrate", path=path, write=write
        ),
        "spec_export": lambda path, target, out: service.safe_call(
            "spec_export", path=path, target=target, out=out
        ),
        "feed_export": lambda inputs, target, out, skip_invalid=False: service.safe_call(
            "feed_export", inputs=inputs, target=target, out=out, skip_invalid=skip_invalid
        ),
        "feed_sitemap": lambda inputs, base_url, out, exclude_closed=False: service.safe_call(
            "feed_sitemap",
            inputs=inputs,
            base_url=base_url,
            out=out,
            exclude_closed=exclude_closed,
        ),
    }


def main() -> None:
    """Run local stdio MCP server."""
    try:
        from mcp.server.fastmcp import FastMCP
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            'MCP dependency not installed. Install with: pip install "neksus-jobspec[mcp]"'
        ) from exc

    service = JobspecMcpService()
    mcp = FastMCP(SERVER_NAME)
    tool_map = build_tool_map(service)
    for name, fn in tool_map.items():
        mcp.tool(name=name)(fn)
    mcp.run()


if __name__ == "__main__":
    main()
