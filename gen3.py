"""Even more generators exercises."""

import collections
import heapq
import itertools
import operator

from util import identity_function


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


_next_or_default_sentinel = object()


# FIXME: To reset this as an exercise, remove the default argument and the "/".
def next_or_default(iterator, default=_next_or_default_sentinel, /):
    """
    Get the next value from an iterator, falling back to a default if supplied.

    This reimplements the full functionality of the next builtin, using only
    the one-argument form of next. The one argument form is overwhelmingly the
    most common and useful, but the two argument form is occasionally handy.
    Reimplementing it without ever passing more than one argument to next gives
    insight into what the two-argument form of next is actually doing.

    >>> it = iter([42, 76])
    >>> next_or_default(it)
    42
    >>> next_or_default(it)
    76
    >>> next_or_default(it)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> next_or_default(it, None) is None
    True

    >>> it = iter([42, 76])
    >>> next_or_default(it, 1000)
    42
    >>> next_or_default(it, 1000)
    76
    >>> next_or_default(it, 1000)
    1000
    >>> next_or_default(it, 999)
    999
    >>> next_or_default(it, None) is None
    True

    >>> next_or_default(it, default=0)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    TypeError: next_or_default() got some positional-only arguments passed as
               keyword arguments: 'default'
    """
    try:
        return next(iterator)
    except StopIteration:
        if default is _next_or_default_sentinel:
            raise
        return default


# FIXME: To reset this as an exercise, remove the default argument and the "/".
def next_or_default_alt(iterator, default=_next_or_default_sentinel, /):
    """
    Get the next value from an iterator, falling back to a default if supplied.

    This alternative implementation of next_or_default() does not use the next
    builtin, nor does it call any other code in this project. It should be done
    in some reasonable way that is not clearly worse than in next_or_default().

    >>> it = iter([42, 76])
    >>> next_or_default_alt(it)
    42
    >>> next_or_default_alt(it)
    76
    >>> next_or_default_alt(it)
    Traceback (most recent call last):
      ...
    StopIteration
    >>> next_or_default_alt(it, None) is None
    True

    >>> it = iter([42, 76])
    >>> next_or_default_alt(it, 1000)
    42
    >>> next_or_default_alt(it, 1000)
    76
    >>> next_or_default_alt(it, 1000)
    1000
    >>> next_or_default_alt(it, 999)
    999
    >>> next_or_default_alt(it, None) is None
    True

    >>> next_or_default_alt(it, default=0)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    TypeError: next_or_default_alt() got some positional-only arguments passed
               as keyword arguments: 'default'
    """
    for value in iterator:
        return value
    if default is not _next_or_default_sentinel:
        return default
    raise StopIteration


# FIXME: To reset this as an exercise, change "key=None" to "key".
def merge_two(iterable1, iterable2, *, key=None):
    """
    Yield values in sorted order from two sorted iterables (two-way merge).

    This is a stable merge: in case of a tie, it yields from iterable1 first.
    Where iterable1 has m elements and iterable2 has n elements, this runs in
    O(m + n) time and uses O(1) auxiliary space.

    >>> next(merge_two([], []))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> list(merge_two([42], [])) == list(merge_two([], [42])) == [42]
    True
    >>> list(merge_two([10], [11])) == list(merge_two([11], [10])) == [10, 11]
    True
    >>> list(merge_two([None], [])) == list(merge_two([], [None])) == [None]
    True

    >>> import operator
    >>> list(merge_two([10], [11], key=operator.neg))
    [11, 10]
    >>> a = ['ox', 'dog', 'tiger', 'bobcat']
    >>> b = ['owl', 'crow', 'raven', 'robin', 'parrot']
    >>> list(merge_two(a, b, key=len))
    ['ox', 'dog', 'owl', 'crow', 'tiger', 'raven', 'robin', 'bobcat', 'parrot']
    >>> list(merge_two(iter(a), iter(b), key=len))
    ['ox', 'dog', 'owl', 'crow', 'tiger', 'raven', 'robin', 'bobcat', 'parrot']

    >>> from itertools import count, islice
    >>> list(islice(merge_two(count(5, 2), count(2, 3)), 20))
    [2, 5, 5, 7, 8, 9, 11, 11, 13, 14, 15, 17, 17, 19, 20, 21, 23, 23, 25, 26]

    >>> it1, it2 = iter([0, 1, 2, 3]), iter([0.0, 1.0, 2.0, 3.0])
    >>> it3 = merge_two(it1, it2)
    >>> list(islice(it3, 3)), next(it1), next(it2), list(islice(it3, 3))
    ([0, 0.0, 1], 2, 2.0, [1.0, 3, 3.0])
    """
    if key is None:
        key = identity_function

    no_value = object()

    it1 = iter(iterable1)
    it2 = iter(iterable2)
    value1 = next(it1, no_value)
    value2 = next(it2, no_value)

    while value1 is not no_value and value2 is not no_value:
        if key(value2) < key(value1):
            yield value2
            value2 = next(it2, no_value)
        else:
            yield value1
            value1 = next(it1, no_value)

    if value1 is not no_value:
        yield value1
        yield from it1
    elif value2 is not no_value:
        yield value2
        yield from it2


