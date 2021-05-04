from typing import Dict

from .message import Message

def generate_dynamic(core_type: str, msg_cat: str) -> Dict[str, Message]: ...
