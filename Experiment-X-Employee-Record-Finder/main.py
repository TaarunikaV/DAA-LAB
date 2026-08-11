"""
Employee Record Finder
-----------------------
A small desktop application that uses Interpolation Search to quickly
locate an employee by their Employee ID from a large, sorted database.
Binary Search is included for performance comparison, exactly as in the
original experiment.

Run with: python main.py
"""

import time
import random
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------------
# CORE ALGORITHMS (unchanged logic from the original DAA experiment)
# ---------------------------------------------------------------------

def interpolation_search(arr, target):
    """
    Interpolation Search Algorithm
    Time Complexity: O(log log n) average, O(n) worst case
    Space Complexity: O(1)
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


def binary_search(arr, target):
    """Binary Search for comparison"""
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


# ---------------------------------------------------------------------
# EMPLOYEE DATABASE (in-memory, sorted by Employee ID)
# ---------------------------------------------------------------------

FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Ananya", "Diya", "Ishaan",
               "Kavya", "Meera", "Rohan", "Sara", "Vihaan", "Zara",
               "Kabir", "Anika", "Dev", "Riya"]
DEPARTMENTS = ["HR", "Finance", "IT", "Sales", "Operations", "Marketing"]


def generate_employees(n):
    """Generate n unique employees, sorted by Employee ID."""
    ids = sorted(random.sample(range(1000, 1000 + n * 10), n))
    employees = []
    for emp_id in ids:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(['Sharma','Patel','Reddy','Nair','Iyer','Khan'])}"
        dept = random.choice(DEPARTMENTS)
        employees.append({"id": emp_id, "name": name, "dept": dept})
    return employees


# ---------------------------------------------------------------------
# GUI APPLICATION
# ---------------------------------------------------------------------

class EmployeeFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Record Finder - Interpolation Search")
        self.root.geometry("760x560")
        self.root.resizable(False, False)

        self.employees = generate_employees(500)
        self.id_array = [e["id"] for e in self.employees]
        self.id_to_employee = {e["id"]: e for e in self.employees}

        self._build_widgets()
        self._populate_table()

    # ---------------- UI construction ----------------
    def _build_widgets(self):
        title = tk.Label(self.root, text="Employee Record Finder",
                          font=("Segoe UI", 16, "bold"))
        title.pack(pady=8)

        subtitle = tk.Label(self.root,
                             text=f"Database size: {len(self.employees)} employees "
                                  f"(sorted by Employee ID) | Core: Interpolation Search",
                             font=("Segoe UI", 9))
        subtitle.pack()

        # ---- Search bar ----
        search_frame = tk.Frame(self.root, pady=10)
        search_frame.pack()

        tk.Label(search_frame, text="Enter Employee ID:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
        self.id_entry = tk.Entry(search_frame, width=15, font=("Segoe UI", 10))
        self.id_entry.grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="Search (Interpolation)", command=self.search_employee,
                  bg="#2e7d32", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Compare with Binary Search", command=self.compare_search,
                  bg="#1565c0", fg="white").grid(row=0, column=3, padx=5)

        sample_hint = tk.Label(self.root,
                                text=f"Try an ID from the table below, e.g. {self.employees[len(self.employees)//2]['id']}",
                                font=("Segoe UI", 8, "italic"), fg="gray")
        sample_hint.pack()

        # ---- Result box ----
        self.result_text = tk.Text(self.root, height=6, width=90, font=("Consolas", 10),
                                    bg="#f4f4f4")
        self.result_text.pack(pady=8)
        self.result_text.config(state="disabled")

        # ---- Performance analysis button ----
        perf_frame = tk.Frame(self.root)
        perf_frame.pack(pady=2)
        tk.Button(perf_frame, text="Run Performance Analysis (Interpolation vs Binary)",
                  command=self.run_performance_analysis, bg="#6a1b9a", fg="white").pack()

        # ---- Employee table ----
        table_label = tk.Label(self.root, text="Employee Database (sample view)", font=("Segoe UI", 10, "bold"))
        table_label.pack(pady=(10, 2))

        columns = ("id", "name", "dept")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="Employee ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("dept", text="Department")
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("name", width=280, anchor="w")
        self.tree.column("dept", width=150, anchor="center")
        self.tree.pack(pady=5)

    def _populate_table(self):
        # Show a readable sample (first 30 records) so the table isn't huge
        for emp in self.employees[:30]:
            self.tree.insert("", "end", values=(emp["id"], emp["name"], emp["dept"]))

    # ---------------- Helper ----------------
    def _get_target_id(self):
        raw = self.id_entry.get().strip()
        if not raw:
            messagebox.showerror("Input Error", "Please enter an Employee ID.")
            return None
        if not raw.isdigit():
            messagebox.showerror("Input Error", "Employee ID must be a positive integer.")
            return None
        return int(raw)

    def _show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    # ---------------- Actions ----------------
    def search_employee(self):
        target = self._get_target_id()
        if target is None:
            return

        start = time.perf_counter()
        index, comparisons = interpolation_search(self.id_array, target)
        elapsed_ms = (time.perf_counter() - start) * 1000

        if index == -1:
            self._show_result(f"Employee ID {target} NOT FOUND.\n"
                               f"Comparisons made: {comparisons}\n"
                               f"Time taken: {elapsed_ms:.5f} ms")
            return

        emp = self.id_to_employee[target]
        self._show_result(
            "RECORD FOUND (Interpolation Search)\n"
            "-------------------------------------\n"
            f"Employee ID : {emp['id']}\n"
            f"Name        : {emp['name']}\n"
            f"Department  : {emp['dept']}\n"
            f"Array Index : {index}\n"
            f"Comparisons : {comparisons}\n"
            f"Time taken  : {elapsed_ms:.5f} ms"
        )

    def compare_search(self):
        target = self._get_target_id()
        if target is None:
            return

        start = time.perf_counter()
        idx_is, comp_is = interpolation_search(self.id_array, target)
        is_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        idx_bs, comp_bs = binary_search(self.id_array, target)
        bs_time = (time.perf_counter() - start) * 1000

        found_text = "NOT FOUND" if idx_is == -1 else f"FOUND at index {idx_is}"

        self._show_result(
            "SEARCH COMPARISON\n"
            "-------------------------------------\n"
            f"Target Employee ID : {target}  ({found_text})\n\n"
            f"{'Algorithm':<22}{'Comparisons':<15}{'Time (ms)':<12}\n"
            f"{'Interpolation Search':<22}{comp_is:<15}{is_time:<12.5f}\n"
            f"{'Binary Search':<22}{comp_bs:<15}{bs_time:<12.5f}\n"
        )

    def run_performance_analysis(self):
        sizes = [500, 2000, 5000, 20000, 50000]
        lines = [
            "PERFORMANCE ANALYSIS: Interpolation Search vs Binary Search",
            "(datasets simulate growing employee databases)",
            "-" * 70,
            f"{'Size':>8}{'IS Time(ms)':>15}{'BS Time(ms)':>15}{'IS Comp':>12}{'BS Comp':>12}"
        ]

        for size in sizes:
            arr = sorted(random.sample(range(size * 10), size))
            target = arr[random.randint(0, size - 1)]

            start = time.perf_counter()
            for _ in range(50):
                idx_is, comp_is = interpolation_search(arr, target)
            is_time = (time.perf_counter() - start) / 50 * 1000

            start = time.perf_counter()
            for _ in range(50):
                idx_bs, comp_bs = binary_search(arr, target)
            bs_time = (time.perf_counter() - start) / 50 * 1000

            lines.append(f"{size:>8}{is_time:>15.5f}{bs_time:>15.5f}{comp_is:>12}{comp_bs:>12}")

        self._show_result("\n".join(lines))


# ---------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeFinderApp(root)
    root.mainloop()
