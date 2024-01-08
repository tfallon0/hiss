"""Generators exercises."""

import contextlib
import itertools


def cubes():
    """
    Yield nonnegative integer cubes in ascending order, indefinitely.

    >>> it = cubes()
    >>> next(it)
    0
    >>> next(it)
    1
    >>> next(it)
    8
    >>> it2 = cubes()
    >>> next(it2)
    0
    >>> next(it2)
    1
    >>> next(it)  # Generator objects from separate calls are independent.
    27
    """
    for index in itertools.count():
        yield index**3


def cubes_alt():
    """
    Yield nonnegative integer cubes in ascending order, indefinitely.

    This is an alternative implementation of cubes(). One uses something from
    the itertools module, while the other does not.

    >>> it = cubes_alt()
    >>> next(it)
    0
    >>> next(it)
    1
    >>> next(it)
    8
    >>> it2 = cubes_alt()
    >>> next(it2)
    0
    >>> next(it2)
    1
    >>> next(it)  # Generator objects from separate calls are independent.
    27
    """
    index = 0
    while True:
        yield index**3
        index += 1


def singleton(value):
    """
    Wrap an object in a generator, yielding only it (and only once).

    >>> list(singleton(42))
    [42]
    >>> it = singleton('foo')
    >>> next(it)
    'foo'
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration
    """
    yield value


def fibonacci():
    """
    Generate the Fibonacci sequence.

    >>> it = fibonacci()
    >>> next(it)
    0
    >>> next(it)
    1
    >>> next(it)
    1
    >>> next(it)
    2
    >>> next(it)
    3
    >>> next(it)
    5

    >>> from itertools import islice
    >>> list(islice(fibonacci(), 15))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
    >>> next(it)
    8
    """
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b


def collatz(start):
    """
    Generate the Collatz sequence from the given starting value, stopping at 1.

    >>> it = collatz(5)
    >>> next(it)
    5
    >>> next(it)
    16
    >>> next(it)
    8
    >>> next(it)
    4
    >>> next(it)
    2
    >>> next(it)
    1
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration

    >>> list(collatz(54))  # doctest: +NORMALIZE_WHITESPACE
    [54, 27, 82, 41, 124, 62, 31, 94, 47, 142, 71, 214, 107, 322, 161, 484,
     242, 121, 364, 182, 91, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700,
     350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334,
     167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958,
     479, 1438, 719, 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911,
     2734, 1367, 4102, 2051, 6154, 3077, 9232, 4616, 2308, 1154, 577, 1732,
     866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, 46, 23, 70, 35,
     106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    """
    yield start
    while start != 1:
        start = start // 2 if start % 2 == 0 else start * 3 + 1
        yield start


def bounded_powers(exponent, bound):
    """
    Yield powers, no greater than the given bound, of nonnegative integers.

    The caller is responsible for ensuring both arguments are of reasonable
    types, but may rely on an immediate ValueError if exponent is nonpositive.

    >>> it = bounded_powers(3, 100)
    >>> next(it)
    0
    >>> list(it)
    [1, 8, 27, 64]
    >>> next(bounded_powers(3, -1))  # Not an error, just nothing to yield.
    Traceback (most recent call last):
      ...
    StopIteration

    >>> list(bounded_powers(1, 9))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> list(bounded_powers(2, 25))
    [0, 1, 4, 9, 16, 25]
    >>> list(bounded_powers(2, 35))
    [0, 1, 4, 9, 16, 25]
    >>> list(bounded_powers(2, 36))
    [0, 1, 4, 9, 16, 25, 36]
    >>> list(bounded_powers(10, 2 * 10**9))
    [0, 1, 1024, 59049, 1048576, 9765625, 60466176, 282475249, 1073741824]

    >>> bounded_powers(0, 10)  # An error.
    Traceback (most recent call last):
      ...
    ValueError: exponent 0 is not positive
    >>> from fractions import Fraction
    >>> bounded_powers(Fraction(-1, 2), 10)  # Also an error.
    Traceback (most recent call last):
      ...
    ValueError: exponent Fraction(-1, 2) is not positive
    """
    if exponent <= 0:
        raise ValueError(f'exponent {exponent!r} is not positive')

    def generate():
        for base in itertools.count():
            power = base**exponent
            if power > bound:
                break
            yield power

    return generate()


