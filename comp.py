"""Basic iteration with loops, generators, and comprehensions."""

from collections import defaultdict, deque
from collections.abc import Iterable, Iterator


def generate_singletons_loop(n: int) -> Iterator[set[int]]:
    """
    Yield singleton sets of 1 up to n, inclusive, using a loop.

    >>> next(generate_singletons_loop(0))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> [list(generate_singletons_loop(n)) for n in range(5)]
    [[], [{1}], [{1}, {2}], [{1}, {2}, {3}], [{1}, {2}, {3}, {4}]]
    """
    raise NotImplementedError


def generate_singletons_comp(n: int) -> Iterator[set[int]]:
    """
    Yield singleton sets of 1 up to n, inclusive, using a comprehension.

    The implementation of this function is a single return statement.

    >>> next(generate_singletons_loop(0))
    Traceback (most recent call last):
      ...
    StopIteration
    >>> [list(generate_singletons_loop(n)) for n in range(5)]
    [[], [{1}], [{1}, {2}], [{1}, {2}, {3}], [{1}, {2}, {3}, {4}]]
    """
    raise NotImplementedError


def list_squares_loop(n: int) -> list[int]:
    """
    Make a list of squares from 1 to n, inclusive, using a loop.

    >>> list_squares_loop(0)
    []
    >>> list_squares_loop(1)
    [1]
    >>> list_squares_loop(10)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    >>> list_squares_loop(14)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
    >>> list_squares_loop(-1)
    []
    """
    raise NotImplementedError


def list_squares_map(n: int) -> list[int]:
    """
    Make a list of squares from 1 to n, inclusive, using the map builtin.

    The implementation of this function is a single return statement.

    >>> list_squares_map(0)
    []
    >>> list_squares_map(1)
    [1]
    >>> list_squares_map(10)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    >>> list_squares_map(14)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
    >>> list_squares_map(-1)
    []
    """
    raise NotImplementedError


def list_squares_comp(n: int) -> list[int]:
    """
    Make a list of squares from 1 to n, inclusive, using a comprehension.

    The implementation of this function is a single return statement.

    >>> list_squares_comp(0)
    []
    >>> list_squares_comp(1)
    [1]
    >>> list_squares_comp(10)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    >>> list_squares_comp(14)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
    >>> list_squares_comp(-1)
    []
    """
    raise NotImplementedError


def list_squares_comp_alt(n: int) -> list[int]:
    """
    Make a list of squares with another kind of comprehension.

    This is an alternative implementation of list_squares_comp(). This
    implementation is also a single return statement, but it does not use the
    same kind of comprehension. Because list comprehensions exist, this is not
    typically a reasonable technique. There are two reasons to know about this
    technique: so you can notice and avoid using it by accident, and because
    some variations on it are both reasonable and useful.

    >>> list_squares_comp_alt(0)
    []
    >>> list_squares_comp_alt(1)
    [1]
    >>> list_squares_comp_alt(10)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    >>> list_squares_comp_alt(14)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
    >>> list_squares_comp_alt(-1)
    []
    """
    raise NotImplementedError


def tuple_squares_comp(n: int) -> tuple[int, ...]:
    """
    Make a tuple of squares from 1 to n, inclusive, using a comprehension.

    The implementation of this function is a single return statement.

    >>> tuple_squares_comp(0)
    ()
    >>> tuple_squares_comp(1)
    (1,)
    >>> tuple_squares_comp(10)
    (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)
    >>> tuple_squares_comp(14)
    (1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196)
    >>> tuple_squares_comp(-1)
    ()
    """
    raise NotImplementedError


def generate_sevenless_loop(n: int) -> Iterator[int]:
    """
    Yield positive integers up to n, indivisible by 7, using a loop.

    >>> it = generate_sevenless_loop(14)
    >>> next(it)
    1
    >>> next(it)
    2
    >>> list(it)
    [3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
    >>> list(generate_sevenless_loop(15))
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15]
    """
    raise NotImplementedError


def generate_sevenless_comp(n: int) -> Iterator[int]:
    """
    Yield positive integers up to n, indivisible by 7, using a comprehension.

    The implementation of this function is a single return statement.

    >>> it = generate_sevenless_comp(14)
    >>> next(it)
    1
    >>> next(it)
    2
    >>> list(it)
    [3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
    >>> list(generate_sevenless_comp(15))
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15]
    """
    raise NotImplementedError


def list_sevenless_squares_loop(n: int) -> list[int]:
    """
    Make a list of squares that have no factor of 7, using a loop.

    Like every other function in this module, this implementation does not call
    anything else in this project, not even other functions in this module.

    >>> list_sevenless_squares_loop(16)
    [1, 4, 9, 16, 25, 36, 64, 81, 100, 121, 144, 169, 225, 256]
    >>> list_sevenless_squares_loop(17)
    [1, 4, 9, 16, 25, 36, 64, 81, 100, 121, 144, 169, 225, 256, 289]
    """
    raise NotImplementedError


