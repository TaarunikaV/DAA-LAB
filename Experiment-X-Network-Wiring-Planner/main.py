"""
Minimum Cost Network Wiring Planner
------------------------------------
Given a set of locations (offices/buildings/computer labs) and the possible
cable-laying cost between pairs of locations, this tool finds the cheapest
way to connect ALL locations using Minimum Spanning Tree algorithms
(Kruskal's and Prim's).

Run: python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import time


# ============================================================
#  CORE DAA ALGORITHMS (unchanged logic from original experiment)
# ============================================================

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(n, edges):
    """edges: list of (weight, u, v)"""
    edges = sorted(edges)  # O(E log E)
    uf = UnionFind(n)
    mst = []
    cost = 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost


def prim(n, adj, start=0):
    """adj: adjacency list {u: [(v, w), ...]}"""
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0
    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost


# ============================================================
#  APPLICATION: Minimum Cost Network Wiring Planner
# ============================================================

class WiringPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimum Cost Network Wiring Planner")
        self.root.geometry("760x600")

        self.locations = []          # list of location names (index = node id)
        self.connections = []        # list of (weight, u, v)

        self.build_ui()
        self.load_sample_data()

    # ---------------- UI SETUP ----------------
    def build_ui(self):
        title = tk.Label(self.root, text="Minimum Cost Network Wiring Planner",
                          font=("Arial", 16, "bold"))
        title.pack(pady=8)

        subtitle = tk.Label(self.root,
                             text="Find the cheapest cabling layout that connects every location",
                             font=("Arial", 10))
        subtitle.pack()

        # ---- Location entry ----
        loc_frame = tk.LabelFrame(self.root, text="Step 1: Add Locations", padx=8, pady=8)
        loc_frame.pack(fill="x", padx=10, pady=6)

        self.loc_entry = tk.Entry(loc_frame, width=25)
        self.loc_entry.grid(row=0, column=0, padx=4)
        tk.Button(loc_frame, text="Add Location", command=self.add_location).grid(row=0, column=1, padx=4)
        tk.Button(loc_frame, text="Remove Last", command=self.remove_location).grid(row=0, column=2, padx=4)

        self.loc_listbox = tk.Listbox(loc_frame, height=4)
        self.loc_listbox.grid(row=1, column=0, columnspan=3, sticky="we", pady=6)

        # ---- Connection entry ----
        conn_frame = tk.LabelFrame(self.root, text="Step 2: Add Possible Cable Connections", padx=8, pady=8)
        conn_frame.pack(fill="x", padx=10, pady=6)

        tk.Label(conn_frame, text="From:").grid(row=0, column=0)
        self.from_box = ttk.Combobox(conn_frame, width=15, state="readonly")
        self.from_box.grid(row=0, column=1, padx=4)

        tk.Label(conn_frame, text="To:").grid(row=0, column=2)
        self.to_box = ttk.Combobox(conn_frame, width=15, state="readonly")
        self.to_box.grid(row=0, column=3, padx=4)

        tk.Label(conn_frame, text="Cost:").grid(row=0, column=4)
        self.cost_entry = tk.Entry(conn_frame, width=8)
        self.cost_entry.grid(row=0, column=5, padx=4)

        tk.Button(conn_frame, text="Add Connection", command=self.add_connection).grid(row=0, column=6, padx=6)

        self.conn_listbox = tk.Listbox(conn_frame, height=5)
        self.conn_listbox.grid(row=1, column=0, columnspan=7, sticky="we", pady=6)

        # ---- Action buttons ----
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=8)

        tk.Button(action_frame, text="Run Kruskal's Algorithm", width=22,
                  command=self.run_kruskal, bg="#cfe8ff").grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Run Prim's Algorithm", width=22,
                  command=self.run_prim, bg="#cfe8ff").grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Compare Both", width=22,
                  command=self.compare_both, bg="#ffe6b3").grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Clear All Data", width=15,
                  command=self.clear_all, bg="#ffcccc").grid(row=0, column=3, padx=5)

        # ---- Result display ----
        result_frame = tk.LabelFrame(self.root, text="Result", padx=8, pady=8)
        result_frame.pack(fill="both", expand=True, padx=10, pady=6)

        self.result_text = tk.Text(result_frame, height=14, font=("Consolas", 10))
        self.result_text.pack(fill="both", expand=True)

    # ---------------- SAMPLE DATA ----------------
    def load_sample_data(self):
        sample_locations = ["Office-A", "Office-B", "Office-C", "Office-D",
                             "Office-E", "Office-F", "Office-G"]
        sample_edges = [
            (7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3), (7, 1, 4),
            (5, 2, 4), (15, 3, 4), (6, 3, 5), (8, 4, 5), (9, 4, 6), (11, 5, 6)
        ]
        for loc in sample_locations:
            self.locations.append(loc)
            self.loc_listbox.insert(tk.END, loc)
        self.connections = sample_edges
        for w, u, v in sample_edges:
            self.conn_listbox.insert(
                tk.END, f"{self.locations[u]}  --  {self.locations[v]}   (Cost: {w})")
        self.refresh_comboboxes()

    # ---------------- LOCATION HANDLERS ----------------
    def refresh_comboboxes(self):
        self.from_box["values"] = self.locations
        self.to_box["values"] = self.locations

    def add_location(self):
        name = self.loc_entry.get().strip()
        if not name:
            messagebox.showerror("Invalid Input", "Please enter a location name.")
            return
        if name in self.locations:
            messagebox.showerror("Invalid Input", "This location already exists.")
            return
        self.locations.append(name)
        self.loc_listbox.insert(tk.END, name)
        self.loc_entry.delete(0, tk.END)
        self.refresh_comboboxes()

    def remove_location(self):
        if not self.locations:
            return
        removed_index = len(self.locations) - 1
        self.locations.pop()
        self.loc_listbox.delete(tk.END)
        # Remove any connections referencing the removed node
        self.connections = [c for c in self.connections
                             if c[1] != removed_index and c[2] != removed_index]
        self.conn_listbox.delete(0, tk.END)
        for w, u, v in self.connections:
            self.conn_listbox.insert(
                tk.END, f"{self.locations[u]}  --  {self.locations[v]}   (Cost: {w})")
        self.refresh_comboboxes()

    # ---------------- CONNECTION HANDLERS ----------------
    def add_connection(self):
        frm = self.from_box.get()
        to = self.to_box.get()
        cost_str = self.cost_entry.get().strip()

        if not frm or not to:
            messagebox.showerror("Invalid Input", "Please select both locations.")
            return
        if frm == to:
            messagebox.showerror("Invalid Input", "From and To locations must differ.")
            return
        if not cost_str.isdigit():
            messagebox.showerror("Invalid Input", "Cost must be a positive whole number.")
            return

        u = self.locations.index(frm)
        v = self.locations.index(to)
        w = int(cost_str)

        self.connections.append((w, u, v))
        self.conn_listbox.insert(tk.END, f"{frm}  --  {to}   (Cost: {w})")
        self.cost_entry.delete(0, tk.END)

    # ---------------- ALGORITHM RUNNERS ----------------
    def get_graph_data(self):
        n = len(self.locations)
        edges = list(self.connections)
        adj = {}
        for w, u, v in edges:
            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))
        return n, edges, adj

    def validate_graph(self):
        if len(self.locations) < 2:
            messagebox.showerror("Not Enough Data", "Add at least 2 locations.")
            return False
        if not self.connections:
            messagebox.showerror("Not Enough Data", "Add at least 1 connection.")
            return False
        return True

    def format_mst(self, mst, cost, algo_name, elapsed):
        lines = [f"=== {algo_name} MST Result ===\n"]
        for u, v, w in mst:
            lines.append(f"  {self.locations[u]:<12} --  {self.locations[v]:<12} Cost: {w}")
        lines.append(f"\n  Total Minimum Wiring Cost: {cost}")
        lines.append(f"  Time Taken: {elapsed:.6f} seconds")
        n = len(self.locations)
        if len(mst) < n - 1:
            lines.append("\n  WARNING: Graph is disconnected — some locations "
                          "cannot be reached with current connections.")
        return "\n".join(lines)

    def run_kruskal(self):
        if not self.validate_graph():
            return
        n, edges, _ = self.get_graph_data()
        start = time.perf_counter()
        mst, cost = kruskal(n, edges)
        elapsed = time.perf_counter() - start
        self.show_result(self.format_mst(mst, cost, "Kruskal's Algorithm", elapsed))

    def run_prim(self):
        if not self.validate_graph():
            return
        n, _, adj = self.get_graph_data()
        start = time.perf_counter()
        mst, cost = prim(n, adj, start=0)
        elapsed = time.perf_counter() - start
        self.show_result(self.format_mst(mst, cost, "Prim's Algorithm", elapsed))

    def compare_both(self):
        if not self.validate_graph():
            return
        n, edges, adj = self.get_graph_data()

        t1 = time.perf_counter()
        k_mst, k_cost = kruskal(n, edges)
        k_time = time.perf_counter() - t1

        t2 = time.perf_counter()
        p_mst, p_cost = prim(n, adj, start=0)
        p_time = time.perf_counter() - t2

        lines = ["=== Performance & Cost Comparison ===\n"]
        lines.append(f"  Kruskal's Algorithm -> Cost: {k_cost:<6} Time: {k_time:.6f} s")
        lines.append(f"  Prim's Algorithm    -> Cost: {p_cost:<6} Time: {p_time:.6f} s\n")

        if k_cost == p_cost:
            lines.append("  Both algorithms produced the SAME minimum cost (as expected).")
        else:
            lines.append("  NOTE: Costs differ - check if graph is disconnected.")

        faster = "Kruskal's" if k_time < p_time else ("Prim's" if p_time < k_time else "Both equal")
        lines.append(f"  Faster on this run: {faster}\n")

        lines.append("  --- Kruskal's MST Edges ---")
        for u, v, w in k_mst:
            lines.append(f"    {self.locations[u]} -- {self.locations[v]}  (Cost: {w})")

        lines.append("\n  --- Prim's MST Edges ---")
        for u, v, w in p_mst:
            lines.append(f"    {self.locations[u]} -- {self.locations[v]}  (Cost: {w})")

        self.show_result("\n".join(lines))

    def clear_all(self):
        self.locations = []
        self.connections = []
        self.loc_listbox.delete(0, tk.END)
        self.conn_listbox.delete(0, tk.END)
        self.refresh_comboboxes()
        self.result_text.delete("1.0", tk.END)

    def show_result(self, text):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)


# ============================================================
#  MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = WiringPlannerApp(root)
    root.mainloop()
