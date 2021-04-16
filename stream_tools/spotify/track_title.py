import argparse
import logging
from pathlib import Path
from typing import Optional, Sequence

import spotipy

from .config_tools import Config_Dict, get_default_config_file, parse_config_file
from .spotify_tools import get_current_track, login


logger = logging.getLogger(__name__)


def login_with_config(config: Config_Dict) -> spotipy.Spotify:
    return login(
        str(config["spotify"]["client_id"]),
        str(config["spotify"]["client_secret"]),
        str(config["spotify"]["redirect_uri"]),
        str(config["track_title"]["scope"]),
    )


def run_track_title(config: Config_Dict, api: spotipy.Spotify) -> None:
    pass


def main(args: Optional[Sequence[str]] = None) -> int:
    pargs = parse_args(args)

    logging.basicConfig(level=pargs.log_level)

    config = parse_config_file(pargs.config)

    spotify_api = login_with_config(config)

    print(get_current_track(spotify_api))
    run_track_title(config, spotify_api)

    return 0


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="spotify-title - Print the current playing Spotify track",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=get_default_config_file(),
        help="Path to Spotify Config File",
    )

    logger_group_parent = parser.add_argument_group(
        title="logging arguments",
        description="Control what log level the log outputs (default: logger.ERROR)",
    )
    logger_group = logger_group_parent.add_mutually_exclusive_group()

    logger_group.add_argument(
        "-d",
        "--debug",
        dest="log_level",
        action="store_const",
        const=logging.DEBUG,
        default=logging.ERROR,
        help="Set log level to DEBUG",
    )
    logger_group.add_argument(
        "-v",
        "--verbose",
        dest="log_level",
        action="store_const",
        const=logging.INFO,
        default=logging.ERROR,
        help="Log at info level",
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    main()