def list_sevenless_squares_comp(n: int) -> list[int]:
    """
    Make a list of squares that have no factor of 7, using a comprehension.

    The implementation of this function is a single return statement. It does
    not call anything else in this project.

    >>> list_sevenless_squares_comp(16)
    [1, 4, 9, 16, 25, 36, 64, 81, 100, 121, 144, 169, 225, 256]
    >>> list_sevenless_squares_comp(17)
    [1, 4, 9, 16, 25, 36, 64, 81, 100, 121, 144, 169, 225, 256, 289]
    """
    raise NotImplementedError


def deque_sevenless_squares_comp(n: int) -> deque[int]:
    """
    Make a list of squares that have no factor of 7, using a comprehension.

    The implementation of this function is a single return statement. It does
    not create an intermediate list, nor call anything else in this project.

    >>> deque_sevenless_squares_comp(16)
    deque([1, 4, 9, 16, 25, 36, 64, 81, 100, 121, 144, 169, 225, 256])
    >>> deque_sevenless_squares_comp(17)
    deque([1, 4, 9, 16, 25, 36, 64, 81, 100, 121, 144, 169, 225, 256, 289])
    """
    raise NotImplementedError


def set_cubes_loop(n: int) -> set[int]:
    """
    Make a set of cubes from 1 to n, inclusive, using a loop.

    >>> set_cubes_loop(0)
    set()
    >>> set_cubes_loop(1)
    {1}
    >>> set_cubes_loop(10) == {1, 8, 27, 64, 125, 216, 343, 512, 729, 1000}
    True
    >>> expected = {1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744}
    >>> set_cubes_loop(14) == expected
    True
    >>> set_cubes_loop(-1)
    set()
    """
    raise NotImplementedError


def set_cubes_map(n: int) -> set[int]:
    """
    Make a set of cubes from 1 to n, inclusive, using the map builtin.

    The implementation of this function is a single return statement.

    >>> set_cubes_map(0)
    set()
    >>> set_cubes_map(1)
    {1}
    >>> set_cubes_map(10) == {1, 8, 27, 64, 125, 216, 343, 512, 729, 1000}
    True
    >>> expected = {1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744}
    >>> set_cubes_map(14) == expected
    True
    >>> set_cubes_map(-1)
    set()
    """
    raise NotImplementedError


def set_cubes_comp(n: int) -> set[int]:
    """
    Make a set of cubes from 1 to n, inclusive, using a comprehension.

    The implementation of this function is a single return statement.

    >>> set_cubes_comp(0)
    set()
    >>> set_cubes_comp(1)
    {1}
    >>> set_cubes_comp(10) == {1, 8, 27, 64, 125, 216, 343, 512, 729, 1000}
    True
    >>> expected = {1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744}
    >>> set_cubes_comp(14) == expected
    True
    >>> set_cubes_comp(-1)
    set()
    """
    raise NotImplementedError


def frozenset_cubes_comp(n: int) -> frozenset[int]:
    """
    Make a frozenset of cubes from 1 to n, inclusive, using a comprehension.

    The implementation of this function is a single return statement. It does
    not (at least not explicitly) create an intermediate set.

    >>> frozenset_cubes_comp(0)
    frozenset()
    >>> frozenset_cubes_comp(1)
    frozenset({1})
    >>> expected = frozenset({1, 8, 27, 64, 125, 216, 343, 512, 729, 1000})
    >>> actual = frozenset_cubes_comp(10)
    >>> isinstance(actual, frozenset) and actual == expected
    True
    >>> expected = frozenset({1, 8, 27, 64, 125, 216, 343, 512, 729, 1000,
    ...                       1331, 1728, 2197, 2744})
    >>> actual = frozenset_cubes_comp(14)
    >>> isinstance(actual, frozenset) and actual == expected
    True
    >>> frozenset_cubes_comp(-1)
    frozenset()
    """
    raise NotImplementedError


def dict_words_loop(words: Iterable[str]) -> dict[str, int]:
    """
    Make a dictionary mapping words to their lengths using a loop.

    >>> dict_words_loop(['cat', 'ox', 'human', 'raven', 'crow'])
    {'cat': 3, 'ox': 2, 'human': 5, 'raven': 5, 'crow': 4}
    """
    raise NotImplementedError


def dict_words_map(words: Iterable[str]) -> dict[str, int]:
    """
    Make a dictionary mapping words to their lengths using the map builtin.

    The implementation of this function is a single return statement.

    Hint: In what ways does the dict type support being constructed?

    >>> dict_words_map(['cat', 'ox', 'human', 'raven', 'crow'])
    {'cat': 3, 'ox': 2, 'human': 5, 'raven': 5, 'crow': 4}
    """
    raise NotImplementedError


