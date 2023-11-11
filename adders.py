"""Higher-order functions for adding."""


def make_adder(left_addend):
    """
    Make a function that adds left_addend and the value it is called with.

    The created function does not give access to left_addend via its public
    interface.

    >>> f = make_adder(3)
    >>> f(7)
    10
    >>> f(-2)
    1
    >>> make_adder('foo')('bar')
    'foobar'
    >>> make_adder([10, 20, 30])([40, 50])
    [10, 20, 30, 40, 50]
    """
    def adder(right_addend):
        return left_addend + right_addend

    return adder


def make_adder_alt(left_addend):
    """
    Make a function that adds left_addend and the value it is called with.

    This is an alternative implementation of make_adder, satisfying all the
    same outward requirements. One uses a lambda and the other does not.

    >>> f = make_adder_alt(3)
    >>> f(7)
    10
    >>> f(-2)
    1
    >>> make_adder_alt('foo')('bar')
    'foobar'
    >>> make_adder_alt([10, 20, 30])([40, 50])
    [10, 20, 30, 40, 50]
    """
    return lambda right_addend: left_addend + right_addend


def make_adder_intro(left_addend):
    """
    Make an adder like in make_adder, but introspective.

    This differs from the above functions because the adder it returns offers
    access to the stored left addend as its left_addend attribute. This
    attribute can be changed; changing it affects the behavior.

    >>> f = make_adder_intro(3)
    >>> f(7)
    10
    >>> f(-2)
    1
    >>> make_adder_intro('foo')('bar')
    'foobar'
    >>> make_adder_intro([10, 20, 30])([40, 50])
    [10, 20, 30, 40, 50]

    >>> f.left_addend
    3
    >>> f.left_addend = 10
    >>> f(7)
    17
    """
    def adder(right_addend):
        return adder.left_addend + right_addend

    adder.left_addend = left_addend
    return adder
