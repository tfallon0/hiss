"""Caching decorators."""


def memoize(func):
    """
    Decorator to memoize a unary function, using hashing.

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
    # FIXME: Implement this.
