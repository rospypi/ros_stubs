from typing import Any, Dict, List, Optional, Protocol, TypedDict, Union

from . import parameter_generator, parameter_generator_catkin
from .msg import BoolParameter as BoolParameter  # NOQA
from .msg import Config as ConfigMsg  # NOQA
from .msg import ConfigDescription as ConfigDescrMsg  # NOQA
from .msg import DoubleParameter as DoubleParameter  # NOQA
from .msg import Group as GroupMsg  # NOQA
from .msg import GroupState as GroupState  # NOQA
from .msg import IntParameter as IntParameter  # NOQA
from .msg import ParamDescription as ParamDescription  # NOQA
from .msg import StrParameter as StrParameter  # NOQA

_GroupType = Union[
    parameter_generator.ParameterGenerator.Group,
    parameter_generator_catkin.ParameterGenerator.Group,
]
_ValueType = Union[int, str, bool, float]

class _DescriptionProtocol(Protocol):
    min: Dict[str, _ValueType]
    max: Dict[str, _ValueType]
    defaults: Dict[str, _ValueType]
    level: Dict[str, int]
    type: Dict[str, str]
    all_level: int
    config_description: "_GroupDict"

class _ParameterDict(TypedDict):
    name: str
    type: str
    default: Optional[_ValueType]
    level: int
    description: str
    min: Optional[_ValueType]
    max: Optional[_ValueType]
    edit_method: str

class _GroupDict(TypedDict):
    id: int
    parent: int
    name: str
    type: str
    state: bool
    groups: List["_GroupDict"]
    parameters: List[_ParameterDict]

class Config(dict):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __getitem__(self, name: str) -> Any: ...
    def __delitem__(self, name: str) -> None: ...
    __getattr__ = __getitem__
    __setattr__ = __setitem__
    def copy(self) -> "Config": ...
    def __deepcopy__(self, memo: Dict[int, object]) -> "Config": ...

def encode_description(descr: _DescriptionProtocol) -> ConfigDescrMsg: ...
def encode_groups(
    parent: Optional[GroupMsg],
    group: _GroupDict,
) -> List[GroupMsg]: ...
def encode_config(config: Config, flat: bool = ...) -> ConfigMsg: ...
def group_dict(group: _GroupType) -> Config: ...
def decode_description(msg: ConfigDescrMsg) -> _GroupDict: ...
def get_tree(m: ConfigDescrMsg, group: Optional[GroupMsg] = ...) -> Config: ...
def initial_config(
    msg: ConfigMsg, description: Optional[_GroupDict] = ...
) -> Config: ...
def decode_config(
    msg: ConfigMsg, description: Optional[_GroupDict] = ...
) -> Config: ...
def extract_params(group: _GroupDict) -> List[_ParameterDict]: ...
def get_parents(group: _GroupDict, descriptions: str) -> List[_GroupDict]: ...
