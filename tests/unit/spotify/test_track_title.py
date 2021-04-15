import logging

from stream_tools.spotify import track_title


def test_main_no_args():
    assert track_title.main() == 0


def test_parse_args_default():
    pargs = track_title.parse_args([])
    assert pargs.log_level == logging.ERROR


def test_parse_args_debug():
    pargs = track_title.parse_args(["--debug"])
    assert pargs.log_level == logging.DEBUG


def test_parse_args_verbose():
    pargs = track_title.parse_args(["--verbose"])
    assert pargs.log_level == logging.INFO
