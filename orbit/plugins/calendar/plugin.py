"""Calendar plugin — fetches upcoming events from Google Calendar."""

from __future__ import annotations

from orbit.core.cache import CacheManager
from orbit.core.config import CalendarConfig
from orbit.core.events import Event, EventType, bus
from orbit.core.logger import get_logger
from orbit.core.plugin import Plugin
from orbit.plugins.calendar.service import CalendarService

logger = get_logger("calendar")


class CalendarPlugin(Plugin):
    """Fetches upcoming Google Calendar events and writes them to cache."""

    def __init__(
        self,
        config: CalendarConfig,
        cache: CacheManager,
        **kwargs,
    ) -> None:
        super().__init__(
            name="calendar",
            update_interval=config.update_interval,
            **kwargs,
        )
        self._cache = cache
        self._service = CalendarService(
            credentials_path=config.credentials_path,
            token_path=config.token_path,
            calendar_id=config.calendar_id,
        )

    def initialize(self) -> None:
        logger.info("Calendar plugin initialized")
        bus.emit(Event(EventType.PLUGIN_STARTED, source=self.name))

    def update(self) -> None:
        try:
            if not self._service.is_available():
                self._cache.set("calendar", {"active": False, "events": []})
                return

            events = self._service.get_events()
            data = {
                "active": True,
                "count": len(events),
                "events": [e.to_dict() for e in events],
            }
            self._cache.set("calendar", data)
            logger.debug("Calendar updated: %d upcoming events", len(events))
            bus.emit(Event(EventType.PLUGIN_UPDATED, source=self.name))
        except Exception:
            logger.exception("Failed to update calendar")
            bus.emit(Event(EventType.PLUGIN_FAILED, source=self.name))

    def shutdown(self) -> None:
        logger.info("Calendar plugin stopped")
        bus.emit(Event(EventType.PLUGIN_STOPPED, source=self.name))
