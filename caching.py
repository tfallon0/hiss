"""Caching decorators."""

import functools


def memoize(func):
    """
    Decorator to memoize a unary function.

    This caches the results of function calls, using hashing.

    We retain memory of previous results even across separate top-level calls,
    for simplicity and because this behavior is sometimes useful (though it
    also has major disadvantages, such as not being thread-safe).

    >>> def fib(n):
    ...     return n if n < 2 else fib(n - 2) + fib(n - 1)
    >>> fib = memoize(fib)
    >>> fib(100)
    354224848179261915075

    >>> @memoize
    ... def fibonacci(n):
    ...     return n if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)
    >>> fibonacci(100)
    354224848179261915075

    >>> @memoize
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
    return memoize_by(lambda arg: arg)(func)


def memoize_by(key):
    """
    Parameterized decorator to memoize a unary function with a key selector.

    This is like memoize, but the key selector function, key, is used to select
    a value representing the information used for hash-based comparison.

    The parameter for the key selector function is somewhat confusingly named
    "key". This is for consistency with the min, max, sorted, and list.sort
    functions accepting key selector functions as keyword-only "key" arguments.

    >>> import math
    >>> from decorators import peek_unary

    >>> @memoize_by(lambda x: x)
    ... def fibonacci(n):
    ...     return n if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)
    >>> fibonacci(100)
    354224848179261915075

    >>> @memoize_by(str.casefold)
    ... def hello(name):
    ...     return f'Hello, {name}!'
    >>> hello('Alice')
    'Hello, Alice!'
    >>> hello('bob')
    'Hello, bob!'
    >>> hello('alice')
    'Hello, Alice!'

    >>> @memoize_by(tuple)
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
    >>> @memoize_by(id)
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
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(arg):
            computed_key = key(arg)
            try:
                return cache[computed_key]
            except KeyError:
                result = func(arg)
                cache[computed_key] = result
                return result

        return wrapper

    return decorator
