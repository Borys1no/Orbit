"""Common utilities for Orbit."""

from __future__ import annotations

import platform
from pathlib import Path
from typing import Any


def project_root() -> Path:
    """Return the absolute path to the project root."""
    return Path(__file__).resolve().parent.parent.parent


def cache_path(cache_dir: str = "cache", filename: str = "") -> Path:
    root = project_root() / cache_dir
    root.mkdir(parents=True, exist_ok=True)
    return root / filename if filename else root


def format_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n = int(n / 1024)
    return f"{n:.1f} PB"


def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        m, s = divmod(seconds, 60)
        return f"{m}m {s}s"
    h, remainder = divmod(seconds, 3600)
    m, _ = divmod(remainder, 60)
    return f"{h}h {m}m"


def safe_get(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default
    return current


def os_info() -> dict[str, str]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
    }
