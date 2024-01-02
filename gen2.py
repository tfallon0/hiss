"""More generators exercises."""

import contextlib
import itertools

from util import identity_function


def my_all(iterable):
    """
    Check if all elements of an iterable are truthy, like the builtin all().

    >>> my_all([])
    True
    >>> my_all([4, 2, 3])
    True
    >>> my_all(iter([4, 2, 3]))
    True
    >>> my_all([4, 0, 3])
    False
    >>> it = iter([4, 0, 3])
    >>> my_all(it)
    False
    >>> next(it)
    3
    """
    for value in iterable:  # noqa: SIM110
        if not value:
            return False

    return True


def my_any(iterable):
    """
    Check if any elements of an iterable are truthy, like the builtin any().

    >>> my_any([])
    False
    >>> my_any(iter([False, 0, 0.0, 0j]))
    False
    >>> my_any([0, 3, 0])
    True
    >>> it = iter([0, 3, 0.0])
    >>> my_any(it)
    True
    >>> next(it)
    0.0
    """
    for value in iterable:  # noqa: SIM110
        if value:
            return True

    return False


def curious_all_input():
    """
    Return an iterable that falsifies all(), then satisfies it.

    >>> mystery = curious_all_input()
    >>> all(mystery)
    False
    >>> all(mystery)
    True
    """
    yield False


def curious_any_input():
    """
    Return an iterable that satisfies any(), then falsifies it.

    >>> mystery = curious_any_input()
    >>> any(mystery)
    True
    >>> any(mystery)
    False
    """
    yield True


def count_simple():
    """
    Yield ascending nonnegative integers indefinitely.

    This is like the 0-argument form of itertools.count.

    >>> it = count_simple()
    >>> next(it)
    0
    >>> next(it)
    1
    >>> next(it)
    2

    >>> from itertools import islice
    >>> it2 = count_simple()
    >>> list(islice(it2, 10))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    >>> list(islice(zip(it, it2), 8))  # Separate iterators are independent.
    [(3, 10), (4, 11), (5, 12), (6, 13), (7, 14), (8, 15), (9, 16), (10, 17)]
    """
    index = 0
    while True:
        yield index
        index += 1


# FIXME: To reset as an exercise, change "start=0" to "start" and remove body.
def enuzip(*iterables, start=0):
    """
    Yield flat enumerated tuples of tuples of elements from each iterable.

    Unlike other zipping functions in this module, it's not considered cheaty
    to implement this straightforwardly using obvious related functions, except
    that it should still not make use of anything defined in this project.

    The yielded tuples need not always really be flat, but have no new nesting.

    >>> from collections.abc import Iterator
    >>> it = enuzip(['A', 'B', 'C', 'D'], {3: 7, 4: 1, 9: 0}, [10, 20, 30, 40])
    >>> isinstance(it, Iterator)
    True
    >>> list(it)
    [(0, 'A', 3, 10), (1, 'B', 4, 20), (2, 'C', 9, 30)]
    >>> list(enuzip('foobar'))  # str is iterable.
    [(0, 'f'), (1, 'o'), (2, 'o'), (3, 'b'), (4, 'a'), (5, 'r')]
    >>> list(enuzip())
    []
    >>> list(enuzip(iter('spam'), iter([9, 8, 7, 6]), start=5))
    [(5, 's', 9), (6, 'p', 8), (7, 'a', 7), (8, 'm', 6)]
    >>> type(enuzip('foobar')) is type(enuzip())
    True
    """
    if iterables:
        return zip(itertools.count(start), *iterables, strict=False)
    return zip(strict=False)


def count_function():
    """
    Create a function whose calls return successive nonnegative integers.

    This is the higher order function analogue of count_simple(). Instead of
    returning an iterator (specifically, a generator object) that yields
    numbers, this returns a function that returns them when called. There are
    no restrictions on how this is implemented or what it may use, besides the
    restrictions on this and count_function_alt() in the latter's docstring.

    >>> f = count_function()
    >>> f()
    0
    >>> f()
    1
    >>> g = count_function()
    >>> f()
    2
    >>> g()
    0
    >>> f()
    3
    >>> g()
    1
    """
    it = itertools.count()
    return lambda: next(it)


