"""Tests for orbit.core.cache."""

import json

import pytest

from orbit.core.cache import CacheManager


@pytest.fixture()
def cache(tmp_path):
    return CacheManager(cache_dir=tmp_path)


def test_set_and_get(cache):
    cache.set("weather", {"temp": 25})
    assert cache.get("weather") == {"temp": 25}


def test_get_missing_returns_none(cache):
    assert cache.get("nonexistent") is None


def test_delete(cache):
    cache.set("weather", {"temp": 25})
    assert cache.delete("weather") is True
    assert cache.get("weather") is None


def test_delete_missing_returns_false(cache):
    assert cache.delete("nonexistent") is False


def test_exists(cache):
    assert cache.exists("weather") is False
    cache.set("weather", {"temp": 25})
    assert cache.exists("weather") is True


def test_clear(cache):
    cache.set("a", {"x": 1})
    cache.set("b", {"x": 2})
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None


def test_creates_dir(tmp_path):
    target = tmp_path / "nested" / "cache"
    mgr = CacheManager(cache_dir=target)
    mgr.set("test", {"val": 1})
    assert target.exists()


def test_file_is_valid_json(cache):
    cache.set("test", {"key": "value"})
    files = list(cache.cache_dir.glob("test.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text())
    assert data == {"key": "value"}


def test_namespace_sanitization(cache):
    cache.set("a/b", {"x": 1})
    assert cache.get("a/b") == {"x": 1}
    files = list(cache.cache_dir.glob("a_b.json"))
    assert len(files) == 1
