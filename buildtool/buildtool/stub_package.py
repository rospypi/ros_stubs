import logging
import pathlib
import shutil
from typing import Any, List, Union

import yaml
from pydantic import BaseModel, PrivateAttr

from .context import BuilderContext
from .stub_build import MessageStubBuild, ServiceStubBuild

_logger = logging.getLogger(__name__)

BuildActions = Union[MessageStubBuild, ServiceStubBuild]
PackageFileName = "_package.yaml"
StubPackageSuffix = "-stubs"


class StubPackage(BaseModel):
    major_version: int
    minor_version: int

    supported_versions: str
    builds: List[BuildActions]

    _package_dir: pathlib.Path = PrivateAttr(default=pathlib.Path())
    _package_name: str = PrivateAttr()
    _target_package: str = PrivateAttr()

    def __init__(self, package_dir: pathlib.Path, **data: Any) -> None:
        super().__init__(**data)

        self._package_dir = package_dir
        assert package_dir.name.endswith(
            StubPackageSuffix
        ), f"The name of stub only package must end with '{StubPackageSuffix}'"
        self._package_name = package_dir.name
        self._target_package = self._package_name[: -len(StubPackageSuffix)]

    @property
    def target_package(self) -> str:
        return self._target_package

    def build(self, context: BuilderContext) -> pathlib.Path:
        dst = context.build_dir / self._package_dir.name
        if dst.exists():
            shutil.rmtree(dst)
        _logger.info("Copying %s into %s", self._package_dir, dst)
        shutil.copytree(self._package_dir, dst)

        _logger.info("Running build actions for %s", self._package_name)
        for b in self.builds:
            b.build(self._target_package, dst, context)

        (dst / PackageFileName).unlink()

        return dst


def load_stub_package(path: pathlib.Path) -> StubPackage:
    with path.open("r") as f:
        content = yaml.safe_load(f)

    return StubPackage(path.resolve().parent, **content)


def find_stub_packages(base: pathlib.Path) -> List[StubPackage]:
    ret: List[StubPackage] = []
    for path in base.glob(f"**/{PackageFileName}"):
        _logger.info("Found: %s", path)
        ret.append(load_stub_package(path))

    return ret
