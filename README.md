# Single-Source Shortest Path Algorithms

This repository provides two reference implementations for computing shortest path
distances from a single source in directed graphs with non-negative edge weights:

1. **Dijkstra's Algorithm** – the classic approach that maintains a global
   priority queue and extracts the minimum tentative distance at each step.
2. **Band-Partitioned SSSP** – a research-inspired algorithm based on
   Duan–Mao–Mao–Shu–Yin (2025), *Breaking the Sorting Barrier for Directed
   Single-Source Shortest Paths*.  It avoids maintaining a total order on a large
   frontier by processing the graph in distance bands, performing limited
   Bellman–Ford relaxations within a band, and ordering only a reduced set of
   pivot vertices.

## Usage

```python
from sssp import dijkstra, band_sssp

# Graph represented as a mapping: node -> iterable of (neighbor, weight)
graph = {
    "A": [("B", 1), ("C", 4)],
    "B": [("C", 2), ("D", 5)],
    "C": [("D", 1)],
    "D": [],
}

print(dijkstra(graph, "A"))      # Classic algorithm
print(band_sssp(graph, "A"))     # Band-partitioned variant
```

## Testing

The test suite exercises both algorithms on a variety of challenging graphs,
including dense graphs, grids with random weights, graphs with zero-weight
edges, and randomly generated sparse graphs.

Install the required dependency and run the tests:

```bash
pip install networkx
pytest -q
```

## References

- Duan, Mao, Mao, Shu, Yin (2025). *Breaking the Sorting Barrier for Directed
  Single-Source Shortest Paths.*
- Dijkstra, E. W. (1959). *A note on two problems in connexion with graphs.*