def count_function_alt():
    """
    Create a function whose calls return successive nonnegative integers.

    This is an alternative implementation of count_function(). One uses an
    iterator. The other uses the "nonlocal" keyword but involves no iterators.

    >>> f = count_function_alt()
    >>> f()
    0
    >>> f()
    1
    >>> g = count_function_alt()
    >>> f()
    2
    >>> g()
    0
    >>> f()
    3
    >>> g()
    1
    """
    index = -1

    def advance():
        nonlocal index
        index += 1
        return index

    return advance


def my_count(start=0, step=1):
    """
    Count and yield integers, like itertools.count.

    >>> it = my_count()
    >>> next(it)
    0
    >>> next(it)
    1
    >>> from itertools import islice
    >>> list(islice(it, 10))
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    >>> it = my_count(100)
    >>> list(islice(it, 3))
    [100, 101, 102]
    >>> it = my_count(step=5)
    >>> list(islice(it, 10))
    [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    >>> it = my_count(1, 5)
    >>> list(islice(it, 10))
    [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
    >>> it = my_count(start=1, step=5)  # Same.
    >>> list(islice(it, 10))
    [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
    """
    while True:
        yield start
        start += step


def limit(iterable, length):
    """
    Yield a prefix of the iterable, of the given length.

    This is like the 2-argument form of itertools.islice.

    >>> next(limit([10, 20, 30, 40, 50], 0))
    Traceback (most recent call last):
      ...
    StopIteration

    >>> list(limit([10, 20, 30, 40, 50], 3))
    [10, 20, 30]
    >>> list(limit([10, 20, 30, 40, 50], 10))
    [10, 20, 30, 40, 50]

    >>> from itertools import count
    >>> list(limit(count(start=42, step=2), 10))
    [42, 44, 46, 48, 50, 52, 54, 56, 58, 60]

    >>> it = iter([10, 20, 30, 40, 50])
    >>> list(limit(it, 3))
    [10, 20, 30]
    >>> list(it)  # Make sure we didn't over-consume the input.
    [40, 50]
    """
    for _, value in zip(range(length), iterable, strict=False):
        yield value


def limit_alt(iterable, length):
    """
    Yield a prefix of the iterable, of the given length.

    This is an alternative implementation limit(). Neither uses
    itertools.islice, but they differ from each other in some substantial and
    interesting way.

    >>> next(limit_alt([10, 20, 30, 40, 50], 0))
    Traceback (most recent call last):
      ...
    StopIteration

    >>> list(limit_alt([10, 20, 30, 40, 50], 3))
    [10, 20, 30]
    >>> list(limit_alt([10, 20, 30, 40, 50], 10))
    [10, 20, 30, 40, 50]

    >>> from itertools import count
    >>> list(limit_alt(count(start=42, step=2), 10))
    [42, 44, 46, 48, 50, 52, 54, 56, 58, 60]

    >>> it = iter([10, 20, 30, 40, 50])
    >>> list(limit_alt(it, 3))
    [10, 20, 30]
    >>> list(it)  # Make sure we didn't over-consume the input.
    [40, 50]
    """
    if length <= 0:
        return

    for value in iterable:
        yield value
        length -= 1
        if length == 0:
            break


def my_filter(predicate, iterable):
    """
    Yield the elements satisfying a predicate, like the filter builtin.

    predicate is usually a unary function, but it may alteratively be None, in
    which case truthy elements are yielded.

    >>> it = my_filter(str.islower, ['foo', 'Bar', 'baz', 'Quux'])
    >>> next(it)
    'foo'
    >>> list(it)
    ['baz']

    >>> from itertools import count, islice
    >>> it = my_filter(lambda x: x % 3 == 0, count())
    >>> list(islice(it, 1000)) == list(islice(count(step=3), 1000))
    True

    >>> list(my_filter(None, (1, 3, None, 0, -2.6, [], [0], '', 'foo')))
    [1, 3, -2.6, [0], 'foo']
    """
    if predicate is None:
        predicate = identity_function

    for value in iterable:
        if predicate(value):
            yield value


def map_one(func, iterable):
    """
    Map a single iterable through a unary function.

    This is like the map builtin when called with two arguments.

    >>> list(map_one(len, ["horse", "ox", "dog", "bear", "owl", "crocodile"]))
    [5, 2, 3, 4, 3, 9]

    >>> from itertools import count
    >>> def square(n):
    ...     print(f'Called square({n!r}).')
    ...     return n**2
    >>> for x in map_one(square, count(start=2, step=3)):
    ...     if x >= 100:
    ...         break
    ...     print(x)
    Called square(2).
    4
    Called square(5).
    25
    Called square(8).
    64
    Called square(11).
    """
    for value in iterable:
        yield func(value)


