"""Tests for orbit.plugins.calendar."""

from unittest.mock import MagicMock

from orbit.core.cache import CacheManager
from orbit.core.config import CalendarConfig
from orbit.plugins.calendar.models import EventData
from orbit.plugins.calendar.plugin import CalendarPlugin
from orbit.plugins.calendar.service import CalendarService


def test_event_data_to_dict():
    event = EventData(
        event_id="evt123",
        summary="Team meeting",
        description="Weekly sync",
        start="2026-07-22T10:00:00Z",
        end="2026-07-22T11:00:00Z",
        location="Zoom",
    )
    d = event.to_dict()
    assert d["event_id"] == "evt123"
    assert d["summary"] == "Team meeting"
    assert d["location"] == "Zoom"


def test_service_is_available_false(tmp_path):
    service = CalendarService(
        credentials_path=str(tmp_path / "missing.json"),
        token_path=str(tmp_path / "token.json"),
    )
    assert service.is_available() is False


def test_service_is_available_true(tmp_path):
    creds = tmp_path / "credentials.json"
    creds.write_text("{}")
    service = CalendarService(
        credentials_path=str(creds),
        token_path=str(tmp_path / "token.json"),
    )
    assert service.is_available() is True


def test_plugin_update_writes_cache(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = CalendarConfig(credentials_path="", token_path="")

    plugin = CalendarPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.return_value = True
    mock_service.get_events.return_value = [
        EventData("1", "Meeting", "", "10:00", "11:00", ""),
        EventData("2", "Lunch", "", "12:00", "13:00", "Cafe"),
    ]
    plugin._service = mock_service

    plugin.update()

    data = cache.get("calendar")
    assert data is not None
    assert data["active"] is True
    assert data["count"] == 2
    assert len(data["events"]) == 2


def test_plugin_update_no_credentials(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = CalendarConfig(credentials_path="", token_path="")

    plugin = CalendarPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.return_value = False
    plugin._service = mock_service

    plugin.update()

    data = cache.get("calendar")
    assert data is not None
    assert data["active"] is False
    assert data["events"] == []


def test_plugin_update_handles_error(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = CalendarConfig(credentials_path="", token_path="")

    plugin = CalendarPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.side_effect = Exception("API error")
    plugin._service = mock_service

    plugin.update()

    assert cache.get("calendar") is None
