from __future__ import annotations

from neksus_jobspec_mcp.server import build_tool_map
from neksus_jobspec_mcp.service import JobspecMcpService


def test_mcp_tool_map_has_representative_tools() -> None:
    tool_map = build_tool_map(JobspecMcpService())
    for key in [
        "version",
        "spec_schema",
        "spec_validate",
        "spec_render",
        "spec_export",
        "feed_export",
        "feed_sitemap",
        "check",
        "config_get",
        "themes_list",
    ]:
        assert key in tool_map
