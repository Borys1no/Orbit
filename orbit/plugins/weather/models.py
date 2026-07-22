"""Weather models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "city": self.city,
            "country": self.country,
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "description": self.description,
            "icon": self.icon,
            "wind_speed": self.wind_speed,
        }
