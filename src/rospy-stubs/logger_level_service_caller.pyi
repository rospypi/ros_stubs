from typing import List

class ROSConsoleException(Exception): ...

class LoggerLevelServiceCaller:
    def __init__(self) -> None: ...
    def get_levels(self) -> List[str]: ...
    def get_loggers(self, node: str) -> List[str]: ...
    def get_node_names(self) -> List[str]: ...
    def send_logger_change_message(
        self, node: str, logger: str, level: str
    ) -> bool: ...
