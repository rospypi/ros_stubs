import pathlib
from typing import Dict, Optional


class BuilderContext:
    def __init__(
        self,
        source_dir: pathlib.Path,
        build_dir: pathlib.Path,
        artifacts_dir: pathlib.Path,
    ) -> None:
        self._source_dir = source_dir.resolve()
        self._build_dir = build_dir.resolve()
        self._artifacts_dir = artifacts_dir.resolve()

        self._variables: Dict[str, str] = {
            "SOURCE_DIR": str(self._source_dir),
            "BUILD_DIR": str(self._build_dir),
            "ARTIFACTS_DIR": str(self._artifacts_dir),
        }

    @property
    def source_dir(self) -> pathlib.Path:
        return self._source_dir

    @property
    def build_dir(self) -> pathlib.Path:
        return self._build_dir

    @property
    def artifacts_dir(self) -> pathlib.Path:
        return self._artifacts_dir

    @property
    def variables(self) -> Dict[str, str]:
        return self._variables

    def format_path(self, path: str, base_dir: Optional[pathlib.Path]) -> pathlib.Path:
        base_dir = base_dir or self.build_dir
        path = path.format(**self.variables)
        return (base_dir / path).resolve()