# FIXME: To reset this as an exercise, change "key=None" to "key".
def merge(*iterables, key=None):
    """
    Yield values in sorted order from sorted iterables (multi-way merge).

    This is a stable merge: in case of a tie, it yields from earlier iterables
    first. It delegates much of its computational work to merge_two(), and the
    key selector function is never called or examined directly, but only passed
    in calls to merge_two(). With k iterables and n total elements, this takes
    O(k + n log k) time and uses O(k log k) auxiliary space.

    >>> next(merge())
    Traceback (most recent call last):
      ...
    StopIteration
    >>> next(merge({42}))
    42
    >>> list(merge([])) == list(merge([], [])) == list(merge([], [], [])) == []
    True

    >>> a = ['px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx']
    >>> b = ['pz', 'qx', 'ry', 'sy', 'tz', 'ux', 'vz', 'w1', 'w7']
    >>> c = []
    >>> d = ['py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy']
    >>> e = ['w2', 'w4', 'w8', 'w9']
    >>> f = ['p']
    >>> g = ['w3', 'w5', 'w6']

    >>> list(merge(a, b, c, d, e, f, g))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']
    >>> list(merge(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...            iter(g)))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']

    >>> import operator
    >>> list(merge(a, b, c, d, e, f, g, key=operator.itemgetter(0)))
    ... # doctest: +NORMALIZE_WHITESPACE
    ['px', 'pz', 'py', 'p', 'qy', 'qx', 'qz', 'rx', 'ry', 'rz', 'sz', 'sy',
     'sx', 'tx', 'tz', 'ty', 'uz', 'ux', 'uy', 'vx', 'vz', 'vy', 'w1', 'w7',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']
    >>> list(merge(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...            iter(g), key=len))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx', 'pz', 'qx', 'ry', 'sy',
     'tz', 'ux', 'vz', 'w1', 'w7', 'py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']

    >>> import random
    >>> r = random.Random(434300959987162159)
    >>> nums = [r.randrange(2**32) for _ in range(2063)]
    >>> singletons = ((x,) for x in nums)
    >>> list(merge(*singletons)) == sorted(nums)
    True
    >>> from itertools import islice, count
    >>> it = merge(count(3), count(9), count(0), count(1), count(4), count(2))
    >>> list(islice(it, 48))  # doctest: +NORMALIZE_WHITESPACE
    [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6,
     7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11]
    """
    match iterables:
        case []:
            return iter(())
        case [iterable]:
            return iter(iterable)
        case _:
            mid = len(iterables) // 2
            left = merge(*iterables[:mid], key=key)
            right = merge(*iterables[mid:], key=key)
            return merge_two(left, right, key=key)


