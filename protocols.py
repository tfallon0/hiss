"""Custom protocols for use in static type annotations."""

__all__ = ['SupportsLessThan', 'HashableSortable']

from collections.abc import Hashable
from typing import Any, Protocol


class SupportsLessThan(Protocol):
    """Protocol representing types that define support for a ``<`` operator."""

    __slots__ = ()

    def __lt__(self, other: Any) -> bool: ...


class HashableSortable(Hashable, SupportsLessThan, Protocol):
    """Protocol representing types that define support for ``<`` and ``hash``."""

    __slots__ = ()