def my_map(func, *iterables):
    """
    Map k iterables through a k-ary function, like the map builtin.

    >>> list(my_map(len, ["horse", "ox", "dog", "bear", "owl", "crocodile"]))
    [5, 2, 3, 4, 3, 9]

    >>> from operator import add
    >>> list(my_map(add, ['foo', 'bar', 'baz'], ['ham', 'spam', 'eggs']))
    ['fooham', 'barspam', 'bazeggs']
    >>> list(my_map(add, ['foo', 'bar'], ['ham', 'spam', 'eggs']))
    ['fooham', 'barspam']
    >>> list(my_map(add, ['foo', 'bar', 'baz'], ['ham', 'spam']))
    ['fooham', 'barspam']

    >>> from itertools import count, islice
    >>> it = my_map(lambda x, y, z: f'{x=}, {y=}, {z=}',
    ...             count(1), count(2), count(3))
    >>> list(islice(it, 4))
    ['x=1, y=2, z=3', 'x=2, y=3, z=4', 'x=3, y=4, z=5', 'x=4, y=5, z=6']

    >>> my_map(lambda: 42)  # No clearly correct output length, treat as error.
    Traceback (most recent call last):
      ...
    TypeError: my_map() must have at least two arguments.
    """
    if not iterables:
        raise TypeError('my_map() must have at least two arguments.')

    def generate():
        for values in zip(*iterables, strict=False):
            yield func(*values)

    return generate()


# FIXME: To reset as an exercise, remove all but the first group of doctests.
def lossy():
    """
    Return a function and sequence that cause the map builtin to drop elements.

    Unlike filter, map should never drop elements, but it will do so under some
    conditions. This function returns values that fool it into doing so. What's
    worse is that these values are not especially pathological: it may be a bit
    tricky to come up with them, yet this can and does happen by accident!

    This can be implemented as a single return statement that fits comfortably
    on one line.

    >>> func, sequence = lossy()
    >>> len(sequence)
    5
    >>> len(list(map(func, sequence)))
    3

    All the mapping functions in this module are conveniently immune:

    >>> func, sequence = lossy()
    >>> len(list(map_one(func, sequence)))
    Traceback (most recent call last):
      ...
    RuntimeError: generator raised StopIteration

    >>> func, sequence = lossy()
    >>> len(list(my_map(func, sequence)))
    Traceback (most recent call last):
      ...
    RuntimeError: generator raised StopIteration
    """
    return (next, [iter([2]), iter([4]), iter([6]), iter([]), iter([10])])


def my_takewhile(predicate, iterable):
    """
    Yield leading values that satisfy a predicate, like itertools.takewhile.

    >>> list(my_takewhile(str.islower, []))
    []
    >>> list(my_takewhile(str.islower, ['a', 'b', 'c', 'D', 'e', 'f', 'g']))
    ['a', 'b', 'c']
    >>> list(my_takewhile(str.islower, ['a', 'b', 'c', 'd', 'e', 'f', 'g']))
    ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    >>> list(my_takewhile(str.isupper, ['a', 'b', 'c', 'd', 'e', 'f', 'g']))
    []

    >>> from itertools import count, islice
    >>> it = my_takewhile(lambda x: x > 0, count(1))
    >>> list(islice(it, 10))  # Ensure that it is lazy.
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    >>> it = count(1)
    >>> list(my_takewhile(lambda x: x < 11, it))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> next(it)  # Ensure it didn't consume more than necessary to check.
    12
    """
    for value in iterable:
        if not predicate(value):
            break
        yield value


def my_dropwhile(predicate, iterable):
    """
    Yield values after a predicate-satisfying prefix, like itertools.dropwhile.

    >>> list(my_dropwhile(str.islower, []))
    []
    >>> list(my_dropwhile(str.islower, ['a', 'b', 'c', 'd', 'e', 'f', 'g']))
    []
    >>> list(my_dropwhile(str.islower, ['a', 'b', 'c', 'D', 'e', 'f', 'g']))
    ['D', 'e', 'f', 'g']
    >>> list(my_dropwhile(str.islower, ['a', 'b', 'c', 'D', 'e', 'F', 'g']))
    ['D', 'e', 'F', 'g']
    >>> list(my_dropwhile(str.isupper, ['a', 'b', 'c', 'D', 'e', 'F', 'g']))
    ['a', 'b', 'c', 'D', 'e', 'F', 'g']

    >>> from itertools import count, islice
    >>> it = my_dropwhile(lambda x: x < 5, count())
    >>> list(islice(it, 10))  # Ensure that it is lazy.
    [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    """
    dropping = True

    for value in iterable:
        if dropping:
            if predicate(value):
                continue
            dropping = False
        yield value


