from typing import Any, Optional

import rosgraph.xmlrpc
from rosgraph.rosenv import DEFAULT_MASTER_PORT as DEFAULT_MASTER_PORT

from ..core import is_shutdown as is_shutdown
from ..core import rospyerr as rospyerr
from ..core import signal_shutdown as signal_shutdown
from .masterslave import ROSHandler as ROSHandler
from .tcpros import init_tcpros as init_tcpros

DEFAULT_NODE_PORT: int

def start_node(
    environ: Any,
    resolved_name: Any,
    master_uri: Optional[Any] = ...,
    port: int = ...,
    tcpros_port: int = ...,
): ...

class RosStreamHandler(rosgraph.roslogging.RosStreamHandler):
    def __init__(
        self,
        colorize: bool = ...,
        stdout: Optional[Any] = ...,
        stderr: Optional[Any] = ...,
    ) -> None: ...
