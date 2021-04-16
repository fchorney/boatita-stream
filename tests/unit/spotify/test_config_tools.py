import filecmp
from pathlib import Path

import pytest

from stream_tools.spotify import config_tools


def create_test_config(tmp_path, text=None):
    d = tmp_path / "test"
    d.mkdir()
    p = d / "config.yaml"
    if text is not None:
        p.write_text(text)
    else:
        p.write_text('---\nspotify:\n  test: "test"')
    return p


def test_get_default_config_file():
    path = config_tools.get_default_config_file()

    # This really seems like it violates DRY. Is there some better way to test this
    # without basically recreating the function itself? Should this not be its own
    # function?
    parts = path.parts
    assert "spotify-config.yaml" == parts[-1]
    assert ".stream-tools" == parts[-2]


def test_config_file_exists_failure():
    assert not config_tools.config_file_exists(Path("does/not/exist.yaml"))


def test_config_file_exists_success(tmp_path):
    p = create_test_config(tmp_path)
    assert config_tools.config_file_exists(p)


def test_get_example_config_file():
    cf = config_tools.get_example_config_file()

    parts = cf.parts
    assert "config.yaml" == parts[-1]
    assert "spotify" == parts[-2]
    assert cf.exists()
    assert cf.is_file()


def test_create_config_file(tmp_path):
    p = tmp_path / "some" / "path" / "config.yaml"

    assert not p.exists()
    config_tools.create_config_file(p)

    assert p.exists()
    assert p.is_file()

    example_config = config_tools.get_example_config_file()
    assert filecmp.cmp(p, example_config, shallow=False)


def test_parse_config_file_success(tmp_path):
    p = create_test_config(tmp_path)
    c = config_tools.parse_config_file(p)
    assert c["spotify"]["test"] == "test"


def test_parse_config_file_not_exists_success(tmp_path):
    p = tmp_path / "config.yaml"
    c = config_tools.parse_config_file(p)

    # This will load in the default config
    assert "spotify" in c
    assert "track_title" in c


def test_parse_config_file_invalid_yaml(tmp_path):
    p = create_test_config(tmp_path, text="---key:\n\tvalue")
    with pytest.raises(Exception):
        config_tools.parse_config_file(p)
