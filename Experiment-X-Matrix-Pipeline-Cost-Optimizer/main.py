"""
Matrix Pipeline Cost Optimizer
---------------------------------
Real-world application of Matrix Chain Multiplication (Dynamic Programming).

Graphics, image-processing and data-analytics pipelines often need to
multiply a long chain of matrices (e.g. transformation matrices, feature
maps). Multiplying them in different orders gives the same final result
but a very different number of scalar multiplications - and therefore very
different running time. This tool finds the cheapest order to multiply a
given chain of matrices, using the DP technique from the experiment.

Core algorithm (Matrix Chain Order DP) is kept exactly as in the original
experiment - only the surrounding application changes.
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------------------
# CORE ALGORITHM (Matrix Chain Multiplication - DP) - unchanged from experiment
# ---------------------------------------------------------------------------
def matrix_chain_order(dims):
    """
    dims: list of dimensions, matrix i has dims[i-1] x dims[i]
    Time: O(n^3), Space: O(n^2)
    """
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        return f'A{i}'
    k = s[i][j]
    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)
    return f'({left} x {right})'


# ---------------------------------------------------------------------------
# APPLICATION: Matrix Pipeline Cost Optimizer (Tkinter GUI)
# ---------------------------------------------------------------------------
class MatrixPipelineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Pipeline Cost Optimizer - Matrix Chain Multiplication (DP)")
        self.root.geometry("700x580")
        self.root.resizable(False, False)

        self._build_ui()

    # ---------------------------- UI LAYOUT ----------------------------
    def _build_ui(self):
        title = tk.Label(self.root, text="Matrix Pipeline Cost Optimizer",
                          font=("Arial", 16, "bold"))
        title.pack(pady=(10, 0))
        subtitle = tk.Label(self.root,
                             text="Find the Cheapest Multiplication Order for a Matrix Chain (DP)",
                             font=("Arial", 10, "italic"), fg="gray")
        subtitle.pack(pady=(0, 10))

        # ---- Input Frame ----
        input_frame = tk.LabelFrame(self.root, text="Matrix Chain Dimensions", padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(input_frame,
                 text="Enter dimensions p0, p1, p2 ... pn\n(matrix Ai has size p(i-1) x pi):"
                 ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.dims_entry = tk.Entry(input_frame, width=45)
        self.dims_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dims_entry.insert(0, "10, 30, 5, 60, 10")

        tk.Button(input_frame, text="Compute Optimal Order", command=self.compute_order,
                  bg="#2b7de9", fg="white").grid(row=1, column=1, padx=10)
        tk.Button(input_frame, text="Load Example", command=self.load_example,
                  bg="#555555", fg="white").grid(row=1, column=2, padx=5)

        # ---- Matrix List Frame ----
        self.matrix_list_label = tk.Label(input_frame, text="", font=("Consolas", 9), justify="left", fg="#333")
        self.matrix_list_label.grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 0))

        # ---- Result Frame ----
        result_frame = tk.LabelFrame(self.root, text="Optimal Result", padx=10, pady=10)
        result_frame.pack(fill="x", padx=15, pady=5)

        self.result_label = tk.Label(result_frame, text="Enter dimensions and click 'Compute Optimal Order'.",
                                      font=("Arial", 11, "bold"), fg="#1a7a1a", justify="left", wraplength=650)
        self.result_label.pack(anchor="w")

        # ---- DP Table Frame ----
        table_frame = tk.LabelFrame(self.root, text="DP Cost Table m[i][j] (Min. Scalar Multiplications)",
                                     padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(table_frame, show="headings", height=8)
        self.tree.pack(fill="both", expand=True)

    # ---------------------------- ACTIONS ----------------------------
    def _parse_dims(self, text):
        parts = [p.strip() for p in text.split(",") if p.strip() != ""]
        if len(parts) < 3:
            raise ValueError("Enter at least 3 dimensions (for at least 2 matrices).")
        try:
            dims = [int(p) for p in parts]
        except ValueError:
            raise ValueError("Dimensions must be whole numbers, separated by commas.")
        if any(d <= 0 for d in dims):
            raise ValueError("Dimensions must be positive numbers.")
        return dims

    def load_example(self):
        self.dims_entry.delete(0, tk.END)
        self.dims_entry.insert(0, "10, 30, 5, 60, 10")

    def compute_order(self):
        text = self.dims_entry.get()
        try:
            dims = self._parse_dims(text)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        n = len(dims) - 1  # number of matrices

        # Show matrix list
        lines = [f"A{i + 1}: {dims[i]} x {dims[i + 1]}" for i in range(n)]
        self.matrix_list_label.config(text="Matrices in the chain:\n" + "   ".join(lines))

        m, s = matrix_chain_order(dims)
        min_cost = m[1][n]
        order = print_optimal_parens(s, 1, n)

        self.result_label.config(
            text=f"Minimum Scalar Multiplications Needed: {min_cost}\n"
                 f"Optimal Multiplication Order: {order}"
        )

        self._fill_table(m, n)

    def _fill_table(self, m, n):
        columns = ["Ai"] + [f"A{j}" for j in range(1, n + 1)]
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        for col in columns:
            self.tree.column(col, width=70, anchor="center")
            self.tree.heading(col, text=col)

        for i in range(1, n + 1):
            row = [f"A{i}"]
            for j in range(1, n + 1):
                if j < i:
                    row.append("---")
                else:
                    row.append(m[i][j])
            self.tree.insert("", tk.END, values=row)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixPipelineApp(root)
    root.mainloop()
