"""Tests for orbit.core.plugin and orbit.core.scheduler."""

import pytest

from orbit.core.events import PluginStatus
from orbit.core.plugin import Plugin
from orbit.core.scheduler import Scheduler


class DummyPlugin(Plugin):
    def __init__(self, **kwargs):
        super().__init__(name="dummy", **kwargs)
        self.init_called = False
        self.update_count = 0
        self.shutdown_called = False

    def initialize(self):
        self.init_called = True

    def update(self):
        self.update_count += 1

    def shutdown(self):
        self.shutdown_called = True


def test_plugin_default_status():
    p = DummyPlugin()
    assert p.status == PluginStatus.READY
    assert p.enabled is True


def test_plugin_disabled():
    p = DummyPlugin(enabled=False)
    assert p.status == PluginStatus.DISABLED


def test_plugin_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Plugin(name="test")


def test_scheduler_register():
    s = Scheduler()
    p = DummyPlugin()
    s.register(p)
    assert len(s.plugins) == 1


def test_scheduler_calls_initialize():
    s = Scheduler()
    p = DummyPlugin()
    s.register(p)
    for plugin in s.plugins:
        plugin.initialize()
    assert p.init_called is True


def test_scheduler_calls_update():
    s = Scheduler()
    p = DummyPlugin(update_interval=0)
    s.register(p)
    p.update()
    assert p.update_count == 1
