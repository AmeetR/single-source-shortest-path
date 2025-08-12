import random
from collections import defaultdict

import networkx as nx
import pytest

from sssp import band_sssp, dijkstra


@pytest.mark.parametrize("algo", [dijkstra, band_sssp])
def test_large_random_graph(algo):
    random.seed(42)
    n = 30
    g = nx.gnp_random_graph(n, 0.2, directed=True)
    graph = defaultdict(list)
    nx_graph = nx.DiGraph()
    for u, v in g.edges():
        w = random.randint(1, 20)
        graph[u].append((v, w))
        nx_graph.add_edge(u, v, weight=w)
    for u in range(n):
        graph[u]  # ensure all nodes are present
    expected = nx.single_source_dijkstra_path_length(nx_graph, 0, weight="weight")
    assert algo(graph, 0) == expected


@pytest.mark.parametrize("algo", [dijkstra, band_sssp])
def test_zero_weight_edges(algo):
    random.seed(0)
    n = 25
    g = nx.gnp_random_graph(n, 0.2, directed=True)
    graph = defaultdict(list)
    nx_graph = nx.DiGraph()
    for u, v in g.edges():
        w = random.randint(0, 5)
        graph[u].append((v, w))
        nx_graph.add_edge(u, v, weight=w)
    for u in range(n):
        graph[u]
    expected = nx.single_source_dijkstra_path_length(nx_graph, 0, weight="weight")
    assert algo(graph, 0) == expected


@pytest.mark.parametrize("algo", [dijkstra, band_sssp])
def test_dense_graph(algo):
    random.seed(1)
    n = 20
    graph = defaultdict(list)
    nx_graph = nx.DiGraph()
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            w = random.randint(1, 50)
            graph[u].append((v, w))
            nx_graph.add_edge(u, v, weight=w)
    expected = nx.single_source_dijkstra_path_length(nx_graph, 0, weight="weight")
    assert algo(graph, 0) == expected


@pytest.mark.parametrize("algo", [dijkstra, band_sssp])
def test_grid_random_weights(algo):
    random.seed(7)
    width = 8
    height = 8
    g = nx.grid_2d_graph(width, height)
    graph = defaultdict(list)
    for u, v in g.edges():
        w = random.randint(0, 9)
        graph[u].append((v, w))
        graph[v].append((u, w))
    nx_graph = nx.DiGraph()
    for u in graph:
        for v, w in graph[u]:
            nx_graph.add_edge(u, v, weight=w)
    expected = nx.single_source_dijkstra_path_length(nx_graph, (0, 0), weight="weight")
    assert algo(graph, (0, 0)) == expected
