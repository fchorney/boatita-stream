import logging
import os
import signal
import time
from pathlib import Path

import pytest
from spotipy import Spotify as OGSpotify

from stream_tools.spotify import track_title

from .test_spotify_tools import mock_spotify  # noqa: F401


@pytest.fixture
def mock_sleep(monkeypatch):
    def mock(*args, **kwargs):
        os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
        return

    monkeypatch.setattr(time, "sleep", mock)


def make_test_config(tmp_path=Path(".")):
    return {
        "spotify": {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "redirect_uri": "test_redirect_uri",
        },
        "track_title": {
            "scope": "test_scope",
            "track_msg": "test",
            "no_track_msg": "no test",
            "market": "US",
            "sleep_time": 5,
            "file_path": tmp_path / "output.txt",
        },
    }


@pytest.mark.skip("Can't test KeyboardInterrupt")
def test_run_track_title_forever(tmp_path, mock_spotify, mock_sleep):  # noqa: F811
    config = make_test_config(tmp_path)
    api = track_title.login_with_config(config)
    track_title.run_track_title(config, api, True)


def test_run_track_title_single(tmp_path, mock_spotify):  # noqa: F811
    config = make_test_config(tmp_path)
    api = track_title.login_with_config(config)
    track_title.run_track_title(config, api, False)

    with config["track_title"]["file_path"].open("r") as f:
        data = f.read()
        assert data == "no test"


def test_get_current_track_with_config(tmp_path, mock_spotify):  # noqa: F811
    config = make_test_config(tmp_path)
    api = track_title.login_with_config(config)
    track = track_title.get_current_track_with_config(api, config)

    assert track == "no test"


def test_login_with_config(mock_spotify):  # noqa: F811
    config = make_test_config()
    api = track_title.login_with_config(config)

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
