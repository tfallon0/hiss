"""Custom protocols for use in static type annotations."""

from collections.abc import Hashable
from typing import Any, Protocol


class SupportsLessThan(Protocol):

    __slots__ = ()

    def __lt__(self, other: Any) -> bool: ...


class HashableSortable(Hashable, SupportsLessThan, Protocol):

    __slots__ = ()