def one_two_three_four(stop_after_one, stop_after_two):
    """
    Yield some or all of the string literals 'one', 'two', 'three', and 'four'.

    This is a basic exercise intended to make clear what "return" does in a
    generator function. So it is best done in a way that somehow uses "return"
    statements. Do not use any expressions other than string literals and the
    parameters, not even compound expressions made out of them.

    >>> list(one_two_three_four(False, False))
    ['one', 'two', 'three', 'four']
    >>> list(one_two_three_four(False, True))
    ['one', 'two']
    >>> list(one_two_three_four(True, False))
    ['one']
    >>> list(one_two_three_four(True, True))
    ['one']

    >>> it = one_two_three_four(False, False)
    >>> it.close()  # Generators have close(). (See rgb() below for details.)
    >>> list(it)
    []
    """
    yield 'one'
    if stop_after_one:
        return
    yield 'two'
    if stop_after_two:
        return
    yield 'three'
    yield 'four'


def empty():
    """
    Yield no elements.

    This is self-contained and reasonably elegant. It does not use the "if",
    "for", or "while" keywords, nor the "match" contextual keyword. It does not
    call any builtins or other library functions.

    >>> list(empty())
    []
    >>> it = empty()
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration

    Although a body like ``return iter([])`` would produce an empty iterator,
    this is not done that way:

    >>> from inspect import isgenerator
    >>> isgenerator(it)
    True
    """
    return
    yield


def empty_alt():
    """
    Yield no elements.

    This is an alternative implementation of empty() and satisfies all the same
    requirements. One implementation uses "yield from" and the other does not.

    >>> list(empty_alt())
    []
    >>> it = empty_alt()
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration

    >>> from inspect import isgenerator
    >>> isgenerator(it)
    True
    """
    yield from ()


# FIXME: To reset as an exercise, change "start=0" to "start" and remove body.
def my_enumerate(iterable, start=0):
    """
    Yield pairs of index and element, like the enumerate builtin.

    >>> it = my_enumerate([10, 20, 30, 40, 50])
    >>> next(it)
    (0, 10)
    >>> next(it)
    (1, 20)
    >>> list(it)
    [(2, 30), (3, 40), (4, 50)]

    >>> it = my_enumerate(['cat', 'mule', 'human', 'ox'], start=42)
    >>> next(it)
    (42, 'cat')
    >>> list(it)
    [(43, 'mule'), (44, 'human'), (45, 'ox')]

    >>> from itertools import count
    >>> it = my_enumerate(count(start=100, step=10), 1)
    >>> next(it)
    (1, 100)
    >>> next(it)
    (2, 110)
    >>> next(it)
    (3, 120)

    >>> it = my_enumerate([10, 20, 30])
    >>> next(it)
    (0, 10)
    >>> it.close()
    >>> list(it)
    []
    """
    for elem in iterable:
        yield start, elem
        start += 1


# FIXME: To reset as an exercise, change "start=0" to "start" and remove body.
def my_enumerate_alt(iterable, start=0):
    """
    Yield pairs of index and element, like the enumerate builtin.

    This is an alternative implementation of my_enumerate(). Of course, neither
    uses the enumerate builtin. One is a generator function that uses no names
    other than its own variables (thus it uses no builtins nor other library
    functions). The other is not a generator function, and it uses a builtin and
    a function from the itertools module. It is possible to infer from the
    doctests which of these functions each of these implementations must be.

    >>> it = my_enumerate_alt([10, 20, 30, 40, 50])
    >>> next(it)
    (0, 10)
    >>> next(it)
    (1, 20)
    >>> list(it)
    [(2, 30), (3, 40), (4, 50)]

    >>> it = my_enumerate_alt(['cat', 'mule', 'human', 'ox'], start=42)
    >>> next(it)
    (42, 'cat')
    >>> list(it)
    [(43, 'mule'), (44, 'human'), (45, 'ox')]

    >>> from itertools import count
    >>> it = my_enumerate_alt(count(start=100, step=10), 1)
    >>> next(it)
    (1, 100)
    >>> next(it)
    (2, 110)
    >>> next(it)
    (3, 120)
    """
    return zip(itertools.count(start), iterable)


