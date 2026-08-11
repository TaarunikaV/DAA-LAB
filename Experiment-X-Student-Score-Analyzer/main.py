"""
Student Score Analyzer
------------------------
Real-world application of the Divide and Conquer Min-Max algorithm.

A teacher enters a class's marks and instantly finds the highest scorer
(topper) and lowest scorer using the Divide and Conquer Min-Max technique.
The tool also compares the number of comparisons used by the Divide and
Conquer method against the naive linear-scan method, and can run a
performance test on randomly generated datasets of increasing size
(exactly as in the original experiment).

Core algorithm (Divide and Conquer Min-Max) is kept exactly as in the
original experiment - only the surrounding application changes.
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------------------
# CORE ALGORITHM (Divide and Conquer Min-Max) - unchanged logic from experiment
# ---------------------------------------------------------------------------
comparison_count = 0  # Global counter


def min_max_dc(arr, low, high):
    global comparison_count
    # Base case: single element
    if low == high:
        return arr[low], arr[low]
    # Base case: two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Conquer: combine with 2 comparisons
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin
    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    mn, mx = arr[0], arr[0]
    comps = 0
    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x
        comps += 1
        if x > mx:
            mx = x
    return mn, mx, comps


# ---------------------------------------------------------------------------
# APPLICATION: Student Score Analyzer (Tkinter GUI)
# ---------------------------------------------------------------------------
class ScoreAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Score Analyzer - Divide & Conquer Min-Max")
        self.root.geometry("650x560")
        self.root.resizable(False, False)

        self._build_ui()

    # ---------------------------- UI LAYOUT ----------------------------
    def _build_ui(self):
        title = tk.Label(self.root, text="Student Score Analyzer",
                          font=("Arial", 16, "bold"))
        title.pack(pady=(10, 0))
        subtitle = tk.Label(self.root, text="Find Topper & Lowest Scorer using Divide & Conquer Min-Max",
                             font=("Arial", 10, "italic"), fg="gray")
        subtitle.pack(pady=(0, 10))

        # ---- Input Frame ----
        input_frame = tk.LabelFrame(self.root, text="Enter Class Marks", padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(input_frame, text="Marks (comma-separated):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.marks_entry = tk.Entry(input_frame, width=55)
        self.marks_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3)
        self.marks_entry.insert(0, "56, 78, 34, 90, 45, 67, 88, 23, 99, 61")

        tk.Button(input_frame, text="Analyze Marks", command=self.analyze_marks,
                  bg="#2b7de9", fg="white").grid(row=1, column=1, pady=8, sticky="w")
        tk.Button(input_frame, text="Generate Random Class (30 students)", command=self.generate_random,
                  bg="#555555", fg="white").grid(row=1, column=2, pady=8, padx=5, sticky="w")

        # ---- Result Frame ----
        result_frame = tk.LabelFrame(self.root, text="Analysis Result", padx=10, pady=10)
        result_frame.pack(fill="x", padx=15, pady=5)

        self.result_label = tk.Label(result_frame, text="Enter marks and click 'Analyze Marks'.",
                                      font=("Arial", 11), justify="left", fg="#1a1a1a")
        self.result_label.pack(anchor="w")

        self.compare_label = tk.Label(result_frame, text="", font=("Arial", 10), justify="left", fg="#2b5fb0")
        self.compare_label.pack(anchor="w", pady=(6, 0))

        # ---- Performance Test Frame ----
        perf_frame = tk.LabelFrame(self.root, text="Performance Test (Random Datasets)", padx=10, pady=10)
        perf_frame.pack(fill="both", expand=True, padx=15, pady=5)

        tk.Button(perf_frame, text="Run Performance Test (10 / 100 / 1000 / 10000 students)",
                  command=self.run_performance_test, bg="#238c23", fg="white").pack(anchor="w", pady=(0, 8))

        columns = ("Size", "D&C Comparisons", "Naive Comparisons", "Formula 3n/2 - 2")
        self.tree = ttk.Treeview(perf_frame, columns=columns, show="headings", height=5)
        for col in columns:
            self.tree.column(col, width=140, anchor="center")
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

    # ---------------------------- ACTIONS ----------------------------
    def _parse_marks(self, text):
        parts = [p.strip() for p in text.split(",") if p.strip() != ""]
        if len(parts) == 0:
            raise ValueError("Please enter at least one mark.")
        try:
            marks = [float(p) for p in parts]
        except ValueError:
            raise ValueError("Marks must be numbers, separated by commas.")
        return marks

    def analyze_marks(self):
        global comparison_count
        text = self.marks_entry.get()
        try:
            marks = self._parse_marks(text)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        comparison_count = 0
        mn, mx = min_max_dc(marks, 0, len(marks) - 1)
        dc_comps = comparison_count

        _, _, naive_comps = min_max_naive(marks)

        self.result_label.config(
            text=f"Number of Students: {len(marks)}\n"
                 f"Lowest Score: {mn}\n"
                 f"Topper's Score: {mx}"
        )
        self.compare_label.config(
            text=f"Divide & Conquer Comparisons: {dc_comps}    |    Naive Comparisons: {naive_comps}"
        )

    def generate_random(self):
        marks = [random.randint(0, 100) for _ in range(30)]
        self.marks_entry.delete(0, tk.END)
        self.marks_entry.insert(0, ", ".join(map(str, marks)))

    def run_performance_test(self):
        global comparison_count
        for row in self.tree.get_children():
            self.tree.delete(row)

        for size in [10, 100, 1000, 10000]:
            arr = [random.randint(1, 10000) for _ in range(size)]
            comparison_count = 0
            min_max_dc(arr, 0, len(arr) - 1)
            dc = comparison_count
            _, _, naive = min_max_naive(arr)
            formula = 3 * size // 2 - 2
            self.tree.insert("", tk.END, values=(size, dc, naive, formula))


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreAnalyzerApp(root)
    root.mainloop()
