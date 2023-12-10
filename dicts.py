"""Functions dealing with dictionaries."""

import graphviz
from collections.abc import Iterable


def invert(d: dict) -> dict:
    """
    Invert the dictionary.

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


def distinct(values: Iterable, *, key=None) -> list:
    """
    Creates a list with every value of the values, but without repeating anything

    >>> distinct([])
    []
    >>> distinct([3,6,123,1,543,1,32,1,3,3,12])
    [3, 6, 123, 1, 543, 32, 12]
    >>> distinct([ {1,2}, {1}, {2,2,1}, {2}, {1,1,1}], key=frozenset)
    [{1, 2}, {1}, {2}]
    """
    if key is None:
        key = lambda x: x

    val_list = []
    val_set = set()

    for val in values:
        if key(val) not in val_set:
            val_set.add(key(val))
            val_list.append(val)
    return val_list


def sorted_al(adj_list: dict[str,set[str]]) -> dict[str,list[str]]:
    """
    Sort an adjacency list.

    This takes an adjacency list represented as a dictionary whose keys are
    vertices and whose values are sets of their outward neighbors, and returns
    a new, similar dictionary whose values are instead sorted lists.
    """
    sl = {}
    for vertex, neighbors in adj_list.items():
        sl[vertex] = sorted(neighbors)
    return sl


def adjacency(edges: list[tuple[str,str]], vertices: Iterable[str] = ()) -> dict[str,set[str]]:
    """
    Make an adjacency list.

    This takes edges expressed as pairs of source and destination vertices, and
    return an adjacency list as a dictionary whose keys are vertices and whose
    values are sets of their outward neighbors.

    >>> adjacency([])
    {}
    >>> adjacency([('a', 'A')])
    {'a': {'A'}}
    >>> adjacency([('a','b'), ('b','c'), ('c','a')])
    {'a': {'b'}, 'b': {'c'}, 'c': {'a'}}
    >>> sorted_al(adjacency([('a','c'), ('a','b'), ('b','c'), ('c','a')]))
    {'a': ['b', 'c'], 'b': ['c'], 'c': ['a']}
    >>> adjacency([('a','b'), ('b','c'), ('c','a')], ('d','a','e'))
    {'a': {'b'}, 'b': {'c'}, 'c': {'a'}, 'd': set(), 'e': set()}
    """
    adj_list = {}
    for source, dest in edges:
        if source in adj_list:
            adj_list[source].add(dest)
        else:
            adj_list[source] = {dest}
    for vertex in vertices:
        if vertex not in adj_list:
            adj_list[vertex] = set()
    return adj_list


# TODO: The parameter annotation is too narrow. Use abstract types instead.
def draw_graph(adj_list: dict[str,set[str]]) -> graphviz.Digraph:
    R"""
    Draw a directed graph.

    >>> graph = draw_graph({'a': {'b', 'c'}, 'b': {'c'}, 'c': {'a'}})
    >>> str(graph) in {
    ...     'digraph {\n\ta -> b\n\ta -> c\n\tb -> c\n\tc -> a\n}\n',
    ...     'digraph {\n\ta -> c\n\ta -> b\n\tb -> c\n\tc -> a\n}\n',
    ... }
    True
    >>> print(draw_graph({1: {2}}))  # doctest: +NORMALIZE_WHITESPACE
    digraph {
        1 -> 2
    }
    """
    g = graphviz.Digraph()
    for source,targets in adj_list.items():
        for dest in targets:
            g.edge(str(source),str(dest))
    return g


def sorted_setoset(unsorted: set[frozenset]) -> list[list]:
    unsorted_list = []
    for collection in unsorted:
        unsorted_list.append(sorted(collection))
    return sorted(unsorted_list)


def components(edges: list[tuple[str,str]]) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list

    >>> components([])
    set()
    >>> sorted_setoset(components( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] ))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_list = []
    for a, b in edges:
        found = None
        for n, component in enumerate(comp_list):
            if a in component and b not in component:
                component.add(b)
                if found is None:
                    found = n
                else:
                    comp_list[found] |= component
                    del comp_list[n]
                    break
            elif a not in component and b in component:
                component.add(a)
                if found is None:
                    found = n
                else:
                    comp_list[found] |= component
                    del comp_list[n]
                    break
            elif a in component and b in component:
                found = n
                break
        if found is None:
            comp_list.append({a,b})
    comp_set = set()
    for component in comp_list:
        comp_set.add(frozenset(component))
    return comp_set


def components_d(edges: list[tuple[str,str]], vertices: Iterable[str] = ()) -> set[frozenset[str]]:
    """
    Identify the connected components from an edge list

    >>> components_d([])
    set()
    >>> sorted_setoset(components_d( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] ))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    return _setofsets(components_dict(edges, vertices))


