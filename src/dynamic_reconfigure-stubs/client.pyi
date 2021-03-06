from typing import Any, Callable, Dict, List, Optional

from .encoding import Config, _GroupDict, _ParameterDict

_ParameterDescription = List[_ParameterDict]

class Client:
    name: str
    config: Optional[Config]
    param_description: Optional[_ParameterDescription]
    group_description: Optional[_GroupDict]
    def __init__(
        self,
        name: str,
        timeout: Optional[float] = ...,
        config_callback: Callable[[Config], None] = ...,
        description_callback: Config[[_ParameterDescription], None] = ...,
    ) -> None: ...
    def get_configuration(self, timeout: Optional[float] = ...) -> Optional[Config]: ...
    def get_parameter_descriptions(
        self, timeout: Optional[float] = ...
    ) -> Optional[_ParameterDescription]: ...
    def get_group_descriptions(self, timeout: Optional[float] = ...) -> _GroupDict: ...
    def update_configuration(self, changes: Dict[str, Any]) -> Config: ...
    def update_groups(self, changes: Dict[str, Any]) -> _GroupDict: ...
    def close(self) -> None: ...
    def get_config_callback(self) -> Optional[Callable[[Config], None]]: ...
    def set_config_callback(
        self, value: Optional[Callable[[Config], None]]
    ) -> None: ...
    config_callback: Optional[Callable[[Config], None]]
    def get_description_callback(
        self,
    ) -> Optional[Callable[[_ParameterDescription], None]]: ...
    def set_description_callback(
        self, value: Optional[Callable[[_ParameterDescription], None]]
    ) -> None: ...
    description_callback: Optional[Callable[[_ParameterDescription], None]]
