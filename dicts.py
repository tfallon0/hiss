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

def al_sorter(adj_list: dict[str,set[str]]) -> dict[str,list[str]]:
    sl = {}
    for vertex, neighbors in adj_list.items():
        sl[vertex] = sorted(neighbors)
    return sl

def adjacency(edges: list[tuple[str,str]]) -> dict[str,set[str]]:
    """Make an adjacency list.

    >>> adjacency([])
    {}
    >>> adjacency([('a', 'A')])
    {'a': {'A'}}
    >>> adjacency([('a','b'), ('b','c'), ('c','a')])
    {'a': {'b'}, 'b': {'c'}, 'c': {'a'}}
    >>> al_sorter(adjacency([('a','c'), ('a','b'), ('b','c'), ('c','a')]))
    {'a': ['b', 'c'], 'b': ['c'], 'c': ['a']}
    """
    adj_list = {}
    for edge in edges:
        if edge[0] in adj_list:
            adj_list[edge[0]] = adj_list[edge[0]] | {edge[1]}
        else:
            adj_list[edge[0]] = {edge[1]}
    return adj_list
