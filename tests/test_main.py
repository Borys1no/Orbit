"""Tests for orbit.__main__."""

import json
from unittest.mock import MagicMock, patch

from orbit.__main__ import _build_parser, _build_plugins
from orbit.core.cache import CacheManager
from orbit.core.config import OrbitConfig, SystemConfig, WeatherConfig


def test_build_parser_defaults():
    parser = _build_parser()
    args = parser.parse_args([])
    assert args.config == "config/orbit.json"


def test_build_parser_custom_config():
    parser = _build_parser()
    args = parser.parse_args(["-c", "custom.json"])
    assert args.config == "custom.json"


def test_build_plugins_empty_when_disabled(tmp_path):
    config = OrbitConfig(
        weather=WeatherConfig(enabled=False),
        system=SystemConfig(enabled=False),
    )
    cache = CacheManager(cache_dir=tmp_path)
    plugins = _build_plugins(config, cache)
    assert len(plugins) == 0


def test_build_plugins_creates_weather(tmp_path):
    config = OrbitConfig(
        weather=WeatherConfig(enabled=True, api_key="abc123", city_id=123),
        system=SystemConfig(enabled=False),
    )
    cache = CacheManager(cache_dir=tmp_path)
    plugins = _build_plugins(config, cache)
    assert len(plugins) == 1
    assert plugins[0].name == "weather"


def test_build_plugins_creates_system(tmp_path):
    config = OrbitConfig(
        weather=WeatherConfig(enabled=False),
        system=SystemConfig(enabled=True),
    )
    cache = CacheManager(cache_dir=tmp_path)
    plugins = _build_plugins(config, cache)
    assert len(plugins) == 1
    assert plugins[0].name == "system"


def test_build_plugins_from_file(tmp_path):
    config_path = tmp_path / "orbit.json"
    config_path.write_text(
        json.dumps(
            {
                "weather": {"enabled": True, "api_key": "test", "city_id": 42},
                "system": {"enabled": False},
                "cache_dir": str(tmp_path / "cache"),
            }
        )
    )
    config = OrbitConfig.from_file(config_path)
    cache = CacheManager(cache_dir=tmp_path / "cache")
    plugins = _build_plugins(config, cache)
    assert len(plugins) == 1


@patch("orbit.__main__.Scheduler")
def test_main_exits_when_no_plugins(mock_scheduler_cls):
    from orbit.__main__ import main

    mock_scheduler = MagicMock()
    mock_scheduler.plugins = []
    mock_scheduler_cls.return_value = mock_scheduler

    try:
        main(["--config", "/nonexistent.json"])
    except SystemExit as e:
        assert e.code == 1
