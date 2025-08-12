# Single-Source Shortest Path Algorithms

This repository contains two implementations for the single-source shortest path (SSSP) problem on directed graphs with non-negative weights:

* **Dijkstra** – the classic algorithm using a priority queue
* **Band-partitioned SSSP** – an experimental implementation inspired by Duan–Mao–Mao–Shu–Yin (2025) that performs k-round relaxations within distance bands to avoid maintaining a large global order

## Running the tests

Tests rely on `pytest` and require `networkx` for reference distances.
Install the dependency and run the suite:

```bash
pip install networkx
pytest -q
```

Expected output (truncated):

```
13 passed in 0.19s
```

The exact timing may vary, but all tests should pass.

