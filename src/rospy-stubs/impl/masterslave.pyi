# WARNING: Automatically generated by stubgen
# Needs to be fixed manually

from typing import Any

from rosgraph.xmlrpc import XmlRpcHandler
from rospy.core import *
from rospy.impl.paramserver import get_param_server_cache as get_param_server_cache
from rospy.impl.registration import RegManager as RegManager
from rospy.impl.registration import get_topic_manager as get_topic_manager
from rospy.impl.validators import ParameterInvalid as ParameterInvalid
from rospy.impl.validators import non_empty as non_empty

STATUS: int
MSG: int
VAL: int

def is_publishers_list(paramName: Any): ...

LOG_API: bool

def apivalidate(error_return_value: Any, validators: Any = ...): ...

class ROSHandler(XmlRpcHandler):
    masterUri: Any = ...
    name: Any = ...
    uri: Any = ...
    done: bool = ...
    protocol_handlers: Any = ...
    reg_man: Any = ...
    def __init__(self, name: Any, master_uri: Any) -> None: ...
    @classmethod
    def remappings(cls, methodName: Any): ...
    def getUri(self, caller_id: Any): ...
    def getName(self, caller_id: Any): ...
    def getBusStats(self, caller_id: Any): ...
    def getBusInfo(self, caller_id: Any): ...
    def getMasterUri(self, caller_id: Any): ...
    def shutdown(self, caller_id: Any, msg: str = ...): ...
    def getPid(self, caller_id: Any): ...
    def getSubscriptions(self, caller_id: Any): ...
    def getPublications(self, caller_id: Any): ...
    def paramUpdate(self, caller_id: Any, parameter_key: Any, parameter_value: Any): ...
    def publisherUpdate(self, caller_id: Any, topic: Any, publishers: Any): ...
    def requestTopic(self, caller_id: Any, topic: Any, protocols: Any): ...
