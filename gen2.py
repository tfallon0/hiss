"""More generators exercises."""


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