def my_dropwhile_alt(predicate, iterable):
    """
    Yield values after a predicate-satisfying prefix, like itertools.dropwhile.

    This is an alternative implementation of my_dropwhile(). One of them uses
    "yield from" to good effect, while the other makes do without it.

    >>> list(my_dropwhile_alt(str.islower, []))
    []
    >>> list(my_dropwhile_alt(str.islower, ['a', 'b', 'c', 'd', 'e', 'f', 'g']))
    []
    >>> list(my_dropwhile_alt(str.islower, ['a', 'b', 'c', 'D', 'e', 'f', 'g']))
    ['D', 'e', 'f', 'g']
    >>> list(my_dropwhile_alt(str.islower, ['a', 'b', 'c', 'D', 'e', 'F', 'g']))
    ['D', 'e', 'F', 'g']
    >>> list(my_dropwhile_alt(str.isupper, ['a', 'b', 'c', 'D', 'e', 'F', 'g']))
    ['a', 'b', 'c', 'D', 'e', 'F', 'g']

    >>> from itertools import count, islice
    >>> it = my_dropwhile_alt(lambda x: x < 5, count())
    >>> list(islice(it, 10))  # Ensure that it is lazy.
    [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    """
    it = iter(iterable)
    for value in it:
        if not predicate(value):
            yield value
            yield from it


def zip_shortest(*iterables):
    """
    Yield tuples of first elements, second elements, etc., while available.

    This is like the zip builtin with strict=False (which is the default).

    >>> next(zip_shortest())  # Not an error, just nothing to yield.
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_zip([3, 4]))
    [(3,), (4,)]

    >>> list(zip_shortest([10, 20, 30], [11, 22, 33]))  # Like zip_two.
    [(10, 11), (20, 22), (30, 33)]
    >>> list(zip_shortest([10, 20, 30], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b'), (30, 33, 'c')]
    >>> list(zip_shortest([10, 20], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(zip_shortest([10, 20, 30], [11, 22], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(zip_shortest([10, 20, 30], [11, 22, 33], ['a', 'b']))
    [(10, 11, 'a'), (20, 22, 'b')]

    >>> from itertools import count
    >>> list(zip_shortest([10, 20, 30], count(), ['a', 'b', 'c']))
    [(10, 0, 'a'), (20, 1, 'b'), (30, 2, 'c')]
    """
    if not iterables:
        return

    iterators = [iter(iterable) for iterable in iterables]

    with contextlib.suppress(StopIteration):
        while True:
            yield tuple([next(it) for it in iterators])


def _my_zip_post_check(iterators, values):
    """Check strictness for my_zip() after it yields its last tuple."""
    if values:
        n = len(values)
        assert n < len(iterators)
        if n == 1:
            msg = 'my_zip() argument 2 is shorter than argument 1'
        else:
            msg = f'my_zip() argument {n + 1} is shorter than arguments 1-{n}'
        raise ValueError(msg)

    for n, it in enumerate(iterators):
        try:
            next(it)
        except StopIteration:
            continue
        assert n > 0
        if n == 1:
            msg = 'my_zip() argument 2 is longer than argument 1'
        else:
            msg = f'my_zip() argument {n + 1} is longer than arguments 1-{n}'
        raise ValueError(msg)


