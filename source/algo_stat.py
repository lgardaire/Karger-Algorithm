import csv
import statistics as stats
from math import log

import matplotlib.pyplot as plt
import networkx as nx

from source.algo import *

min_graph_size = 3
max_graph_size = 30
a = 2
b = 4


def generate_random_graph(max_vertices):
    v = max_vertices
    graph = {i: [] for i in range(0, v)}
    p = random.random()
    edges = [(i, j) for i in range(0, v) for j in range(0, i) if random.random() < p]
    for i, j in edges:
        add_edge_to_graph(graph, i, j)
    return graph


def graph_to_file(filename, graph):
    with open(filename, "w") as f:
        edges = list_edges(graph)
        f.write(f"{len(graph)} {len(list_edges(graph))}\n")
        for e in edges:
            f.write(f"{' '.join(map(str,e))}\n")
        f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", help="example to load")
    parser.add_argument("--plot", help="csv to load to display")
    args = parser.parse_args()
    if args.example is None:
        if args.plot is None:
            execute_and_save_stats()
            load_and_display_plots("results.csv")
        else:
            load_and_display_plots(args.plot)
    else:
        graph = graph_from_file(args.example)
        nx_graph = convert_to_nx_graph(graph)
        results = get_stats_for_graph(graph, nx_graph)
        print_statistics(results, nx.stoer_wagner(nx_graph)[0])


def execute_and_save_stats():
    f = open("results.csv", "w", newline='')
    writer = csv.writer(f, delimiter=';', )
    writer.writerow(["graph_edges", "graph_nodes", "karger_contraction", "recursive_contraction",
                     "my_contraction", "karger_freq", "recursive_freq", "my_freq"])
    for i in range(min_graph_size, max_graph_size):
        while True:
            gr = generate_random_graph(i)
            g = convert_to_nx_graph(gr)
            if nx.is_connected(g):
                break
        results = get_stats_for_graph(gr, g)
        karger_values = results["karger"]
        recursive_values = results["recursive"]
        custom_values = results["custom"]
        writer.writerow(
            [len(list_edges(gr)), len(gr), stats.mean(karger_values["contractions"]),
             stats.mean(recursive_values["contractions"]), stats.mean(custom_values["contractions"]),
             karger_values["frequency"], recursive_values["frequency"], custom_values["frequency"]])
    f.close()


def load_and_display_plots(file):
    f = open(file, "r")
    reader = csv.DictReader(f, delimiter=";")
    karger_contractions = []
    karger_freqs = []
    recursive_contractions = []
    recursive_freqs = []
    custom_contractions = []
    custom_freqs = []
    for row in reader:
        karger_contractions.append(float(row["karger_contraction"]))
        recursive_contractions.append(float(row["recursive_contraction"]))
        custom_contractions.append(float(row["my_contraction"]))
        karger_freqs.append(float(row["karger_freq"]))
        recursive_freqs.append(float(row["recursive_freq"]))
        custom_freqs.append(float(row["my_freq"]))
    f.close()
    subplot = plt.subplot(121)
    subplot.plot(karger_contractions, label="karger")
    subplot.plot(recursive_contractions, label="recursive")
    subplot.plot(custom_contractions, label="custom")
    subplot.set_xlabel("nodes")
    subplot.set_ylabel("contractions")
    subplot.legend()
    subplot = plt.subplot(122)
    subplot.plot(karger_freqs, label="karger")
    subplot.plot(recursive_freqs, label="recursive")
    subplot.plot(custom_freqs, label="custom")
    subplot.set_xlabel("nodes")
    subplot.set_ylabel("correct min cut frequency")
    subplot.legend()
    plt.show()


def get_stats_for_graph(gr, g):
    min_cut = nx.stoer_wagner(g)[0]
    # plt.subplot(111)
    # nx.draw(g, with_labels=True, font_weight='bold')
    # plt.show()
    i = 0
    n = len(gr)
    iterations = int(log(n) ** 2)
    results = create_results(["karger", "recursive", "custom"])
    print(f"Iterations {iterations}")
    print(f"Graph Size {n}")

    while i < iterations:
        get_results(results, "karger", karger, min_cut, gr)
        get_results(results, "recursive", recursive_karger, min_cut, gr)
        get_results(results, "custom", recursive_karger, min_cut, gr, a, b)
        i += 1
    # print_statistics(results, min_cut[0])
    return results


def get_results(results, name, func, min_cut, *args):
    karger_res = results[name]
    value, contraction = func(*args)
    karger_res["contractions"].append(contraction)
    karger_res["values"].append(value)
    set_frequency(min_cut, karger_res)


def create_results(names):
    results = {}
    for name in names:
        results[name] = {"values": [], "contractions": []}
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
        print(f"mean contractions: {stats.mean(res['contractions'])}")


def set_frequency(min_cut, res):
    values = res['values']
    c = 0
    for i in values:
        if i == min_cut:
            c += 1
    p = c / len(values)
    res["frequency"] = p


def convert_to_nx_graph(gr):
    g = nx.Graph()
    g.add_nodes_from(gr.keys())
    b = [(v, i[0]) for i in gr.items() for v in i[1]]
    g.add_edges_from(b)
    return g


if __name__ == '__main__':
    main()
