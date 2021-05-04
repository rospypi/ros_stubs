from typing import Any

SEP: str
MSG_DIR: str
SRV_DIR: str
EXT_MSG: str
EXT_SRV: str
CONSTCHAR: str
COMMENTCHAR: str
IODELIM: str
verbose: bool

def log_verbose(value: bool) -> None: ...
def log(*args: Any) -> None: ...
def plog(msg: Any, obj: Any) -> None: ...

class InvalidMsgSpec(Exception): ...
class MsgGenerationException(Exception): ...
