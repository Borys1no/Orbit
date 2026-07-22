"""Tests for orbit.core.config."""

import json

from orbit.core.config import OrbitConfig, WeatherConfig


def test_default_config():
    cfg = OrbitConfig()
    assert cfg.weather.enabled is False
    assert cfg.weather.units == "metric"
    assert cfg.system.enabled is True
    assert cfg.cache_dir == "cache"
    assert cfg.log_file is None


def test_from_file(tmp_path):
    p = tmp_path / "orbit.json"
    data = {
        "weather": {
            "enabled": True,
            "api_key": "abc",
            "city_id": 123,
            "update_interval": 600,
        },
        "system": {"enabled": True, "update_interval": 10},
    }
    p.write_text(json.dumps(data))
    cfg = OrbitConfig.from_file(p)
    assert cfg.weather.enabled is True
    assert cfg.weather.api_key == "abc"
    assert cfg.weather.city_id == 123
    assert cfg.system.update_interval == 10


def test_from_file_missing_returns_defaults(tmp_path):
    cfg = OrbitConfig.from_file(tmp_path / "missing.json")
    assert cfg.weather == WeatherConfig()


def test_to_dict_roundtrip(tmp_path):
    cfg = OrbitConfig(weather=WeatherConfig(enabled=True, api_key="xyz", city_id=42))
    p = tmp_path / "orbit.json"
    cfg.save(p)
    loaded = OrbitConfig.from_file(p)
    assert loaded.weather.enabled is True
    assert loaded.weather.api_key == "xyz"
    assert loaded.weather.city_id == 42


def test_save_creates_parent_dirs(tmp_path):
    cfg = OrbitConfig()
    p = tmp_path / "a" / "b" / "config.json"
    cfg.save(p)
    assert p.exists()
