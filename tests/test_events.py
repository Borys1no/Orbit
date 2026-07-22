"""Tests for orbit.core.events."""

from orbit.core.events import Event, EventBus, EventType, PluginStatus


def test_plugin_status_values():
    assert PluginStatus.READY.value == "ready"
    assert PluginStatus.ERROR.value == "error"


def test_event_type_values():
    assert EventType.PLUGIN_STARTED.value == "plugin.started"


def test_event_bus_emit():
    bus = EventBus()
    received = []

    bus.on(EventType.PLUGIN_STARTED, lambda e: received.append(e))

    event = Event(EventType.PLUGIN_STARTED, source="weather")
    bus.emit(event)

    assert len(received) == 1
    assert received[0].source == "weather"


def test_event_bus_off():
    bus = EventBus()
    received = []

    def handler(e):
        received.append(e)

    bus.on(EventType.PLUGIN_STARTED, handler)
    bus.off(EventType.PLUGIN_STARTED, handler)

    bus.emit(Event(EventType.PLUGIN_STARTED))
    assert len(received) == 0


def test_event_bus_multiple_listeners():
    bus = EventBus()
    results = {"a": 0, "b": 0}

    bus.on(
        EventType.PLUGIN_UPDATED, lambda e: results.__setitem__("a", results["a"] + 1)
    )
    bus.on(
        EventType.PLUGIN_UPDATED, lambda e: results.__setitem__("b", results["b"] + 1)
    )

    bus.emit(Event(EventType.PLUGIN_UPDATED))
    assert results == {"a": 1, "b": 1}


def test_event_bus_string_event_type():
    bus = EventBus()
    received = []

    bus.on("custom.event", lambda e: received.append(e))
    bus.emit(Event("custom.event"))

    assert len(received) == 1
