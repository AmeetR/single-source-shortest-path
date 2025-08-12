"""Dijkstra's single-source shortest path algorithm.

This implementation follows the algorithm described in
Edsger W. Dijkstra's 1959 paper, "A note on two problems in connexion with graphs".
"""

from __future__ import annotations

import heapq
from typing import Dict, Hashable, Iterable, List, Tuple


Weight = float
Graph = Dict[Hashable, Iterable[Tuple[Hashable, Weight]]]


def dijkstra(graph: Graph, source: Hashable) -> Dict[Hashable, Weight]:
    """Compute shortest path distances from *source* to all other vertices.

    Parameters
    ----------
    graph:
        Mapping of node -> iterable of (neighbor, weight).
    source:
        Node from which to compute shortest paths.

    Returns
    -------
    Dict[Hashable, Weight]
        Mapping of node -> distance from *source*.

    Raises
    ------
    ValueError
        If the graph contains a negative edge weight.
    """

    distances: Dict[Hashable, Weight] = {source: 0.0}
    pq: List[Tuple[Weight, Hashable]] = [(0.0, source)]

    while pq:
        dist_u, u = heapq.heappop(pq)
        if dist_u > distances[u]:
            continue  # Found a stale entry.
        for v, weight in graph.get(u, []):
            if weight < 0:
                raise ValueError("Dijkstra's algorithm does not allow negative edge weights")
            alt = dist_u + weight
            if v not in distances or alt < distances[v]:
                distances[v] = alt
                heapq.heappush(pq, (alt, v))

    return distances
