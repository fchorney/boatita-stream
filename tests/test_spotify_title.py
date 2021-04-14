import logging

from stream_tools import spotify_title


def test_main_no_args():
    assert spotify_title.main() == 0


def test_parse_args_default():
    pargs = spotify_title.parse_args([])
    assert pargs.log_level == logging.ERROR


def test_parse_args_debug():
    pargs = spotify_title.parse_args(["--debug"])
    assert pargs.log_level == logging.DEBUG


def test_parse_args_verbose():
    pargs = spotify_title.parse_args(["--verbose"])
    assert pargs.log_level == logging.INFO