def zip_two(iterable1, iterable2):
    """
    Yield pairs of first elements, second elements, and so forth.

    This is like the zip builtin when called with two (positional) arguments.

    >>> it = zip_two([10, 20, 30], [11, 22, 33])
    >>> next(it)
    (10, 11)
    >>> list(it)
    [(20, 22), (30, 33)]

    >>> list(zip_two([10, 20], [11, 22, 33]))
    [(10, 11), (20, 22)]
    >>> list(zip_two([10, 20, 30], [11, 22]))
    [(10, 11), (20, 22)]

    >>> from itertools import count, islice
    >>> list(zip_two([10, 20, 30], count(start=11, step=11)))
    [(10, 11), (20, 22), (30, 33)]
    >>> list(zip_two(count(start=10, step=10), [11, 22, 33]))
    [(10, 11), (20, 22), (30, 33)]
    >>> it = zip_two(count(start=10, step=10), count(start=11, step=11))
    >>> list(islice(it, 5))
    [(10, 11), (20, 22), (30, 33), (40, 44), (50, 55)]
    """
    it1 = iter(iterable1)
    it2 = iter(iterable2)
    with contextlib.suppress(StopIteration):
        while True:
            yield next(it1), next(it2)


def transpose(matrix):
    """
    Transpose a matrix represented as a rectangular tuple of tuples.

    >>> transpose(())
    ()
    >>> transpose(((23,),))
    ((23,),)
    >>> transpose(((10, 20), (30, 40)))
    ((10, 30), (20, 40))
    >>> a = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16))
    >>> transpose(a)
    ((1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15), (4, 8, 12, 16))
    """
    return tuple(zip(*matrix, strict=True))


def transpose_alt(matrix):
    """
    Transpose a matrix represented as a rectangular tuple of tuples.

    This is an alternative implementation of transpose(). One of them is very
    simple and elegant, consisting of a single return statement comprising at
    most 45 characters. The other is not, using some totally different (and far
    more cumbersome, yet hopefully interesting) technique.

    >>> transpose_alt(())
    ()
    >>> transpose_alt(((23,),))
    ((23,),)
    >>> transpose_alt(((10, 20), (30, 40)))
    ((10, 30), (20, 40))
    >>> a = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16))
    >>> transpose_alt(a)
    ((1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15), (4, 8, 12, 16))
    """
    if not matrix:
        return ()

    height = len(matrix)
    width = len(matrix[0])

    return tuple(
        tuple(matrix[i][j] for i in range(height))
        for j in range(width)
    )


# FIXME: To reset as an exercise, remove the last group of doctests.
def will_raise(exception_type, *args):
    """
    Yield nothing, like empty(), but raise an exception instead.

    >>> it = will_raise(ValueError, "pretending to fail")  # Don't raise yet.
    >>> next(it)
    Traceback (most recent call last):
      ...
    ValueError: pretending to fail

    >>> list(will_raise(ZeroDivisionError))
    Traceback (most recent call last):
      ...
    ZeroDivisionError

    Is there an exception type that can be passed to will_raise() to cause it
    to behave as empty() does?

    >>> next(will_raise(StopIteration))
    Traceback (most recent call last):
      ...
    RuntimeError: generator raised StopIteration

    (You should make sure you understand the reason for that behavior.)
    """
    raise exception_type(*args)
    yield


