"""Functions dealing with dictionaries."""

from collections import defaultdict, deque
from collections.abc import Callable, Hashable, Iterable, Iterator, Mapping

import graphviz

from protocols import HashableSortable
from supply import distinct


def invert[K: Hashable, V: Hashable](d: dict[K,V]) -> dict[V,K]:
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


def sorted_al[T: HashableSortable](adj_list: dict[T,set[T]]) -> dict[T,list[T]]:
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


def adjacency[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (), *, directed: bool = True,
    ) -> dict[T,set[T]]:
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

    >>> adjacency([], directed=False)
    {}
    >>> adjacency([('a', 'A')], directed=False)
    {'a': {'A'}, 'A': {'a'}}
    >>> sorted_al(adjacency([('a','b'), ('b','c'), ('c','a')], directed=False))
    {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b']}
    >>> sorted_al(adjacency([('a','c'), ('a','b'), ('b','c'), ('c','a')],
    ...                     directed=False))
    {'a': ['b', 'c'], 'c': ['a', 'b'], 'b': ['a', 'c']}
    >>> sorted_al(adjacency([('a','b'), ('b','c'), ('c','a')], ('d','a','e'),
    ...                     directed=False))
    {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b'], 'd': [], 'e': []}
    """
    adj_list = {}

    for source, dest in edges:
        if source in adj_list:
            adj_list[source].add(dest)
        else:
            adj_list[source] = {dest}

        if not directed:
            if dest in adj_list:
                adj_list[dest].add(source)
            else:
                adj_list[dest] = {source}

    for vertex in vertices:
        if vertex not in adj_list:
            adj_list[vertex] = set()

    return adj_list


def adjacency_alt[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (), *, directed: bool = True,
    ) -> dict[T,set[T]]:
    """
    Make an adjacency list.

    This takes edges expressed as pairs of source and destination vertices, and
    return an adjacency list as a dictionary whose keys are vertices and whose
    values are sets of their outward neighbors.

    >>> adjacency_alt([])
    {}
    >>> adjacency_alt([('a', 'A')])
    {'a': {'A'}}
    >>> adjacency_alt([('a','b'), ('b','c'), ('c','a')])
    {'a': {'b'}, 'b': {'c'}, 'c': {'a'}}
    >>> sorted_al(adjacency_alt([('a','c'), ('a','b'), ('b','c'), ('c','a')]))
    {'a': ['b', 'c'], 'b': ['c'], 'c': ['a']}
    >>> adjacency_alt([('a','b'), ('b','c'), ('c','a')], ('d','a','e'))
    {'a': {'b'}, 'b': {'c'}, 'c': {'a'}, 'd': set(), 'e': set()}

    >>> adjacency_alt([], directed=False)
    {}
    >>> adjacency_alt([('a', 'A')], directed=False)
    {'a': {'A'}, 'A': {'a'}}
    >>> sorted_al(adjacency_alt([('a','b'), ('b','c'), ('c','a')], directed=False))
    {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b']}
    >>> sorted_al(adjacency_alt([('a','c'), ('a','b'), ('b','c'), ('c','a')],
    ...                         directed=False))
    {'a': ['b', 'c'], 'c': ['a', 'b'], 'b': ['a', 'c']}
    >>> sorted_al(adjacency_alt([('a','b'), ('b','c'), ('c','a')], ('d','a','e'),
    ...                         directed=False))
    {'a': ['b', 'c'], 'b': ['a', 'c'], 'c': ['a', 'b'], 'd': [], 'e': []}
    """
    adj_list = defaultdict(set)
    for source, dest in edges:
        adj_list[source].add(dest)
        if not directed:
            adj_list[dest].add(source)
    for vertex in vertices:
        adj_list[vertex]
    return dict(adj_list)


def draw_graph[T](adj_list: dict[T,set[T]]) -> graphviz.Digraph:
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


# TODO: Modify this to use a comprehension.
def sorted_setoset[T: HashableSortable](unsorted: set[frozenset[T]]) -> list[list[T]]:
    """Convert a family of (frozen)sets into a nested list."""
    unsorted_list = []
    for collection in unsorted:
        unsorted_list.append(sorted(collection))  # noqa: PERF401
    return sorted(unsorted_list)


def components[T: Hashable](edges: list[tuple[T,T]]) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list.

    >>> components([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components(edges))
    [[2, 3, 7, 12], [4, 5, 6]]
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


def components_d[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list.

    >>> components_d([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_d(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_d(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components_d(edges))
    [[2, 3, 7, 12], [4, 5, 6]]
    """
    return _setofsets(components_dict(edges, vertices))


def _setofsets[K: Hashable, T: Hashable](
        set_dict: Mapping[K,Iterable[T]],
    ) -> set[frozenset[T]]:
    """Make a set of frozensets (components_d must assure preconditions)."""
    vals = set()
    for val in distinct(set_dict.values(), key=id):
        vals.add(frozenset(val))
    return vals


def _setofsets_alt[K: Hashable, T: Hashable](
        set_dict: Mapping[K,Iterable[T]],
    ) -> set[frozenset[T]]:
    """Make a set of frozensets (like _setofsets, same preconditions)."""
    list_of_sets = distinct(set_dict.values(), key=id)
    return set(map(frozenset, list_of_sets))


# TODO: Make a third version of _setofsets that uses a comprehension.


def components_dict[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> dict[T,list[T]]:
    """
    Identify the connected components from an edge list.

    Approximately uses the quick-find algorithm.

    >>> components_dict([])
    {}
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(_setofsets(components_dict(edges)))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for u, v in edges:
        if u in comp_dict and v in comp_dict:
            if comp_dict[u] is not comp_dict[v]:
                small, big = (u,v) if len(comp_dict[u]) < len(comp_dict[v]) else (v,u)
                comp_dict[big] += comp_dict[small]
                for elm in comp_dict[small]:
                    comp_dict[elm] = comp_dict[big]
        elif u in comp_dict:
            comp_dict[u].append(v)
        elif v in comp_dict:
            comp_dict[v].append(u)
        else:
            comp_dict[u] = [u,v]
            comp_dict[v] = comp_dict[u]
    for vertex in vertices:
        if vertex not in comp_dict:
            comp_dict[vertex] = [vertex]
    return comp_dict


def components_dict_alt[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> dict[T,list[T]]:
    """
    Identify the connected components from an edge list.

    uses the quick-find algorithm.

    O(m log(n))
    m = #edges
    n = #vertices

    >>> components_dict_alt([])
    {}
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(_setofsets(components_dict_alt(edges)))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for u, v in edges:
        comp_dict[u] = [u]
        comp_dict[v] = [v]
    for vertex in vertices:
        comp_dict[vertex] = [vertex]

    for u, v in edges:
        if comp_dict[u] is not comp_dict[v]:
            small, big = (u,v) if len(comp_dict[u]) < len(comp_dict[v]) else (v,u)
            comp_dict[big] += comp_dict[small]
            for elm in comp_dict[small]:
                comp_dict[elm] = comp_dict[big]
    return comp_dict


# FIXME: Actually implement classic quick-find.
def components_dict_alt2[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> dict[T,list[T]]:
    """
    Identify the connected components from an edge list.

    Uses the classic quick-find algorithm.

    >>> components_dict_alt2([])
    {}
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(_setofsets(components_dict_alt2(edges)))
    [['1', '2', '3', '7'], ['4', '5', '6']]
    """
    comp_dict = {}
    for u, v in edges:
        comp_dict[u] = [u]
        comp_dict[v] = [v]
    for vertex in vertices:
        comp_dict[vertex] = [vertex]

    for u, v in edges:
        if comp_dict[u][0] != comp_dict[v][0]:
            small, big = (u,v) if len(comp_dict[u]) < len(comp_dict[v]) else (v,u)
            comp_dict[big] += comp_dict[small]
            for elm in comp_dict[small]:
                comp_dict[elm] = comp_dict[big]
    return comp_dict


def components_dfs[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list.

    That thing where the paths are traversed and the entire component is found,
    then move to the next component.

    >>> components_dfs([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components_dfs(edges))
    [[2, 3, 7, 12], [4, 5, 6]]
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(source: T, action: Callable[[T], None]) -> None:
        visited.add(source)
        action(source)
        for dest in adj_list[source]:
            if dest not in visited:
                explore(dest, action)

    for node in adj_list:
        if node not in visited:
            component = []
            explore(node, component.append)
            comp_set.add(frozenset(component))

    return comp_set


def components_dfs_alt[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list.

    That thing where the paths are traversed and the entire component is found,
    then move to the next component.

    >>> components_dfs_alt([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs_alt(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs_alt(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components_dfs_alt(edges))
    [[2, 3, 7, 12], [4, 5, 6]]
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(source: T) -> Iterable[T]:
        visited.add(source)
        yield source
        for dest in adj_list[source]:
            if dest not in visited:
                yield from explore(dest)

    for node in adj_list:
        if node not in visited:
            comp_set.add(frozenset(explore(node)))

    return comp_set


# TODO: Modify this for arbitrary recursion limits, and to use a comprehension.
def devious() -> list[tuple[str,str]]:
    """
    Create a list of edges that defeats components_dfs.

    >>> components_dfs(devious())
    Traceback (most recent call last):
      ...
    RecursionError: maximum recursion depth exceeded
    """
    edges = []
    labels = range(1337)
    for index in labels:
        edges.append((str(index),str(index+1)))  # noqa: PERF401
    return edges


def components_dfs_iter[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list.

    This is like components_dfs(), but it tolerates even graphs that would
    cause it to fail with RecursionError (i.e., graphs with long chains).

    >>> components_dfs_iter([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs_iter(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_dfs_iter(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components_dfs_iter(edges))
    [[2, 3, 7, 12], [4, 5, 6]]

    >>> devious_vertices = map(str, range(1338))
    >>> components_dfs_iter(devious()) == {frozenset(devious_vertices)}
    True
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(start: T) -> Iterable[T]:
        visited.add(start)
        yield start
        itst = [iter(adj_list[start])]
        while itst:
            try:
                node = next(itst[-1])
            except StopIteration:
                del itst[-1]
            else:
                if node not in visited:
                    visited.add(node)
                    yield node
                    itst.append(iter(adj_list[node]))

    for node in adj_list:
        if node not in visited:
            comp_set.add(frozenset(explore(node)))

    return comp_set


def components_bfs[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list, breadth-first.

    >>> components_bfs([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_bfs(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_bfs(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components_bfs(edges))
    [[2, 3, 7, 12], [4, 5, 6]]

    >>> devious_vertices = map(str, range(1338))
    >>> components_bfs(devious()) == {frozenset(devious_vertices)}
    True
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(start: T) -> list[T]:
        component = [start]
        visited.add(start)
        i = 0
        while i < len(component):
            for node in adj_list[component[i]]:
                if node not in visited:
                    component.append(node)
                    visited.add(node)
            i += 1
        return component

    for node in adj_list:
        if node not in visited:
            comp_set.add(frozenset(explore(node)))

    return comp_set


def components_bfs_alt[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list, breadth-first.

    >>> components_bfs_alt([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_bfs_alt(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_bfs_alt(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components_bfs_alt(edges))
    [[2, 3, 7, 12], [4, 5, 6]]

    >>> devious_vertices = map(str, range(1338))
    >>> components_bfs_alt(devious()) == {frozenset(devious_vertices)}
    True
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(start: T) -> Iterator[T]:
        node_queue = deque([start])
        while node_queue:
            node = node_queue.popleft()
            if node not in visited:
                visited.add(node)
                yield node
                node_queue.extend(adj_list[node])

    for node in adj_list:
        if node not in visited:
            comp_set.add(frozenset(explore(node)))

    return comp_set


def components_bfs_alt2[T: Hashable](
        edges: list[tuple[T,T]], vertices: Iterable[T] = (),
    ) -> set[frozenset[T]]:
    """
    Identify the connected components from an edge list, breadth-first.

    >>> components_bfs_alt2([])
    set()
    >>> edges = [('1','2'), ('1','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_bfs_alt2(edges))
    [['1', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [('12','2'), ('12','3'), ('4','5'),
    ...          ('5','6'), ('3','7'), ('2','7')]
    >>> sorted_setoset(components_bfs_alt2(edges))
    [['12', '2', '3', '7'], ['4', '5', '6']]

    >>> edges = [(12,2), (12,3), (4,5), (5,6), (3,7), (2,7)]
    >>> sorted_setoset(components_bfs_alt2(edges))
    [[2, 3, 7, 12], [4, 5, 6]]

    >>> devious_vertices = map(str, range(1338))
    >>> components_bfs_alt2(devious()) == {frozenset(devious_vertices)}
    True
    """
    adj_list = adjacency(edges, vertices, directed=False)
    comp_set = set()
    visited = set()

    def explore(start: T) -> Iterator[T]:
        node_queue = deque([start])
        visited.add(start)
        while node_queue:
            parent = node_queue.popleft()
            yield parent
            for child in adj_list[parent]:
                if child not in visited:
                    node_queue.append(child)
                    visited.add(child)

    for node in adj_list:
        if node not in visited:
            comp_set.add(frozenset(explore(node)))

    return comp_set
