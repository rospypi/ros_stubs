from typing import Dict

NUMPY_DTYPE: Dict[str, str]

def unpack_numpy(var: str, count: int, dtype: str, buff: str) -> str: ...
def pack_numpy(var: str) -> str: ...