def dict_words_comp(words: Iterable[str]) -> dict[str, int]:
    """
    Make a dictionary mapping words to their lengths using a comprehension.

    The implementation of this function is a single return statement.

    >>> dict_words_comp(['cat', 'ox', 'human', 'raven', 'crow'])
    {'cat': 3, 'ox': 2, 'human': 5, 'raven': 5, 'crow': 4}
    """
    raise NotImplementedError


def dict_words_comp_alt(words: Iterable[str]) -> dict[str, int]:
    """
    Make a word-lengths dictionary using a different kind of comprehension.

    This is an alternative implementation of dict_words_comp(). This
    implementation is also a single return statement, but it does not use the
    same kind of comprehension. dict_words_comp() is how this actually should
    be done, while this alternative approach resembles dict_words_map(), though
    it does not make any use of the map builtin. Because dict comprehensions
    exist, this is not typically a reasonable technique. But it is useful to
    know about, because some variations on it are reasonable and useful.

    >>> dict_words_comp_alt(['cat', 'ox', 'human', 'raven', 'crow'])
    {'cat': 3, 'ox': 2, 'human': 5, 'raven': 5, 'crow': 4}
    """
    raise NotImplementedError


def defaultdict_words_comp(words: Iterable[str]) -> defaultdict[str, int | None]:
    """
    Make a word-lengths defaultdict that associates None with unknown words.

    The implementation of this function is a single return statement. Sometimes
    it may be justifiable to create a dict first, because in some cases, that
    may increase code readability. But this does not do that.

    >>> d = defaultdict_words_comp(['cat', 'ox', 'human', 'raven', 'crow'])
    >>> d  # doctest: +ELLIPSIS
    defaultdict(..., {'cat': 3, 'ox': 2, 'human': 5, 'raven': 5, 'crow': 4})
    >>> d['raven']
    5
    >>> d['eagle'] is None
    True
    """
    raise NotImplementedError


def matrix_indices_loop(m: int, n: int) -> Iterator[tuple[int, int]]:
    """
    Yield 1-based index pairs for an m-by-n matrix, using nested loops.

    >>> it = matrix_indices_loop(3, 4)
    >>> next(it)
    (1, 1)
    >>> next(it)
    (1, 2)
    >>> next(it)
    (1, 3)
    >>> list(it)
    [(1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4)]
    """
    raise NotImplementedError


def matrix_indices_comp(m: int, n: int) -> Iterator[tuple[int, int]]:
    """
    Yield 1-based index pairs for an m-by-n matrix, using a comprehension.

    The implementation of this function is a single return statement.

    >>> it = matrix_indices_comp(3, 4)
    >>> next(it)
    (1, 1)
    >>> next(it)
    (1, 2)
    >>> next(it)
    (1, 3)
    >>> list(it)
    [(1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4)]
    """
    raise NotImplementedError


def matrix_indices_product(m: int, n: int) -> Iterator[tuple[int, int]]:
    """
    Yield 1-based index pairs for an m-by-n matrix, using itertools.product.

    This uses no loops and no comprehensions.

    >>> it = matrix_indices_product(3, 4)
    >>> next(it)
    (1, 1)
    >>> next(it)
    (1, 2)
    >>> next(it)
    (1, 3)
    >>> list(it)
    [(1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4)]
    """
    raise NotImplementedError


def upper_matrix_indices_loop(n: int) -> Iterator[tuple[int, int]]:
    """
    Yield n-by-n index pairs above the main diagonal, using nested loops.

    >>> it = upper_matrix_indices_loop(5)
    >>> next(it)
    (1, 2)
    >>> next(it)
    (1, 3)
    >>> list(it)
    [(1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
    """
    raise NotImplementedError


def upper_matrix_indices_comp(n: int) -> Iterator[tuple[int, int]]:
    """
    Yield n-by-n index pairs above the main diagonal, using a comprehension.

    The implementation of this function is a single return statement.

    >>> it = upper_matrix_indices_comp(5)
    >>> next(it)
    (1, 2)
    >>> next(it)
    (1, 3)
    >>> list(it)
    [(1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
    """
    raise NotImplementedError


def upper_matrix_indices_combinatoric(n: int) -> Iterator[tuple[int, int]]:
    """
    Yield n-by-n index pairs above the main diagonal, using itertools.

    This uses no loops or comprehensions. The itertools module offer several
    combinatoric iterators, including product, which should not be used here,
    and others, one of which should be used here.

    >>> it = upper_matrix_indices_combinatoric(5)
    >>> next(it)
    (1, 2)
    >>> next(it)
    (1, 3)
    >>> list(it)
    [(1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
    """
    raise NotImplementedError
