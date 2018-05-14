#!/usr/bin/python3
import argparse
import random
from math import sqrt


def karger(graph, limit=2.0, copy=True):
    """
    A monte carlo algorithm that can return the minimum cut of a graph with a probability of at least (n choose 2)^-1
    :param graph: a graph in a adjacency list style
    :param limit: the graph size at which the algorithm stops, defaults to 2
    :param copy: if true does not modify the graph passed to the function
    :param contraction: the number of contractions until now
    :return: the min cut found
    """
    if copy:
        graph = graph.copy()
    contraction = 0
    while len(graph) > limit and len(graph) > 2:
        a, b = random.choice(list_edges(graph))
        contract(graph, a, b)
        contraction += 1
    return len(next(iter(graph.values()))), contraction


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


def recursive_karger(graph, limit=sqrt(2), nb_recursion=2, copy=True):
    if copy:
        graph = graph.copy()
    depth = len(graph) / limit
    cut, ctr = karger(graph, depth, False)
    contraction = ctr
    if depth <= 2:
        return cut, contraction
    res = []
    for _ in range(nb_recursion):
        cut, ctr = recursive_karger(graph, limit)
        contraction += ctr
        res.append(cut)
    return min(res), contraction


def graph_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    lines = [[int(j) for j in i.split()] for i in lines]
    graph = {i: [] for i in range(0, lines[0][0])}
    for i, j in lines[1:]:
        add_edge_to_graph(graph, i, j)
    return graph


def add_edge_to_graph(graph, i, j):
    graph[i].append(j)
    graph[j].append(i)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("example", help="Path to the example file to load")
    parser.add_argument("algorithm", help="Algorithm to execute can be: karger recursive or custom")
    parser.add_argument("-r", help="Number of times to repeat the algorithm")
    parser.add_argument("-a", help="Sets the a value for the custom algorithm defaults to 1/2")
    parser.add_argument("-b", help="Sets the b value for the custom algorithm defaults to 4")
    args = parser.parse_args()
    if args.example is not None:
        algorithm = karger
        graph = graph_from_file(args.example)
        str = ""
        algo_args = [graph]
        if args.algorithm == "recursive":
            algorithm = recursive_karger
        elif args.algorithm == "custom":
            algorithm = recursive_karger
            a = 0.5
            b = 4
            if args.a is not None:
                a = float(args.a)
            if args.b is not None:
                b = int(args.b)
            algo_args += [1 / a, b]
            str = f"with a={a} and b={b}"
        n = len(graph)
        iterations = int(n ** 2 / 2)
        if args.r is not None and int(args.r) > 0:
            iterations = int(args.r)
        min_cut = 1000000000000000000000000000000
        for _ in range(iterations):
            cut, contractions = algorithm(*algo_args)
            print(f"{algorithm.__name__} found cut {cut} with {contractions} contractions")
            if cut < min_cut:
                min_cut = cut
        print(
            f"The min cut found with the {algorithm.__name__} algorithm and {iterations} iterations is: {min_cut} {str}")


if __name__ == '__main__':
    main()
