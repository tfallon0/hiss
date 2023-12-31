"""Even more generators exercises."""

import collections
import itertools
import operator

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
    for value in iterable:
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
    for value in iterable:
        if value:
            return True

    return False


def curious_all():
    """
    Return an iterable that falsifies all(), then satisfies it.

    >>> mystery = curious_all()
    >>> all(mystery)
    False
    >>> all(mystery)
    True
    """
    yield False


def curious_any():
    """
    Return an iterable that satisfies any(), then falsifies it.

    >>> mystery = curious_any()
    >>> any(mystery)
    True
    >>> any(mystery)
    False
    """
    yield True


def my_starmap(func, arg_tuples):
    """
    Map arguments from an iterable of argument tuples, like itertools.starmap.

    >>> import operator
    >>> list(my_starmap(lambda: 42, [(), (), ()]))
    [42, 42, 42]
    >>> list(my_starmap(len, [("wolf",), ("bobcat",), ("emu",)]))
    [4, 6, 3]
    >>> list(my_starmap(operator.sub, iter([(3, 4), (1, 1), (6, -1), (0, 2)])))
    [-1, 0, 7, -2]

    >>> def comma_join(*args):
    ...     return ', '.join(args)
    >>> list(my_starmap(comma_join, iter([['ab', 'cd'], ['ef', 'gh', 'ij']])))
    ['ab, cd', 'ef, gh, ij']
    >>> nested_iterators = iter([iter(['ab', 'cd']), iter(['ef', 'gh', 'ij'])])
    >>> list(my_starmap(comma_join, nested_iterators))
    ['ab, cd', 'ef, gh, ij']

    >>> from itertools import count, islice
    >>> it = my_starmap(operator.add, zip(count(2, 2), count(5, 3)))
    >>> list(islice(it, 15))
    [7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77]
    """
    for args in arg_tuples:
        yield func(*args)


# FIXME: To reset as an exercise, change "fillvalue=None" to "fillvalue".
def my_zip_longest(*iterables, fillvalue=None):
    """
    Yield zipped tuples but pad shorter ones, like itertools.zip_longest.

    >>> next(my_zip_longest())  # Not an error, just nothing to yield.
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_zip_longest([3, 4]))
    [(3,), (4,)]

    >>> list(my_zip_longest([10, 20, 30], [11, 22, 33]))  # Like zip_two.
    [(10, 11), (20, 22), (30, 33)]
    >>> list(my_zip_longest([10], [11, 22, 33]))
    [(10, 11), (None, 22), (None, 33)]
    >>> list(my_zip_longest([10], [11, 22, 33], fillvalue=0))
    [(10, 11), (0, 22), (0, 33)]
    >>> list(my_zip_longest([10, 20, 30], [11]))
    [(10, 11), (20, None), (30, None)]
    >>> list(my_zip_longest([10, 20, 30], [11], fillvalue=0))
    [(10, 11), (20, 0), (30, 0)]

    >>> list(my_zip_longest([10, 20, 30], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b'), (30, 33, 'c')]
    >>> list(my_zip_longest([10, 20], [11, 22, 33], ['a', 'b', 'c']))
    [(10, 11, 'a'), (20, 22, 'b'), (None, 33, 'c')]
    >>> list(my_zip_longest([10, 20, 30], [11, 22], ['a', 'b', 'c'], fillvalue=99))
    [(10, 11, 'a'), (20, 22, 'b'), (30, 99, 'c')]
    >>> list(my_zip_longest([10, 20, 30], [11, 22, 33], ['a', 'b'], fillvalue='z'))
    [(10, 11, 'a'), (20, 22, 'b'), (30, 33, 'z')]

    >>> from itertools import count, islice
    >>> list(islice(my_zip_longest([10, 20, 30], count(), ['a', 'b', 'c']), 5))
    [(10, 0, 'a'), (20, 1, 'b'), (30, 2, 'c'), (None, 3, None), (None, 4, None)]
    """
    iterators = [iter(iterable) for iterable in iterables]

    while True:
        values = []
        misses = 0

        for it in iterators:
            try:
                values.append(next(it))
            except StopIteration:
                values.append(fillvalue)
                misses += 1

        if misses == len(iterators):
            break

        yield tuple(values)


