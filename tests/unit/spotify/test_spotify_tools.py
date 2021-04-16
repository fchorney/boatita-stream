import logging

import pytest
import spotipy

from stream_tools.spotify import spotify_tools


TEST_USER = "test_user"
TEST_TRACK = "test_track"
TEST_ALBUM = "test_album"
TEST_ARTISTS = [{"name": "artist a"}, {"name": "artist b"}]
TEST_ARTIST = "artist a, artist b"


@pytest.fixture
def mock_spotify(monkeypatch):
    class Mock(object):
        def __init__(self, *args, **kwargs):
            pass

        def me(self, *args, **kwargs):
            return {"display_name": TEST_USER}

        def current_playback(self, *args, market="US", **kwargs):
            # Using `market` in this mocked class to decide what to return. This isn't
            # necessarily how the actual object works
            if market == "US":
                return None
            else:
                return {
                    "item": {
                        "name": TEST_TRACK,
                        "album": {"name": TEST_ALBUM},
                        "artists": TEST_ARTISTS,
                    }
                }

    monkeypatch.setattr(spotipy, "Spotify", Mock)


def test_login(mock_spotify, caplog):
    caplog.set_level(logging.INFO)
    spotify_tools.login("1", "2", "3", "4")

    assert f"Logged in as: {TEST_USER}" in [rec.message for rec in caplog.records]


def test_get_current_track_no_track(mock_spotify):
    api = spotify_tools.login("1", "2", "3", "4")

    track = spotify_tools.get_current_track(api)
    assert track == "No Track Playing"


def test_get_current_track_success(mock_spotify):
    api = spotify_tools.login("1", "2", "3", "4")

    track = spotify_tools.get_current_track(api, market="CA")
    assert track == f"{TEST_TRACK} by {TEST_ARTIST}"