# FIXME: To reset this as an exercise, change "key=None" to "key".
def merge_alt(*iterables, key=None):
    """
    Yield values in sorted order from sorted iterables (multi-way merge).

    This alternative implementation of merge() satisfies the same requirements,
    with the same asymptotic time and asymptotic auxiliary space complexities.
    One implementation is of a naturally recursive algorithm and implemented
    with recursion, while the other is of a naturally iterative algorithm and
    implemented without recursion. The algorithms are very closely related. It
    might seem intuitively that the non-recursive implementation would have a
    smaller asymptotic space complexity, but that is not the case. (Neither
    should be confused with merge_pq() below, which differs greatly from both.)

    The effects of calling merge() or merge_alt(), once they have returned, may
    be indistinguishable, not just in the values they will yield when iterated,
    but in the objects in memory and the way they refer to and use one another.
    Specifically, these effects are indistinguishable IF the functions:

    1. were implemented [FIXME: what about their implementations?], and

    2. are passed an arbitrarily large number of arguments, but [FIXME: what?].

    >>> next(merge_alt())
    Traceback (most recent call last):
      ...
    StopIteration
    >>> next(merge_alt({42}))
    42
    >>> (list(merge_alt([])) == list(merge_alt([], []))
    ...  == list(merge_alt([], [], [])) == [])
    True

    >>> a = ['px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx']
    >>> b = ['pz', 'qx', 'ry', 'sy', 'tz', 'ux', 'vz', 'w1', 'w7']
    >>> c = []
    >>> d = ['py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy']
    >>> e = ['w2', 'w4', 'w8', 'w9']
    >>> f = ['p']
    >>> g = ['w3', 'w5', 'w6']

    >>> list(merge_alt(a, b, c, d, e, f, g))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']
    >>> list(merge_alt(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...                iter(g)))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']

    >>> import operator
    >>> list(merge_alt(a, b, c, d, e, f, g, key=operator.itemgetter(0)))
    ... # doctest: +NORMALIZE_WHITESPACE
    ['px', 'pz', 'py', 'p', 'qy', 'qx', 'qz', 'rx', 'ry', 'rz', 'sz', 'sy',
     'sx', 'tx', 'tz', 'ty', 'uz', 'ux', 'uy', 'vx', 'vz', 'vy', 'w1', 'w7',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']
    >>> list(merge_alt(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...                iter(g), key=len))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx', 'pz', 'qx', 'ry', 'sy',
     'tz', 'ux', 'vz', 'w1', 'w7', 'py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']

    >>> import random
    >>> r = random.Random(434300959987162159)
    >>> nums = [r.randrange(2**32) for _ in range(2063)]
    >>> singletons = ((x,) for x in nums)
    >>> list(merge_alt(*singletons)) == sorted(nums)
    True
    >>> from itertools import islice, count
    >>> it = merge_alt(count(3), count(9), count(0), count(1), count(4), count(2))
    >>> list(islice(it, 48))  # doctest: +NORMALIZE_WHITESPACE
    [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6,
     7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11]
    """
    if not iterables:
        return iter(())

    groups = [iter(iterable) for iterable in iterables]

    while len(groups) != 1:
        merged_groups = []
        for batch in itertools.batched(groups, 2):
            match batch:
                case [left, right]:
                    merged_groups.append(merge_two(left, right, key=key))
                case [last]:
                    merged_groups.append(last)
        groups = merged_groups

    return groups[0]


# FIXME: To reset this as an exercise, change "key=None" to "key".
def merge_simple(*iterables, key=None):
    """
    Materialize values in sorted order from sorted iterables (multi-way merge).

    This is a stable merge highly likely to run in O(k + n log k) time. Unlike
    merge(), merge_alt(), merge_pq() below, which return iterators and only
    iterate through each input just enough to support each yielded value, this
    iterates through all its input iterables and returns a sorted list. It thus
    writes to O(n) space. It may also use O(n) further auxiliary space beyond
    that. The code is a single return statement that fits easily on one line.

    In CPython, this ought to take only O(k + n log k) time, but it's possible
    some high-quality Python implementation may take as long as O(k + n log n)
    time even on average. The reason is that, in CPython, [FIXME: what?].

    >>> (merge_simple() == merge_simple([]) == merge_simple([], [])
    ...  == merge_simple([], [], []) == [])
    True
    >>> merge_simple({42})
    [42]

    >>> a = ['px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx']
    >>> b = ['pz', 'qx', 'ry', 'sy', 'tz', 'ux', 'vz', 'w1', 'w7']
    >>> c = []
    >>> d = ['py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy']
    >>> e = ['w2', 'w4', 'w8', 'w9']
    >>> f = ['p']
    >>> g = ['w3', 'w5', 'w6']

    >>> merge_simple(a, b, c, d, e, f, g)  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']
    >>> merge_simple(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...              iter(g))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']

    >>> import operator
    >>> merge_simple(a, b, c, d, e, f, g, key=operator.itemgetter(0))
    ... # doctest: +NORMALIZE_WHITESPACE
    ['px', 'pz', 'py', 'p', 'qy', 'qx', 'qz', 'rx', 'ry', 'rz', 'sz', 'sy',
     'sx', 'tx', 'tz', 'ty', 'uz', 'ux', 'uy', 'vx', 'vz', 'vy', 'w1', 'w7',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']
    >>> merge_simple(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...              iter(g), key=len)  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx', 'pz', 'qx', 'ry', 'sy',
     'tz', 'ux', 'vz', 'w1', 'w7', 'py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']

    >>> import random
    >>> r = random.Random(434300959987162159)
    >>> nums = [r.randrange(2**32) for _ in range(2063)]
    >>> singletons = ((x,) for x in nums)
    >>> merge_simple(*singletons) == sorted(nums)
    True
    """
    return sorted(itertools.chain.from_iterable(iterables), key=key)


