# Minimum Cost Network Wiring Planner

A small Tkinter desktop application that uses **Kruskal's** and **Prim's**
Minimum Spanning Tree algorithms to find the cheapest way to connect a set
of locations (offices, buildings, or computer labs) with network/cable
wiring.

## Main Features
- Add locations (nodes) and possible cable connections with cost (edges).
- Run **Kruskal's Algorithm** to compute the minimum wiring cost.
- Run **Prim's Algorithm** to compute the minimum wiring cost.
- **Compare Both** algorithms side-by-side — shows cost, execution time,
  and the MST edges produced by each.
- Preloaded with a sample 7-location network for instant demonstration.
- Simple input validation with clear error messages.
- Detects disconnected graphs and warns the user.

## How to Run
```
python main.py
```
Requires only the Python standard library (`tkinter`, `heapq`, `time`).

## Files Included
- `main.py` – Complete application (algorithms + GUI)
- `README.md` – This file
