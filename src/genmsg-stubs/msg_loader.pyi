from typing import Any, Dict, List, Optional

from .msgs import MsgSpec
from .srvs import SrvSpec

class MsgNotFound(Exception):
    base_type: Optional[str] = ...
    package: Optional[str] = ...
    search_path: Optional[str] = ...
    def __init__(
        self,
        message: str,
        base_type: Optional[str] = ...,
        package: Optional[str] = ...,
        search_path: Optional[Dict[str, List[str]]] = ...,
    ) -> None: ...

class MsgContext:
    def __init__(self) -> None: ...
    def set_file(self, full_msg_type: str, file_path: str) -> None: ...
    def get_file(self, full_msg_type: str) -> Optional[str]: ...
    def set_depends(self, full_msg_type: str, dependencies: List[str]) -> None: ...
    def get_depends(self, full_msg_type: str) -> List[str]: ...
    def get_all_depends(self, full_msg_type: str) -> List[str]: ...
    @staticmethod
    def create_default() -> "MsgContext": ...
    def register(self, full_msg_type: str, msgspec: MsgSpec) -> None: ...
    def is_registered(self, full_msg_type: str) -> bool: ...
    def get_registered(self, full_msg_type: str) -> MsgSpec: ...

# functions for msg
def get_msg_file(
    package: str, base_type: str, search_path: Dict[str, List[str]], ext: str = ...
) -> str: ...
def get_srv_file(
    package: str, base_type: str, search_path: Dict[str, List[str]]
) -> str: ...
def load_msg_by_type(
    msg_context: MsgContext, msg_type: str, search_path: Dict[str, List[str]]
) -> MsgSpec: ...
def load_srv_by_type(
    msg_context: MsgContext, srv_type: str, search_path: Dict[str, List[str]]
) -> MsgSpec: ...
def convert_constant_value(field_type: str, val: Any) -> Any: ...
def load_msg_from_string(
    msg_context: MsgContext, text: str, full_name: str
) -> MsgSpec: ...
def load_msg_from_file(
    msg_context: MsgContext, file_path: str, full_name: str
) -> MsgSpec: ...
def load_msg_depends(
    msg_context: MsgContext, spec: MsgSpec, search_path: Dict[str, List[str]]
) -> List[str]: ...
def load_depends(
    msg_context: MsgContext, spec: MsgSpec, msg_search_path: Dict[str, List[str]]
) -> List[str]: ...

# functions for srv
def load_srv_from_string(
    msg_context: MsgContext, text: str, full_name: str
) -> SrvSpec: ...
def load_srv_from_file(
    msg_context: MsgContext, file_path: str, full_name: str
) -> SrvSpec: ...
