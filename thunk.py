"""Functions that wrap a result."""


def _make_thunk(result):
    return lambda: result


def count(start, stop):
    """
    Make a list of functions returning integers in the range [start, stop).

    Functions like this are sometimes known as thunks. They represent values,
    which are obtained by calling them, so they provide an extra layer of
    indirection around a result that is already known. In practice they are
    most useful when non-thunks may also appear: the consumer of functions,
    some of which are thunks, doesn't need to care for which operations the
    result is already known, and which have to compute it on demand.

    >>> functions = count(1, 6)
    >>> for func in functions:
    ...     print(func())
    1
    2
    3
    4
    5
    >>> functions[3]()
    4
    """
    func_list = []
    for value in range(start, stop):
        func_list.append(_make_thunk(value))

    return func_list


def fizzbuzz():
    """
    Return a list of thunks that play classic FizzBuzz when called in order.

    The kth element of the returned list, when called, prints k. But if it is a
    multiple of 3, it prints "Fizz" instead of the number, and if it is a
    multiple of 5, it prints "Buzz" instead of the number. If it is a multiple
    of both 3 and 5, it prints "FizzBuzz".

    These are not thunks, but they are conceptually related. This is not *just*
    a variation on the above problem (count). It is fairly elegant to solve
    with a technique that would be inelegant there.

    >>> functions = fizzbuzz()
    >>> len(functions)
    100
    >>> for func in functions[:7]:  # indices [0, 7) - nums 1 through 7
    ...     func()
    1
    2
    Fizz
    4
    Buzz
    Fizz
    7
    >>> for func in functions[9:20]:  # indices [9, 20) - nums 10 through 20
    ...     func()
    Buzz
    11
    Fizz
    13
    14
    FizzBuzz
    16
    17
    Fizz
    19
    Buzz
    >>> for func in functions[-5:]:  # indices [95, ...) - nums 96 through 100
    ...     func()
    Fizz
    97
    98
    Fizz
    Buzz
    """
    # FIXME: Implement this.
