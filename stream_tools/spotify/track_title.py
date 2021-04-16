import argparse
import logging
from pathlib import Path
from typing import Optional, Sequence

from .config_tools import get_default_config_file, parse_config_file


logger = logging.getLogger(__name__)


def main(args: Optional[Sequence[str]] = None) -> int:
    pargs = parse_args(args)

    config = parse_config_file(pargs.config)

    print(config)

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
