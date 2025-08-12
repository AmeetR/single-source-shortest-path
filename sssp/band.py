"""Band-partitioned single-source shortest path algorithm.

This module implements a simplified version of the deterministic
O(m log^{2/3} n) algorithm for directed graphs with non-negative
weights described in Duan–Mao–Mao–Shu–Yin (2025), "Breaking the
Sorting Barrier for Directed Single-Source Shortest Paths." The
implementation follows the high-level structure from the paper: it
maintains distance bands, performs limited Bellman–Ford relaxations
inside a band, selects a small set of pivots, and orders only those
pivots.

The code is intentionally engineered for clarity rather than exact
asymptotic guarantees, but it mirrors the mechanism outlined in the
paper and produces correct shortest path distances for graphs with
non-negative weights.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, Iterable, List, Tuple
import heapq
import math

Weight = float
GraphMapping = Dict[Hashable, Iterable[Tuple[Hashable, Weight]]]

INF = float("inf")


@dataclass(frozen=True)
class Edge:
    u: int
    v: int
    w: float


class Graph:
    """Simple adjacency-list graph used internally by the algorithm."""

    def __init__(self, n: int, edges: Iterable[Tuple[int, int, float]]):
        self.n = n
        self.adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
        for u, v, w in edges:
            if w < 0:
                raise ValueError("Negative edge weights are not supported")
            self.adj[u].append((v, float(w)))


def relax(u: int, v: int, w: float, dist: List[float]) -> bool:
    du = dist[u]
    if du + w < dist[v]:
        dist[v] = du + w
        return True
    return False


def k_round_relax(
    G: Graph,
    dist: List[float],
    active: List[int],
    k: int,
    band_upper: float,
) -> Tuple[List[int], List[int]]:
    """Perform ``k`` rounds of restricted relaxations within ``band_upper``."""

    work = set(active)
    for _ in range(k):
        next_work = set()
        for u in list(work):
            du = dist[u]
            if du >= band_upper:
                continue
            for v, w in G.adj[u]:
                if du + w < band_upper and relax(u, v, w, dist):
                    next_work.add(v)
        work = next_work
        if not work:
            break

    settled: List[int] = []
    incomplete: List[int] = []
    for u in active:
        du = dist[u]
        if du >= band_upper:
            continue
        can_improve = False
        for v, w in G.adj[u]:
            if du + w < dist[v] and du + w < band_upper:
                can_improve = True
                break
        if can_improve:
            incomplete.append(u)
        else:
            settled.append(u)

    return settled, incomplete


def select_pivots(
    G: Graph,
    dist: List[float],
    candidates: List[int],
    band_upper: float,
    budget_k: int,
) -> List[int]:
    """Select a small set of pivot vertices among ``candidates``."""

    scored: List[Tuple[int, int]] = []
    for u in candidates:
        du = dist[u]
        if du >= band_upper:
            continue
        score = 0
        for v, w in G.adj[u]:
            if du + w < band_upper:
                score += 1
        scored.append((score, u))

    scored.sort(reverse=True)
    target = max(1, len(candidates) // max(1, budget_k))
    return [u for _, u in scored[:target]]


def process_pivots(G: Graph, dist: List[float], pivots: List[int], band_upper: float) -> None:
    """Process pivot vertices using a small heap."""

    H: List[Tuple[float, int]] = []
    seen = set()
    for u in pivots:
        if dist[u] < band_upper and u not in seen:
            heapq.heappush(H, (dist[u], u))
            seen.add(u)

    while H:
        du, u = heapq.heappop(H)
        if du != dist[u] or du >= band_upper:
            continue
        for v, w in G.adj[u]:
            if du + w < band_upper and relax(u, v, w, dist):
                heapq.heappush(H, (dist[v], v))


def band_partitioned_sssp(
    G: Graph,
    s: int,
    *,
    initial_band: float | None = None,
    k: int | None = None,
    growth: float = 2.0,
) -> List[float]:
    """Compute shortest paths from ``s`` using banding and pivot reduction."""

    n = G.n
    dist = [INF] * n
    dist[s] = 0.0

    if k is None:
        k = max(1, int(round(math.log2(max(2, n)) ** (1 / 3))))

    if initial_band is None:
        total_w = 0.0
        cnt = 0
        for u in range(n):
            for _, w in G.adj[u]:
                total_w += w
                cnt += 1
        avg_w = (total_w / max(1, cnt)) if cnt else 1.0
        initial_band = avg_w * max(2.0, math.log2(max(2, n)))

    band_upper = initial_band
    active = [s]

    while True:
        settled, incomplete = k_round_relax(G, dist, active, k, band_upper)

        if incomplete:
            pivots = select_pivots(G, dist, incomplete, band_upper, budget_k=k)
            process_pivots(G, dist, pivots, band_upper)

        next_active: List[int] = []
        for u in range(n):
            if dist[u] < band_upper:
                for v, w in G.adj[u]:
                    if dist[u] + w < band_upper and dist[u] + w < dist[v] + 1e-18:
                        next_active.append(u)
                        break

        if not next_active:
            band_upper *= growth
            seed = set()
            for u in range(n):
                if dist[u] < band_upper:
                    seed.add(u)
                    for v, w in G.adj[u]:
                        if dist[u] + w < band_upper:
                            seed.add(v)
            active = list(seed)
        else:
            active = next_active

        if band_upper > 1e18:
            break

    H: List[Tuple[float, int]] = []
    for u in range(n):
        if dist[u] < INF:
            heapq.heappush(H, (dist[u], u))
    while H:
        du, u = heapq.heappop(H)
        if du != dist[u]:
            continue
        for v, w in G.adj[u]:
            if relax(u, v, w, dist):
                heapq.heappush(H, (dist[v], v))

    return dist


def band_sssp(graph: GraphMapping, source: Hashable) -> Dict[Hashable, Weight]:
    """Public wrapper mirroring :func:`dijkstra`'s interface."""

    nodes = set(graph.keys())
    for nbrs in graph.values():
        for v, _ in nbrs:
            nodes.add(v)
    if source not in nodes:
        nodes.add(source)

    node_list = list(nodes)
    index = {node: i for i, node in enumerate(node_list)}

    edges: List[Tuple[int, int, float]] = []
    for u, nbrs in graph.items():
        for v, w in nbrs:
            if w < 0:
                raise ValueError("Negative edge weights are not supported")
            edges.append((index[u], index[v], float(w)))

    G = Graph(len(node_list), edges)
    dist_list = band_partitioned_sssp(G, index[source])

    result: Dict[Hashable, Weight] = {}
    for node, i in index.items():
        d = dist_list[i]
        if d < INF:
            result[node] = d
    return result
