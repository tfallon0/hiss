"""Some higher order functions related to function composition."""


def compose2(f, g):
    """
    Compose the unary functions f and g.

    This computes f ∘ g, the composition of f and g.

    >>> h = compose2(lambda x: x + 1, lambda x: x * 2)
    >>> h(0)
    1
    >>> h(5)
    11
    >>> compose2(len, lambda x: x * 3)('foobar')
    18
    >>> a = []
    >>> b = ['A', 'B', 'C', 'D', 'E', 'F']
    """
    return lambda x: f(g(x))


def compose2_alt(f, g):
    """
    Compose the unary functions f and g. Alternative implementation.

    This behaves the same as compose2, but they are implemented differently.
    One implementation uses a lambda expression and is a single line long. The
    other uses no lambda expressions (though its doctests do).

    >>> h = compose2_alt(lambda x: x + 1, lambda x: x * 2)
    >>> h(0)
    1
    >>> h(5)
    11
    >>> compose2_alt(len, lambda x: x * 3)('foobar')
    18
    """
    def fog(x):
        return f(g(x))

    return fog


def repeat_compose(func, count):
    """
    Compose func with itself count times.

    >>> repeat_compose(lambda x: x + 1, 0)(23)
    23
    >>> repeat_compose(lambda x: x + 1, 1)(23)
    24
    >>> repeat_compose(lambda x: x + 1, 10_000)(23)
    10023
    >>> repeat_compose(lambda x: x + 1, 10_000)(-1)
    9999
    >>> repeat_compose(lambda x: x * 1.002, 9999)(1.002)
    475570943.60609066
    >>> repeat_compose(lambda x: x * 1.002, 10_000)(1)
    475570943.60609066
    """
    if count == 0:
        return lambda x: x
    elif count%2 == 0:
        t = repeat_compose(func, count//2)
        return compose2(t,t)
    else:
        t = repeat_compose(func, count//2)
        return compose2(func, compose2(t,t))


def repeat_compose_alt(func, count):
    """
    Compose func iteratively with itself count times.

    >>> repeat_compose_alt(lambda x: x + 1, 0)(23)
    23
    >>> repeat_compose_alt(lambda x: x + 1, 1)(23)
    24
    >>> repeat_compose_alt(lambda x: x + 1, 10_000)(23)
    10023
    >>> repeat_compose_alt(lambda x: x + 1, 10_000)(-1)
    9999
    >>> repeat_compose_alt(lambda x: x * 1.002, 9999)(1.002)
    475570943.60609066
    >>> repeat_compose_alt(lambda x: x * 1.002, 10_000)(1)
    475570943.60609066
    """
    def f(x):
        for n in range(0,count):
            x = func(x)
        return x
    return f

def compose(*functions):
    """
    Compose a chain of functions.

    >>> compose()(42)
    42
    >>> compose()('seventy-six')
    'seventy-six'
    >>> compose(len)('foo')
    3
    >>> compose(len)([])
    0
    >>> compose(lambda x: x + 1, lambda x: x * 2)(0)
    1
    >>> compose(lambda x: x + 1, lambda x: x * 2)(5)
    11
    >>> all_same = [lambda x: x * 1.002] * 10_000
    >>> compose(*all_same)(1)
    475570943.60609066

    >>> not_all_same = [lambda x: x + [1], lambda x: x + [2], lambda x: x * 2]
    >>> compose(*not_all_same)([7])
    [7, 7, 2, 1]
    >>> compose(*(not_all_same * 3))([4])
    [4, 4, 2, 1, 4, 4, 2, 1, 2, 1, 4, 4, 2, 1, 4, 4, 2, 1, 2, 1, 2, 1]
    """
    # FIXME: Implement this.


def curry_one(func):
    """
    Curry a binary function.

    This converts a binary function to a unary function. Calling the result
    binds the first argument, return a function of only the second argument.

    >>> curry_one(pow)(2)(10)
    1024

    >>> import math, operator

    >>> f = curry_one(operator.sub)
    >>> subtract_from_three = f(3)
    >>> subtract_from_three(5)
    -2
    >>> subtract_from_three(1)
    2

    >>> g = curry_one(math.perm)
    >>> g(10)(3)
    720
    >>> g(10)(10)
    3628800
    >>> g(10)(11)
    0
    """
    # FIXME: Implement this.


def curry_one_alt(func):
    """
    Curry a binary function. Alternative implementation.

    This achieves an effect like that of curry_one, but they are implemented
    differently. One of them uses functools.partial and the other does not.

    >>> curry_one_alt(pow)(2)(10)
    1024

    >>> import math, operator

    >>> f = curry_one_alt(operator.sub)
    >>> subtract_from_three = f(3)
    >>> subtract_from_three(5)
    -2
    >>> subtract_from_three(1)
    2

    >>> g = curry_one_alt(math.perm)
    >>> g(10)(3)
    720
    >>> g(10)(10)
    3628800
    >>> g(10)(11)
    0
    """
    # FIXME: Implement this.