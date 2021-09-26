from typing import Sequence

from .encoding import _DescriptionProtocol

class DynamicReconfigureException(Exception): ...
class DynamicReconfigureParameterException(DynamicReconfigureException): ...
class DynamicReconfigureCallbackException(DynamicReconfigureException): ...

def find_reconfigure_services() -> Sequence[str]: ...
def get_parameter_names(descr: _DescriptionProtocol) -> str: ...