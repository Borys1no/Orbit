"""JSON-based cache for Orbit plugins."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any


class CacheManager:
    """Thread-safe JSON cache manager.

    Each plugin stores its data in a separate JSON file under the cache
    directory. Conky reads these files directly without calling Python.
    """

    def __init__(self, cache_dir: str | Path = "cache") -> None:
        self._cache_dir = Path(cache_dir)
        self._lock = threading.Lock()
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

    def _path_for(self, namespace: str) -> Path:
        safe = namespace.replace("/", "_").replace("\\", "_")
        return self._cache_dir / f"{safe}.json"

    def get(self, namespace: str) -> dict[str, Any] | None:
        path = self._path_for(namespace)
        if not path.exists():
            return None
        with self._lock:
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError, OSError:
                return None

    def set(self, namespace: str, data: dict[str, Any]) -> None:
        path = self._path_for(namespace)
        with self._lock:
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    def delete(self, namespace: str) -> bool:
        path = self._path_for(namespace)
        with self._lock:
            if path.exists():
                path.unlink()
                return True
            return False

    def exists(self, namespace: str) -> bool:
        return self._path_for(namespace).exists()

    def clear(self) -> None:
        with self._lock:
            for f in self._cache_dir.glob("*.json"):
                f.unlink()