def _setofsets(set_dict: dict[object,Iterable]) -> set:
    vals = set()
    for val in distinct(set_dict.values(), key=id):
        vals.add(frozenset(val))
    return vals


def _setofsets_alt(set_dict: dict[object,Iterable]) -> set:
    list_of_sets = distinct(set_dict.values(), key=id)
    return set(map(frozenset, list_of_sets))


def components_dict(edges: list[tuple[str,str]], vertices: Iterable[str] = ()) -> dict[str,list[str]]:
    """
    Identify the connected components from an edge list.

    Approximately uses the quickfind algorithm.

    >>> components_dict([])
    {}
    >>> sorted_setoset(_setofsets(components_dict( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] )))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for source, dest in edges:
        if source in comp_dict and dest in comp_dict:
            if comp_dict[source] is not comp_dict[dest]:
                (small,big) = (source,dest) if len(comp_dict[source]) < len(comp_dict[dest]) else (dest,source)
                comp_dict[big] += comp_dict[small]
                for elm in comp_dict[small]:
                    comp_dict[elm] = comp_dict[big]
        elif source in comp_dict:
            comp_dict[source].append(dest)
        elif dest in comp_dict:
            comp_dict[dest].append(source)
        else:
            comp_dict[source] = [source,dest]
            comp_dict[dest] = comp_dict[source]
    for vertex in vertices:
        if vertex not in comp_dict:
            comp_dict[vertex] = [vertex]
    return comp_dict


def components_dict_alt(edges: list[tuple[str,str]], vertices: Iterable[str] = ()) -> dict[str,list[str]]:
    """
    Identify the connected components from an edge list.

    uses the quickfind algorithm.

    O(m log(n))
    m = #edges
    n = #vertices

    >>> components_dict_alt([])
    {}
    >>> sorted_setoset(_setofsets(components_dict_alt( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] )))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for source, dest in edges:
        comp_dict[source] = [source]
        comp_dict[dest] = [dest]
    for vertex in vertices:
        comp_dict[vertex] = [vertex]

    for source, dest in edges:
        if comp_dict[source] is not comp_dict[dest]:
            (small,big) = (source,dest) if len(comp_dict[source]) < len(comp_dict[dest]) else (dest,source)
            comp_dict[big] += comp_dict[small]
            for elm in comp_dict[small]:
                comp_dict[elm] = comp_dict[big]
    return comp_dict


#FIXME: Actually implement classic quickfind
def components_dict_alt2(edges: list[tuple[str,str]], vertices: Iterable[str] = ()) -> dict[str,list[str]]:
    """
    Identify the connected components from an edge list.

    uses the classic quickfind algorithm.

    >>> components_dict_alt2([])
    {}
    >>> sorted_setoset(_setofsets(components_dict_alt2( [ ('1','2'), ('1','3'), ('4','5'), ('5','6'), ('3','7'), ('2','7') ] )))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for source, dest in edges:
        comp_dict[source] = [source]
        comp_dict[dest] = [dest]
    for vertex in vertices:
        comp_dict[vertex] = [vertex]

    for source, dest in edges:
        if comp_dict[source][0] != comp_dict[dest][0]:
            (small,big) = (source,dest) if len(comp_dict[source]) < len(comp_dict[dest]) else (dest,source)
            comp_dict[big] += comp_dict[small]
            for elm in comp_dict[small]:
                comp_dict[elm] = comp_dict[big]
    return comp_dict


#FIXME: finish this
def components_dfs(edges: list[tuple[str,str]], vertices: Iterable[str] = ()) -> set[frozenset[str]]:
    comp_set = set()
    adj_list = adjacency(edges)
    for vertex in vertices:
        if vertex not in adj_list:
            adj_list[vertex] = set()


    return comp_set