def my_zip(*iterables, strict=False):
    """
    Yield tuples of first elements, second element, etc., like the zip builtin.

    >>> next(my_zip())  # Not an error, just nothing to yield.
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_zip(strict=False)), list(my_zip(strict=True))  # Same here.
    ([], [])
    >>> list(my_zip([3, 4]))
    [(3,), (4,)]
    >>> it = my_zip(iter([10, 20, 30]), iter([11, 22, 33]))  # Iterators OK.
    >>> next(it)
    (10, 11)
    >>> it.close()  # Generators support closing, this is nothing special.
    >>> list(it)
    []

    >>> from itertools import count
    >>> list(my_zip([10, 20, 30], [11, 22, 33]))  # Like zip_two.
    [(10, 11), (20, 22), (30, 33)]
    >>> list(my_zip([10, 20, 30], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b'), (30, 33, 'c')]
    >>> list(my_zip([10, 20], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip([10, 20, 30], [11, 22], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip([10, 20, 30], [11, 22, 33], ['a', 'b']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip([10, 20, 30], count(), ['a', 'b', 'c']))
    [(10, 0, 'a'), (20, 1, 'b'), (30, 2, 'c')]

    >>> list(my_zip([10, 20, 30], [11, 22], ['a', 'b', 'c'], strict=False))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip([10, 20, 30], [11, 22], ['a', 'b', 'c'], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: my_zip() argument 2 is shorter than argument 1
    >>> list(my_zip([10, 20], [11, 22, 33], ['a', 'b', 'c'], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: my_zip() argument 2 is longer than argument 1
    >>> list(my_zip([10, 20], [11, 22], ['a', 'b', 'c'], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: my_zip() argument 3 is longer than arguments 1-2
    >>> list(my_zip([10, 20], [11, 22], [6, 8], [0], [7, 9], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: my_zip() argument 4 is shorter than arguments 1-3
    >>> list(my_zip([10, 20], [11, 22], [6, 8], count(), [7, 9], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: my_zip() argument 4 is longer than arguments 1-3
    """
    if not iterables:
        return

    iterators = [iter(iterable) for iterable in iterables]

    # Build the list with a loop so we can examine it on StopIteration.
    while True:
        values = []
        try:
            for it in iterators:
                values.append(next(it))  # noqa: PERF401
        except StopIteration:
            break
        else:
            yield tuple(values)

    if strict:
        _my_zip_post_check(iterators, values)


def my_zip_cheaty(*iterables, strict=False):
    """
    Use the zip builtin to do what the zip builtin does.

    The implementation should be a single statement and definitely not more
    than 45 characters. (Do not rename the parameters to make them shorter.)
    It should either be obvious that no simpler implementation is possible, or
    a comment should briefly explain the reason the code looks overcomplicated.
    (Such a comment, if warranted, is exempt from the 45-character limit.)

    >>> next(my_zip_cheaty())  # Not an error, just nothing to yield.
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_zip_cheaty(strict=False)), list(my_zip_cheaty(strict=True))
    ([], [])
    >>> list(my_zip_cheaty([3, 4]))
    [(3,), (4,)]
    >>> it = my_zip_cheaty(iter([10, 20, 30]), iter([11, 22, 33]))
    >>> next(it)
    (10, 11)
    >>> it.close()
    >>> list(it)
    []

    >>> from itertools import count
    >>> list(my_zip_cheaty([10, 20, 30], [11, 22, 33]))  # Like zip_two.
    [(10, 11), (20, 22), (30, 33)]
    >>> list(my_zip_cheaty([10, 20, 30], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b'), (30, 33, 'c')]
    >>> list(my_zip_cheaty([10, 20], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip_cheaty([10, 20, 30], [11, 22], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip_cheaty([10, 20, 30], [11, 22, 33], ['a', 'b']))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip_cheaty([10, 20, 30], count(), ['a', 'b', 'c']))
    [(10, 0, 'a'), (20, 1, 'b'), (30, 2, 'c')]

    >>> list(my_zip_cheaty([10, 20, 30], [11, 22], ['a', 'b', 'c'], strict=False))
    [(10, 11, 'a'), (20, 22, 'b')]
    >>> list(my_zip_cheaty([10, 20, 30], [11, 22], ['a', 'b', 'c'], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: zip() argument 2 is shorter than argument 1
    >>> list(my_zip_cheaty([10, 20], [11, 22, 33], ['a', 'b', 'c'], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: zip() argument 2 is longer than argument 1
    >>> list(my_zip_cheaty([10, 20], [11, 22], ['a', 'b', 'c'], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: zip() argument 3 is longer than arguments 1-2
    >>> list(my_zip_cheaty([10, 20], [11, 22], [6, 8], [0], [7, 9], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: zip() argument 4 is shorter than arguments 1-3
    >>> list(my_zip_cheaty([10, 20], [11, 22], [6, 8], count(), [7, 9], strict=True))
    Traceback (most recent call last):
      ...
    ValueError: zip() argument 4 is longer than arguments 1-3
    """
    # We can't just return the zip object, as it has no close() method.
    yield from zip(*iterables, strict=strict)
