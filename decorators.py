"""Various decorators."""

# ruff: noqa: D401


def call(func):
    """
    Decorator to immediately call a function when defining it.

    >>> @call
    ... def hello():
    ...     print('Hello, world!')
    Hello, world!
    >>> hello()
    Hello, world!
    """
    # FIXME: Implement this.


def twice_unary(func):
    """
    Decorator to call a unary function two times.

    The result of the second call is returned.

    >>> twice_unary(print)('Hello!')
    Hello!
    Hello!
    >>> a = [5]
    >>> twice_unary(a.append)(10)
    >>> a
    [5, 10, 10]
    >>> twice_unary(a.pop)(0)  # Remove from front twice.
    10
    >>> a
    [10]

    >>> def square(x):
    ...     print(f'Squaring {x}.')
    ...     return x**2
    >>> square = twice_unary(square)
    >>> square(3)
    Squaring 3.
    Squaring 3.
    9

    >>> @twice_unary
    ... def cube(x):
    ...     print(f'Cubing {x}.')
    ...     return x**3
    >>> cube(3)
    Cubing 3.
    Cubing 3.
    27

    >>> square.__name__, cube.__name__
    ('square', 'cube')
    """
    # FIXME: Implement this.


def peek_unary(func):
    """
    Decorator to print calls and returns of a unary function.

    >>> from fractions import Fraction

    >>> @peek_unary
    ... def square(x):
    ...     print(f'Squaring {x}.')
    ...     return x**2
    >>> s = square(Fraction(1, 3))
    square(Fraction(1, 3))
    Squaring 1/3.
    square(Fraction(1, 3)) -> Fraction(1, 9)
    >>> print(s)
    1/9
    >>> square.__name__
    'square'

    >>> peek_unary(print)('Hello.')
    print('Hello.')
    Hello.
    print('Hello.') -> None

    >>> @peek_unary
    ... def factorial(n):
    ...     return 1 if n == 0 else n * factorial(n - 1)
    >>> factorial(5)
    factorial(5)
    factorial(4)
    factorial(3)
    factorial(2)
    factorial(1)
    factorial(0)
    factorial(0) -> 1
    factorial(1) -> 1
    factorial(2) -> 2
    factorial(3) -> 6
    factorial(4) -> 24
    factorial(5) -> 120
    120

    >>> @peek_unary
    ... def append_foo(target):
    ...     target.append('foo')
    >>> a = []
    >>> append_foo(a)
    append_foo([])
    append_foo([]) -> None
    >>> a
    ['foo']
    """
    # FIXME: Implement this.


def twice(func):
    R"""
    Decorator to call an arbitrary function two times.

    >>> a = [5]
    >>> twice(a.append)(10)
    >>> a
    [5, 10, 10]
    >>> twice(a.pop)(0)  # Remove from front twice.
    10
    >>> a
    [10]

    >>> @twice
    ... def show_pair(x, y):
    ...     print(f'{x=}, {y=}')
    >>> show_pair('foo', 'bar')
    x='foo', y='bar'
    x='foo', y='bar'
    >>> show_pair.__name__
    'show_pair'

    >>> twice(print)(10, 20, 30, sep='; ', end='.\n')
    10; 20; 30.
    10; 20; 30.
    >>> show_pair(x=10, y=20)
    x=10, y=20
    x=10, y=20
    >>> show_pair(11, y=22)
    x=11, y=22
    x=11, y=22
    """
    # FIXME: Implement this.


def repeat(count):
    R"""
    Parameterized decorator to all a function a given number of times.

    This is a parameterized decorator, also known as a decorator factory. It is
    called with the number of repetitions, and it returns a decorator like
    the twice decorator above, but for that number of times.

    The return value from the last call is returned. If the count is zero, then
    None is returned.

    >>> repeat(3)(print)("Hello", end='!\n')
    Hello!
    Hello!
    Hello!
    >>> a = [10, 20, 30, 40, 50]
    >>> repeat(3)(a.pop)()
    30
    >>> a
    [10, 20]

    >>> @repeat(3)
    ... def f():
    ...     a.append(a[-1]**2)
    ...     return a[-1]
    >>> f()
    25600000000
    >>> a
    [10, 20, 400, 160000, 25600000000]

    >>> repeat(1)(print)('Hello.')
    Hello.
    >>> repeat(0)(lambda: 42)() is None
    True
    """
    # FIXME: Implement this.


