"""Filesystem gateway used by app-layer use cases."""

from __future__ import annotations

import shutil
from pathlib import Path


class FileSystemGateway:
    """Small wrapper for filesystem side effects."""

    def read_text(self, path: Path, encoding: str = "utf-8") -> str:
        """Read text content from a file path."""
        return path.read_text(encoding=encoding)

    def write_text(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        """Write text content to a file path."""
        path.write_text(content, encoding=encoding)

    def mkdir(self, path: Path, parents: bool = True, exist_ok: bool = True) -> None:
        """Create a directory path with optional parent creation."""
        path.mkdir(parents=parents, exist_ok=exist_ok)

    def remove_tree(self, path: Path) -> None:
        """Delete a directory tree recursively."""
        shutil.rmtree(path)
