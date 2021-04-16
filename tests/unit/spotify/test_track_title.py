import logging

from spotipy import Spotify as OGSpotify

from stream_tools.spotify import track_title

from .test_spotify_tools import mock_spotify  # noqa: F401


def test_login_with_config(mock_spotify):  # noqa: F811
    api = track_title.login_with_config(
        {
            "spotify": {
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "redirect_uri": "test_redirect_uri",
            },
            "track_title": {"scope": "test_scope"},
        }
    )
    assert type(api) != OGSpotify


def test_main_no_args(mock_spotify):  # noqa: F811
    assert track_title.main([]) == 0


def test_parse_args_default():
    pargs = track_title.parse_args([])
    assert pargs.log_level == logging.ERROR


def test_parse_args_debug():
    pargs = track_title.parse_args(["--debug"])
    assert pargs.log_level == logging.DEBUG


def test_parse_args_verbose():
    pargs = track_title.parse_args(["--verbose"])
    assert pargs.log_level == logging.INFO
