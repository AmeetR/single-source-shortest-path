import random
from collections import defaultdict

import networkx as nx
import pytest

from sssp import dijkstra


def test_dijkstra_basic():
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }
    assert dijkstra(graph, "A") == {"A": 0.0, "B": 1.0, "C": 3.0, "D": 4.0}


def test_dijkstra_disconnected():
    graph = {"A": [("B", 1)], "B": [], "C": [("D", 1)], "D": []}
    assert dijkstra(graph, "A") == {"A": 0.0, "B": 1.0}


def test_dijkstra_negative_edge():
    graph = {"A": [("B", -1)]}
    with pytest.raises(ValueError):
        dijkstra(graph, "A")


def test_dijkstra_large_random():
    random.seed(0)
    g = nx.gnp_random_graph(50, 0.2, directed=True)
    graph = defaultdict(list)
    nx_graph = nx.DiGraph()
    for u, v in g.edges():
        w = random.randint(1, 20)
        graph[u].append((v, w))
        nx_graph.add_edge(u, v, weight=w)
    expected = nx.single_source_dijkstra_path_length(nx_graph, 0, weight="weight")
    assert dijkstra(graph, 0) == expected


def test_dijkstra_grid():
    g = nx.grid_2d_graph(10, 10)
    graph = defaultdict(list)
    for u, v in g.edges():
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    expected = nx.single_source_dijkstra_path_length(g, (0, 0))
    assert dijkstra(graph, (0, 0)) == expected