# FIXME: To reset this as an exercise, change "key=None" to "key".
def merge_pq(*iterables, key=None):
    """
    Yield values in sorted order from sorted iterables (multi-way merge).

    Like merge() and merge_alt(), this is a stable merge: in case of a tie, it
    yields from earlier iterables first. But this uses an entirely different
    technique, making no use of merge_two(). With k iterables and n total
    elements, this still takes O(k + n log k) time, but this uses only O(k)
    auxiliary space. This is thus like heapq.merge with no "reverse" parameter.
    This does not use heapq.merge, but it may use other heapq functions.

    >>> next(merge_pq())
    Traceback (most recent call last):
      ...
    StopIteration
    >>> next(merge_pq({42}))
    42
    >>> list(merge_pq([])) == list(merge_pq([], [])) == list(merge_pq([], [], [])) == []
    True

    >>> a = ['px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx']
    >>> b = ['pz', 'qx', 'ry', 'sy', 'tz', 'ux', 'vz', 'w1', 'w7']
    >>> c = []
    >>> d = ['py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy']
    >>> e = ['w2', 'w4', 'w8', 'w9']
    >>> f = ['p']
    >>> g = ['w3', 'w5', 'w6']

    >>> list(merge_pq(a, b, c, d, e, f, g))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']
    >>> list(merge_pq(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...               iter(g)))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'py', 'pz', 'qx', 'qy', 'qz', 'rx', 'ry', 'rz', 'sx', 'sy',
     'sz', 'tx', 'ty', 'tz', 'ux', 'uy', 'uz', 'vx', 'vy', 'vz', 'w1', 'w2',
     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']

    >>> import operator
    >>> list(merge_pq(a, b, c, d, e, f, g, key=operator.itemgetter(0)))
    ... # doctest: +NORMALIZE_WHITESPACE
    ['px', 'pz', 'py', 'p', 'qy', 'qx', 'qz', 'rx', 'ry', 'rz', 'sz', 'sy',
     'sx', 'tx', 'tz', 'ty', 'uz', 'ux', 'uy', 'vx', 'vz', 'vy', 'w1', 'w7',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']
    >>> list(merge_pq(iter(a), iter(b), iter(c), iter(d), iter(e), iter(f),
    ...               iter(g), key=len))  # doctest: +NORMALIZE_WHITESPACE
    ['p', 'px', 'qy', 'rx', 'sz', 'tx', 'uz', 'vx', 'pz', 'qx', 'ry', 'sy',
     'tz', 'ux', 'vz', 'w1', 'w7', 'py', 'qz', 'rz', 'sx', 'ty', 'uy', 'vy',
     'w2', 'w4', 'w8', 'w9', 'w3', 'w5', 'w6']

    >>> import random
    >>> r = random.Random(434300959987162159)
    >>> nums = [r.randrange(2**32) for _ in range(2063)]
    >>> singletons = ((x,) for x in nums)
    >>> list(merge_pq(*singletons)) == sorted(nums)
    True
    >>> from itertools import islice, count
    >>> it = merge_pq(count(3), count(9), count(0), count(1), count(4), count(2))
    >>> list(islice(it, 48))  # doctest: +NORMALIZE_WHITESPACE
    [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6,
     7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11]
    """
    if key is None:
        key = identity_function

    no_value = object()
    heap = [
        (key(value), index, it, value)
        for index, it in enumerate(map(iter, iterables))
        if (value := next(it, no_value)) is not no_value
    ]
    heapq.heapify(heap)

    while heap:
        _, index, it, value = heap[0]
        yield value
        try:
            value = next(it)
        except StopIteration:
            heapq.heappop(heap)
        else:
            heapq.heapreplace(heap, (key(value), index, it, value))


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


