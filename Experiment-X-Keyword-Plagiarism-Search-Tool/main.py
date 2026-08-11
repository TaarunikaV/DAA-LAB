"""
Keyword & Plagiarism Search Tool
---------------------------------
A small desktop application that searches a document for occurrences of a
keyword/phrase using three classic string matching algorithms:
Naive Search, KMP (Knuth-Morris-Pratt), and Rabin-Karp.

Useful as a mini plagiarism/keyword checker: paste any document, search for
a suspicious phrase, and see exactly where it appears plus how each
algorithm performs.

Run with: python main.py
"""

import time
import random
import tkinter as tk
from tkinter import messagebox


# ---------------------------------------------------------------------
# CORE ALGORITHMS (unchanged logic from the original DAA experiment)
# ---------------------------------------------------------------------

def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comparisons


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)
    d = 256
    h = pow(d, m - 1, q)
    p_hash = t_hash = 0
    matches, comparisons = [], 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)
        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# ---------------------------------------------------------------------
# SAMPLE DOCUMENT
# ---------------------------------------------------------------------

SAMPLE_TEXT = (
    "Data structures and algorithms form the foundation of efficient software "
    "design. String matching algorithms are widely used in plagiarism detection "
    "systems, search engines, and text editors. The naive approach checks every "
    "position in the text, while smarter algorithms like KMP and Rabin-Karp avoid "
    "unnecessary comparisons by preprocessing the pattern. Plagiarism detection "
    "tools often scan documents for repeated phrases such as data structures and "
    "algorithms to flag copied content. Efficient string matching makes such tools "
    "practical even on large documents."
)


# ---------------------------------------------------------------------
# GUI APPLICATION
# ---------------------------------------------------------------------

class KeywordSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyword & Plagiarism Search Tool - String Matching")
        self.root.geometry("800x640")
        self.root.resizable(False, False)

        self._build_widgets()

    # ---------------- UI construction ----------------
    def _build_widgets(self):
        title = tk.Label(self.root, text="Keyword & Plagiarism Search Tool",
                          font=("Segoe UI", 16, "bold"))
        title.pack(pady=8)

        subtitle = tk.Label(self.root,
                             text="Core algorithms: Naive Search, KMP, Rabin-Karp",
                             font=("Segoe UI", 9))
        subtitle.pack()

        # ---- Document input ----
        doc_label = tk.Label(self.root, text="Document Text:", font=("Segoe UI", 10, "bold"))
        doc_label.pack(anchor="w", padx=15, pady=(10, 0))

        self.doc_text = tk.Text(self.root, height=9, width=95, font=("Consolas", 10), wrap="word")
        self.doc_text.pack(padx=15, pady=5)
        self.doc_text.insert(tk.END, SAMPLE_TEXT)

        tk.Button(self.root, text="Load Sample Text", command=self.load_sample,
                  bg="#616161", fg="white").pack(pady=(0, 5))

        # ---- Pattern input ----
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Keyword / Phrase to Search:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
        self.pattern_entry = tk.Entry(search_frame, width=30, font=("Segoe UI", 10))
        self.pattern_entry.grid(row=0, column=1, padx=5)
        self.pattern_entry.insert(0, "data structures and algorithms")

        tk.Button(search_frame, text="Search Document", command=self.search_document,
                  bg="#2e7d32", fg="white").grid(row=0, column=2, padx=5)

        # ---- Result box ----
        self.result_text = tk.Text(self.root, height=9, width=95, font=("Consolas", 10), bg="#f4f4f4")
        self.result_text.pack(pady=8)
        self.result_text.config(state="disabled")

        # ---- Performance analysis button ----
        tk.Button(self.root, text="Run Performance Analysis (large random text, multiple patterns)",
                  command=self.run_performance_analysis, bg="#6a1b9a", fg="white").pack(pady=5)

    # ---------------- Helpers ----------------
    def load_sample(self):
        self.doc_text.delete("1.0", tk.END)
        self.doc_text.insert(tk.END, SAMPLE_TEXT)

    def _show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def _get_inputs(self):
        doc = self.doc_text.get("1.0", tk.END).rstrip("\n")
        pattern = self.pattern_entry.get()

        if not doc.strip():
            messagebox.showerror("Input Error", "Document text cannot be empty.")
            return None, None
        if not pattern:
            messagebox.showerror("Input Error", "Please enter a keyword/phrase to search.")
            return None, None
        if len(pattern) > len(doc):
            messagebox.showerror("Input Error", "Pattern cannot be longer than the document.")
            return None, None

        return doc, pattern

    # ---------------- Actions ----------------
    def search_document(self):
        doc, pattern = self._get_inputs()
        if doc is None:
            return

        results = []
        for name, func in (("Naive Search", naive_search),
                            ("KMP", kmp_search),
                            ("Rabin-Karp", rabin_karp)):
            start = time.perf_counter()
            matches, comparisons = func(doc, pattern)
            elapsed_ms = (time.perf_counter() - start) * 1000
            results.append((name, matches, comparisons, elapsed_ms))

        lines = [f"Document length: {len(doc)} characters",
                 f"Pattern searched: \"{pattern}\"  (length {len(pattern)})",
                 "-" * 70]

        naive_matches = results[0][1]
        if naive_matches:
            lines.append(f"Occurrences found at positions: {naive_matches}")
            lines.append(f"Total occurrences: {len(naive_matches)}")
        else:
            lines.append("No occurrences found in the document.")

        lines.append("-" * 70)
        lines.append(f"{'Algorithm':<16}{'Matches':<10}{'Comparisons':<14}{'Time (ms)':<12}")
        for name, matches, comparisons, elapsed_ms in results:
            lines.append(f"{name:<16}{len(matches):<10}{comparisons:<14}{elapsed_ms:<12.5f}")

        self._show_result("\n".join(lines))

    def run_performance_analysis(self):
        text_large = ''.join(random.choices('ABCD', k=10000))
        patterns = ['AB', 'ABCD', 'ABCDAB', 'ABCDABCD']

        lines = [
            "PERFORMANCE ANALYSIS: Naive vs KMP vs Rabin-Karp",
            "(random 10,000-character text, varying pattern lengths)",
            "-" * 60,
            f"{'Pattern':>14}{'Naive':>12}{'KMP':>12}{'Rabin-Karp':>14}"
        ]

        for p in patterns:
            _, c1 = naive_search(text_large, p)
            _, c2 = kmp_search(text_large, p)
            _, c3 = rabin_karp(text_large, p)
            lines.append(f"{p:>14}{c1:>12}{c2:>12}{c3:>14}")

        lines.append("-" * 60)
        lines.append("Values shown are character comparisons made by each algorithm.")

        self._show_result("\n".join(lines))


# ---------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = KeywordSearchApp(root)
    root.mainloop()
