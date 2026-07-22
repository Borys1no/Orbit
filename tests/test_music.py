"""Tests for orbit.plugins.music."""

from unittest.mock import MagicMock, patch

from orbit.core.cache import CacheManager
from orbit.core.config import MusicConfig
from orbit.plugins.music.models import TrackData
from orbit.plugins.music.plugin import MusicPlugin
from orbit.plugins.music.service import MusicService


def test_track_data_to_dict():
    track = TrackData(
        title="Song",
        artist="Artist",
        album="Album",
        player="spotify",
        status="Playing",
        position=60000,
        duration=240000,
    )
    d = track.to_dict()
    assert d["title"] == "Song"
    assert d["artist"] == "Artist"
    assert d["status"] == "Playing"


@patch("orbit.plugins.music.service.subprocess.run")
def test_service_get_track(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stderr="")
    mock_run.side_effect = [
        MagicMock(returncode=0, stdout="My Song\n", stderr=""),
        MagicMock(returncode=0, stdout="Artist Name\n", stderr=""),
        MagicMock(returncode=0, stdout="Album Name\n", stderr=""),
        MagicMock(returncode=0, stdout="spotify\n", stderr=""),
        MagicMock(returncode=0, stdout="Playing\n", stderr=""),
        MagicMock(returncode=0, stdout="60000\n", stderr=""),
        MagicMock(returncode=0, stdout="240000\n", stderr=""),
    ]

    service = MusicService()
    track = service.get_track()

    assert track.title == "My Song"
    assert track.artist == "Artist Name"
    assert track.album == "Album Name"
    assert track.player == "spotify"
    assert track.status == "Playing"


@patch("orbit.plugins.music.service.subprocess.run")
def test_service_no_player(mock_run):
    mock_run.return_value = MagicMock(
        returncode=1, stdout="", stderr="No players found"
    )

    service = MusicService()
    assert service.is_available() is False


def test_plugin_update_writes_cache(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = MusicConfig()

    plugin = MusicPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.return_value = True
    mock_service.get_track.return_value = TrackData(
        title="Test Song",
        artist="Test Artist",
        album="Test Album",
        player="spotify",
        status="Playing",
        position=0,
        duration=180000,
    )
    plugin._service = mock_service

    plugin.update()

    data = cache.get("music")
    assert data is not None
    assert data["active"] is True
    assert data["title"] == "Test Song"


def test_plugin_update_no_player(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = MusicConfig()

    plugin = MusicPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.return_value = False
    plugin._service = mock_service

    plugin.update()

    data = cache.get("music")
    assert data is not None
    assert data["active"] is False


def test_plugin_update_handles_error(tmp_path):
    cache = CacheManager(cache_dir=tmp_path)
    config = MusicConfig()

    plugin = MusicPlugin(config=config, cache=cache)

    mock_service = MagicMock()
    mock_service.is_available.side_effect = Exception("playerctl error")
    plugin._service = mock_service

    plugin.update()

    assert cache.get("music") is None
