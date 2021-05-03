import logging
import pathlib
import shutil
import zipfile
from typing import List, Optional, Sequence
from urllib.request import urlopen

import yaml
from pydantic import BaseModel

# NOTE: Most of the following code was imported from
# https://github.com/rospypi/simple/blob/634b9e785f2c0f0bef36eee2ce0e56570270b466/rospy-builder/rospy_builder/build.py  # NOQA
# TODO: Refactor ropypi/simple/rospy_builder to make it easier to use in buildtool

_logger = logging.getLogger(__name__)

DOWNLOAD_CACHE_DIRNAME = ".download_cache"


def _download_archive_from_github(
    dest_dir: pathlib.Path,
    repo: str,
    ver: str,
) -> pathlib.Path:
    url = f"https://github.com/{repo}/archive/{ver}.zip"
    zip_file = dest_dir / f'{repo.replace("/", "_")}_{ver}.zip'
    if not zip_file.exists():
        _logger.info(" -> Downloading: %s", url)
        u = urlopen(url)
        with open(zip_file, "wb") as outs:
            block_sz = 8192
            while True:
                buf = u.read(block_sz)
                if not buf:
                    break
                outs.write(buf)
    else:
        _logger.info(" -> Use cache: %s", url)
    return zip_file


def _unzip(
    zip_file: pathlib.Path,
    dest_dir: pathlib.Path,
    sub_dir: Optional[pathlib.Path] = None,
) -> None:
    with open(zip_file, "rb") as f:
        if sub_dir:
            _logger.info(" -> Unarchiving: %s (target: %s)", zip_file, sub_dir)
        else:
            _logger.info(" -> Unarchiving: %s", zip_file)

        zipfp = zipfile.ZipFile(f)
        for zip_file_name in zipfp.namelist():
            original = pathlib.Path(zip_file_name)
            name = pathlib.Path(*original.parts[1:])
            if sub_dir:
                try:
                    name.relative_to(sub_dir)
                except ValueError:
                    continue
                fname = dest_dir / pathlib.Path(*name.parts[len(sub_dir.parts) :])
            else:
                fname = dest_dir / name
            data = zipfp.read(zip_file_name)
            if zip_file_name.endswith("/"):
                if not fname.exists():
                    fname.mkdir(parents=True)
            else:
                fname.write_bytes(data)


class EnvItem(BaseModel):
    name: str
    repository: str
    version: str
    path: Optional[str] = None


_IgnoreFields: List[str] = [
    "native_build",
    "release_version",
    "requires",
    "src",
    "type",
    "unrequires",
]


def _download_item_from_github(item: EnvItem, build_env_dir: pathlib.Path) -> None:
    cache_dir = build_env_dir / DOWNLOAD_CACHE_DIRNAME
    cache_dir.mkdir(parents=True, exist_ok=True)
    zipfile = _download_archive_from_github(cache_dir, item.repository, item.version)

    package_dir = build_env_dir / item.name
    if package_dir.exists():
        raise RuntimeError(
            f"{package_dir} exists! -> "
            f"the name of package: '{item.name}' is conflicted with other packages"
        )

    package_dir.mkdir(exist_ok=False)

    subdir: Optional[pathlib.Path] = None
    if item.path is not None:
        subdir = pathlib.Path(item.path)
    _unzip(zipfile, package_dir, subdir)


def setup_build_env(
    items: Sequence[EnvItem],
    build_env_dir: pathlib.Path,
) -> None:
    for item in items:
        _download_item_from_github(item, build_env_dir)


def load_env_package_yaml(path: pathlib.Path) -> List[EnvItem]:
    with path.open("r") as f:
        packages = yaml.safe_load(f)
        assert isinstance(packages, list)

    items: List[EnvItem] = []

    for package in packages:
        assert isinstance(package, dict)
        if "repository" not in package:
            # skip if repository is not in the package
            continue

        for field in _IgnoreFields:
            package.pop(field, None)

        items.append(EnvItem.parse_obj(package))

    return items


def clean_build_env_dir(build_env_dir: pathlib.Path) -> None:
    if not build_env_dir.exists():
        return

    for directory in list(build_env_dir.iterdir()):
        if directory.name == DOWNLOAD_CACHE_DIRNAME:
            continue

        shutil.rmtree(directory)
