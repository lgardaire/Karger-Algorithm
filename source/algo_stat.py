import csv
import statistics as stats
import time
from math import log

import matplotlib.pyplot as plt
import networkx as nx

from algo import *


def generate_random_graph(max_vertices):
    # v = random.randint(5, max_vertices)
    v = max_vertices
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
    f = open("salut.csv", "w", newline='')
    writer = csv.writer(f, delimiter=';', )
    writer.writerow(["graph_edges", "graph_nodes", "karger_time", "recursive_time",
                     "my_time", "karger_freq", "recursive_freq", "my_freq"])
    freqs = [[], [], []]
    for i in range(3, 24):
        while True:
            gr = generate_random_graph(i)
            g = convertToNxgraph(gr)
            if nx.is_connected(g):
                break
        results = get_stats_for_graph(gr, g)
        karger_values = results["karger"]
        recursive_values = results["recursive"]
        improved_values = results["improved"]
        writer.writerow(
            [len(list_edges(gr)), len(gr), stats.mean(karger_values["times"]), stats.mean(recursive_values["times"]),
             stats.mean(improved_values["times"]), karger_values["frequency"], recursive_values["frequency"],
             improved_values["frequency"]])

    f.close()
    f = open("salut.csv", "r")
    reader = csv.DictReader(f, delimiter=";")
    karger_times = []
    karger_freqs = []
    recursive_times = []
    recursive_freqs = []
    improved_times = []
    improved_freqs = []
    for row in reader:
        karger_times.append(float(row["karger_time"]))
        recursive_times.append(float(row["recursive_time"]))
        improved_times.append(float(row["my_time"]))
        karger_freqs.append(float(row["karger_freq"]))
        recursive_freqs.append(float(row["recursive_freq"]))
        improved_freqs.append(float(row["my_freq"]))
    subplot = plt.subplot(121)
    subplot.plot(karger_times, label="karger")
    subplot.plot(recursive_times, label="recursive")
    subplot.plot(improved_times, label="improved")
    subplot.legend()
    subplot = plt.subplot(122)
    subplot.plot(karger_freqs, label="karger")
    subplot.plot(recursive_freqs, label="recursive")
    subplot.plot(improved_freqs, label="improved")
    subplot.legend()
    plt.show()


def get_stats_for_graph(gr, g):
    min_cut = nx.stoer_wagner(g)[0]
    # plt.subplot(111)
    # nx.draw(g, with_labels=True, font_weight='bold')
    # plt.show()
    i = 0
    n = len(gr)
    iterations = int(n * (n - 1) * log(n) / 2)
    results = create_results(["karger", "recursive", "improved"])
    print(f"Iterations {iterations}")
    print(f"Graph Size {n}")
    f = sqrt(8) / sqrt(5)
    while i < iterations:
        get_results(results, "karger", karger, min_cut, gr)
        get_results(results, "recursive", recursive_karger, min_cut, gr)
        get_results(results, "improved", recursive_karger, min_cut, gr, 2, 2)
        i += 1
    # print_statistics(results, min_cut[0])
    return results


def get_results(results, name, func, min_cut, *args):
    karger_res = results[name]
    start = time.time()
    value = func(*args)
    karger_res["times"].append((time.time() - start) * 1000)
    karger_res["values"].append(value)
    set_frequency(min_cut, karger_res)


def create_results(names):
    results = {}
    for name in names:
        results[name] = {"values": [], "times": []}
    return results


def print_statistics(results, min_cut):
    for algo, res in results.items():
        values = res['values']
        print(f"############ {algo} ############")
        print(f"{algo}: {values}")
        print(f"mean: {stats.mean(values)}")
        print(f"variance: {stats.variance(values)}")
        set_frequency(min_cut, res)
        print(f"min cut frequency for {algo}: {res['frequency']}")
        print(f"mean time: {stats.mean(res['times'])} ms")


def set_frequency(min_cut, res):
    values = res['values']
    c = 0
    for i in values:
        if i == min_cut:
            c += 1
    p = c / len(values)
    res["frequency"] = p


def convertToNxgraph(gr):
    g = nx.Graph()
    g.add_nodes_from(gr.keys())
    b = [(v, i[0]) for i in gr.items() for v in i[1]]
    g.add_edges_from(b)
    return g


if __name__ == '__main__':
    main()