def make_debug_simple():
    """
    Make a factory of counting generators that report being closed.

    Each call to make_debug_simple() returns an independent function. The
    generator objects returned by one such function are interdependent, but
    completely independent of the generator objects returned by other such
    functions.

    The way generator objects returned by the same function make_debug_simple()
    returns are interdependent is not in the values they yield -- which are
    independent and consist of ascending integers starting from 1 -- but
    instead in the messages they print when closed, which begin with the
    generator object's number. That number is determined at the time the
    function creates the generator object: each function make_debug_simple()
    returns maintains its own count, separate from other functions' counts, of
    how many generator objects it has created. The numbers associated with
    generator objects from the same function are ascending integers starting
    from 1, but they should not be confused with the values the generator
    objects yield.

    If a never-iterated generator object is closed, nothing is printed.

    >>> f, g = make_debug_simple(), make_debug_simple()
    >>> fit1, git1, git2, fit2, git3, fit3 = f(), g(), g(), f(), g(), f()
    >>> next(git1), next(fit1), next(fit2), next(fit1), next(git2), next(git1)
    (1, 1, 1, 2, 1, 2)
    >>> next(fit3), next(fit2), next(git3), next(fit1), next(git1), next(git2)
    (1, 2, 1, 3, 3, 2)
    >>> next(git3), next(git3), next(fit1), next(git1), next(fit3), next(fit2)
    (2, 3, 4, 4, 2, 3)
    >>> del fit3
    3 closed (next=3).
    >>> del fit1
    1 closed (next=5).
    >>> next(git2), next(git1), next(git1), next(git2), next(git1), next(git2)
    (3, 5, 6, 4, 7, 5)
    >>> del git2
    2 closed (next=6).
    >>> git1 = None  # Assigning another object also decrements a refcount.
    1 closed (next=8).
    >>> next(fit2), next(fit2), next(git3), next(fit2), next(fit2), next(git3)
    (4, 5, 4, 6, 7, 5)
    >>> del git3, fit2
    3 closed (next=6).
    2 closed (next=8).

    >>> fit4, fit5, fit6 = f(), f(), f()
    >>> del fit6  # No next() call on fit6, so nothing printed for it.
    >>> next(fit5)
    1
    >>> del fit4, fit5  # Prints for fit5 only, since it got a next() call.
    5 closed (next=2).

    Bonus: Can you do it with no statements of the form "yield <expression>"?
    """
    outer_counter = itertools.count(1)

    def debug():
        outer_index = next(outer_counter)

        def generate():
            inner_counter = itertools.count(1)
            try:
                yield from inner_counter
            finally:
                print(f'{outer_index} closed (next={next(inner_counter)}).')

        return generate()

    return debug