# FIXME: To reset as an exercise, remove the 2nd to 6th groups of doctests.
def rgb():
    """
    Yield the string literals 'red', 'green', and 'blue', in that order.

    No expressions other than string literals may appear. It follows that no
    names may appear. This really is as simple as it seems. The real meat of
    this exercise is to write all but the first of six groups of doctests.

    >>> list(rgb())
    ['red', 'green', 'blue']

    Generator objects from separate calls to a generator function are
    independent iterators:

    >>> it1 = rgb()
    >>> it2 = rgb()
    >>> next(it1)
    'red'
    >>> next(it1)
    'green'
    >>> list(it2)
    ['red', 'green', 'blue']
    >>> next(it1)
    'blue'

    inspect.getgeneratorstate() provides state information about a generator
    object. All the states it distinguishes except one are demonstrated below.

    >>> from inspect import getgeneratorstate
    >>> it = rgb()
    >>> getgeneratorstate(it)
    'GEN_CREATED'
    >>> next(it)
    'red'
    >>> getgeneratorstate(it)
    'GEN_SUSPENDED'
    >>> list(it)
    ['green', 'blue']
    >>> getgeneratorstate(it)
    'GEN_CLOSED'
    >>> list(it)
    []

    One of the states shown above, [FIXME: which one?] can, and usually does,
    actually cover multiple separate states the generator object can be in:

    >>> it = rgb()
    >>> next(it)
    'red'
    >>> getgeneratorstate(it)
    'GEN_SUSPENDED'
    >>> next(it)
    'green'
    >>> getgeneratorstate(it)
    'GEN_SUSPENDED'
    >>> next(it)
    'blue'
    >>> getgeneratorstate(it)
    'GEN_SUSPENDED'

    Calling close() on a generator object closes it, as shown:

    >>> it = rgb()
    >>> it.close()
    >>> getgeneratorstate(it)  # FIXME: Use 3.12.1, reenable.  # doctest: +SKIP
    'GEN_CLOSED'
    >>> list(it)
    []
    >>> it = rgb()
    >>> next(it)
    'red'
    >>> it.close()
    >>> list(it)
    []

    Although generator objects have a close() method, most other iterators do
    not. For example, here's an iterator constructed using the results of rgb()
    that yields the same values in the same order but is not a generator object
    and (as shown) does not have a close() method:

    >>> iter(list(rgb())).close()
    Traceback (most recent call last):
      ...
    AttributeError: 'list_iterator' object has no attribute 'close'
    """
    yield 'red'
    yield 'green'
    yield 'blue'


def chain_two(iterable1, iterable2):
    """
    Yield elements from one iterable, then another.

    This is like itertools.chain when called with two arguments.

    >>> list(chain_two([10, 20, 30], [40, 50, 60, 70]))
    [10, 20, 30, 40, 50, 60, 70]
    >>> list(chain_two(iter([10, 20, 30]), [40, 50, 60]))
    [10, 20, 30, 40, 50, 60]
    >>> list(chain_two([10, 20, 30], iter([40, 50, 60, 70])))
    [10, 20, 30, 40, 50, 60, 70]
    >>> list(chain_two(iter([10, 20, 30]), iter([40, 50, 60, 70])))
    [10, 20, 30, 40, 50, 60, 70]

    >>> from itertools import count, islice
    >>> list(islice(chain_two(range(4), count()), 20))
    [0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    >>> it = iter(range(4))
    >>> list(islice(chain_two(count(), it), 20))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    >>> list(it)  # It never gets to the second iterable.
    [0, 1, 2, 3]
    """
    yield from iterable1
    yield from iterable2


def chain_two_alt(iterable1, iterable2):
    """
    Yield elements from one iterable, then another.

    This is an alternative implementation of chain_two(). One implementation
    uses "yield from", while the other forgoes it for purposes of illustration.

    >>> list(chain_two_alt([10, 20, 30], [40, 50, 60, 70]))
    [10, 20, 30, 40, 50, 60, 70]
    >>> list(chain_two_alt(iter([10, 20, 30]), [40, 50, 60]))
    [10, 20, 30, 40, 50, 60]
    >>> list(chain_two_alt([10, 20, 30], iter([40, 50, 60, 70])))
    [10, 20, 30, 40, 50, 60, 70]
    >>> list(chain_two_alt(iter([10, 20, 30]), iter([40, 50, 60, 70])))
    [10, 20, 30, 40, 50, 60, 70]

    >>> from itertools import count, islice
    >>> list(islice(chain_two_alt(range(4), count()), 20))
    [0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    >>> it = iter(range(4))
    >>> list(islice(chain_two_alt(count(), it), 20))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    >>> list(it)  # It never gets to the second iterable.
    [0, 1, 2, 3]
    """
    for value in iterable1:
        yield value
    for value in iterable2:
        yield value


