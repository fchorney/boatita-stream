import argparse
import logging
import time
from pathlib import Path
from typing import Optional, Sequence

import spotipy

from stream_tools.spotify.config_tools import (
    Config_Dict,
    get_default_config_file,
    parse_config_file,
)
from stream_tools.spotify.spotify_tools import get_current_track, login
from stream_tools.utils import create_filepath_parents


logger = logging.getLogger(__name__)


def login_with_config(config: Config_Dict) -> spotipy.Spotify:
    return login(
        str(config["spotify"]["client_id"]),
        str(config["spotify"]["client_secret"]),
        str(config["spotify"]["redirect_uri"]),
        str(config["track_title"]["scope"]),
    )


def get_current_track_with_config(api: spotipy.Spotify, config: Config_Dict) -> str:
    return get_current_track(
        api,
        track_msg=str(config["track_title"]["track_msg"]),
        no_track_msg=str(config["track_title"]["no_track_msg"]),
        market=str(config["track_title"]["market"]),
    )


def run_track_title(config: Config_Dict, api: spotipy.Spotify, forever: bool) -> None:
    sleep_time = int(config["track_title"]["sleep_time"])
    filepath = Path(str(config["track_title"]["file_path"]))
    create_filepath_parents(filepath)

    logger.info(f"Sleep Time: {sleep_time}")
    logger.info(f"Filepath: {filepath}")

    current_track = ""
    try:
        while True:
            track = get_current_track_with_config(api, config)

            if track != current_track:
                current_track = track
                logger.info(f"Track Changed to: {track}")
                with filepath.open("w") as f:
                    f.write(track)

            if not forever:
                break

            time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass


def main(args: Optional[Sequence[str]] = None) -> int:
    pargs = parse_args(args)
    forever = pargs.forever

    logging.basicConfig(level=pargs.log_level)

    config = parse_config_file(pargs.config)
    spotify_api = login_with_config(config)
    run_track_title(config, spotify_api, forever)

    print("Exiting")
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

    parser.add_argument(
        "-f",
        "--forever",
        action="store_true",
        help="Run forever until a CTRL-C is detected",
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
