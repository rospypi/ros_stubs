import pathlib
from typing import Optional, Sequence

from pysen import ComponentBase, Config, PluginBase, PluginConfig, Source
from pysen.factory import ConfigureLintOptions
from pysen.flake8 import Flake8, Flake8Setting


class StubFlake8Plugin(PluginBase):
    def load(
        self,
        file_path: pathlib.Path,
        raw_config: PluginConfig,
        root: Config,
    ) -> Sequence[ComponentBase]:
        source: Optional[Source] = None
        config = root.lint or ConfigureLintOptions()
        if config.source is not None:
            source = config.source

        stub_flake8_setting = Flake8Setting(
            max_line_length=config.line_length or 88,
        ).to_black_compatible()
        assert stub_flake8_setting.ignore is not None
        stub_flake8_setting.ignore.extend(
            [
                "E301",  # E301 expected 1 blank line, found 0
                "E302",  # E302: expected 2 blank lines
                "E305",  # E305 expected 2 blank lines after class or function definition, found 1  # NOQA
                "E701",  # E701 multiple statements on one line (colon)
                "E704",  # E704: multiple statements on one line (def)
                "E741",  # E741: Do not use variables named 'I', 'O', or 'l'
            ]
        )

        return [Flake8("stub_flake8", setting=stub_flake8_setting, source=source)]


def plugin() -> PluginBase:
    return StubFlake8Plugin()