def subscribe(collection):
    """
    Parameterized decorator to add a function to a collection when defining it.

    Lists, sets, and dictionaries are supported, as are any objects that
    support the operations of lists, sets, or dictionaries. It is acceptable to
    assume that no unsuitable collections will ever be used.

    >>> a = []
    >>> s = set()
    >>> d = {}
    >>> @subscribe(a)
    ... @subscribe(s)
    ... @subscribe(d)
    ... def square(n):
    ...     return n**2
    >>> a  # doctest: +ELLIPSIS
    [<function square at 0x...>]
    >>> s  # doctest: +ELLIPSIS
    {<function square at 0x...>}
    >>> d  # doctest: +ELLIPSIS
    {'square': <function square at 0x...>}
    >>> a[0] is list(s)[0] is d['square'] is square
    True
    >>>
    """
    # FIXME: Implement this.


def peek(func):
    R"""
    Decorator to print calls and returns of a function of any signature.

    This is like peek_unary, but the function may take arbitrary positional and
    keyword arguments.

    >>> from fractions import Fraction
    >>> @peek
    ... def square(x):
    ...     print(f'Squaring {x}.')
    ...     return x**2
    >>> _ = square(Fraction(1, 3))
    square(Fraction(1, 3))
    Squaring 1/3.
    square(Fraction(1, 3)) -> Fraction(1, 9)
    >>> _ = square(x=Fraction(1, 3))
    square(x=Fraction(1, 3))
    Squaring 1/3.
    square(x=Fraction(1, 3)) -> Fraction(1, 9)

    >>> @peek
    ... def hypot_squared(*sides):  # TODO: Make hypot_squared a one-liner.
    ...     acc = 0
    ...     for side in sides:
    ...         acc += side**2
    ...     return acc
    >>> hypot_squared()
    hypot_squared()
    hypot_squared() -> 0
    0
    >>> hypot_squared(2, 4, 3)
    hypot_squared(2, 4, 3)
    hypot_squared(2, 4, 3) -> 29
    29

    >>> import math, operator
    >>> @peek
    ... def fold(*xs, op):
    ...     '''Sort of like functools.reduce, but underwhelming.'''
    ...     return xs[0] if len(xs) == 1 else op(fold(*xs[:-1], op=op), xs[-1])
    >>> fold(2, 14, 3, op=operator.mul) == math.prod([2, 14, 3]) == 84
    fold(2, 14, 3, op=<built-in function mul>)
    fold(2, 14, op=<built-in function mul>)
    fold(2, op=<built-in function mul>)
    fold(2, op=<built-in function mul>) -> 2
    fold(2, 14, op=<built-in function mul>) -> 28
    fold(2, 14, 3, op=<built-in function mul>) -> 84
    True
    >>> fold.__name__, fold.__doc__
    ('fold', 'Sort of like functools.reduce, but underwhelming.')
    >>> fold.__wrapped__(7, 5, op=operator.mul)  # Make sure to understand why.
    fold(7, op=<built-in function mul>)
    fold(7, op=<built-in function mul>) -> 7
    35

    >>> peek(print)(10, 20, 30, sep='; ', end='.\n')
    print(10, 20, 30, sep='; ', end='.\n')
    10; 20; 30.
    print(10, 20, 30, sep='; ', end='.\n') -> None
    """
    # FIXME: Implement this.


def timed(func):
    """
    Decorator to print the elapsed time of a function, even when it fails.

    This prints the elapsed time in seconds for each call of the decorated
    function, including when the function fails with an exception. Information
    about arguments and return values is not printed. This is for simplicity,
    but it is also sometimes desired, because in some cases the representations
    of one or more of those objects could be very long or expensive to compute.

    The function's duration is timed with time.perf_counter. The output doesn't
    include literal ellipses, which are doctest wildcards for the test runner.
    Duration is reported in a fixed precision of six digits after the decimal
    point. (The doctests below may not verify requirements in this paragraph.)

    >>> import datetime, time

    >>> @timed
    ... def wait():
    ...     time.sleep(0.125)
    >>> wait()  # doctest: +ELLIPSIS
    wait: took 0.12... s

    >>> @timed
    ... def fail_wait(message):
    ...     time.sleep(0.225)
    ...     raise ValueError(message)
    >>> try:  # doctest: +ELLIPSIS
    ...     fail_wait(message='refusing to say hello world')
    ... except ValueError as error:
    ...     print(error)
    fail_wait: took 0.22... s
    refusing to say hello world

    >>> @timed
    ... def wait_for(delta):
    ...     time.sleep(delta.total_seconds())
    ...     return delta  # Return the time delta passed in, for some reason.
    >>> wait_for(datetime.timedelta(milliseconds=155))  # doctest: +ELLIPSIS
    wait_for: took 0.15... s
    datetime.timedelta(microseconds=155000)
    >>> wait_for.__name__
    'wait_for'

    >>> @timed
    ... def have_patience():
    ...     time.sleep(datetime.timedelta(days=18_250).total_seconds() + 0.55)
    ...     print('It has been about fifty years.')
    >>> have_patience()  # TODO: Run this, somehow.  # doctest: +ELLIPSIS +SKIP
    It has been about fifty years.
    have_patience: took 1576800000.5... s
    """
    # FIXME: Implement this.


