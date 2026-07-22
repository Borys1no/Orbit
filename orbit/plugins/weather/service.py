"""Weather service."""

from orbit.plugins.weather.models import WeatherData


class WeatherService:
    """Handles weather retrieval."""

    def get_weather(self) -> WeatherData:
        """Retrieve current weather."""

        raise NotImplementedError
