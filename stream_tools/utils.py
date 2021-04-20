from pathlib import Path


def create_filepath_parents(filepath: Path) -> None:
    abspath = filepath.resolve()
    abspath.parent.mkdir(parents=True, exist_ok=True)
