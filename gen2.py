"""More generators exercises."""


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
    raise NotImplementedError


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
    raise NotImplementedError


def curious_all_input():
    """
    Return an iterable that falsifies all(), then satisfies it.

    >>> mystery = curious_all_input()
    >>> all(mystery)
    False
    >>> all(mystery)
    True
    """
    raise NotImplementedError


def curious_any_input():
    """
    Return an iterable that satisfies any(), then falsifies it.

    >>> mystery = curious_any_input()
    >>> any(mystery)
    True
    >>> any(mystery)
    False
    """
    raise NotImplementedError


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
    raise NotImplementedError


def enuzip(*iterables, start):
    """
    Yield flat enumerated tuples of elements from each iterable.

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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


def my_count(start, step):
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
    raise NotImplementedError


def limit(iterable, length):
    """
    Yield a prefix of the iterable, of the given length.

    This is like the 2-argument form of itertools.islice.

    Regarding this function, and its alternative implementations limit_alt()
    and limit_alt2() below, two use loops but differ from each other in some
    substantial and interesting way, and one uses a comprehension but is
    similar to one of the ones that uses a loop.

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
    raise NotImplementedError


def limit_alt(iterable, length):
    """
    Yield a prefix of the iterable, of the given length.

    This is a second implementation of limit(). See limit() for details.

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
    raise NotImplementedError


def limit_alt2(iterable, length):
    """
    Yield a prefix of the iterable, of the given length.

    This is a third implementation of limit(). See limit() for details.

    >>> next(limit_alt2([10, 20, 30, 40, 50], 0))
    Traceback (most recent call last):
      ...
    StopIteration

    >>> list(limit_alt2([10, 20, 30, 40, 50], 3))
    [10, 20, 30]
    >>> list(limit_alt2([10, 20, 30, 40, 50], 10))
    [10, 20, 30, 40, 50]

    >>> from itertools import count
    >>> list(limit_alt2(count(start=42, step=2), 10))
    [42, 44, 46, 48, 50, 52, 54, 56, 58, 60]

    >>> it = iter([10, 20, 30, 40, 50])
    >>> list(limit_alt2(it, 3))
    [10, 20, 30]
    >>> list(it)  # Make sure we didn't over-consume the input.
    [40, 50]
    """
    raise NotImplementedError


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
    raise NotImplementedError


def my_filter_alt(predicate, iterable):
    """
    Yield the elements satisfying a predicate, like the filter builtin.

    This is an alternative implementation of my_filter(). One uses a loop while
    the other uses a comprehension.

    >>> it = my_filter_alt(str.islower, ['foo', 'Bar', 'baz', 'Quux'])
    >>> next(it)
    'foo'
    >>> list(it)
    ['baz']

    >>> from itertools import count, islice
    >>> it = my_filter_alt(lambda x: x % 3 == 0, count())
    >>> list(islice(it, 1000)) == list(islice(count(step=3), 1000))
    True

    >>> list(my_filter_alt(None, (1, 3, None, 0, -2.6, [], [0], '', 'foo')))
    [1, 3, -2.6, [0], 'foo']
    """
    raise NotImplementedError


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
    raise NotImplementedError


def map_one_alt(func, iterable):
    """
    Map a single iterable through a unary function.

    This is an alternative implementation of map_one(). One uses a loop while
    the other uses a comprehension.

    >>> list(map_one_alt(len, ["horse", "ox", "dog", "bear", "owl", "crocodile"]))
    [5, 2, 3, 4, 3, 9]

    >>> from itertools import count
    >>> def square(n):
    ...     print(f'Called square({n!r}).')
    ...     return n**2
    >>> for x in map_one_alt(square, count(start=2, step=3)):
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
    raise NotImplementedError


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
    raise NotImplementedError


