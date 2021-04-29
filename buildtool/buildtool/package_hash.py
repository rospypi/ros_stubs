import hashlib
import logging
import pathlib
import tarfile
from typing import Dict

_logger = logging.getLogger(__name__)


def get_package_hashes(sdist_path: pathlib.Path) -> Dict[str, str]:
    with sdist_path.open("rb") as fs:
        tar = tarfile.open(mode="r|*", fileobj=fs)
        contents = {}
        for member in tar:
            if not member.isfile():
                continue

            path = member.name.split("/", 2)
            if len(path) != 3 and path[1] != "packages":
                continue

            package_dir = path[2].split("/", 1)
            if package_dir[0].endswith(".egg-info"):
                # skip contents of .egg-info directory
                continue

            f = tar.extractfile(member)
            assert f is not None
            # use the path after packages for the key
            contents[path[2]] = hashlib.sha256(f.read()).hexdigest()

        return contents


def has_same_package_hashes(c1: Dict[str, str], c2: Dict[str, str]) -> bool:
    if len(c1.keys()) != len(c2.keys()):
        _logger.info(
            "The number of contents is not same: %d -> %d",
            len(c1.keys()),
            len(c2.keys()),
        )
        return False

    for key in c1.keys():
        if key not in c2:
            _logger.info("File does not exist: %s", key)
            return False

        if c1[key] != c2[key]:
            _logger.info("File is not equal: %s", key)
            return False

    return True
