import pathlib
from typing import Any, Callable, Dict, List, Literal, Optional, Union

import genpyi.cli
from pydantic import PrivateAttr

from .build_action import BuildAction
from .context import BuilderContext


class StubBuild(BuildAction):
    source_dir: str
    out_dir: str
    generate_module: bool = True
    include_paths: Dict[str, Union[str, List[str]]]

    _source_extension: str = PrivateAttr(default="")
    _stubgen_impl: Callable[
        [Any, str, List[str], Optional[str], Dict[str, List[str]]], None
    ] = PrivateAttr()

    class Config:
        allow_population_by_field_name = True

    def get_formatted_include_paths(
        self, package_dir: pathlib.Path, context: BuilderContext
    ) -> Dict[str, List[str]]:
        include_paths: Dict[str, List[str]] = {}

        for module, paths in self.include_paths.items():
            if not isinstance(paths, list):
                paths = [paths]

            include_paths[module] = [
                str(context.format_path(p, package_dir)) for p in paths
            ]

        return include_paths

    def build(
        self,
        target_package: str,
        package_dir: pathlib.Path,
        context: BuilderContext,
    ) -> None:
        source_dir = context.format_path(self.source_dir, package_dir)
        out_dir = context.format_path(self.out_dir, package_dir)
        source_files = list(
            [str(x) for x in source_dir.glob(f"*{self._source_extension}")]
        )
        include_paths = self.get_formatted_include_paths(package_dir, context)

        self._stubgen_impl(target_package, source_files, str(out_dir), include_paths)
        genpyi.cli.run_module(source_dir, str(out_dir), "genmsg")


class MessageStubBuild(StubBuild):
    type: Literal["msg_stub_gen"]
    _source_extension = PrivateAttr(".msg")
    _stubgen_impl = PrivateAttr(genpyi.cli.run_message)


class ServiceStubBuild(StubBuild):
    type: Literal["srv_stub_gen"]

    _source_extension = PrivateAttr(".srv")
    _stubgen_impl = PrivateAttr(genpyi.cli.run_service)