def make_debug():
    """
    Make a factory of counting generators that always report being closed.

    This is like make_debug_simple(), except the generator objects -- which are
    returned by functions make_debug() returns -- always print their "closed"
    messages, even the caller of the function that created them discards them
    without ever calling next() on them or otherwise iterating them.

    >>> f, g = make_debug(), make_debug()
    >>> fit1, git1, git2, fit2, git3, fit3 = f(), g(), g(), f(), g(), f()
    >>> next(git1), next(fit1), next(fit2), next(fit1), next(git2), next(git1)
    (1, 1, 1, 2, 1, 2)
    >>> next(fit3), next(fit2), next(git3), next(fit1), next(git1), next(git2)
    (1, 2, 1, 3, 3, 2)
    >>> next(git3), next(git3), next(fit1), next(git1), next(fit3), next(fit2)
    (2, 3, 4, 4, 2, 3)
    >>> del fit3
    3 closed (next=3).
    >>> del fit1
    1 closed (next=5).
    >>> next(git2), next(git1), next(git1), next(git2), next(git1), next(git2)
    (3, 5, 6, 4, 7, 5)
    >>> del git2
    2 closed (next=6).
    >>> git1 = None  # Assigning another object also decrements a refcount.
    1 closed (next=8).
    >>> next(fit2), next(fit2), next(git3), next(fit2), next(fit2), next(git3)
    (4, 5, 4, 6, 7, 5)
    >>> del git3, fit2
    3 closed (next=6).
    2 closed (next=8).

    >>> fit4, fit5, fit6 = f(), f(), f()
    >>> del fit6  # We didn't call next() on fit6, yet it still prints.
    6 closed (next=1).
    >>> next(fit5)
    1
    >>> del fit4, fit5  # Prints for both fit4 and fit5.
    4 closed (next=1).
    5 closed (next=2).
    """
    outer_counter = itertools.count(1)

    def debug():
        outer_index = next(outer_counter)

        def generate():
            inner_counter = itertools.count(0)
            try:
                yield from inner_counter
            finally:
                print(f'{outer_index} closed (next={next(inner_counter)}).')

        it = generate()
        next(it)
        return it

    return debug


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
    Yield all overlapping tuples of the given "width", in order.

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
    >>> from gen1 import cubes
    >>> list(islice(windowed(cubes(), 4), 4))
    [(0, 1, 8, 27), (1, 8, 27, 64), (8, 27, 64, 125), (27, 64, 125, 216)]
    """
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, width), maxlen=width)
    if len(window) < width:
        return

    yield tuple(window)
    for value in it:
        window.append(value)
        yield tuple(window)


# FIXME: To reset as an exercise, remove the default arguments.
def is_sorted_simple(iterable, *, key=None, reverse=False):
    """
    Check if an iterable is sorted, in the simple way that is often best.

    This is the easy straightforward way to check if a finite iterable is
    sorted. It is often in practice the fastest. For a length-n iterable, it
    takes O(n log n) time and uses O(n) auxiliary space. At least on CPython,
    on input for which True shall be returned, it takes only O(n) time. A major
    limitation is this cannot be used on an infinite iterable even if it could
    be found unsorted only by inspecting the first few elements.

    If a key selector function is passed, sorting is checked with respect to
    it. If reverse=True is passed, the check is for descending-order sorting.

    >>> import operator
    >>> is_sorted_simple([])
    True
    >>> is_sorted_simple([3, 3, 3, 3, 3, 3, 3])
    True
    >>> is_sorted_simple(iter(range(1000)), reverse=False)
    True
    >>> is_sorted_simple(iter(range(1000)), reverse=True)
    False
    >>> is_sorted_simple(iter(range(1000)), key=operator.neg, reverse=False)
    False
    >>> is_sorted_simple(iter(range(1000)), key=operator.neg, reverse=True)
    True
    >>> a = ['px', 'py', 'qy', 'qx', 'rx', 'ry']
    >>> is_sorted_simple(a)
    False
    >>> is_sorted_simple(a, key=operator.itemgetter(0))
    True
    >>> is_sorted_simple(reversed(a), key=operator.itemgetter(0))
    False
    >>> is_sorted_simple(reversed(a), reverse=True)
    False
    >>> is_sorted_simple(a[::-1], key=operator.itemgetter(0), reverse=True)
    True
    """
    values = list(iterable)
    return sorted(values, key=key, reverse=reverse) == values


# FIXME: To reset as an exercise, remove the default arguments.
def is_sorted(iterable, *, key=None, reverse=False):
    """
    Check if an iterable is sorted.

    This checks if the provided iterable is sorted. For an iterable whose
    longest sorted prefix is length k, this takes O(k) time and uses O(1)
    auxiliary space. It is therefore sometimes suitable for use on iterables
    that may be very long or infinite, though it would never complete on an
    infinite sorted iterable. Like is_sorted_simple, this does not use any
    loops. Parameters are as in is_sorted_simple.

    >>> import itertools, operator
    >>> is_sorted([])
    True
    >>> is_sorted([3, 3, 3, 3, 3, 3, 3])
    True
    >>> is_sorted(iter(range(1000)), reverse=False)
    True
    >>> is_sorted(itertools.count(), reverse=True)
    False
    >>> is_sorted(itertools.count(), key=operator.neg, reverse=False)
    False
    >>> is_sorted(iter(range(1000)), key=operator.neg, reverse=True)
    True
    >>> a = ['px', 'py', 'qy', 'qx', 'rx', 'ry']
    >>> is_sorted(itertools.cycle(a))
    False
    >>> is_sorted(a, key=operator.itemgetter(0))
    True
    >>> is_sorted(itertools.cycle(reversed(a)), key=operator.itemgetter(0))
    False
    >>> is_sorted(reversed(a), reverse=True)
    False
    >>> is_sorted(a[::-1], key=operator.itemgetter(0), reverse=True)
    True
    """
    if key is not None:
        iterable = map(key, iterable)
    compare = operator.ge if reverse else operator.le
    pairs = itertools.pairwise(iterable)
    return all(itertools.starmap(compare, pairs))


# FIXME: To reset as an exercise, remove the default arguments.
def is_sorted_alt(iterable, *, key=None, reverse=False):
    """
    Check if an iterable is sorted.

    This is an alternative implementation of is_sorted(), satisfying all the
    same requirements and using effectively the same algorithm. One contains no
    comprehensions but uses itertools.starmap, while the other uses exactly
    one comprehension but not map, starmap, nor any similar function.

    >>> import itertools, operator
    >>> is_sorted_alt([])
    True
    >>> is_sorted_alt([3, 3, 3, 3, 3, 3, 3])
    True
    >>> is_sorted_alt(iter(range(1000)), reverse=False)
    True
    >>> is_sorted_alt(itertools.count(), reverse=True)
    False
    >>> is_sorted_alt(itertools.count(), key=operator.neg, reverse=False)
    False
    >>> is_sorted_alt(iter(range(1000)), key=operator.neg, reverse=True)
    True
    >>> a = ['px', 'py', 'qy', 'qx', 'rx', 'ry']
    >>> is_sorted_alt(itertools.cycle(a))
    False
    >>> is_sorted_alt(a, key=operator.itemgetter(0))
    True
    >>> is_sorted_alt(itertools.cycle(reversed(a)), key=operator.itemgetter(0))
    False
    >>> is_sorted_alt(reversed(a), reverse=True)
    False
    >>> is_sorted_alt(a[::-1], key=operator.itemgetter(0), reverse=True)
    True
    """
    if key is None:
        key = identity_function
    compare = operator.ge if reverse else operator.le
    pairs = itertools.pairwise(iterable)
    return all(compare(key(lhs), key(rhs)) for lhs, rhs in pairs)


def equal_simple(lhs, rhs):
    """
    Check if corresponding elements of the iterable lhs and rhs are equal.

    For iterables of lengths m and n, this takes O(min(m, n)) time and uses
    O(1) auxiliary space. It does not use any loops, nor do the "if" or "try"
    keywords, nor the "match" contextual keyword, appear in the implementation.

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


