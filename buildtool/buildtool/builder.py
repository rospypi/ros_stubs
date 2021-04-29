import dataclasses
import datetime
import logging
import pathlib
import shutil
from typing import List, Optional, Tuple

from .artifacts import find_latest_version, get_next_available_version, get_sdist_path
from .context import BuilderContext
from .package_hash import get_package_hashes, has_same_package_hashes
from .packaging import create_artifacts
from .stub_package import StubPackage, find_stub_packages
from .version import DateVersion, NumericVersion, Version

_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class _ArtifactsInfo:
    name: str
    previous_version: Optional[Version]
    generated_version: Version


def _build_package(
    artifacts_dir: pathlib.Path,
    package_name: str,
    release_version: Version,
    built_dirs: List[pathlib.Path],
    previous_version: Optional[Version] = None,
    install_requires: Optional[List[str]] = None,
) -> Version:
    with create_artifacts(
        package_name, release_version, built_dirs, install_requires
    ) as artifacts:
        if previous_version:
            # compare the contents betweet the previous build and this build
            previous_hash = get_package_hashes(
                get_sdist_path(artifacts_dir, package_name, previous_version)
            )
            artifact_hash = get_package_hashes(artifacts.sdist_path)

            if has_same_package_hashes(previous_hash, artifact_hash):
                _logger.info(
                    "Package '%s' has not been updated from the latest version: %s",
                    package_name,
                    previous_version,
                )
                return previous_version

        _logger.info(
            "Package '%s' is going to be released (Version: %s)",
            package_name,
            release_version,
        )
        package_dir = artifacts_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(artifacts.sdist_path, package_dir)
        shutil.copy2(artifacts.bdist_path, package_dir)

        return release_version


def _build_all_in_one_package(
    artifacts_dir: pathlib.Path,
    built_dirs: List[pathlib.Path],
) -> _ArtifactsInfo:
    package_name = "ros-stubs-all"
    desired_version = DateVersion(datetime.date.today())
    latest_version = find_latest_version(artifacts_dir, package_name, DateVersion)
    release_version = get_next_available_version(
        artifacts_dir, package_name, desired_version
    )

    ret = _build_package(
        artifacts_dir,
        package_name,
        release_version,
        built_dirs=built_dirs,
        previous_version=latest_version,
    )

    return _ArtifactsInfo(package_name, latest_version, ret)


def _build_single_stub_package(
    artifacts_dir: pathlib.Path,
    package: StubPackage,
    build_dir: pathlib.Path,
) -> _ArtifactsInfo:
    package_name = build_dir.name
    desired_version = NumericVersion(package.major_version, package.minor_version, 0)

    latest_version = find_latest_version(artifacts_dir, package_name, NumericVersion)
    previous_version: Optional[Version] = None
    if (
        latest_version is not None
        and latest_version.as_tuple()[:2] == desired_version.as_tuple()[:2]
    ):
        # latest version has the same major and minor numbers
        # -> Use the next patch number of latest_version
        #    Also, set previous_version in order not to generate artifacts
        #    when contents haven't changed.
        desired_version = latest_version.next_version
        previous_version = latest_version

    release_version = get_next_available_version(
        artifacts_dir, package_name, desired_version
    )
    ret = _build_package(
        artifacts_dir,
        package_name,
        release_version,
        built_dirs=[build_dir],
        previous_version=previous_version,
        install_requires=[f"{package.target_package}{package.supported_versions}"],
    )
    return _ArtifactsInfo(package_name, latest_version, ret)


def build(context: BuilderContext) -> List[_ArtifactsInfo]:
    packages = find_stub_packages(context.source_dir)
    built_dirs: List[Tuple[pathlib.Path, StubPackage]] = []
    artifacts_info: List[_ArtifactsInfo] = []

    for p in packages:
        outdir = p.build(context)
        built_dirs.append((outdir, p))

    artifacts_info.append(
        _build_all_in_one_package(
            context.artifacts_dir,
            [p[0] for p in built_dirs],
        )
    )

    # create each stub package
    for build_dir, package in built_dirs:
        artifacts_info.append(
            _build_single_stub_package(
                context.artifacts_dir,
                package,
                build_dir,
            )
        )

    return artifacts_info
