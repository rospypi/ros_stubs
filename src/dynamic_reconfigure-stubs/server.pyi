import threading
from typing import Any, Callable, Dict

import rospy

from .encoding import Config, ConfigDescrMsg, ConfigMsg, _DescriptionProtocol

class Server:
    mutex: threading.Lock
    ns: str
    type: _DescriptionProtocol
    config: Config
    description: ConfigDescrMsg
    callback: Callable[[Config, int], Config]
    descr_topic: rospy.Publisher[ConfigDescrMsg]
    update_topic: rospy.Publisher[ConfigMsg]
    set_service: rospy.Service
    def __init__(
        self,
        type: _DescriptionProtocol,
        callback: Callable[[Config, int], Config],
        namespace: str = ...,
    ) -> None: ...
    def update_configuration(self, changes: Dict[str, Any]) -> Config: ...
