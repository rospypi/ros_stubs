from string import Template
from typing import Any, Dict, List, Optional, Sequence, TypedDict

from . import encoding

LINEDEBUG: str
str_t: str
bool_t: str
int_t: str
double_t: str
id: int

def check_description(description: str) -> None: ...
def check_name(name: str) -> None: ...

class _ParameterDict(encoding._ParameterDict):
    name: str
    type: str
    default: Optional[Any]
    level: int
    description: str
    min: Optional[Any]
    max: Optional[Any]
    srcline: Optional[int]
    srcfile: Optional[str]
    edit_method: str

class _ConstantDict(TypedDict):
    name: str
    type: str
    value: Any
    srcline: Optional[int]
    srcfile: Optional[str]
    description: str

class _GroupDict(encoding._GroupDict):
    cstate: str
    srcline: Optional[int]
    srcfile: Optional[str]
    parentclass: str
    parentname: str
    field: str
    upper: str
    lower: str

class ParameterGenerator:
    minval: Dict[str, Any]
    maxval: Dict[str, Any]
    defval: Dict[str, Any]
    class Group:
        instances: Dict[int, "ParameterGenerator.Group"]
        name: str
        type: str
        groups: List["ParameterGenerator.Group"]
        parameters: List[_ParameterDict]
        gen: "ParameterGenerator"
        id: int
        parent: int
        state: bool
        srcline: Optional[int]
        srcfile: Optional[str]
        def __init__(
            self,
            gen: "ParameterGenerator",
            name: str,
            type: str,
            state: bool,
            id: int,
            parent: int,
        ) -> None: ...
        def get_group(self, id: int) -> "ParameterGenerator.Group": ...
        def add_group(
            self, name: str, type: str = ..., state: bool = ...
        ) -> "ParameterGenerator.Group": ...
        def add(
            self,
            name: str,
            paramtype: str,
            level: int,
            description: str,
            default: Optional[Any] = ...,
            min: Optional[Any] = ...,
            max: Optional[Any] = ...,
            edit_method: str = ...,
        ) -> None: ...
        def get_parameters(self) -> List[_ParameterDict]: ...
        def get_parents(self) -> List[str]: ...
        def get_field(self) -> str: ...
        def get_class(self, parent: bool = ...) -> str: ...
        def to_dict(self) -> _GroupDict: ...
    def pytype(self, drtype: str) -> type: ...
    def check_type(self, param: _ParameterDict, field: str) -> None: ...
    def fill_type(self, param: _ParameterDict) -> None: ...
    def check_type_fill_default(
        self, param: _ParameterDict, field: str, default: Any
    ) -> None: ...
    group: Group
    constants: List[_ConstantDict]
    dynconfpath: str
    binary_dir: str
    cpp_gen_dir: str
    py_gen_dir: str
    def __init__(self) -> None: ...
    def const(self, name: str, type: str, value: Any, descr: str) -> _ConstantDict: ...
    def enum(self, constants: Sequence[_ConstantDict], description: str) -> str: ...
    def add(
        self,
        name: str,
        paramtype: str,
        level: int,
        description: str,
        default: Optional[Any] = ...,
        min: Optional[Any] = ...,
        max: Optional[Any] = ...,
        edit_method: str = ...,
    ) -> None: ...
    def add_group(self, name: str, type: str = ..., state: bool = ...) -> Group: ...
    def mkdirabs(self, path: str) -> None: ...
    pkgname: Optional[str]
    name: Optional[str]
    nodename: Optional[str]
    msgname: Optional[str]
    def generate(self, pkgname: str, nodename: str, name: str) -> None: ...
    def generatewikidoc(self) -> None: ...
    def generatedoc(self) -> None: ...
    def generateusage(self) -> None: ...
    def crepr(self, param: _ParameterDict, val: Any) -> Any: ...
    def appendline(
        self,
        list: List[Template],
        text: str,
        param: _ParameterDict,
        value: Optional[Any] = ...,
    ) -> None: ...
    def appendgroup(self, list: List[Template], group: Group) -> None: ...
    def generatecpp(self) -> None: ...
    def replace_infinity(self, config_dict: Dict[str, Any]): ...
    def generatepy(self) -> None: ...
