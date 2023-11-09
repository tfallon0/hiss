def invert(d: dict) -> dict:
    """Invert the dictionary.

    If the dict is not injective an arbitrary choice is made.

    >>> invert({"one": 1, "pi": 3, "tau": 6.283185307179586})
    {1: 'one', 3: 'pi', 6.283185307179586: 'tau'}
    >>> invert({})
    {}
    """
    inv_d = {}
    for key, value in d.items():
        inv_d[value] = key
    return inv_d


def adjacency(edges: list[tuple[str,str]]) -> dict[str,set[str]]:
    """Make an adjacency list.

    >>> adjacency([])
    {}
    """
    # TODO: add more tests and implementaiton, setup vscode test-runner
