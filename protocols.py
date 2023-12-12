"""Custom protocols for use in static type annotations."""

from collections.abc import Hashable
from typing import Protocol, Self


class Sortable(Protocol):

    __slots__ = ()

    def __lt__(self, other: Self) -> bool: ...


class HashableSortable(Hashable, Sortable, Protocol):

    __slots__ = ()
