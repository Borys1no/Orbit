"""Weather models."""

from dataclasses import dataclass


@dataclass(slots=True)
class WeatherData:
    """Represents current weather information."""

    city: str
    country: str

    temperature: float
    feels_like: float

    humidity: int
    pressure: int

    description: str
    icon: str

    wind_speed: float
