from __future__ import annotations

from pathlib import Path

from neksus.core.jobspec.parser import load_jobspec
from neksus.core.jobspec.renderer import render_jobspec


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HTML_PATH = (
    ROOT / "fixtures" / "stitch" / "isolated-jobspec-output.soft-professional.html"
)
CANONICAL_PNG_PATH = ROOT / "fixtures" / "stitch" / "isolated-jobspec-output.soft-professional.png"


def _normalized(value: str) -> str:
    return value.replace("\r\n", "\n")


def test_soft_professional_html_matches_stitch_contract() -> None:
    spec = load_jobspec(ROOT / "examples" / "danish-job-detail.jobspec.yaml")
    rendered = render_jobspec(spec, format="web", theme="soft-professional")
    expected = CANONICAL_HTML_PATH.read_text(encoding="utf-8")
    assert _normalized(rendered) == _normalized(expected)


def test_soft_professional_reference_screenshot_is_pinned() -> None:
    assert CANONICAL_PNG_PATH.exists()
    assert CANONICAL_PNG_PATH.stat().st_size > 0
