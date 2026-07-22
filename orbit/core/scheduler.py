"""Orbit scheduler."""

from __future__ import annotations

import time

from orbit.core.plugin import Plugin


class Scheduler:
    """Simple scheduler for Orbit plugins."""

    def __init__(self) -> None:
        self.plugins: list[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        self.plugins.append(plugin)

    def start(self) -> None:
        """Start all registered plugins."""

        for plugin in self.plugins:
            plugin.initialize()

        while True:
            now = time.time()

            for plugin in self.plugins:
                if now - plugin.last_update >= plugin.update_interval:
                    plugin.update()
                    plugin.last_update = now

            time.sleep(1)
