from typing import Dict, Optional, Sequence

def generate_from_file(
    input_file: str,
    package_name: str,
    output_dir: str,
    template_dir: str,
    include_path: Optional[Sequence[str]],
    msg_template_dict: Dict[str, str],
    srv_template_dict: Dict[str, str],
) -> None: ...
def generate_module(
    package_name: str, output_dir: str, template_dir: str, template_dict: Dict[str, str]
) -> None: ...
def generate_from_command_line_options(
    argv: Sequence[str],
    msg_template_dict: Dict[str, str],
    srv_template_dict: Dict[str, str],
    module_template_dict: Dict[str, str] = ...,
) -> None: ...
