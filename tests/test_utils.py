"""Tests for orbit.core.utils."""

from orbit.core.utils import format_bytes, format_duration, safe_get


def test_format_bytes():
    assert format_bytes(0) == "0.0 B"
    assert format_bytes(1024) == "1.0 KB"
    assert format_bytes(1048576) == "1.0 MB"


def test_format_duration_seconds():
    assert format_duration(30) == "30s"


def test_format_duration_minutes():
    assert format_duration(90) == "1m 30s"


def test_format_duration_hours():
    assert format_duration(3661) == "1h 1m"


def test_safe_get_simple():
    data = {"a": {"b": {"c": 42}}}
    assert safe_get(data, "a", "b", "c") == 42


def test_safe_get_missing():
    data = {"a": 1}
    assert safe_get(data, "x", "y") is None


def test_safe_get_default():
    data = {"a": 1}
    assert safe_get(data, "x", default=99) == 99
