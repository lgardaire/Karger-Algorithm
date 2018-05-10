import csv
import random
import statistics
from math import log

import matplotlib.pyplot as plt
import networkx as nx

from source.algo import karger, recursive_karger, list_edges


def generate_erdos_renyi(max_vertices):
    v = random.randint(3, max_vertices)
    graph = {i: [] for i in range(0, v)}

    p = random.random()
    edges = [(i, j) for i in range(0, v) for j in range(0, i) if random.random() < p]

    for i, j in edges:
        add_edge_to_graph(graph, i, j)
    return graph


def graph_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    lines = [[int(j) for j in i.split()] for i in lines]
    graph = {i: [] for i in range(0, lines[0][0])}
    for i, j in lines[1:]:
        add_edge_to_graph(graph, i, j)
    return graph


def graph_to_file(filename, graph):
    with open(filename, "w") as f:
        edges = list_edges(graph)
        f.write(f"{len(graph)} {len(list_edges(graph))}\n")
        for e in edges:
            f.write(f"{' '.join(map(str,e))}\n")
        f.close()


def add_edge_to_graph(graph, i, j):
    graph[i].append(j)
    graph[j].append(i)


def main():
    while True:
        gr = generate_erdos_renyi(20)
        g = convertToNxgraph(gr)
        if nx.is_connected(g):
            break

    min_cut = nx.stoer_wagner(g)
    file = graph_from_file("../exemples/empty")
    graph_to_file("lol", file)
    plt.subplot(121)
    nx.draw(g, with_labels=True, font_weight='bold')
    plt.subplot(122)
    nx.draw(convertToNxgraph(file), with_labels=True)
    plt.show()

    print(min_cut)
    i = 0
    n = len(gr)
    iterations = int(n ** 2 * log(n) / 2)
    results = create_results(["karger", "recursive", "improved"])
    print(f"Iterations {iterations}")
    print(f"Graph Size {n}")
    print(f"1/n= {1-1/n}")
    karger_values = results["karger"]["values"]
    recursive_values = results["recursive"]["values"]
    improved_values = results["improved"]["values"]
    while i < iterations:
        karger_values.append(karger(gr.copy()))
        recursive_values.append(recursive_karger(gr.copy()))
        improved_values.append(recursive_karger(gr.copy(), 2, 3))
        i += 1

    get_statistics(results, min_cut[0])
    with open('names.csv', 'w', newline='') as csvfile:
        columns = ["karger", "recursive", "improved"]
        writer = csv.DictWriter(csvfile, columns, d)
        writer.writeheader()
        for i in range(iterations):
            writer.writerow(
                {"karger": karger_values[i], "recursive": recursive_values[i], "improved": improved_values[i]})


def create_results(names):
    results = {}
    for name in names:
        results[name] = {"values": []}
    return results


def get_statistics(results, min_cut):
    for algo, res in results.items():
        values = res['values']
        print(f"############ {algo} ############")
        print(f"{algo}: {values}")
        print(f"mean: {statistics.mean(values)}")
        print(f"variance: {statistics.variance(values)}")
        c = 0
        for i in values:
            if i == min_cut:
                c += 1
        p = c / len(values)
        print(f"min cut frequency for {algo}: {p}")


def convertToNxgraph(gr):
    g = nx.Graph()
    g.add_nodes_from(gr.keys())
    b = [(v, i[0]) for i in gr.items() for v in i[1]]
    g.add_edges_from(b)
    return g


if __name__ == '__main__':
    main()