# FIXME: To reset this as an exercise, remove the last group of doctests.
def singleton_event(value, *, callback=None):
    """
    Yield a single value. Optionally calls a callback when closed.

    This takes advantage of a Python language feature that tries hard to ensure
    code will run after other code. Because it is implemented in a generator
    function whose code is never entered if next is never called on it, closing
    the generator without ever making use of it does not call the callback.

    >>> list(singleton_event(42))
    [42]
    >>> list(singleton_event(76, callback=lambda: print('Done (A).')))
    Done (A).
    [76]
    >>> it = singleton_event('a parrot', callback=lambda: print('Done (B).'))
    >>> it.close()  # Never entered.
    >>> it = singleton_event('a parrot', callback=lambda: print('Done (C).'))
    >>> next(it)
    'a parrot'
    >>> it.close()
    Done (C).

    When a generator object in a suspended state is destroyed, it is closed,
    with the same effect as calling close(). Several Python implementations are
    in use, but if using CPython, these tests will pass because CPython's
    primary garbage collection strategy is reference counting:

    >>> it1 = it2 = singleton_event('foo', callback=lambda: print('Done (D).'))
    >>> next(it1)
    'foo'
    >>> del it1
    >>> del it2
    Done (D).

    Here we prevent this from happening by causing the generator object to be
    in (or reachable from) a reference cycle. The cyclic garbage collector
    would probably destroy it eventually, but it is not destroyed immediately.
    After demonstrating this, we use something from the gc module to trigger a
    garbage collection cycle explicitly. That way, we don't get the side effect
    later when it might interfere with another test, and we verify that the
    generator object is closed even when it is destroyed in this manner.

    >>> import gc
    >>> a = [singleton_event('Hello!', callback=lambda: print('Goodbye!'))]
    >>> a.append(a)
    >>> next(a[0])
    'Hello!'
    >>> del a
    >>> print('Still around.')
    Still around.
    >>> _ = gc.collect()
    Goodbye!
    """
    try:
        yield value
    finally:
        if callback is not None:
            callback()


def maybe_singleton(value, *, fail=False):
    """
    Yield the value, or raise ValueError if fail is True.

    This demonstrates that an exception of any kind propagating out of a
    generator closes the generator. It should therefore be coded in such a way
    that failure causes control to pass over a yield statement, i.e., if the
    code that raises the exception were commented out, then it would yield.

    This is not special. It's analogous to how a return statement or falling
    off the end closes the generator. Control has the left the scope of the
    function. Nonetheless it may be unintuitive if one is unaccustomed to it.

    >>> list(maybe_singleton('foo'))
    ['foo']
    >>> list(maybe_singleton('foo', fail=True))
    Traceback (most recent call last):
      ...
    ValueError: failing instead of yielding 'foo'

    >>> it = maybe_singleton(10, fail=True)  # We don't fail yet...
    >>> next(it)  # Now we fail.
    Traceback (most recent call last):
      ...
    ValueError: failing instead of yielding 10
    >>> list(it)
    []
    """
    if fail:
        raise ValueError(f'failing instead of yielding {value!r}')
    yield value


# FIXME: To reset this as an exercise, remove the last group of doctests.
def doublet(value1, value2, *, callback=None):
    """
    Yield the two arguments in order. Optionally calls a callback when closed.

    This is like singleton(), but it demonstrates that the effect of closing
    was not dependent on being suspended at the last yield that would run.

    >>> list(doublet(42, 76))
    [42, 76]
    >>> list(doublet(76, 42, callback=lambda: print('Done (A).')))
    Done (A).
    [76, 42]
    >>> it = doublet('foo', 'bar', callback=lambda: print('Done (B).'))
    >>> next(it)
    'foo'
    >>> it.close()
    Done (B).

    When a suspended generator is closed, cleanup is performed by raising a
    GeneratorExit exception in it. That is, control resumes from where it left
    off, but with a GeneratorExit exception raised at that point. This lets it
    clean up resources, such as open files, in the way it usually would. It is
    rarely useful to catch GeneratorExit, though occasionally it may be useful
    to do so to distinguish that condition from others. Other than that, one
    reason to catch GeneratorExit may be to observe that this is really what
    happens when a suspended generator is closed. (A generator can't use this
    to refuse to close; a yield after GeneratorExit raises RuntimeError.)

    However, here we demonstrate in a different way that closing a suspended
    generator raises GeneratorExit in it. This uses no except clause (nor any
    with-statement). The callback uses something in the sys module that allows
    it to check if any exception is currently raised and, if so, to get
    information about it, including its type:

    >>> import sys
    >>> def callback():
    ...     print(type(sys.exception()).__name__)
    >>> list(doublet(42, 76, callback=callback))
    NoneType
    [42, 76]
    >>> it = doublet(76, 42, callback=callback)
    >>> next(it)
    76
    >>> it.close()
    GeneratorExit
    """
    try:
        yield value1
        yield value2
    finally:
        if callback is not None:
            callback()


def my_pairwise(iterable):
    """
    Yield all overlapping pairs of elements, in order, like itertools.pairwise.

    >>> next(my_pairwise([]))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> next(my_pairwise(['A']))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(my_pairwise(iter(['A', 'B'])))
    [('A', 'B')]
    >>> list(my_pairwise(['A', 'B', 'C']))
    [('A', 'B'), ('B', 'C')]
    >>> list(my_pairwise(iter(['A', 'B', 'C', 'D'])))
    [('A', 'B'), ('B', 'C'), ('C', 'D')]
    >>> list(my_pairwise(['A', 'B', 'C', 'D', 'E']))
    [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')]
    """
    it = iter(iterable)
    try:
        previous = next(it)
    except StopIteration:
        return

    for current in it:
        yield previous, current
        previous = current


