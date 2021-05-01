from __future__ import annotations

import pathlib
from typing import Optional, Type

from .version import TVersion, Version

WHEEL_NAME_TEMPLATE = "{package_name}-{version}-py2.py3-none-any.whl"
SDIST_NAME_TEMPLATE = "{package_name}-{version}.tar.gz"
SDIST_EXTENSION = ".tar.gz"


def to_package_dir_name(name: str) -> str:
    return name.replace("_", "-")


def get_universal_wheel_name(package_name: str, version: str) -> str:
    return WHEEL_NAME_TEMPLATE.format(
        package_name=package_name.replace("-", "_"),
        version=version,
    )


def get_universal_wheel_path(
    artifacts_dir: pathlib.Path,
    package_name: str,
    version: Version,
) -> pathlib.Path:
    return (
        artifacts_dir
        / to_package_dir_name(package_name)
        / get_universal_wheel_name(package_name, version.version)
    )


def get_sdist_name(package_name: str, version: str) -> str:
    return SDIST_NAME_TEMPLATE.format(
        package_name=package_name,
        version=version,
    )


def get_sdist_path(
    artifacts_dir: pathlib.Path,
    package_name: str,
    version: Version,
) -> pathlib.Path:
    return (
        artifacts_dir
        / to_package_dir_name(package_name)
        / get_sdist_name(package_name, version.version)
    )


def extract_version(sdist_path: str) -> str:
    version_with_ext = sdist_path.rsplit("-", 1)[-1]
    assert version_with_ext.endswith(SDIST_EXTENSION)
    return version_with_ext[: -len(SDIST_EXTENSION)]


def get_next_available_version(
    artifacts_dir: pathlib.Path,
    package_name: str,
    desired_version: TVersion,
) -> TVersion:
    while True:
        if not get_sdist_path(artifacts_dir, package_name, desired_version).exists():
            return desired_version

        desired_version = desired_version.next_version


def find_latest_version(
    artifacts_dir: pathlib.Path,
    package_name: str,
    version_class: Type[TVersion],
) -> Optional[TVersion]:
    package_dir = artifacts_dir / package_name
    if not package_dir.exists():
        return None

    sdist_pattern = get_sdist_name(package_name, "*")

    items = list(package_dir.glob(sdist_pattern))
    if len(items) == 0:
        return None

    versions = [version_class.parse(extract_version(s.name)) for s in items]
    return max(versions)