def chained_countdowns():
    """
    Yield countdowns from 0, from 1, from 2, and so on.

    These are "chained" in the sense that a single iterator yields values from
    all the countdowns, chained one after the others. Do not call any other
    functions related to chaining.

    >>> from itertools import islice
    >>> list(islice(chained_countdowns(), 25))
    [0, 1, 0, 2, 1, 0, 3, 2, 1, 0, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0, 6, 5, 4, 3]
    """
    for up in itertools.count():
        yield from range(up, -1, -1)


def chained_countdowns_alt():
    """
    Yield countdowns from 0, from 1, from 2, and so on.

    This is an alternative implementation of chained_countdowns(), subject to
    the same implementation restrictions, but one of them uses "yield from"
    while the other forgoes it for purposes of illustration.

    >>> from itertools import islice
    >>> list(islice(chained_countdowns_alt(), 25))
    [0, 1, 0, 2, 1, 0, 3, 2, 1, 0, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0, 6, 5, 4, 3]
    """
    for up in itertools.count():
        for down in range(up, -1, -1):  # noqa: UP028
            yield down


def nested_countdowns():
    """
    Yield independent iterators that count down from 0, from 1, from 2, etc.

    The iterator this function returns is a generator object, but the iterators
    yielded by that iterator are not generator objects. Space usage is O(1).

    >>> from inspect import isgenerator
    >>> from itertools import islice
    >>> outer = nested_countdowns()
    >>> isgenerator(outer)
    True
    >>> a = list(islice(outer, 20))
    >>> next(a[10])
    10
    >>> next(a[10])
    9
    >>> next(a[5])
    5
    >>> next(a[10])
    8
    >>> list(a[19])
    [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> list(a[19])
    []
    >>> next(a[10])
    7
    >>> isgenerator(a[10])
    False
    """
    for up in itertools.count():
        yield iter(range(up, -1, -1))


def product_two(iterable1, iterable2):
    """
    Generate the Cartesian product of two iterables.

    This is like itertools.product when called with two arguments.

    >>> next(product_two([], []))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(product_two([10, 20], []))
    []
    >>> list(product_two([], [10, 20]))
    []
    >>> list(product_two([10, 20, 30], [40, 50]))
    [(10, 40), (10, 50), (20, 40), (20, 50), (30, 40), (30, 50)]
    >>> list(product_two(iter([10, 20, 30]), iter([40, 50])))
    [(10, 40), (10, 50), (20, 40), (20, 50), (30, 40), (30, 50)]

    >>> from itertools import product
    >>> it = product_two(iter(range(556)), iter(range(721)))
    >>> all(x == y for x, y in zip(it, product(range(556), range(721))))
    True
    """
    xs = list(iterable1)
    ys = list(iterable2)
    for x in xs:
        for y in ys:
            yield x, y


def product_two_flexible(iterable1, iterable2):
    """
    Generate the Cartesian product of two iterables, with less restrictions.

    This is like itertools.product when called with two arguments, except that
    it is slightly more versatile, at the expense of less symmetry (see tests).

    >>> next(product_two_flexible([], []))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(product_two_flexible([10, 20], []))
    []
    >>> list(product_two_flexible([], [10, 20]))
    []
    >>> list(product_two_flexible([10, 20, 30], [40, 50]))
    [(10, 40), (10, 50), (20, 40), (20, 50), (30, 40), (30, 50)]
    >>> list(product_two(iter([10, 20, 30]), iter([40, 50])))
    [(10, 40), (10, 50), (20, 40), (20, 50), (30, 40), (30, 50)]

    >>> from itertools import count, islice, product
    >>> it = product_two_flexible(iter(range(556)), iter(range(721)))
    >>> all(x == y for x, y in zip(it, product(range(556), range(721))))
    True
    >>> it = product_two_flexible(count(), iter(range(3)))
    >>> list(islice(it, 18))  # doctest: +NORMALIZE_WHITESPACE
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2),
     (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]
    """
    ys = list(iterable2)
    for x in iterable1:
        for y in ys:
            yield x, y


