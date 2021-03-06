import struct
from typing import Any, BinaryIO, Callable, Dict, List, Optional, TypeVar, Union

from .rostime import Time, TVal

_TMessage = TypeVar("_TMessage", bound="Message")

long = int
struct_I: struct.Struct

class RosMsgUnicodeErrors:
    msg_type: Optional[str] = ...
    def __init__(self) -> None: ...
    def __call__(self, err: Exception) -> str: ...

def isstring(s: Any) -> bool: ...

class MessageException(Exception): ...
class DeserializationError(MessageException): ...
class SerializationError(MessageException): ...

def strify_message(
    val: str,
    indent: str = ...,
    time_offset: Optional[Time] = ...,
    current_time: Optional[Time] = ...,
    field_filter: Optional[Callable[["_TValidMessage"], str]] = ...,
    fixed_numeric_width: Optional[int] = ...,
) -> str: ...
def check_type(field_name: str, field_type: str, field_val: Any) -> None: ...

class Message:
    def __init__(self, *args: Any, **kwds: Any) -> None: ...
    def serialize(self, buff: BinaryIO) -> None: ...
    def deserialize(self: _TMessage, str_: bytes) -> _TMessage: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...

_TValidMessage = Union[Message, TVal]

def get_printable_message_args(
    msg: _TValidMessage, buff: Optional[BinaryIO] = ..., prefix: str = ...
) -> str: ...
def fill_message_args(
    msg: _TValidMessage, msg_args: List[str], keys: Dict[str, str] = ...
) -> None: ...
def get_message_class(
    message_type: str, reload_on_error: bool = ...
) -> _TValidMessage: ...
def get_service_class(
    service_type: str, reload_on_error: bool = ...
) -> _TValidMessage: ...
