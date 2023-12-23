"""Custom protocols for use in static type annotations."""

from collections.abc import Hashable
from typing import Protocol


class SupportsLessThan[T](Protocol):

    __slots__ = ()

    def __lt__(self, other: T) -> bool: ...


class HashableSortable[T](Hashable, SupportsLessThan[T], Protocol):

    __slots__ = ()
