"""System models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CpuData:
    percent: float
    cores_physical: int
    cores_logical: int
    frequency_current: float


@dataclass(slots=True)
class MemoryData:
    total: int
    available: int
    used: int
    percent: float


@dataclass(slots=True)
class DiskData:
    total: int
    used: int
    free: int
    percent: float


@dataclass(slots=True)
class SystemData:
    hostname: str
    os: str
    kernel: str
    uptime: int

    cpu: CpuData = field(default_factory=lambda: CpuData(0, 0, 0, 0))
    memory: MemoryData = field(default_factory=lambda: MemoryData(0, 0, 0, 0))
    disk: DiskData = field(default_factory=lambda: DiskData(0, 0, 0, 0))

    def to_dict(self) -> dict[str, Any]:
        return {
            "hostname": self.hostname,
            "os": self.os,
            "kernel": self.kernel,
            "uptime": self.uptime,
            "cpu": {
                "percent": self.cpu.percent,
                "cores_physical": self.cpu.cores_physical,
                "cores_logical": self.cpu.cores_logical,
                "frequency_current": self.cpu.frequency_current,
            },
            "memory": {
                "total": self.memory.total,
                "available": self.memory.available,
                "used": self.memory.used,
                "percent": self.memory.percent,
            },
            "disk": {
                "total": self.disk.total,
                "used": self.disk.used,
                "free": self.disk.free,
                "percent": self.disk.percent,
            },
        }
