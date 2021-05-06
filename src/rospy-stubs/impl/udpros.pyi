# WARNING: Automatically generated by stubgen
# Needs to be fixed manually

from typing import Any

import rospy.impl.transport

def get_max_datagram_size(): ...

class UDPROSHandler(rospy.transport.ProtocolHandler):
    port: Any = ...
    buff_size: Any = ...
    def __init__(self, port: int = ...) -> None: ...
    server: Any = ...
    def init_server(self) -> None: ...
    def run(self) -> None: ...
    def shutdown(self) -> None: ...
    def create_transport(self, topic_name: Any, pub_uri: Any, protocol_params: Any): ...
    def supports(self, protocol: Any): ...
    def get_supported(self): ...
    def init_publisher(self, topic_name: Any, protocol_params: Any): ...
    def topic_connection_handler(self, sock: Any, client_addr: Any, header: Any): ...

class UDPROSTransport(rospy.transport.Transport):
    transport_type: str = ...
    done: bool = ...
    header: Any = ...
    def __init__(self, protocol: Any, name: Any, header: Any) -> None: ...
    def send_message(self, msg: Any, seq: Any) -> None: ...
    def write_data(self, data: Any) -> None: ...
    def receive_once(self) -> None: ...
    def receive_loop(self, msgs_callback: Any) -> None: ...
    def close(super: Any) -> None: ...

def get_handler(): ...