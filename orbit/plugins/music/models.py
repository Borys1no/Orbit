"""Music models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class TrackData:
    title: str
    artist: str
    album: str
    player: str
    status: str
    position: int
    duration: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "player": self.player,
            "status": self.status,
            "position": self.position,
            "duration": self.duration,
        }
