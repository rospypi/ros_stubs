from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header

_DATATYPES: Dict[int, Tuple[str, int]]

def read_points(
    cloud: PointCloud2,
    field_names: Optional[Iterable[str]] = ...,
    skip_nans: bool = ...,
    uvs: Optional[Sequence[Tuple[int, int]]] = ...,
) -> Iterator[Tuple[Any, ...]]: ...
def read_points_list(
    cloud: PointCloud2,
    field_names: Optional[Iterable[str]] = ...,
    skip_nans: bool = ...,
    uvs: Optional[Sequence[Tuple[int, int]]] = ...,
) -> List[Any]: ...
def create_cloud(
    header: Header, fields: Iterable[PointField], points: Sequence[Iterable[Any]]
) -> PointCloud2: ...
def create_cloud_xyz32(
    header: Header, points: Sequence[Iterable[float]]
) -> PointCloud2: ...
def _get_struct_fmt(
    is_bigendian: bool,
    fields: Iterable[PointField],
    field_names: Optional[Iterable[str]] = ...,
) -> str: ...
