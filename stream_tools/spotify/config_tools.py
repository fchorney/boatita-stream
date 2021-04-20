import logging
import shutil
from pathlib import Path
from typing import Dict, Union

from yaml import Loader, load

from stream_tools.utils import create_filepath_parents


logger = logging.getLogger(__name__)

# Custom Dict Type for Config File
Config_Dict = Dict[str, Dict[str, Union[str, int]]]


def get_default_config_file() -> Path:
    return Path.home() / ".stream-tools" / "spotify-config.yaml"


def config_file_exists(config_path: Path) -> bool:
    return config_path.exists() and config_path.is_file()


def get_example_config_file() -> Path:
    parent = Path(__file__).resolve().parent
    return parent / "config.yaml"


def create_config_file(config_path: Path) -> None:
    create_filepath_parents(config_path)
    example_config_file = get_example_config_file()
    shutil.copyfile(example_config_file, config_path)


def parse_config_file(config_path: Path) -> Config_Dict:
    if not config_file_exists(config_path):
        create_config_file(config_path)

    with config_path.open("rb") as f:
        config_bytes = f.read()

    try:
        config_dict = load(config_bytes, Loader=Loader)
    except Exception:
        logger.error(
            f"Could not read config file: {config_path}."
            "Please make sure it is properly formatted YAML"
        )
        raise

    return config_dict
