"""Tests for orbit.plugins.tasks."""

from unittest.mock import MagicMock

from orbit.core.cache import CacheManager
from orbit.core.config import TasksConfig
from orbit.plugins.tasks.models import TaskData
from orbit.plugins.tasks.plugin import TasksPlugin
from orbit.plugins.tasks.service import TasksService


def test_task_data_to_dict():
    task = TaskData(
        task_id="abc123",
        title="Buy milk",
        notes="2%",
        status="needsAction",
        due="2026-01-15T00:00:00.000Z",
    )
    d = task.to_dict()
    assert d["task_id"] == "abc123"
    assert d["title"] == "Buy milk"
    assert d["status"] == "needsAction"


def test_service_is_available_false(tmp_path):
    service = TasksService(
        credentials_path=str(tmp_path / "missing.json"),
        token_path=str(tmp_path / "token.json"),
    )
    assert service.is_available() is False


def test_service_is_available_true(tmp_path):
    creds = tmp_path / "credentials.json"
    creds.write_text("{}")
    service = TasksService(
        credentials_path=str(creds),
        token_path=str(tmp_path / "token.json"),
    )
    assert service.is_available() is True


def test_plugin_update_writes_cache(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = TasksConfig(credentials_path="", token_path="")

    plugin = TasksPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.return_value = True
    mock_service.get_tasks.return_value = [
        TaskData("1", "Task 1", "", "needsAction", ""),
        TaskData("2", "Task 2", "", "needsAction", ""),
    ]
    plugin._service = mock_service

    plugin.update()

    data = cache.get("tasks")
    assert data is not None
    assert data["active"] is True
    assert data["count"] == 2
    assert len(data["items"]) == 2


def test_plugin_update_no_credentials(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = TasksConfig(credentials_path="", token_path="")

    plugin = TasksPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.return_value = False
    plugin._service = mock_service

    plugin.update()

    data = cache.get("tasks")
    assert data is not None
    assert data["active"] is False
    assert data["items"] == []


def test_plugin_update_handles_error(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = TasksConfig(credentials_path="", token_path="")

    plugin = TasksPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.side_effect = Exception("API error")
    plugin._service = mock_service

    plugin.update()

    assert cache.get("tasks") is None