def bad_pi(func):
    """
    Decorator that causes a function to use the fraction 22/7 for math.pi.

    Behavior of functions called before or after the decorated function must be
    unaffected. However, correct behavior is not guaranteed if other threads
    access math.pi, which on some Python implementations could be a data race,
    and which on any implementation might give them the wrong value of pi, too.

    For simplicity, math.tau is unaffected, but it is also not used in any way.
    The better value of pi is not hard-coded except in the tests, nor computed.

    >>> @bad_pi
    ... def circle_area(radius):
    ...     return math.pi * radius**2
    >>> math.pi
    3.141592653589793
    >>> circle_area(10), circle_area(radius=10)
    (Fraction(2200, 7), Fraction(2200, 7))
    >>> math.pi, circle_area.__wrapped__(10)
    (3.141592653589793, 314.1592653589793)

    >>> @bad_pi
    ... def unit_pizza_slice_area(slice_count):
    ...     return math.pi / slice_count
    >>> unit_pizza_slice_area(slice_count=2)  # Acceptable. We "eta" pizza.
    Fraction(11, 7)
    >>> unit_pizza_slice_area(slice_count=1j)  # Acceptable.
    -3.142857142857143j
    >>> unit_pizza_slice_area(slice_count=0)  # Unacceptable.
    Traceback (most recent call last):
      ...
    ZeroDivisionError: Fraction(1, 0)
    >>> math.pi
    3.141592653589793

    >>> @bad_pi
    ... def pi_times(multiplier):
    ...     return 0 if multiplier == 0 else pi_times(multiplier - 1) + math.pi
    >>> pi_times(10), math.pi
    (Fraction(220, 7), 3.141592653589793)
    """
    # FIXME: Implement this.


def monkeypatch(target, **attributes):
    """
    Decorator factory for setting attributes on a target object temporarily.

    When a function is decorated using an expression that is a call to this
    parameterized decorator, it causes the decorated function to patch in the
    attributes passed as keyword arguments when called, and to unpatch them
    when control exits it (either by returning or due to an exception).

    Attributes are unpatched in the reverse of the order in which they are
    patched. Although an exception from the decorated function must not prevent
    unpatching, if an exception is raised while attempting to unpatch an
    attribute then any remaining still-patched attributes won't be unpatched.
    However, if patching an attribute fails, then any attributes already
    patched will still be unpatched (and still in reverse order).

    Functions decorated with @monkeypatch(...) may themselves be recursive, but
    recursion is not used in any way in the implementation of monkeypatch.
    Decorating a function @monkeypatch(target, **attributes) augments its time
    and space complexity by O(attributes), and never more.

    For simplicity, it is assumed that all attributes to patch already exist.
    However, if that turns out not to be the case, then the above requirements
    still hold with respect to any resulting exceptions.

    TODO: Eventually implement setting and deleting formerly absent attributes.

    >>> @monkeypatch(math, pi=Fraction(22, 7), tau=Fraction(44, 7))
    ... def circle_area(radius):
    ...     by_pi = math.pi * radius**2
    ...     by_tau = math.tau * radius**2 / 2
    ...     assert by_pi == by_tau
    ...     return by_pi
    >>> math.pi, math.tau
    (3.141592653589793, 6.283185307179586)
    >>> circle_area(10)
    Fraction(2200, 7)
    >>> math.pi, math.tau
    (3.141592653589793, 6.283185307179586)

    >>> @monkeypatch(math, pi=Fraction(22, 7), tau=Fraction(44, 7))
    ... def raise_error():
    ...     raise ValueError('changing the value of pi (and tau) is absurd')
    >>> raise_error()
    Traceback (most recent call last):
      ...
    ValueError: changing the value of pi (and tau) is absurd
    >>> math.pi, math.tau
    (3.141592653589793, 6.283185307179586)

    >>> import builtins
    >>> @monkeypatch(builtins, input=lambda *args: 'Countess von Willdebrandt')
    ... def interactive_hello():
    ...     name = input('What is your name? ')
    ...     print(f'Hello, {name}!')
    >>> input
    <built-in function input>
    >>> interactive_hello()
    Hello, Countess von Willdebrandt!
    >>> input
    <built-in function input>

    >>> from types import SimpleNamespace
    >>> ns = SimpleNamespace(w=5, x=10, y=20, z=30)
    >>> @monkeypatch(ns, w=2, x=11, z=33)
    ... def f():
    ...     print(ns)
    >>> ns
    namespace(w=5, x=10, y=20, z=30)
    >>> f()
    namespace(w=2, x=11, y=20, z=33)
    >>> @monkeypatch(ns, w=2, x=11, y=22, __class__=int, z=33)
    ... def g():
    ...     print(ns)
    >>> g()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: __class__ assignment only supported for mutable types or ...
    >>> ns
    namespace(w=5, x=10, y=20, z=30)
    """
    # FIXME: Implement this.


