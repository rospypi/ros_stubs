from typing import Dict, List, Optional, Tuple

def find_msg_dependencies_with_type(
    pkg_name: str, msg_file: str, search_paths: Dict[str, List[str]]
) -> List[Tuple[str, Optional[str]]]: ...
def find_msg_dependencies(
    pkg_name: str, msg_file: str, search_paths: Dict[str, List[str]]
) -> List[Optional[str]]: ...
def find_srv_dependencies_with_type(
    pkg_name: str, msg_file: str, search_paths: Dict[str, List[str]]
) -> List[Tuple[str, Optional[str]]]: ...
def find_srv_dependencies(
    pkg_name: str, msg_file: str, search_paths: Dict[str, List[str]]
) -> List[Optional[str]]: ...
