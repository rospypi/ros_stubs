from typing import Any, BinaryIO, List, Optional, Type, TypeVar

import genpy

_TMessage = TypeVar("_TMessage", bound=genpy.Message)

class AnyMsg(genpy.Message):
    def __init__(self, *args: Any) -> None: ...
    def serialize(self, buff: BinaryIO) -> None: ...
    def deserialize(self, str: BinaryIO) -> "AnyMsg": ...

def args_kwds_to_message(
    data_class: Type[_TMessage], args: Any, kwds: Any
) -> _TMessage: ...
def serialize_message(b: BinaryIO, seq: int, msg: genpy.Message) -> None: ...
def deserialize_messages(
    b: BinaryIO,
    msg_queue: List[_TMessage],
    data_class: Type[_TMessage],
    queue_size: Optional[int] = ...,
    max_msgs: Optional[int] = ...,
    start: int = ...,
) -> None: ...
