"""Caching decorators."""

# ruff: noqa: D401


def memoize_unary(func):
    """
    Decorator to memoize a unary function.

    This caches the results of function calls, using hashing.

    We retain memory of previous results even across separate top-level calls,
    for simplicity and because this behavior is sometimes useful. It also has
    major disadvantages, such as not being thread-safe. But it's more versatile
    than it may seem, because one can define an undecorated top-level function
    that defines a decorated local helper function. (The example of this in the
    doctests uses variables from the enclosing scope, but the technique is also
    sometimes useful just to eliminate global state and make concurrency safe.)

    >>> @memoize_unary
    ... def fibonacci(n):
    ...     return n if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)
    >>> fibonacci(100)
    354224848179261915075

    >>> def fib(n, *, a, b):
    ...     @memoize_unary
    ...     def helper(n):
    ...         if n == 0:
    ...             return a
    ...         if n == 1:
    ...             return b
    ...         return helper(n - 2) + helper(n - 1)
    ...     return helper(n)
    >>> fib(100, a=0, b=1)
    354224848179261915075
    >>> fib(100, a=2, b=1)  # Compute a Lucas number.
    792070839848372253127

    >>> @memoize_unary
    ... def hello(name):
    ...     print(f'Hello, {name}!')
    >>> hello('Alice')
    Hello, Alice!
    >>> hello('Bob')
    Hello, Bob!
    >>> hello('Alice')  # Doesn't print.

    >>> fib.__name__, fibonacci.__name__, hello.__name__
    ('fib', 'fibonacci', 'hello')
    >>>
    """
    # FIXME: Implement this.


def memoize_unary_by(key):
    """
    Parameterized decorator to memoize a unary function with a key selector.

    This is like memoize_unary, but the key selector function, key, is used to
    select a value representing the information used for hash-based comparison.

    The parameter for the key selector function is somewhat confusingly named
    "key". This is for consistency with the min, max, sorted, and list.sort
    functions accepting key selector functions as keyword-only "key" arguments.

    Note that the circumstance under which it is safe to use id as a key
    selector are limited by how ids are reused: they are only guaranteed unique
    across objects with overlapping lifetimes.

    >>> import math
    >>> from decorators import peek_unary

    >>> @memoize_unary_by(lambda x: x)
    ... def fibonacci(n):
    ...     return n if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)
    >>> fibonacci(100)
    354224848179261915075

    >>> @memoize_unary_by(str.casefold)
    ... def hello(name):
    ...     return f'Hello, {name}!'
    >>> hello('Alice')
    'Hello, Alice!'
    >>> hello('bob')
    'Hello, bob!'
    >>> hello('alice')
    'Hello, Alice!'

    >>> @memoize_unary_by(tuple)
    ... @peek_unary
    ... def pythagorean(values):
    ...     return math.hypot(*values)
    >>> pythagorean([2, 3, 4])
    pythagorean([2, 3, 4])
    pythagorean([2, 3, 4]) -> 5.385164807134504
    5.385164807134504
    >>> pythagorean([2, 3, 4])
    5.385164807134504
    >>> pythagorean([2, 4, 3])
    pythagorean([2, 4, 3])
    pythagorean([2, 4, 3]) -> 5.385164807134504
    5.385164807134504

    >>> rows = ([], [], [], [], [], [], [], [])  # Imagine this were bigger.
    >>> @memoize_unary_by(id)
    ... @peek_unary
    ... def row_index(row):
    ...     for index, current_row in enumerate(rows):
    ...         if current_row is row:
    ...             return index
    ...     raise ValueError(f'row with id {id(row)} not found')
    >>> row_index(rows[3])
    row_index([])
    row_index([]) -> 3
    3
    >>> row_index(rows[3])
    3
    """
    # FIXME: Implement this.


def memoize(func):
    """
    Decorator to memoize a function.

    This caches results of function calls, using hashing. Subsequent calls with
    equal corresponding arguments in the same order return a cached result.

    >>> import functools, itertools, random

    >>> @memoize
    ... def fibonacci(n):
    ...     return n if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)
    >>> fibonacci(100)
    354224848179261915075

    >>> def knapsack(vals, weights, capacity):  # 0-1 knapsack problem.
    ...     @memoize
    ...     def solve_from(i, c):
    ...         if i == len(vals):
    ...             return 0
    ...         ret = solve_from(i + 1, c)
    ...         if weights[i] <= c:
    ...             ret = max(ret, vals[i] + solve_from(i + 1, c - weights[i]))
    ...         return ret
    ...     return solve_from(0, capacity)
    >>> knapsack([410, 23, 8, 46, 19, 1, 16], [200, 11, 6, 29, 12, 1, 13], 250)
    488
    >>> r = functools.partial(random.Random(13932671453525407).randint, 1, 100)
    >>> knapsack([r() for _ in range(100)], [r() for _ in range(100)], 2500)
    4009

    >>> counter = itertools.count()
    >>> @memoize
    ... def label(*args, **kwargs):
    ...     return next(counter)
    >>> label(14, 'foo', 'walleye', x=frozenset({2, 3}), y=(42,))
    0
    >>> label()
    1
    >>> label(14, 'foo', 'walleye', x=frozenset({2, 3}), y='(42,)')
    2
    >>> label(14.0, 'foo', 'walleye', x=frozenset({3, 2}), y=(42 + 0j,))
    0
    >>> label(14, 'foo', 'walleye', y=(42,), x=frozenset({2, 3}))
    3
    """
    # FIXME: Implement this.


