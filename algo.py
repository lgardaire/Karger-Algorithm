import random


def karger(graph):
    """
    A monte carlo algorithm that can return the minimum cut of a graph
    :param graph: a graph in a adjacency list style
    :return: the min cut found
    """
    tmp_graph = graph.copy()
    while len(tmp_graph) > 2:
        print(tmp_graph)
        vertex = random.choice(list(tmp_graph))
        edges = tmp_graph[vertex]
        contract(tmp_graph, vertex, random.choice(edges))
    print(tmp_graph)
    return len(tmp_graph.popitem()[1])


def contract(graph, u, v):
    """
    Function that contracts the edge between u and v so that the edges linked to v become linked to u and v is removed
    :param graph: a graph in a adjacency list style
    :param u: vertex
    :param v: vertex
    """
    print(f"Contracting {u} {v}")
    values = graph.pop(v)
    values = [i for i in values if i != u]
    graph[u] = [i for i in graph[u] if i != v]
    graph[u] += values
    for k in values:
        graph[k] = [i if i != v else u for i in graph[k]]


def main():
    graph = {1: [2], 2: [1, 3, 4, 5], 3: [2], 4: [2, 5], 5: [2, 4]}
    print(karger(graph))


if __name__ == '__main__':
    main()
