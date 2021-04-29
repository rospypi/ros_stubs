from __future__ import annotations

import dataclasses
import datetime
from typing import Optional, Tuple, Type, TypeVar, Union

TVersion = TypeVar("TVersion", bound="Version")

POST_PREFIX = "post"


class Version:
    @property
    def version(self) -> str:
        raise NotImplementedError()

    @classmethod
    def parse(cls: Type[TVersion], version: str) -> TVersion:
        raise NotImplementedError()

    @property
    def next_version(self: TVersion) -> TVersion:
        raise NotImplementedError()

    def __lt__(self: TVersion, other: TVersion) -> bool:
        return NotImplemented


@dataclasses.dataclass(frozen=True, order=False)
class NumericVersion(Version):
    major: int
    minor: int
    patch: Union[str, int]

    @classmethod
    def parse(cls, version: str) -> NumericVersion:
        parts = version.split(".")
        return NumericVersion(*map(int, parts))

    @property
    def version(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def next_version(self) -> NumericVersion:
        if isinstance(self.patch, str):
            raise ValueError("Cannot get next version for string patch")

        return NumericVersion(self.major, self.minor, self.patch + 1)

    def as_tuple(self) -> Tuple[int, int, Union[str, int]]:
        return (self.major, self.minor, self.patch)

    def __lt__(self, other: NumericVersion) -> bool:
        # check whether self < other
        lhs = self.as_tuple()
        rhs = other.as_tuple()
        if isinstance(lhs[2], str) or isinstance(rhs[2], str):
            raise ValueError("Cannot compare with string patch")

        return lhs < rhs


def _format_date(date: datetime.date) -> str:
    # NOTE: setuptools trims leading 0 for version representations
    # (e.g. 2021.04.29 -> 2021.4.29)
    # Therefore, do not use strftime('%Y.%m.%d')
    return "{}.{}.{}".format(date.year, date.month, date.day)


@dataclasses.dataclass(frozen=True, order=False)
class DateVersion(Version):
    date: datetime.date
    post: Optional[int] = None

    @classmethod
    def parse(cls, version: str) -> DateVersion:
        parts = version.split(".")
        post_num: Optional[int] = None

        if len(parts) == 4:
            post = parts[3]
            assert post.startswith(POST_PREFIX)
            post_num = int(parts[3][len(POST_PREFIX) :])
            parts = parts[:3]

        assert len(parts) == 3
        return DateVersion(datetime.date(*map(int, parts)), post_num)

    @property
    def version(self) -> str:
        version = f"{_format_date(self.date)}"
        if self.post is None:
            return version

        return f"{version}.post{self.post}"

    @property
    def next_version(self) -> DateVersion:
        post: int
        if self.post is None:
            post = 0
        else:
            post = self.post + 1

        return DateVersion(self.date, post)

    def __lt__(self, other: DateVersion) -> bool:
        # check whether self < other
        if self.date != other.date:
            return self.date < other.date

        lhs_post = self.post or -1
        rhs_post = other.post or -1

        return lhs_post < rhs_post
