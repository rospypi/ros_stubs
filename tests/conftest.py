import pytest
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture()
def repo_root() -> pathlib.Path:
    return REPO_ROOT