def equal_simple_alt(lhs, rhs):
    """
    Check if corresponding elements of the iterable lhs and rhs are equal.

    This is an alternative implementation of equal_simple(), satisfying all the
    same requirements and using effectively the same algorithm. One contains no
    comprehensions but uses itertools.starmap, while the other uses exactly
    one comprehension but not map, starmap, nor any similar function. (This is
    to say that the relationship between equal_simple() and equal_simple_alt()
    is roughly analogous to that between is_sorted() and is_sorted_alt().)

    >>> [] == ()  # For contrast.
    False
    >>> equal_simple_alt([], ())
    True
    >>> equal_simple_alt('barbaz', ['b', 'a', 'r', 'b', 'a', 'z'])
    True
    >>> equal_simple_alt('barbaz', ['b', 'a', 'r', 'b', 'o', 'z'])
    False
    >>> equal_simple_alt('barba', ['b', 'a', 'r', 'b', 'a', 'z'])
    False
    >>> equal_simple_alt('barbaz', ['b', 'a', 'r', 'b', 'a'])
    False
    >>> equal_simple_alt([], [None])
    False
    >>> equal_simple_alt([None], [])
    False
    >>> equal_simple_alt(iter('hamspameggs'), iter(list('hamspameggs')))
    True
    >>> equal_simple_alt(iter('hamspamegg'), iter(list('hamspameggs')))
    False
    >>> equal_simple_alt(iter('hamspameggs'), iter(list('hamspamegg')))
    False
    """
    zipped = itertools.zip_longest(lhs, rhs, fillvalue=object())
    return all(x == y for x, y in zipped)


# FIXME: To reset as an exercise, change "key=None" to "key".
def equal(*iterables, key=None):
    """
    Check if corresponding elements are equal, with an optional key selector.

    For k iterables the shortest of which is length n, this takes O(k n) time
    and uses O(k) auxiliary space.

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


# FIXME: Create the following exercises here:
#
#   - my_product
#   - my_product_alt
#   - my_product_iterative
#   - tee_two
#   - my_tee
