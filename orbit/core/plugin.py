"""Base classes for Orbit plugins."""

from __future__ import annotations
from abc import ABC, abstractmethod
from orbit.core.events import PluginStatus


class Plugin(ABC):
    """Base class for every Orbit plugin"""

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        update_interval: int = 60,
        enabled: bool = True,
    ) -> None:
        self.name = name
        self.version = version
        self.update_interval = update_interval
        self.enabled = enabled
        self.status = PluginStatus.READY if enabled else PluginStatus.DISABLED
        self.last_update = 0.0

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin."""

    @abstractmethod
    def update(self) -> None:
        """Update the plugin data."""

    @abstractmethod
    def shutdown(self) -> None:
        """Release plugin resources."""
