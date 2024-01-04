"""Ways for a function to supply multiple results obtained over time."""

from collections.abc import Callable, Hashable, Iterable, Iterator
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
    >>> distinct([{1,2}, {1}, {2,2,1}, {2}, {1,1,1}], key=frozenset)
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
def distinct_push[T](
        values: Iterable[T], action: Callable[[T],None], *, key: Callable[[T],Hashable],
    ) -> None: ...


@overload
def distinct_push[T: Hashable](
        values: Iterable[T], action: Callable[[T],None], *, key: None = ...,
    ) -> None: ...


def distinct_push(values, action, *, key=None):
    """
    Call a callback with every value of the values, but without repeating any.

    >>> distinct_push([], print)  # No values, nothing printed.
    >>> distinct_push([3,6,123,1,543,1,32,1,3,3,12], print)
    3
    6
    123
    1
    543
    32
    12
    >>> values = [{1,2}, {1}, {2,2,1}, {2}, {1,1,1}]
    >>> results = []
    >>> distinct_push(values, results.append, key=frozenset)
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


@overload
def distinct_gen[T](values: Iterable[T], *, key: Callable[[T],Hashable]) -> Iterator[T]: ...


@overload
def distinct_gen[T: Hashable](values: Iterable[T], *, key: None = ...) -> Iterator[T]: ...


def distinct_gen[T](
        values: Iterable[T], *, key: Callable[[T],Hashable] | None = None,
    ) -> Iterator[T]:
    """
    Yield every value of the values, but without repeating any.

    >>> it = distinct_gen([])
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(distinct_gen([3,6,123,1,543,1,32,1,3,3,12]))
    [3, 6, 123, 1, 543, 32, 12]
    >>> it = distinct_gen([{1,2}, {1}, {2,2,1}, {2}, {1,1,1}], key=frozenset)
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


@overload
def distinct_pull[T](
        values: Iterable[T], *, key: Callable[[T],Hashable],
    ) -> Callable[[], T]: ...


@overload
def distinct_pull[T: Hashable](
        values: Iterable[T], *, key: None = ...,
    ) -> Callable[[], T]: ...


def distinct_pull(values, *, key=None):
    """
    Make a function that returns a value of the values, without repeating any.

    Calling the returned function when there are no more distinct values raises
    StopIteration.

    >>> f = distinct_pull([])
    >>> f()
    Traceback (most recent call last):
      ...
    StopIteration

    >>> def to_list(puller):
    ...     results = []
    ...     while True:
    ...         try:
    ...             results.append(puller())
    ...         except StopIteration:
    ...             break
    ...     return results

    >>> to_list(distinct_pull([3,6,123,1,543,1,32,1,3,3,12]))
    [3, 6, 123, 1, 543, 32, 12]

    >>> values = [{1,2}, {1}, {2,2,1}, {2}, {1,1,1}]
    >>> to_list(distinct_pull(values, key=frozenset)) == [{1, 2}, {1}, {2}]
    True
    """
    it = distinct_gen(values, key=key)
    return lambda: next(it)


@overload
def distinct_pull_alt[T](
        values: Iterable[T], *, key: Callable[[T],Hashable],
    ) -> Callable[[], T]: ...


@overload
def distinct_pull_alt[T: Hashable](
        values: Iterable[T], *, key: None = ...,
    ) -> Callable[[], T]: ...


def distinct_pull_alt(values, *, key=None):
    """
    Make a function that returns a value of the values, without repeating any.

    This is an alternative implementation of distinct_pull(). One of them is
    very short and simple, making use of another function in this module. The
    other is more involved because it does not call any other function in this
    module, nor does it make any use of generators or other iterators other
    than to iterate through the provided values.

    >>> f = distinct_pull_alt([])
    >>> f()
    Traceback (most recent call last):
      ...
    StopIteration

    >>> def to_list(puller):
    ...     results = []
    ...     while True:
    ...         try:
    ...             results.append(puller())
    ...         except StopIteration:
    ...             break
    ...     return results

    >>> to_list(distinct_pull_alt([3,6,123,1,543,1,32,1,3,3,12]))
    [3, 6, 123, 1, 543, 32, 12]

    >>> values = [{1,2}, {1}, {2,2,1}, {2}, {1,1,1}]
    >>> to_list(distinct_pull_alt(values, key=frozenset)) == [{1, 2}, {1}, {2}]
    True
    """
    if key is None:
        key = identity_function

    seen = set()
    it = iter(values)

    def get_next_value():
        for value in it:
            computed_key = key(value)
            if computed_key not in seen:
                seen.add(computed_key)
                return value

        raise StopIteration

    return get_next_value
