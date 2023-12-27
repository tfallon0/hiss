"""Generators exercises."""

import contextlib
import itertools

from util import identity_function


def squares():
    """
    Yield nonnegative integer squares in ascending order, indefinitely.

    >>> it = squares()
    >>> next(it)
    0
    >>> next(it)
    1
    >>> next(it)
    4
    >>> it2 = squares()
    >>> next(it2)
    0
    >>> next(it2)
    1
    >>> next(it)  # Generator objects from separate calls are independent.
    9
    """
    for index in itertools.count():
        yield index**2


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

    >>> list(empty())
    []
    >>> it = empty()
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration
    """
    return
    yield


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
    function). The other is not a generator function, and it uses a builtin and
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
    most 40 characters. The other is not, using some totally different (and far
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

    In case it's somehow relevant, on a Unix-like system (including Codespaces)
    you can end all Python processes by running "killall python" in a terminal.

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


def empty_alt():
    """
    Yield no elements.

    This is an alternative implementation of empty(). Each is self-contained
    and reasonably elegant. One uses "yield from" and the other does not.
    Neither uses the "if", "for", or "while" keyword or the "match" contextual
    keyword (if empty() does, it should be changed now so that it does not).

    >>> list(empty_alt())
    []
    >>> it = empty_alt()
    >>> next(it)
    Traceback (most recent call last):
      ...
    StopIteration
    """
    yield from ()


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


def count_function():
    """
    Create a function whose calls return successive nonnegative integers.

    This is the higher order function analogue of count_simple. Instead of
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
    one one line.

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
    Yield tuples of first, elements, second elements, etc., while available.

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
