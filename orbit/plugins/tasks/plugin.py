"""Tasks plugin — fetches pending tasks from Google Tasks."""

from __future__ import annotations

from orbit.core.cache import CacheManager
from orbit.core.config import TasksConfig
from orbit.core.events import Event, EventType, bus
from orbit.core.logger import get_logger
from orbit.core.plugin import Plugin
from orbit.plugins.tasks.service import TasksService

logger = get_logger("tasks")


class TasksPlugin(Plugin):
    """Fetches pending Google Tasks and writes them to cache for Conky."""

    def __init__(
        self,
        config: TasksConfig,
        cache: CacheManager,
        **kwargs,
    ) -> None:
        super().__init__(
            name="tasks",
            update_interval=config.update_interval,
            **kwargs,
        )
        self._cache = cache
        self._service = TasksService(
            credentials_path=config.credentials_path,
            token_path=config.token_path,
            task_list=config.task_list,
        )

    def initialize(self) -> None:
        logger.info("Tasks plugin initialized")
        bus.emit(Event(EventType.PLUGIN_STARTED, source=self.name))

    def update(self) -> None:
        try:
            if not self._service.is_available():
                self._cache.set("tasks", {"active": False, "items": []})
                return

            tasks = self._service.get_tasks()
            data = {
                "active": True,
                "count": len(tasks),
                "items": [t.to_dict() for t in tasks],
            }
            self._cache.set("tasks", data)
            logger.debug("Tasks updated: %d pending", len(tasks))
            bus.emit(Event(EventType.PLUGIN_UPDATED, source=self.name))
        except Exception:
            logger.exception("Failed to update tasks")
            bus.emit(Event(EventType.PLUGIN_FAILED, source=self.name))

    def shutdown(self) -> None:
        logger.info("Tasks plugin stopped")
        bus.emit(Event(EventType.PLUGIN_STOPPED, source=self.name))
