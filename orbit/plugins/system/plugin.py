"""System plugin — collects CPU, memory and disk metrics."""

from __future__ import annotations

from orbit.core.cache import CacheManager
from orbit.core.config import SystemConfig
from orbit.core.events import Event, EventType, bus
from orbit.core.logger import get_logger
from orbit.core.plugin import Plugin
from orbit.plugins.system.service import SystemService

logger = get_logger("system")


class SystemPlugin(Plugin):
    """Gathers system metrics and writes them to cache for Conky."""

    def __init__(
        self,
        config: SystemConfig,
        cache: CacheManager,
        **kwargs,
    ) -> None:
        super().__init__(
            name="system",
            update_interval=config.update_interval,
            **kwargs,
        )
        self._cache = cache
        self._service = SystemService()

    def initialize(self) -> None:
        logger.info("System plugin initialized")
        bus.emit(Event(EventType.PLUGIN_STARTED, source=self.name))

    def update(self) -> None:
        try:
            data = self._service.get_system_data()
            self._cache.set("system", data.to_dict())
            logger.debug(
                "System updated: CPU %.1f%%, RAM %.1f%%, Disk %.1f%%",
                data.cpu.percent,
                data.memory.percent,
                data.disk.percent,
            )
            bus.emit(Event(EventType.PLUGIN_UPDATED, source=self.name))
        except Exception:
            logger.exception("Failed to update system data")
            bus.emit(Event(EventType.PLUGIN_FAILED, source=self.name))

    def shutdown(self) -> None:
        logger.info("System plugin stopped")
        bus.emit(Event(EventType.PLUGIN_STOPPED, source=self.name))
