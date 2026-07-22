"""System service — collects system metrics using psutil."""

from __future__ import annotations

import platform
import time

import psutil

from orbit.plugins.system.models import CpuData, DiskData, MemoryData, SystemData


class SystemService:
    """Retrieves system information via psutil."""

    def get_system_data(self) -> SystemData:
        return SystemData(
            hostname=platform.node(),
            os=f"{platform.system()} {platform.release()}",
            kernel=platform.release(),
            uptime=int(time.time() - psutil.boot_time()),
            cpu=self._cpu(),
            memory=self._memory(),
            disk=self._disk(),
        )

    @staticmethod
    def _cpu() -> CpuData:
        freq = psutil.cpu_freq()
        return CpuData(
            percent=psutil.cpu_percent(interval=0.1),
            cores_physical=psutil.cpu_count(logical=False) or 0,
            cores_logical=psutil.cpu_count(logical=True) or 0,
            frequency_current=freq.current if freq else 0.0,
        )

    @staticmethod
    def _memory() -> MemoryData:
        mem = psutil.virtual_memory()
        return MemoryData(
            total=mem.total,
            available=mem.available,
            used=mem.used,
            percent=mem.percent,
        )

    @staticmethod
    def _disk() -> DiskData:
        disk = psutil.disk_usage("/")
        return DiskData(
            total=disk.total,
            used=disk.used,
            free=disk.free,
            percent=disk.percent,
        )
