"""Ways for a function to supply multiple results obtained over time."""

from collections.abc import Callable, Hashable, Iterable
from typing import overload

from util import identity_function


@overload
def distinct[T](values: Iterable[T], *, key: Callable[[T],Hashable]) -> list[T]: ...


@overload
def distinct[T: Hashable](values: Iterable[T], *, key: None = ...) -> list[T]: ...


def distinct(values, *, key=None):
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


@overload
def distinct_fn[T](
        values: Iterable[T], action: Callable[[T],None], *, key: Callable[[T],Hashable],
    ) -> None: ...


@overload
def distinct_fn[T: Hashable](
        values: Iterable[T], action: Callable[[T],None], *, key: None = ...,
    ) -> None: ...


def distinct_fn(values, action, *, key=None):
    """
    Create a list with every value of the values, but without repeating any.

    >>> distinct_fn([], print)  # No values, nothing printed.
    >>> distinct_fn([3,6,123,1,543,1,32,1,3,3,12], print)
    3
    6
    123
    1
    543
    32
    12
    >>> values = [{1,2}, {1}, {2,2,1}, {2}, {1,1,1}]
    >>> results = []
    >>> distinct_fn(values, results.append, key=frozenset)
    >>> results == [{1, 2}, {1}, {2}]
    True
    """
    if key is None:
        key = identity_function

    val_set = set()
    for val in values:
        if key(val) not in val_set:
            val_set.add(key(val))
            action(val)


def distinct_gen(values, *, key=None):
    """
    Create a list with every value of the values, but without repeating any.

    >>> it = distinct_gen([])
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(distinct_gen([3,6,123,1,543,1,32,1,3,3,12]))
    [3, 6, 123, 1, 543, 32, 12]
    >>> it = distinct_gen([ {1,2}, {1}, {2,2,1}, {2}, {1,1,1}], key=frozenset)
    >>> next(it) == {1, 2}
    True
    >>> list(it)
    [{1}, {2}]
    """
    if key is None:
        key = identity_function

    val_set = set()
    for val in values:
        if key(val) not in val_set:
            val_set.add(key(val))
            yield val
