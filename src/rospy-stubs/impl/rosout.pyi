import logging
from typing import Any

from rospy.core import get_caller_id as get_caller_id
from rospy.exceptions import ROSException as ROSException
from rospy.impl.registration import get_topic_manager as get_topic_manager
from rospy.rostime import Time as Time
from rospy.topics import Publisher as Publisher
from rospy.topics import Subscriber as Subscriber

def init_rosout(): ...

class RosOutHandler(logging.Handler):
    def emit(self, record: Any) -> None: ...

def load_rosout_handlers(level: Any) -> None: ...
