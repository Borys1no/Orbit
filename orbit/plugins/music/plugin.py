"""Music plugin — reads currently playing track via playerctl."""

from __future__ import annotations

from orbit.core.cache import CacheManager
from orbit.core.config import MusicConfig
from orbit.core.events import Event, EventType, bus
from orbit.core.logger import get_logger
from orbit.core.plugin import Plugin
from orbit.plugins.music.service import MusicService, NoPlayerError

logger = get_logger("music")


class MusicPlugin(Plugin):
    """Gathers currently playing track info and writes it to cache for Conky."""

    def __init__(
        self,
        config: MusicConfig,
        cache: CacheManager,
        **kwargs,
    ) -> None:
        super().__init__(
            name="music",
            update_interval=config.update_interval,
            **kwargs,
        )
        self._cache = cache
        self._service = MusicService(player=config.player)

    def initialize(self) -> None:
        logger.info("Music plugin initialized")
        bus.emit(Event(EventType.PLUGIN_STARTED, source=self.name))

    def update(self) -> None:
        try:
            if not self._service.is_available():
                self._cache.set("music", {"active": False})
                return

            track = self._service.get_track()
            data = track.to_dict()
            data["active"] = True
            self._cache.set("music", data)
            logger.debug("Now playing: %s - %s", track.artist, track.title)
            bus.emit(Event(EventType.PLUGIN_UPDATED, source=self.name))
        except NoPlayerError:
            self._cache.set("music", {"active": False})
        except Exception:
            logger.exception("Failed to update music data")
            bus.emit(Event(EventType.PLUGIN_FAILED, source=self.name))

    def shutdown(self) -> None:
        logger.info("Music plugin stopped")
        bus.emit(Event(EventType.PLUGIN_STOPPED, source=self.name))
