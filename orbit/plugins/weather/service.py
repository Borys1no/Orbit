"""Weather service — fetches data from OpenWeatherMap API."""

from __future__ import annotations

from typing import Any

import requests

from orbit.core.logger import get_logger
from orbit.plugins.weather.models import WeatherData

logger = get_logger("weather")

_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherService:
    """Retrieves and parses weather data from OpenWeatherMap."""

    def __init__(
        self,
        api_key: str,
        city_id: int,
        units: str = "metric",
        language: str = "es",
    ) -> None:
        self._api_key = api_key
        self._city_id = city_id
        self._units = units
        self._language = language

    def get_weather(self) -> WeatherData:
        """Fetch current weather from the API."""
        params: dict[str, Any] = {
            "id": self._city_id,
            "appid": self._api_key,
            "units": self._units,
            "lang": self._language,
        }

        logger.debug("Fetching weather for city_id=%s", self._city_id)
        response = requests.get(_BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return self._parse(data)

    @staticmethod
    def _parse(data: dict[str, Any]) -> WeatherData:
        main = data["main"]
        wind = data["wind"]
        weather = data["weather"][0]

        return WeatherData(
            city=data["name"],
            country=data["sys"]["country"],
            temperature=main["temp"],
            feels_like=main["feels_like"],
            humidity=main["humidity"],
            pressure=main["pressure"],
            description=weather["description"],
            icon=weather["icon"],
            wind_speed=wind["speed"],
        )