def windowed(iterable, width):
    """
    Yield all overlapping tuples of the given width, in order.

    Auxiliary space complexity is O(width). The collections module can help.

    >>> list(windowed([], 0))
    [()]
    >>> list(windowed([], 5))
    []
    >>> list(windowed('ABCDEFG', 0))
    [(), (), (), (), (), (), (), ()]
    >>> list(windowed(iter('ABCDEFG'), 1))
    [('A',), ('B',), ('C',), ('D',), ('E',), ('F',), ('G',)]
    >>> list(windowed('ABCDEFG', 2))  # Like pairwise.
    [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('F', 'G')]
    >>> list(windowed(iter('ABCDEFG'), 3))  # doctest: +NORMALIZE_WHITESPACE
    [('A', 'B', 'C'), ('B', 'C', 'D'), ('C', 'D', 'E'),
     ('D', 'E', 'F'), ('E', 'F', 'G')]
    >>> list(windowed('ABCDEFG', 4))  # doctest: +NORMALIZE_WHITESPACE
    [('A', 'B', 'C', 'D'), ('B', 'C', 'D', 'E'),
     ('C', 'D', 'E', 'F'), ('D', 'E', 'F', 'G')]
    >>> list(windowed(iter('ABCDEFG'), 5))  # doctest: +NORMALIZE_WHITESPACE
    [('A', 'B', 'C', 'D', 'E'), ('B', 'C', 'D', 'E', 'F'),
     ('C', 'D', 'E', 'F', 'G')]
    >>> list(windowed('ABCDEFG', 6))
    [('A', 'B', 'C', 'D', 'E', 'F'), ('B', 'C', 'D', 'E', 'F', 'G')]
    >>> list(windowed(iter('ABCDEFG'), 7))
    [('A', 'B', 'C', 'D', 'E', 'F', 'G')]
    >>> list(windowed('ABCDEFG', 8))
    []
    >>> list(windowed(iter('ABCDEFG'), 1000))
    []

    >>> from itertools import islice
    >>> from gen1 import squares
    >>> list(islice(windowed(squares(), 4), 4))
    [(0, 1, 4, 9), (1, 4, 9, 16), (4, 9, 16, 25), (9, 16, 25, 36)]
    """
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, width), maxlen=width)
    if len(window) < width:
        return

    yield tuple(window)
    for value in it:
        window.append(value)
        yield tuple(window)


def equal_simple(lhs, rhs):
    """
    Check if corresponding elements of the iterable lhs and rhs are equal.

    >>> [] == ()  # For contrast.
    False
    >>> equal_simple([], ())
    True
    >>> equal_simple('barbaz', ['b', 'a', 'r', 'b', 'a', 'z'])
    True
    >>> equal_simple('barbaz', ['b', 'a', 'r', 'b', 'o', 'z'])
    False
    >>> equal_simple('barba', ['b', 'a', 'r', 'b', 'a', 'z'])
    False
    >>> equal_simple('barbaz', ['b', 'a', 'r', 'b', 'a'])
    False
    >>> equal_simple([], [None])
    False
    >>> equal_simple([None], [])
    False
    >>> equal_simple(iter('hamspameggs'), iter(list('hamspameggs')))
    True
    >>> equal_simple(iter('hamspamegg'), iter(list('hamspameggs')))
    False
    >>> equal_simple(iter('hamspameggs'), iter(list('hamspamegg')))
    False
    """
    zipped = itertools.zip_longest(lhs, rhs, fillvalue=object())
    return all(itertools.starmap(operator.eq, zipped))


# FIXME: To reset as an exercise, change "key=None" to "key".
def equal(*iterables, key=None):
    """
    Check if corresponding elements are equal, with an optional key selector.

    >>> equal()
    True
    >>> import math
    >>> equal(iter([math.nan]), iter([math.nan]))
    False
    >>> equal(iter([math.nan]), iter([math.nan]), key=id)
    True
    >>> equal('abc', iter('abc'), ['a', 'b', 'c'], iter(['a', 'b', 'c']))
    True
    >>> equal('abc', iter('abc'), ['a', 'b'], iter(['a', 'b', 'c']))
    False
    >>> equal('abc', iter('abc'), ['a', 'b', 'c', 'd'], iter(['a', 'b', 'c']))
    False
    >>> equal('abc', iter('abc'), iter('abC'), iter('abC'))
    False
    >>> equal('abc', iter('abc'), iter('abC'), iter('abC'), key=str.casefold)
    True
    """
    if key is None:
        key = identity_function

    return all(
        lhs == rhs
        for row in itertools.zip_longest(*iterables, fillvalue=object())
        for lhs, rhs in itertools.pairwise(map(key, row))
    )


def product_two(iterable1, iterable2):
    """
    Yield elements of the Cartesian product of two iterables.

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
    >>> it = product_two(iter(range(556)), iter(range(721)))
    >>> from itertools import product
    >>> all(x == y for x, y in zip(it, product(range(556), range(721))))
    True
    """
    xs = list(iterable1)
    ys = list(iterable2)
    for x in xs:
        for y in ys:
            yield x, y
