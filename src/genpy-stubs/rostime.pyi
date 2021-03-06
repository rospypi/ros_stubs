import numbers
from typing import Any, Tuple, Type, TypeVar, overload

_TTVal = TypeVar("_TTVal", bound="TVal")

class TVal:
    @overload
    def __init__(self, secs: float = ...) -> None: ...
    @overload
    def __init__(self, secs: int = ..., nsecs: int = ...) -> None: ...
    @classmethod
    def from_sec(cls: Type[_TTVal], float_secs: float) -> _TTVal: ...
    def is_zero(self) -> bool: ...
    secs: int = ...
    nsecs: int = ...
    def set(self, secs: int, nsecs: int) -> None: ...
    def canon(self) -> None: ...
    def to_sec(self) -> float: ...
    def to_nsec(self) -> int: ...
    def __hash__(self) -> int: ...
    def __nonzero__(self) -> bool: ...
    def __bool__(self) -> bool: ...
    def __lt__(self: _TTVal, other: _TTVal) -> bool: ...
    def __le__(self: _TTVal, other: _TTVal) -> bool: ...
    def __gt__(self: _TTVal, other: _TTVal) -> bool: ...
    def __ge__(self: _TTVal, other: _TTVal) -> bool: ...
    def __ne__(self: _TTVal, other: _TTVal) -> bool: ...
    def __cmp__(self: _TTVal, other: _TTVal) -> int: ...
    def __eq__(self, other: Any) -> bool: ...

class Time(TVal):
    def to_time(self) -> float: ...
    def __add__(self, other: "Duration") -> "Time": ...
    def __radd__(self, other: "Duration") -> "Time": ...
    @overload
    def __sub__(self, other: "Duration") -> "Time": ...
    @overload
    def __sub__(self, other: "Time") -> "Duration": ...

class Duration(TVal):
    def __neg__(self) -> "Duration": ...
    def __abs__(self) -> "Duration": ...
    def __add__(self, other: "Duration") -> "Duration": ...
    def __radd__(self, other: "Duration") -> "Duration": ...
    def __sub__(self, other: "Duration") -> "Duration": ...
    def __mul__(self, val: numbers.Real) -> "Duration": ...
    def __rmul__(self, val: numbers.Real) -> "Duration": ...
    @overload
    def __floordiv__(self, val: numbers.Real) -> "Duration": ...
    @overload
    def __floordiv__(self, val: numbers.Integral) -> "Duration": ...
    @overload
    def __floordiv__(self, val: "Duration") -> int: ...
    @overload
    def __div__(self, val: numbers.Real) -> "Duration": ...
    @overload
    def __div__(self, val: numbers.Integral) -> "Duration": ...
    @overload
    def __div__(self, val: "Duration") -> float: ...
    @overload
    def __truediv__(self, val: numbers.Real) -> "Duration": ...
    @overload
    def __truediv__(self, val: "Duration") -> float: ...
    def __mod__(self, val: "Duration") -> "Duration": ...
    def __divmod__(self, val: "Duration") -> Tuple[int, "Duration"]: ...