def mock_time(func):
    """
    Decorator to cause time.sleep to only simulate the passage of time.

    Adding this decorator to a function definition makes the function think its
    calls to time.sleep (and those due to functions it calls) have taken the
    amount of time, in seconds, passed to time.sleep, at least if the function
    uses time.perf_counter to check. But it is a lie. Instead, time.sleep and
    time.perf_counter conspire to lie to it.

    It is dangerous to mock time. The lie is told to functions called by the
    decorated function that themselves use time.sleep and time.perf_counter, as
    well as affecting any code running on another thread between when the
    decorated function is called and when it returns. In particular, if
    time.sleep is used to wait between performing actions over a network that
    must be rate limited, such as requests to a REST API, then the host may
    temporarily (or in some cases permanently) block the host.

    Therefore, as in other mocking scenarios, it's worth considering dependency
    injection as an alternative to monkey-patching. In dependency injection, a
    function that sleeps and checks time would receive sleep and perf_counter
    implementations when called, or be a method of a class instantiated with
    them. Then, in testing, it can use mock implementations without disrupting
    other parts of the system. This decorator is for when that can't be done.

    The decorated function does not lose track of actually elapsed time. All
    discrepancies are due to time.sleep. When time actually passes, such as due
    to a computation, that is reflected in the passage of time as shown by
    time.perf_counter.

    >>> import datetime, time
    >>> epsilon = 0.005

    >>> @mock_time
    ... def sleep_ten(throw):
    ...     start = time.perf_counter()
    ...     time.sleep(10)
    ...     elapsed = time.perf_counter() - start
    ...     if not throw:
    ...         return elapsed
    ...     ex = ValueError()
    ...     ex.elapsed = elapsed
    ...     raise ex

    >>> start = time.perf_counter()
    >>> fake1 = sleep_ten(False)
    >>> real1 = time.perf_counter() - start
    >>> abs(fake1 - 10) < epsilon
    True
    >>> abs(real1) < epsilon
    True

    >>> start = time.perf_counter()
    >>> try:
    ...     sleep_ten(True)
    ... except ValueError as ex:
    ...     fake2 = ex.elapsed
    >>> real2 = time.perf_counter() - start
    >>> abs(fake2 - 10) < epsilon
    True
    >>> abs(real2) < epsilon
    True

    >>> @mock_time
    ... def heterogeneous_wait(spin_time, sleep_time, reps):
    ...     full_start = time.perf_counter()
    ...     for _ in range(reps):
    ...         spin_start = time.perf_counter()
    ...         while time.perf_counter() - spin_start < spin_time:
    ...             pass
    ...         time.sleep(sleep_time)
    ...     return time.perf_counter() - full_start
    >>> start = time.perf_counter()
    >>> fake3 = heterogeneous_wait(spin_time=0.1, sleep_time=1000, reps=3)
    >>> real3 = time.perf_counter() - start
    >>> abs(fake3 - 3000.3) < epsilon
    True
    >>> abs(real3 - 0.3) < epsilon
    True
    """
    # FIXME: Implement this.
