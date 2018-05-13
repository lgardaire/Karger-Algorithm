import random
from math import sqrt


def karger(graph, limit=2.0, copy=True):
    """
    A monte carlo algorithm that can return the minimum cut of a graph with a probability of at least (n choose 2)^-1
    :param graph: a graph in a adjacency list style
    :param limit: the graph size at which the algorithm stops, defaults to 2
    :param copy: if true does not modify the graph passed to the function
    :return: the min cut found
    """
    if copy:
        graph = graph.copy()
    while len(graph) > limit and len(graph) > 2:
        # print(graph)
        a, b = random.choice(list_edges(graph))
        contract(graph, a, b)
    # print(graph)
    return len(next(iter(graph.values())))


def list_edges(graph):
    edges = []
    for k, v in graph.items():
        for a in v:
            if a >= k:
                edges.append((k, a))
    return edges


def contract(graph, u, v):
    """
    Function that contracts the edge between u and v so that the edges linked to v become linked to u and v is removed
    :param graph: a graph in a adjacency list style
    :param u: vertex
    :param v: vertex
    """
    # print(f"Contracting {u} {v}")
    values = graph.pop(v)
    values = [i for i in values if i != u]
    graph[u] = [i for i in graph[u] if i != v]
    graph[u] += values
    for k in values:
        graph[k] = [i if i != v else u for i in graph[k]]


def recursive_karger(graph, limit=sqrt(2), nbrecursive=2, copy=True):
    if copy:
        graph = graph.copy()
    depth = len(graph) / limit
    cut = karger(graph, depth, False)
    if depth <= 2:
        return cut
    arg1 = [recursive_karger(graph, limit, nbrecursive) for _ in range(nbrecursive)]
    return min(arg1)


def main():
    gr = {0: [1, 2], 1: [0], 2: [0]}
    print(f"karger:    {karger(gr)}")
    print(f"recursive: {recursive_karger(gr)}")


if __name__ == '__main__':
    main()
