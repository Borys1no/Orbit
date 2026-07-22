"""Typed configuration system for Orbit."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class WeatherConfig:
    api_key: str = ""
    city_id: int = 0
    units: str = "metric"
    language: str = "es"
    update_interval: int = 1800


@dataclass(slots=True)
class CalendarConfig:
    credentials_path: str = ""
    token_path: str = ""
    calendar_id: str = "primary"
    update_interval: int = 300


@dataclass(slots=True)
class TasksConfig:
    credentials_path: str = ""
    token_path: str = ""
    task_list: str = "@default"
    update_interval: int = 60


@dataclass(slots=True)
class MusicConfig:
    player: str = ""
    update_interval: int = 1


@dataclass(slots=True)
class SystemConfig:
    update_interval: int = 5


@dataclass(slots=True)
class OrbitConfig:
    weather: WeatherConfig = field(default_factory=WeatherConfig)
    calendar: CalendarConfig = field(default_factory=CalendarConfig)
    tasks: TasksConfig = field(default_factory=TasksConfig)
    music: MusicConfig = field(default_factory=MusicConfig)
    system: SystemConfig = field(default_factory=SystemConfig)
    cache_dir: str = "cache"
    log_file: str | None = None

    @classmethod
    def from_file(cls, path: str | Path) -> OrbitConfig:
        p = Path(path)
        if not p.exists():
            return cls()
        raw: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
        return cls._from_dict(raw)

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> OrbitConfig:
        return cls(
            weather=WeatherConfig(**data.get("weather", {})),
            calendar=CalendarConfig(**data.get("calendar", {})),
            tasks=TasksConfig(**data.get("tasks", {})),
            music=MusicConfig(**data.get("music", {})),
            system=SystemConfig(**data.get("system", {})),
            cache_dir=data.get("cache_dir", "cache"),
            log_file=data.get("log_file"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "weather": {
                "api_key": self.weather.api_key,
                "city_id": self.weather.city_id,
                "units": self.weather.units,
                "language": self.weather.language,
                "update_interval": self.weather.update_interval,
            },
            "calendar": {
                "credentials_path": self.calendar.credentials_path,
                "token_path": self.calendar.token_path,
                "calendar_id": self.calendar.calendar_id,
                "update_interval": self.calendar.update_interval,
            },
            "tasks": {
                "credentials_path": self.tasks.credentials_path,
                "token_path": self.tasks.token_path,
                "task_list": self.tasks.task_list,
                "update_interval": self.tasks.update_interval,
            },
            "music": {
                "player": self.music.player,
                "update_interval": self.music.update_interval,
            },
            "system": {
                "update_interval": self.system.update_interval,
            },
            "cache_dir": self.cache_dir,
            "log_file": self.log_file,
        }

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
