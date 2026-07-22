"""Tests for orbit.plugins.weather."""

from unittest.mock import MagicMock, patch

from orbit.core.cache import CacheManager
from orbit.core.config import WeatherConfig
from orbit.plugins.weather.models import WeatherData
from orbit.plugins.weather.plugin import WeatherPlugin
from orbit.plugins.weather.service import WeatherService

SAMPLE_API_RESPONSE = {
    "name": "Buenos Aires",
    "sys": {"country": "AR"},
    "main": {
        "temp": 22.5,
        "feels_like": 21.0,
        "humidity": 65,
        "pressure": 1013,
    },
    "weather": [{"description": "cielo despejado", "icon": "01d"}],
    "wind": {"speed": 3.2},
}


def test_weather_data_to_dict():
    w = WeatherData(
        city="Buenos Aires",
        country="AR",
        temperature=22.5,
        feels_like=21.0,
        humidity=65,
        pressure=1013,
        description="cielo despejado",
        icon="01d",
        wind_speed=3.2,
    )
    d = w.to_dict()
    assert d["city"] == "Buenos Aires"
    assert d["temperature"] == 22.5
    assert d["humidity"] == 65


def test_service_parse():
    result = WeatherService._parse(SAMPLE_API_RESPONSE)
    assert result.city == "Buenos Aires"
    assert result.country == "AR"
    assert result.temperature == 22.5
    assert result.description == "cielo despejado"


@patch("orbit.plugins.weather.service.requests.get")
def test_service_get_weather(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = SAMPLE_API_RESPONSE
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    service = WeatherService(api_key="test", city_id=123)
    weather = service.get_weather()

    assert weather.city == "Buenos Aires"
    mock_get.assert_called_once()


def test_plugin_update_writes_cache(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = WeatherConfig(api_key="test", city_id=123)

    plugin = WeatherPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.get_weather.return_value = WeatherData(
        city="Buenos Aires",
        country="AR",
        temperature=22.5,
        feels_like=21.0,
        humidity=65,
        pressure=1013,
        description="cielo despejado",
        icon="01d",
        wind_speed=3.2,
    )
    plugin._service = mock_service

    plugin.update()

    data = cache.get("weather")
    assert data is not None
    assert data["city"] == "Buenos Aires"


def test_plugin_update_handles_error(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = WeatherConfig(api_key="test", city_id=123)

    plugin = WeatherPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.get_weather.side_effect = Exception("API error")
    plugin._service = mock_service

    plugin.update()

    assert cache.get("weather") is None
