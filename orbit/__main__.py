"""Orbit entry point — python -m orbit"""

from __future__ import annotations

import argparse
import signal
import sys

from orbit.core.cache import CacheManager
from orbit.core.config import OrbitConfig
from orbit.core.logger import setup_logging
from orbit.core.scheduler import Scheduler


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="orbit", description="Orbit desktop dashboard")
    p.add_argument(
        "-c",
        "--config",
        default="config/orbit.json",
        help="Path to configuration file (default: config/orbit.json)",
    )
    return p


def _build_plugins(config: OrbitConfig, cache: CacheManager) -> list:
    plugins: list = []

    if config.weather.enabled:
        from orbit.plugins.weather.plugin import WeatherPlugin

        plugins.append(WeatherPlugin(config=config.weather, cache=cache))

    if config.system.enabled:
        from orbit.plugins.system.plugin import SystemPlugin

        plugins.append(SystemPlugin(config=config.system, cache=cache))

    if config.music.enabled:
        from orbit.plugins.music.plugin import MusicPlugin

        plugins.append(MusicPlugin(config=config.music, cache=cache))

    if config.tasks.enabled:
        from orbit.plugins.tasks.plugin import TasksPlugin

        plugins.append(TasksPlugin(config=config.tasks, cache=cache))

    if config.calendar.enabled:
        from orbit.plugins.calendar.plugin import CalendarPlugin

        plugins.append(CalendarPlugin(config=config.calendar, cache=cache))

    return plugins


def main(argv: list[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)

    config = OrbitConfig.from_file(args.config)
    setup_logging(log_file=config.log_file)

    cache = CacheManager(cache_dir=config.cache_dir)
    scheduler = Scheduler()

    for plugin in _build_plugins(config, cache):
        scheduler.register(plugin)

    if not scheduler.plugins:
        print("No plugins enabled. Check your configuration.")
        sys.exit(1)

    def _shutdown(*_args: object) -> None:
        for plugin in scheduler.plugins:
            plugin.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    print(f"Orbit started with {len(scheduler.plugins)} plugin(s)")
    scheduler.start()


if __name__ == "__main__":
    main()
