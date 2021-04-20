from stream_tools import utils


def test_create_filepath_parents(tmp_path):
    p = tmp_path / "some" / "path" / "test.cfg"

    assert not p.exists()
    assert not p.parent.exists()
    utils.create_filepath_parents(p)

    assert p.parent.exists()
    assert p.parent.is_dir()
    assert not p.exists()