def index_pairs(bound):
    """
    Efficiently yield pairs of indices (i, j) where 0 <= i <= j <= bound.

    This is not just efficient in the sense of completing in O(bound) time, but
    also in iterating in a way that avoids an obvious constant-factor slowdown.

    Auxiliary space complexity is [FIXME: do the next one, then fill this in].

    >>> next(index_pairs(0))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(index_pairs(1))
    [(0, 0)]
    >>> list(index_pairs(2))
    [(0, 0), (0, 1), (1, 1)]
    >>> list(index_pairs(3))
    [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    >>> list(index_pairs(4))
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
    """
    return itertools.combinations_with_replacement(range(bound), 2)


def index_pairs_flexible(bound):
    """
    Efficiently yield pairs of indices (i, j) where 0 <= i <= j <= bound.

    This is like index_pairs() above, satisfying all its stated requirements.
    But this is slightly more versatile (see tests). One of the two functions
    uses something in itertools, while the other does not.

    Auxiliary space complexity is [FIXME: what?].

    >>> next(index_pairs_flexible(0))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(index_pairs_flexible(1))
    [(0, 0)]
    >>> list(index_pairs_flexible(2))
    [(0, 0), (0, 1), (1, 1)]
    >>> list(index_pairs_flexible(3))
    [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    >>> list(index_pairs_flexible(4))
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

    >>> from itertools import islice
    >>> list(islice(index_pairs_flexible(2**31 - 1), 10))
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)]
    """
    for i in range(bound):
        for j in range(i, bound):
            yield i, j


def my_cycle(iterable):
    """
    Yield elements, repeating if they run out, like itertools.cycle.

    >>> from itertools import count, islice
    >>> list(my_cycle([]))
    []
    >>> list(my_cycle(iter([])))
    []
    >>> list(islice(my_cycle([10, 20, 30]), 10))
    [10, 20, 30, 10, 20, 30, 10, 20, 30, 10]
    >>> list(islice(my_cycle(iter([10, 20, 30])), 10))
    [10, 20, 30, 10, 20, 30, 10, 20, 30, 10]

    In case it's somehow relevant: On a Unix-like system (including Codespaces)
    you can end all Python processes by running "killall python" in a terminal.
    On Windows you can use the Task Manager to terminate python.exe processes
    (you may need to look in the Details tab).

    >>> list(islice(my_cycle(count()), 20))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    """
    elements = []

    for value in iterable:
        elements.append(value)
        yield value

    while elements:
        yield from elements


def my_chain(*iterables):
    """
    Yield values from each iterable in order, like itertools.chain.

    >>> list(my_chain())
    []
    >>> list(my_chain([], [], []))
    []
    >>> list(my_chain(iter([]), iter([]), iter([])))
    []
    >>> list(my_chain([10, 20, 30], [], [40], [50, 60, 70], [], []))
    [10, 20, 30, 40, 50, 60, 70]
    >>> list(my_chain(iter([10, 20, 30]), [40], iter([50]), [60]))
    [10, 20, 30, 40, 50, 60]
    >>> list(my_chain([], [], [], [10, 20, 30], [], iter([40, 50, 60, 70])))
    [10, 20, 30, 40, 50, 60, 70]
    >>> list(my_chain(iter([10, 20, 30]), iter([]), iter([40, 50, 60, 70])))
    [10, 20, 30, 40, 50, 60, 70]

    >>> from itertools import count, islice
    >>> list(islice(my_chain([10, 20, 30], count(), [40, 50]), 20))
    [10, 20, 30, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    >>> list(my_chain.from_iterable([[10, 20], [30, 40, 50]]))
    [10, 20, 30, 40, 50]
    >>> list(my_chain.from_iterable([]))
    []
    >>> list(my_chain.from_iterable([()] * 1000))
    []
    >>> list(islice(my_chain.from_iterable(nested_countdowns()), 25))
    [0, 1, 0, 2, 1, 0, 3, 2, 1, 0, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0, 6, 5, 4, 3]
    """
    return _chain_from_iterable(iterables)


def _chain_from_iterable(iterables):
    for iterable in iterables:
        yield from iterable


my_chain.from_iterable = _chain_from_iterable
