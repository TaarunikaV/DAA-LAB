# Delivery Route Planner (Dijkstra's Algorithm)

A small GUI application that finds the shortest delivery route between
locations on a delivery map using **Dijkstra's Single Source Shortest Path
Algorithm** (min-heap based).

## Main Features
- Find the shortest route and distance between any two locations.
- View shortest distances (and paths) from any hub location to all other
  locations on the map.
- Add new roads (edges) to the delivery map dynamically.
- View the current delivery map (adjacency list) at any time.
- Simple error handling for invalid or missing inputs.

## How to Run
```
python main.py
```
Requires Python 3 with Tkinter (included in standard Python installation).

## Files Included
- `main.py` — Dijkstra's algorithm implementation + Tkinter GUI application.
- `README.md` — This file.
