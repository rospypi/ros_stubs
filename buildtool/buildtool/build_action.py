import pathlib

from pydantic import BaseModel

from .context import BuilderContext


class BuildAction(BaseModel):
    def build(
        self, package_name: str, package_path: pathlib.Path, context: BuilderContext
    ) -> None:
        raise NotImplementedError()
