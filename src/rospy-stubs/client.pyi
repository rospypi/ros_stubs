from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from genpy.rostime import Duration

from .msproxy import MasterProxy
from .topics import Message

_TMessage = TypeVar("_TMessage", bound=Message)

TIMEOUT_READY: float
DEBUG: int
INFO: int
WARN: int
ERROR: int
FATAL: int

def myargv(argv: Optional[Sequence[str]] = ...) -> List[str]: ...
def load_command_line_node_params(argv: List[str]) -> Dict[str, Any]: ...
def on_shutdown(h: Callable[[], None]) -> None: ...
def spin() -> None: ...
def init_node(
    name: str,
    argv: Optional[Sequence[str]] = ...,
    anonymous: bool = ...,
    log_level: Optional[int] = ...,
    disable_rostime: bool = ...,
    disable_rosout: bool = ...,
    disable_signals: bool = ...,
    xmlrpc_port: int = ...,
    tcpros_port: int = ...,
) -> None: ...
def get_master(env: Mapping[str, str] = ...) -> MasterProxy: ...
def get_published_topics(namespace: str = ...) -> List[str]: ...

class _WFM:
    msg: Optional[Message] = ...
    def __init__(self) -> None: ...
    def cb(self, msg: Message) -> None: ...

def wait_for_message(
    topic: str,
    topic_type: Type[_TMessage],
    timeout: Optional[Union[float, Duration]] = ...,
) -> _TMessage: ...

class _Unspecified: ...

def get_param(param_name: str, default: Any = ...) -> Any: ...
def get_param_cached(param_name: str, default: Any = ...) -> Any: ...
def get_param_names() -> List[str]: ...
def set_param(param_name: str, param_value: Any) -> None: ...
def search_param(param_name: str) -> str: ...
def delete_param(param_name: str) -> None: ...
def has_param(param_name: str) -> bool: ...
