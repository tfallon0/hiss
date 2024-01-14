"""Basic iteration with builtins."""

import operator
from collections.abc import Callable, Iterable, Iterator, Sized
from typing import Any


def show_indexed(iterable: Iterable[object]) -> None:
    """
    Show all elements of an iterable with an associated index.

    >>> show_indexed(range(10, 14))  # Ranges are sequences, and thus iterable.
    0: 10
    1: 11
    2: 12
    3: 13
    >>> show_indexed(['foo', 'bar', 'baz'])  # Lists are sequences.
    0: 'foo'
    1: 'bar'
    2: 'baz'
    >>> show_indexed('hi')  # Strings are sequences of length-1 strings.
    0: 'h'
    1: 'i'
    >>> show_indexed(iter(['foo', 'bar', 'baz']))  # Iterators are iterable.
    0: 'foo'
    1: 'bar'
    2: 'baz'
    """
    for index, value in enumerate(iterable):
        print(f'{index}: {value!r}')


def explain_colors(
        colors: Iterable[str],
        positives: Iterable[str],
        negatives: Iterable[str],
        neutrals: Iterable[str],
    ) -> None:
    """
    Characterize strings as colors, elaborating with other strings.

    >>> explain_colors(
    ...     colors=['red', 'green', 'orange'],
    ...     positives=['love', 'nature', 'oranges'],
    ...     negatives=['war', 'envy', 'being hard to rhyme'],
    ...     neutrals=['heat', 'chlorinated emeralds', 'fire'],
    ... )
    The color red represents love, war, and heat.
    The color green represents nature, envy, and chlorinated emeralds.
    The color orange represents oranges, being hard to rhyme, and fire.
    """
    zipped = zip(colors, positives, negatives, neutrals, strict=True)
    for color, pos, neg, neut in zipped:
        print(f'The color {color} represents {pos}, {neg}, and {neut}.')


def itemize_attitudes(things: Iterable[str], attitudes: Iterable[str]) -> None:
    """
    Print a numbered list of how the caller feels about various things.

    >>> itemize_attitudes(
    ...     ['sunsets', 'stubbing my toe', 'crows', 'Python'],
    ...     ['enjoy', 'deplore', 'am impressed by', 'am undecided about'],
    ... )
    1. I enjoy sunsets.
    2. I deplore stubbing my toe.
    3. I am impressed by crows.
    4. I am undecided about Python.
    """
    zipped = zip(things, attitudes, strict=True)
    for index, (thing, attitude) in enumerate(zipped, start=1):
        print(f'{index}. I {attitude} {thing}.')


def lengths(collections: Iterable[Sized]) -> Iterator[int]:
    """
    Yield the lengths of each sequence or other sized thing in collections.

    Although this could be implemented to return a generator object, that is
    not done. An instance of another built-in iterator type is returned. The
    implementation of this function is a single short return statement.

    >>> it = lengths(['foo'])
    >>> next(it)
    3
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(lengths([{10, 20, 30, 40}, 'foobar', ['A', 'B', 'C'], range(10)]))
    [4, 6, 3, 10]
    """
    return map(len, collections)


def binary_sums(left_addends: Iterable, right_addends: Iterable) -> Iterator:
    """
    Yield the sums of corresponding pairs of elements.

    This could be implemented to return a generator object, but it is instead
    implemented along the lines of lengths above. The implementation of this
    function is a single short return statement.

    (Precise type-hinting for supporting arithmetic operations is cumbersome,
    so the annotations here omit it. Iterable without a type argument means the
    same thing as Iterable[Any], where typing.Any is the dynamic type, i.e., it
    is an escape hatch from the optional static type system.)

    >>> it = binary_sums([1, 2, 7, -1.0, 'foo'], [10, 26, 30, -2, 'bar'])
    >>> next(it)
    11
    >>> list(it)
    [28, 37, -3.0, 'foobar']
    >>> list(binary_sums([1.5, 0.2, 1.1], [1.0, 0.3]))  # Extras are ignored.
    [2.5, 0.5]
    """
    return map(operator.add, left_addends, right_addends)


def find_callables(objects: Iterable[object]) -> Iterator[Callable[..., Any]]:
    """
    Yield just the objects that are callable.

    This does not call the objects, because doing so can produce undesired side
    effects, and because calls to callable objects may still raise TypeError,
    such as if they are called with the wrong number, or sometimes type, of
    arguments. It also does not use the abstract Callable class to perform the
    check, though that could be done. There is a builtin that facilitates this.

    Although this could be implemented to return a generator object, that is
    not done. An instance of another built-in iterator type is returned. The
    implementation of this function is a single short return statement.

    >>> it = find_callables([42, len, int, 'x', str, find_callables, callable])
    >>> next(it)
    <built-in function len>
    >>> list(it) == [int, str, find_callables, callable]
    True
    """
    return filter(callable, objects)
