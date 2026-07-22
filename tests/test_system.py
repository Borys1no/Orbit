"""Tests for orbit.plugins.system."""

from unittest.mock import MagicMock, patch

from orbit.core.cache import CacheManager
from orbit.core.config import SystemConfig
from orbit.plugins.system.models import CpuData, DiskData, MemoryData, SystemData
from orbit.plugins.system.plugin import SystemPlugin
from orbit.plugins.system.service import SystemService


def test_system_data_to_dict():
    data = SystemData(
        hostname="test-host",
        os="Linux 6.0",
        kernel="6.0.0",
        uptime=12345,
        cpu=CpuData(
            percent=45.0, cores_physical=4, cores_logical=8, frequency_current=3200
        ),
        memory=MemoryData(
            total=8000000000, available=4000000000, used=4000000000, percent=50.0
        ),
        disk=DiskData(
            total=500000000000, used=200000000000, free=300000000000, percent=40.0
        ),
    )
    d = data.to_dict()
    assert d["hostname"] == "test-host"
    assert d["cpu"]["percent"] == 45.0
    assert d["memory"]["percent"] == 50.0
    assert d["disk"]["percent"] == 40.0


@patch("orbit.plugins.system.service.psutil")
def test_service_get_system_data(mock_psutil):
    mock_psutil.boot_time.return_value = 1000000
    mock_psutil.cpu_percent.return_value = 25.0
    mock_psutil.cpu_count.side_effect = lambda logical=True: 4 if logical else 2
    mock_psutil.cpu_freq.return_value = MagicMock(current=2400.0)

    mock_mem = MagicMock()
    mock_mem.total = 8000000000
    mock_mem.available = 6000000000
    mock_mem.used = 2000000000
    mock_mem.percent = 25.0
    mock_psutil.virtual_memory.return_value = mock_mem

    mock_disk = MagicMock()
    mock_disk.total = 500000000000
    mock_disk.used = 100000000000
    mock_disk.free = 400000000000
    mock_disk.percent = 20.0
    mock_psutil.disk_usage.return_value = mock_disk

    service = SystemService()
    data = service.get_system_data()

    assert data.hostname != ""
    assert data.cpu.cores_physical == 2
    assert data.memory.percent == 25.0
    assert data.disk.percent == 20.0


def test_plugin_update_writes_cache(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = SystemConfig()

    plugin = SystemPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.get_system_data.return_value = SystemData(
        hostname="test",
        os="Linux",
        kernel="6.0",
        uptime=100,
        cpu=CpuData(10.0, 2, 4, 2000.0),
        memory=MemoryData(8000000000, 6000000000, 2000000000, 25.0),
        disk=DiskData(500000000000, 100000000000, 400000000000, 20.0),
    )
    plugin._service = mock_service

    plugin.update()

    data = cache.get("system")
    assert data is not None
    assert data["hostname"] == "test"
    assert data["cpu"]["percent"] == 10.0


def test_plugin_update_handles_error(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = SystemConfig()

    plugin = SystemPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.get_system_data.side_effect = Exception("psutil error")
    plugin._service = mock_service

    plugin.update()

    assert cache.get("system") is None
