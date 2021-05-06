import logging
import sys
from typing import Any, Callable, Dict, Mapping, Optional, Set, Tuple, TypeVar

from .rostime import Time

if sys.version_info[0] == 3:
    # For Python 3.x
    import xmlrpc.client as xmlrpcclient
else:
    # For Python 2.x
    import xmlrpclib as xmlrpcclient

_TCallable = TypeVar("_TCallable", bound=Callable[..., Any])

def deprecated(func: _TCallable) -> _TCallable: ...

ROSRPC: str

def parse_rosrpc_uri(uri: str) -> Tuple[str, int]: ...
def rospydebug(msg: str, *args: Any, **kwargs: Any) -> None: ...
def rospyinfo(msg: str, *args: Any, **kwargs: Any) -> None: ...
def rospyerr(msg: str, *args: Any, **kwargs: Any) -> None: ...
def rospywarn(msg: str, *args: Any, **kwargs: Any) -> None: ...
def logdebug(msg: str, *args: Any, **kwargs: Any) -> None: ...
def loginfo(msg: str, *args: Any, **kwargs: Any) -> None: ...
def logwarn(msg: str, *args: Any, **kwargs: Any) -> None: ...
def logerr(msg: str, *args: Any, **kwargs: Any) -> None: ...
def logfatal(msg: str, *args: Any, **kwargs: Any) -> None: ...

logout = loginfo
logerror = logerr

class LoggingThrottle:
    last_logging_time_table: Dict[str, Time] = ...
    def __call__(self, caller_id: str, period: float) -> bool: ...

def logdebug_throttle(period: float, msg: str, *args: Any, **kwargs: Any) -> None: ...
def loginfo_throttle(period: float, msg: str, *args: Any, **kwargs: Any) -> None: ...
def logwarn_throttle(period: float, msg: str, *args: Any, **kwargs: Any) -> None: ...
def logerr_throttle(period: float, msg: str, *args: Any, **kwargs: Any) -> None: ...
def logfatal_throttle(period: float, msg: str, *args: Any, **kwargs: Any) -> None: ...

class LoggingIdentical:
    last_logging_msg_table: Dict[str, str] = ...
    def __call__(self, caller_id: str, msg: str) -> bool: ...

def logdebug_throttle_identical(
    period: float, msg: str, *args: Any, **kwargs: Any
) -> None: ...
def loginfo_throttle_identical(
    period: float, msg: str, *args: Any, **kwargs: Any
) -> None: ...
def logwarn_throttle_identical(
    period: float, msg: str, *args: Any, **kwargs: Any
) -> None: ...
def logerr_throttle_identical(
    period: float, msg: str, *args: Any, **kwargs: Any
) -> None: ...
def logfatal_throttle_identical(
    period: float, msg: str, *args: Any, **kwargs: Any
) -> None: ...

class LoggingOnce:
    called_caller_ids: Set[str] = ...
    def __call__(self, caller_id: str) -> bool: ...

def logdebug_once(msg: str, *args: Any, **kwargs: Any) -> None: ...
def loginfo_once(msg: str, *args: Any, **kwargs: Any) -> None: ...
def logwarn_once(msg: str, *args: Any, **kwargs: Any) -> None: ...
def logerr_once(msg: str, *args: Any, **kwargs: Any) -> None: ...
def logfatal_once(msg: str, *args: Any, **kwargs: Any) -> None: ...

MASTER_NAME: str

def get_ros_root(
    required: bool = ..., env: Optional[Mapping[str, str]] = ...
) -> str: ...
def get_node_uri() -> str: ...
def set_node_uri(uri: str) -> None: ...
def configure_logging(node_name: str, level: int = ...) -> None: ...

class NullHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None: ...

def is_initialized() -> bool: ...
def set_initialized(initialized: bool) -> None: ...
def is_shutdown() -> bool: ...
def is_shutdown_requested() -> bool: ...
def add_client_shutdown_hook(h: Callable[[], None]) -> None: ...
def add_preshutdown_hook(h: Callable[[str], None]) -> None: ...
def add_shutdown_hook(h: Callable[[str], None]) -> None: ...
def signal_shutdown(reason: str) -> None: ...
def register_signals() -> None: ...
def is_topic(param_name: str) -> Callable[[str, str], str]: ...
def xmlrpcapi(uri: str, cache: bool = ...) -> Optional[xmlrpcclient.ServerProxy]: ...

class _LockedServerProxy(xmlrpcclient.ServerProxy):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...