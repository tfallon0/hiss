"""Ways for a function to supply multiple results obtained over time."""

from collections.abc import Callable, Hashable, Iterable
from typing import overload

from util import identity_function


@overload
def distinct[T](values: Iterable[T], *, key: Callable[[T],Hashable]) -> list[T]: ...


@overload
def distinct[T: Hashable](values: Iterable[T], *, key: None = ...) -> list[T]: ...


def distinct(values, *, key = None):
    """
    Create a list with every value of the values, but without repeating any.

    >>> distinct([])
    []
    >>> distinct([3,6,123,1,543,1,32,1,3,3,12])
    [3, 6, 123, 1, 543, 32, 12]
    >>> distinct([ {1,2}, {1}, {2,2,1}, {2}, {1,1,1}], key=frozenset)
    [{1, 2}, {1}, {2}]
    """
    if key is None:
        key = identity_function

    val_list = []
    val_set = set()

    for val in values:
        if key(val) not in val_set:
            val_set.add(key(val))
            val_list.append(val)
    return val_list
