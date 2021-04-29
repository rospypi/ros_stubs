import contextlib
import dataclasses
import json
import pathlib
import shutil
import tempfile
from typing import Any, Dict, Iterator, List, Optional

import build

from .artifacts import get_sdist_name, get_universal_wheel_name
from .version import Version

MANIFEST_IN_CONTENT = "recursive-include packages *.py *.pyi"
SETUP_PY_TEMPLATE = """from setuptools import setup

setup(
{content}
)
"""
SETUP_CFG_CONTENT = """[bdist_wheel]
universal=1"""


_WORKAROUND_CASES = {
    "true": "True",
    "false": "False",
}


def _conversion_workaround(content: str) -> str:
    return _WORKAROUND_CASES.get(content, content)


def _generate_setup_py(contents: Dict[str, Any]) -> str:
    ret: List[str] = []

    for key, value in contents.items():
        rendered = "{}={},".format(
            key, _conversion_workaround(json.dumps(value, indent=4))
        )
        for line in rendered.splitlines():
            ret.append("    {}".format(line))

    return SETUP_PY_TEMPLATE.format(content="\n".join(ret))


def _create_artifacts(path: pathlib.Path, outdir: pathlib.Path) -> None:
    builder = build.ProjectBuilder(str(path))

    # NOTE: As no build dependencies are required for building a stub package,
    # we do not use build.env.IsolatedEnvBuilder but use builder directly.
    builder.build("sdist", str(outdir))
    builder.build("wheel", str(outdir))


@dataclasses.dataclass
class _BuiltArtifacts:
    sdist_path: pathlib.Path
    bdist_path: pathlib.Path


@contextlib.contextmanager
def create_artifacts(
    package_name: str,
    version: Version,
    built_dirs: List[pathlib.Path],
    install_requires: Optional[List[str]] = None,
) -> Iterator[_BuiltArtifacts]:
    # TODO: Create a tempdir, generate artifacts into tempdir,
    # then copy to artifacts dir with the expected name
    with tempfile.TemporaryDirectory() as td:
        temp_dir = pathlib.Path(td)
        work_dir = temp_dir / "src"

        package_dir = work_dir / "packages"

        include_packages: List[str] = []
        for p in built_dirs:
            name = p.name
            shutil.copytree(p, package_dir / name)
            include_packages.append(name)

        setup_args: Dict[str, Any] = {
            "name": package_name,
            "version": version.version,
            "packages": include_packages,
            "package_dir": {"": "packages"},
            "include_package_data": True,
        }

        if install_requires is not None:
            setup_args["install_requires"] = install_requires

        # create setup files
        setup_content = _generate_setup_py(setup_args)
        (work_dir / "setup.py").write_text(setup_content)
        (work_dir / "setup.cfg").write_text(SETUP_CFG_CONTENT)
        (work_dir / "MANIFEST.in").write_text(MANIFEST_IN_CONTENT)

        out_dir = temp_dir / "out"
        _create_artifacts(work_dir, out_dir)

        sdist_path = out_dir / get_sdist_name(package_name, version.version)
        bdist_path = out_dir / get_universal_wheel_name(package_name, version.version)

        assert sdist_path.exists()
        assert bdist_path.exists()

        yield _BuiltArtifacts(sdist_path, bdist_path)
