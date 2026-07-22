"""Event system and plugin lifecycle states for Orbit."""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable


class PluginStatus(Enum):
    """Lifecycle states for Orbit plugins."""

    DISABLED = "disabled"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


class EventType(Enum):
    """Built-in event types."""

    PLUGIN_STARTED = "plugin.started"
    PLUGIN_STOPPED = "plugin.stopped"
    PLUGIN_UPDATED = "plugin.updated"
    PLUGIN_FAILED = "plugin.failed"


class Event:
    """Simple event payload."""

    __slots__ = ("event_type", "source", "data")

    def __init__(
        self,
        event_type: EventType | str,
        source: str = "",
        data: dict[str, Any] | None = None,
    ) -> None:
        self.event_type = event_type
        self.source = source
        self.data = data or {}


class EventBus:
    """Minimal publish / subscribe event bus."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[[Event], None]]] = {}

    def on(
        self,
        event_type: EventType | str,
        callback: Callable[[Event], None],
    ) -> None:
        key = event_type.value if isinstance(event_type, EventType) else event_type
        self._listeners.setdefault(key, []).append(callback)

    def off(
        self,
        event_type: EventType | str,
        callback: Callable[[Event], None],
    ) -> None:
        key = event_type.value if isinstance(event_type, EventType) else event_type
        listeners = self._listeners.get(key, [])
        if callback in listeners:
            listeners.remove(callback)

    def emit(self, event: Event) -> None:
        key = (
            event.event_type.value
            if isinstance(event.event_type, EventType)
            else event.event_type
        )
        for callback in self._listeners.get(key, []):
            callback(event)


bus = EventBus()