def memoize_by(key):
    """
    Parameterized decorator to memoize a function with a key selector.

    This is like memoize, but the key selector function, key, is used to select
    a value representing the information used for hash-based comparison, when
    called in the same way as the decorated function was itself called.

    >>> @memoize_by(str.casefold)
    ... def hello(name):
    ...     return f'Hello, {name}!'
    >>> hello('Alice')
    'Hello, Alice!'
    >>> hello('bob')
    'Hello, bob!'
    >>> hello('alice')
    'Hello, Alice!'

    >>> @memoize_by(lambda seq, start, stop: (id(seq), start, stop))
    ... def cached_range_sum(seq, start, stop):
    ...     return sum(seq[start:stop])
    >>> a = [4, 17, 9, 8, -3, 1]
    >>> cached_range_sum(a, 2, 5)
    14
    >>> a[2] += 10
    >>> cached_range_sum(a, 1, 5)
    41
    >>> cached_range_sum(a, 2, 5)
    14
    >>> b = a[:]  # Must assign this to a variable, so its id can't be reused!
    >>> cached_range_sum(b, 2, 5)
    24
    >>> a.clear()
    >>> c = a[:]
    >>> cached_range_sum(c, 2, 5)
    0
    >>> cached_range_sum(a, stop=5, start=2)
    14
    """
    # FIXME: Implement this.


def lru(max_size):
    R"""
    Parameterized decorator implementing a least recently used (LRU) cache.

    Decorating a function with the decorator returned by calling lru places an
    LRU cache in front of the function, so the max_size most recent calls are
    cached. When a cache miss occurs and the computation succeeds, the least
    recently used mapping from arguments to their result is evicted from the
    cache, and the newly computed mapping replaces it.

    >>> lru(0)
    Traceback (most recent call last):
      ...
    ValueError: max_size must be strictly positive (got 0)
    >>> lru(5.0)
    Traceback (most recent call last):
      ...
    TypeError: max_size must be an int or infinity (got 'float')
    >>> lru(0.0)
    Traceback (most recent call last):
      ...
    TypeError: max_size must be an int or infinity (got 'float')

    >>> @lru(5)
    ... def square(n):
    ...     '''Square a number, pretending this is very resource-intensive.'''
    ...     print(f'Pretending to call the expensive SQUARING API for {n=}.')
    ...     return n**2
    >>> square(3)
    Pretending to call the expensive SQUARING API for n=3.
    9
    >>> square(4)
    Pretending to call the expensive SQUARING API for n=4.
    16
    >>> square(3.0)
    9
    >>> square(5)
    Pretending to call the expensive SQUARING API for n=5.
    25
    >>> square(-5)
    Pretending to call the expensive SQUARING API for n=-5.
    25
    >>> square(-10)
    Pretending to call the expensive SQUARING API for n=-10.
    100
    >>> try:
    ...     square('a parrot')
    ... except TypeError as error:
    ...     print(error)
    Pretending to call the expensive SQUARING API for n='a parrot'.
    unsupported operand type(s) for ** or pow(): 'str' and 'int'
    >>> square(4)
    16
    >>> square(7)
    Pretending to call the expensive SQUARING API for n=7.
    49
    >>> square(5)
    25
    >>> square(-10)
    100
    >>> square(3.0)
    Pretending to call the expensive SQUARING API for n=3.0.
    9.0

    >>> import math
    >>> a = []
    >>> f = lru(math.inf)(a.append)
    >>> for i in range(10_000): f(i)  # Should work with larger numbers too.
    >>> f(23)
    >>> a == list(range(10_000))
    True

    >>> @lru(True)  # Bad way to say @lru(1). Works since bool subclasses int.
    ... def idempotent_printf(format, *args, end=''):
    ...     text = format % args
    ...     print(text, end=end)
    ...     return len(text) + len(end)
    >>> idempotent_printf('%r is %d letters.', 'parrot', len('parrot'),
    ...                   end='\n')
    'parrot' is 6 letters.
    23
    >>> idempotent_printf('%r is %d letters.', 'parrot', len('parrot'),
    ...                   end='\n')
    23
    >>> idempotent_printf('%r is %d letters.\n', 'parrot', len('parrot'))
    'parrot' is 6 letters.
    23
    >>> idempotent_printf('%r has %d letters.\n', 'parrot', len('parrot'))
    'parrot' has 6 letters.
    24
    >>> idempotent_printf('%r has %d letters.\n', 'parrot', 6.0)
    24
    >>> idempotent_printf('%r has %d letters.\n', 'parrot', 6.99)
    'parrot' has 6 letters.
    24
    >>> idempotent_printf('%r has %d letters.\n', 'parrot', 6.0)  # max_size==1
    'parrot' has 6 letters.
    24

    >>> square(4)
    16
    >>> square(3)
    9.0
    >>> square(6)
    Pretending to call the expensive SQUARING API for n=6.
    36
    >>> square(7)
    Pretending to call the expensive SQUARING API for n=7.
    49
    >>> square.clear()
    >>> square(7)
    Pretending to call the expensive SQUARING API for n=7.
    49
    >>> idempotent_printf('%r has %d letters.\n', 'parrot', 6.0)
    24
    >>> square(7)
    49

    >>> set(dir(square.__wrapped__)) == set(dir(lambda: None))
    True
    >>> sorted(set(dir(square)) - set(dir(square.__wrapped__)))
    ['__wrapped__', 'clear']
    >>> square.__name__, square.__doc__
    ('square', 'Square a number, pretending this is very resource-intensive.')
    >>> square.clear.__name__, square.clear.__doc__
    ('clear', "Clear the wrapped function's LRU cache.")
    """
    # FIXME: Implement this.
