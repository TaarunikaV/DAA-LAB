"""
Delivery Route Planner
-----------------------
Real-world application of Dijkstra's Single Source Shortest Path Algorithm.

A delivery company has several locations (warehouse, stores, customer areas)
connected by roads with distances. This tool finds the shortest delivery
route (and its distance) between any two locations, and can also show the
shortest distance from a chosen hub to every other location on the map.

Core algorithm (Dijkstra using a min-heap) is kept exactly as in the
original experiment - only the surrounding application changes.
"""

import heapq
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------------------
# CORE ALGORITHM (Dijkstra's Shortest Path) - unchanged logic from experiment
# ---------------------------------------------------------------------------
def dijkstra(graph, source):
    """
    graph: dict {location: [(neighbor, weight), ...]}
    Returns: dist (dict location -> shortest distance),
             prev (dict location -> previous location on shortest path)
    Time: O((V + E) log V), Space: O(V)
    """
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0
    pq = [(0, source)]          # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path and path[0] == source:
        return path
    return []


# ---------------------------------------------------------------------------
# APPLICATION: Delivery Route Planner (Tkinter GUI)
# ---------------------------------------------------------------------------
class RoutePlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Route Planner - Dijkstra's Algorithm")
        self.root.geometry("650x560")
        self.root.resizable(False, False)

        # Default city/delivery map (adjacency list: location -> [(neighbor, distance_km), ...])
        self.graph = {
            "Warehouse": [("Store A", 4), ("Store B", 1)],
            "Store A":   [("Mall", 1)],
            "Store B":   [("Store A", 2), ("Mall", 5)],
            "Mall":      [("Hospital", 3)],
            "Hospital":  [("Airport", 2)],
            "Airport":   [],
        }

        self._build_ui()

    # ---------------------------- UI LAYOUT ----------------------------
    def _build_ui(self):
        title = tk.Label(self.root, text="Delivery Route Planner",
                          font=("Arial", 16, "bold"))
        title.pack(pady=(10, 0))
        subtitle = tk.Label(self.root, text="Shortest Route Finder using Dijkstra's Algorithm",
                             font=("Arial", 10, "italic"), fg="gray")
        subtitle.pack(pady=(0, 10))

        # ---- Route Finder Frame ----
        route_frame = tk.LabelFrame(self.root, text="Find Shortest Route", padx=10, pady=10)
        route_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(route_frame, text="From:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.source_var = tk.StringVar()
        self.source_menu = ttk.Combobox(route_frame, textvariable=self.source_var,
                                         values=list(self.graph.keys()), state="readonly", width=15)
        self.source_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(route_frame, text="To:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_menu = ttk.Combobox(route_frame, textvariable=self.dest_var,
                                       values=list(self.graph.keys()), state="readonly", width=15)
        self.dest_menu.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(route_frame, text="Find Shortest Route", command=self.find_route,
                  bg="#2b7de9", fg="white").grid(row=0, column=4, padx=10)

        self.route_result = tk.Label(route_frame, text="", font=("Arial", 10, "bold"),
                                      fg="#1a7a1a", justify="left")
        self.route_result.grid(row=1, column=0, columnspan=5, sticky="w", pady=(8, 0))

        # ---- All Distances Frame ----
        all_frame = tk.LabelFrame(self.root, text="All Shortest Distances From a Hub", padx=10, pady=10)
        all_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(all_frame, text="Hub Location:").grid(row=0, column=0, sticky="w", padx=5)
        self.hub_var = tk.StringVar()
        self.hub_menu = ttk.Combobox(all_frame, textvariable=self.hub_var,
                                      values=list(self.graph.keys()), state="readonly", width=15)
        self.hub_menu.grid(row=0, column=1, padx=5)

        tk.Button(all_frame, text="Show All Distances", command=self.show_all_distances,
                  bg="#2b7de9", fg="white").grid(row=0, column=2, padx=10)

        columns = ("Location", "Distance (km)", "Route")
        self.tree = ttk.Treeview(all_frame, columns=columns, show="headings", height=6)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180 if col == "Route" else 110, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=3, pady=8)

        # ---- Add Road Frame ----
        add_frame = tk.LabelFrame(self.root, text="Add a New Road (updates map)", padx=10, pady=10)
        add_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(add_frame, text="From:").grid(row=0, column=0, padx=5, pady=3)
        self.new_from = tk.Entry(add_frame, width=12)
        self.new_from.grid(row=0, column=1, padx=5)

        tk.Label(add_frame, text="To:").grid(row=0, column=2, padx=5)
        self.new_to = tk.Entry(add_frame, width=12)
        self.new_to.grid(row=0, column=3, padx=5)

        tk.Label(add_frame, text="Distance (km):").grid(row=0, column=4, padx=5)
        self.new_dist = tk.Entry(add_frame, width=8)
        self.new_dist.grid(row=0, column=5, padx=5)

        tk.Button(add_frame, text="Add Road", command=self.add_road,
                  bg="#238c23", fg="white").grid(row=0, column=6, padx=10)

        # ---- Map View ----
        map_frame = tk.LabelFrame(self.root, text="Current Delivery Map (Roads)", padx=10, pady=10)
        map_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.map_text = tk.Text(map_frame, height=7, font=("Consolas", 10))
        self.map_text.pack(fill="both", expand=True)
        self.refresh_map_view()

    # ---------------------------- ACTIONS ----------------------------
    def refresh_dropdowns(self):
        locations = list(self.graph.keys())
        self.source_menu["values"] = locations
        self.dest_menu["values"] = locations
        self.hub_menu["values"] = locations

    def refresh_map_view(self):
        self.map_text.delete("1.0", tk.END)
        for loc, edges in self.graph.items():
            if edges:
                road_list = ", ".join(f"{n} ({w} km)" for n, w in edges)
            else:
                road_list = "(no outgoing roads)"
            self.map_text.insert(tk.END, f"{loc:<12} -> {road_list}\n")

    def find_route(self):
        src, dst = self.source_var.get(), self.dest_var.get()
        if not src or not dst:
            messagebox.showerror("Input Error", "Please select both From and To locations.")
            return
        if src == dst:
            messagebox.showerror("Input Error", "From and To locations must be different.")
            return

        dist, prev = dijkstra(self.graph, src)
        path = reconstruct_path(prev, src, dst)

        if not path:
            self.route_result.config(
                text=f"No route exists from {src} to {dst}.", fg="#b03030")
        else:
            self.route_result.config(
                text=f"Shortest Route: {' -> '.join(path)}\nTotal Distance: {dist[dst]} km",
                fg="#1a7a1a")

    def show_all_distances(self):
        hub = self.hub_var.get()
        if not hub:
            messagebox.showerror("Input Error", "Please select a hub location.")
            return

        dist, prev = dijkstra(self.graph, hub)
        for row in self.tree.get_children():
            self.tree.delete(row)

        for loc in self.graph:
            path = reconstruct_path(prev, hub, loc)
            path_str = " -> ".join(path) if path else "No path"
            d = dist[loc] if dist[loc] != float('inf') else "INF"
            self.tree.insert("", tk.END, values=(loc, d, path_str))

    def add_road(self):
        frm = self.new_from.get().strip()
        to = self.new_to.get().strip()
        dist_str = self.new_dist.get().strip()

        if not frm or not to or not dist_str:
            messagebox.showerror("Input Error", "Please fill in From, To and Distance.")
            return
        if frm == to:
            messagebox.showerror("Input Error", "From and To locations must be different.")
            return
        try:
            weight = float(dist_str)
            if weight <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Distance must be a positive number.")
            return

        self.graph.setdefault(frm, [])
        self.graph.setdefault(to, [])
        self.graph[frm].append((to, weight))

        self.refresh_dropdowns()
        self.refresh_map_view()
        self.new_from.delete(0, tk.END)
        self.new_to.delete(0, tk.END)
        self.new_dist.delete(0, tk.END)
        messagebox.showinfo("Success", f"Road added: {frm} -> {to} ({weight} km)")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RoutePlannerApp(root)
    root.mainloop()
