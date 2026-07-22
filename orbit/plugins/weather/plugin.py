"""Weather plugin — orchestrates weather data collection."""

from __future__ import annotations

from orbit.core.cache import CacheManager
from orbit.core.config import WeatherConfig
from orbit.core.events import Event, EventType, bus
from orbit.core.logger import get_logger
from orbit.core.plugin import Plugin
from orbit.plugins.weather.service import WeatherService

logger = get_logger("weather")


class WeatherPlugin(Plugin):
    """Collects weather data and writes it to cache for Conky."""

    def __init__(
        self,
        config: WeatherConfig,
        cache: CacheManager,
        **kwargs,
    ) -> None:
        super().__init__(
            name="weather",
            update_interval=config.update_interval,
            **kwargs,
        )
        self._config = config
        self._cache = cache
        self._service = WeatherService(
            api_key=config.api_key,
            city_id=config.city_id,
            units=config.units,
            language=config.language,
        )

    def initialize(self) -> None:
        logger.info("Weather plugin initialized")
        bus.emit(Event(EventType.PLUGIN_STARTED, source=self.name))

    def update(self) -> None:
        try:
            weather = self._service.get_weather()
            self._cache.set("weather", weather.to_dict())
            logger.info(
                "Weather updated: %s, %.1f°C",
                weather.city,
                weather.temperature,
            )
            bus.emit(Event(EventType.PLUGIN_UPDATED, source=self.name))
        except Exception:
            logger.exception("Failed to update weather")
            bus.emit(Event(EventType.PLUGIN_FAILED, source=self.name))

    def shutdown(self) -> None:
        logger.info("Weather plugin stopped")
        bus.emit(Event(EventType.PLUGIN_STOPPED, source=self.name))
