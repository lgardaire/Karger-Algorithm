import random
from math import log

import matplotlib.pyplot as plt
import networkx as nx

from source.algo import karger, recursive_karger


def create_random_graph(size=-1, density=1.0):
    if size <= 1:
        size = random.randint(3, 30)
    vertices = {i for i in range(size)}
    graph = dict(zip(vertices, [[] for _ in range(size)]))
    for i in range(size):
        if len(graph[i]) == 0:
            vertices.remove(i)
            a = random.sample(vertices, 1)[0]
            graph[i].append(a)
            graph[a].append(i)
            vertices.add(i)
    for i in range(int(size * density)):
        a, b = random.sample(vertices, 2)
        if b not in graph[a]:
            graph[a].append(b)
            graph[b].append(a)
    return graph


def main():
    gr = create_random_graph(20, 4)
    g = nx.Graph()
    g.add_nodes_from(gr.keys())
    b = [(v, i[0]) for i in gr.items() for v in i[1]]
    g.add_edges_from(b)
    print(nx.stoer_wagner(g))
    plt.subplot(111)
    nx.draw(g, with_labels=True, font_weight='bold')
    plt.show()
    i = 0
    n = len(gr)
    iterations = int(n ** 2 * log(n) / 2)
    while i < iterations:
        print(f"karger:    {karger(gr.copy())}")
        print(f"recursive: {recursive_karger(gr.copy())}")
        i += 1


if __name__ == '__main__':
    main()
