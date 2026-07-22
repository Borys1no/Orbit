"""Orbit core package."""

from orbit.core.cache import CacheManager
from orbit.core.config import (
    CalendarConfig,
    MusicConfig,
    OrbitConfig,
    SystemConfig,
    TasksConfig,
    WeatherConfig,
)
from orbit.core.events import Event, EventBus, EventType, PluginStatus, bus
from orbit.core.logger import get_logger, setup_logging
from orbit.core.plugin import Plugin
from orbit.core.scheduler import Scheduler

__all__ = [
    "CacheManager",
    "CalendarConfig",
    "Event",
    "EventBus",
    "EventType",
    "MusicConfig",
    "OrbitConfig",
    "Plugin",
    "PluginStatus",
    "Scheduler",
    "SystemConfig",
    "TasksConfig",
    "WeatherConfig",
    "bus",
    "get_logger",
    "setup_logging",
]
