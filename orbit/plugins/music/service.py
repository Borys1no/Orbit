"""Music service — reads metadata from playerctl."""

from __future__ import annotations

import subprocess

from orbit.core.logger import get_logger
from orbit.plugins.music.models import TrackData

logger = get_logger("music")


class NoPlayerError(Exception):
    """Raised when no active player is found."""


class MusicService:
    """Retrieves track information via playerctl."""

    def __init__(self, player: str = "") -> None:
        self._player = player

    def _run(self, fmt: str) -> str:
        cmd = ["playerctl", "format", fmt]
        if self._player:
            cmd = ["playerctl", "-p", self._player, "format", fmt]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            raise NoPlayerError(result.stderr.strip() or "No active player")
        return result.stdout.strip()

    def get_track(self) -> TrackData:
        title = self._run("{{ title }}")
        artist = self._run("{{ artist }}")
        album = self._run("{{ album }}")
        player_name = self._run("{{ playerName }}")
        status = self._run("{{ status }}")
        position = int(self._run("{{ position(mpris:position) }}") or 0)
        duration = int(self._run("{{ mpris:length }}") or 0)

        return TrackData(
            title=title,
            artist=artist,
            album=album,
            player=player_name,
            status=status,
            position=position,
            duration=duration,
        )

    def is_available(self) -> bool:
        try:
            self._run("{{ title }}")
            return True
        except NoPlayerError:
            return False