def my_map_alt(func, *iterables):
    """
    Map k iterables through a k-ary function, like the map builtin.

    This is an alternative implementation of my_map(). One uses a loop, while
    the other uses a comprehension.

    >>> list(my_map_alt(len, ["horse", "ox", "dog", "bear", "owl", "crocodile"]))
    [5, 2, 3, 4, 3, 9]

    >>> from operator import add
    >>> list(my_map_alt(add, ['foo', 'bar', 'baz'], ['ham', 'spam', 'eggs']))
    ['fooham', 'barspam', 'bazeggs']
    >>> list(my_map_alt(add, ['foo', 'bar'], ['ham', 'spam', 'eggs']))
    ['fooham', 'barspam']
    >>> list(my_map_alt(add, ['foo', 'bar', 'baz'], ['ham', 'spam']))
    ['fooham', 'barspam']

    >>> from itertools import count, islice
    >>> it = my_map_alt(lambda x, y, z: f'{x=}, {y=}, {z=}',
    ...             count(1), count(2), count(3))
    >>> list(islice(it, 4))
    ['x=1, y=2, z=3', 'x=2, y=3, z=4', 'x=3, y=4, z=5', 'x=4, y=5, z=6']

    >>> my_map_alt(lambda: 42)  # No clearly correct output length, treat as error.
    Traceback (most recent call last):
      ...
    TypeError: my_map_alt() must have at least two arguments.
    """
    raise NotImplementedError


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

    [FIXME: Add doctests that demonstrate their immunity.]
    """
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


def my_product(*iterables):
    """
    Generate the Cartesian product of iterables.

    This is like itertools.product, except that, for simplicity, this does not
    support the "repeat" parameter.

    This is reasonably efficient. It also avoids any inefficiencies not
    inherent to the technique chosen. With k iterables of total length n, its
    auxiliary space complexity is O(k + n). It is the first of three
    implementations, each of which satisfies these requirements. Each takes an
    approach differing in some interesting way from the other two approaches.

    No further hard requirements are imposed, to avoid stymying exploration and
    creativity. However, it is *suggested* that at least one implementation be
    recursive, at least one be non-recursive, and at least one have
    asymptotically optimal time complexity. When no iterable is empty, and
    taking p as the product of the lengths of each of the k iterables, the
    asymptotically optimal time complexity is O(k * p) when fully iterated.

    This implementation [FIXME: very briefly characterize it].

    >>> list(my_product())
    [()]
    >>> next(my_product([]))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_product(iter([10, 20, 30])))
    [(10,), (20,), (30,)]
    >>> list(my_product('ABC', 'XY'))
    [('A', 'X'), ('A', 'Y'), ('B', 'X'), ('B', 'Y'), ('C', 'X'), ('C', 'Y')]
    >>> it = my_product(iter('ABC'), iter('PQ'), iter('XYZ'))
    >>> list(map(''.join, it))  # doctest: +NORMALIZE_WHITESPACE
    ['APX', 'APY', 'APZ', 'AQX', 'AQY', 'AQZ', 'BPX', 'BPY', 'BPZ', 'BQX',
     'BQY', 'BQZ', 'CPX', 'CPY', 'CPZ', 'CQX', 'CQY', 'CQZ']
    >>> it = my_product('ABC', 'PQ', 'R', 'XYZ', 'ST', 'U')
    >>> list(map(''.join, it))  # doctest: +NORMALIZE_WHITESPACE
    ['APRXSU', 'APRXTU', 'APRYSU', 'APRYTU', 'APRZSU', 'APRZTU', 'AQRXSU',
     'AQRXTU', 'AQRYSU', 'AQRYTU', 'AQRZSU', 'AQRZTU', 'BPRXSU', 'BPRXTU',
     'BPRYSU', 'BPRYTU', 'BPRZSU', 'BPRZTU', 'BQRXSU', 'BQRXTU', 'BQRYSU',
     'BQRYTU', 'BQRZSU', 'BQRZTU', 'CPRXSU', 'CPRXTU', 'CPRYSU', 'CPRYTU',
     'CPRZSU', 'CPRZTU', 'CQRXSU', 'CQRXTU', 'CQRYSU', 'CQRYTU', 'CQRZSU',
     'CQRZTU']
    >>> list(my_product('ABC', 'PQ', 'R', 'XYZ', '', 'ST', 'U'))
    []
    >>> list(my_product(iter([1, 1]), iter([1, 1])))
    [(1, 1), (1, 1), (1, 1), (1, 1)]
    """
    raise NotImplementedError


def my_product_alt(*iterables):
    """
    Generate the Cartesian product of iterables.

    This is the second implementation of my_product(). See my_product() for
    details.

    This implementation [FIXME: very briefly characterize it].

    >>> list(my_product_alt())
    [()]
    >>> next(my_product_alt([]))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_product_alt(iter([10, 20, 30])))
    [(10,), (20,), (30,)]
    >>> list(my_product_alt('ABC', 'XY'))
    [('A', 'X'), ('A', 'Y'), ('B', 'X'), ('B', 'Y'), ('C', 'X'), ('C', 'Y')]
    >>> it = my_product_alt(iter('ABC'), iter('PQ'), iter('XYZ'))
    >>> list(map(''.join, it))  # doctest: +NORMALIZE_WHITESPACE
    ['APX', 'APY', 'APZ', 'AQX', 'AQY', 'AQZ', 'BPX', 'BPY', 'BPZ', 'BQX',
     'BQY', 'BQZ', 'CPX', 'CPY', 'CPZ', 'CQX', 'CQY', 'CQZ']
    >>> it = my_product_alt('ABC', 'PQ', 'R', 'XYZ', 'ST', 'U')
    >>> list(map(''.join, it))  # doctest: +NORMALIZE_WHITESPACE
    ['APRXSU', 'APRXTU', 'APRYSU', 'APRYTU', 'APRZSU', 'APRZTU', 'AQRXSU',
     'AQRXTU', 'AQRYSU', 'AQRYTU', 'AQRZSU', 'AQRZTU', 'BPRXSU', 'BPRXTU',
     'BPRYSU', 'BPRYTU', 'BPRZSU', 'BPRZTU', 'BQRXSU', 'BQRXTU', 'BQRYSU',
     'BQRYTU', 'BQRZSU', 'BQRZTU', 'CPRXSU', 'CPRXTU', 'CPRYSU', 'CPRYTU',
     'CPRZSU', 'CPRZTU', 'CQRXSU', 'CQRXTU', 'CQRYSU', 'CQRYTU', 'CQRZSU',
     'CQRZTU']
    >>> list(my_product_alt('ABC', 'PQ', 'R', 'XYZ', '', 'ST', 'U'))
    []
    >>> list(my_product_alt(iter([1, 1]), iter([1, 1])))
    [(1, 1), (1, 1), (1, 1), (1, 1)]
    """
    raise NotImplementedError


def my_product_alt2(*iterables):
    """
    Generate the Cartesian product of iterables.

    This is the third implementation of my_product(). See my_product() for
    details.

    This implementation [FIXME: very briefly characterize it].

    >>> list(my_product_alt2())
    [()]
    >>> next(my_product_alt2([]))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_product_alt2(iter([10, 20, 30])))
    [(10,), (20,), (30,)]
    >>> list(my_product_alt2('ABC', 'XY'))
    [('A', 'X'), ('A', 'Y'), ('B', 'X'), ('B', 'Y'), ('C', 'X'), ('C', 'Y')]
    >>> it = my_product_alt2(iter('ABC'), iter('PQ'), iter('XYZ'))
    >>> list(map(''.join, it))  # doctest: +NORMALIZE_WHITESPACE
    ['APX', 'APY', 'APZ', 'AQX', 'AQY', 'AQZ', 'BPX', 'BPY', 'BPZ', 'BQX',
     'BQY', 'BQZ', 'CPX', 'CPY', 'CPZ', 'CQX', 'CQY', 'CQZ']
    >>> it = my_product_alt2('ABC', 'PQ', 'R', 'XYZ', 'ST', 'U')
    >>> list(map(''.join, it))  # doctest: +NORMALIZE_WHITESPACE
    ['APRXSU', 'APRXTU', 'APRYSU', 'APRYTU', 'APRZSU', 'APRZTU', 'AQRXSU',
     'AQRXTU', 'AQRYSU', 'AQRYTU', 'AQRZSU', 'AQRZTU', 'BPRXSU', 'BPRXTU',
     'BPRYSU', 'BPRYTU', 'BPRZSU', 'BPRZTU', 'BQRXSU', 'BQRXTU', 'BQRYSU',
     'BQRYTU', 'BQRZSU', 'BQRZTU', 'CPRXSU', 'CPRXTU', 'CPRYSU', 'CPRYTU',
     'CPRZSU', 'CPRZTU', 'CQRXSU', 'CQRXTU', 'CQRYSU', 'CQRYTU', 'CQRZSU',
     'CQRZTU']
    >>> list(my_product_alt2('ABC', 'PQ', 'R', 'XYZ', '', 'ST', 'U'))
    []
    >>> list(my_product_alt2(iter([1, 1]), iter([1, 1])))
    [(1, 1), (1, 1), (1, 1), (1, 1)]
    """
    raise NotImplementedError
