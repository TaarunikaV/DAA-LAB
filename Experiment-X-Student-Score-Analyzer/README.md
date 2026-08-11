# Student Score Analyzer (Divide & Conquer Min-Max)

A small GUI application that finds the **topper (highest mark)** and
**lowest scorer (lowest mark)** in a class using the **Divide and Conquer
Min-Max algorithm**, and compares its efficiency against the naive
linear-scan approach.

## Main Features
- Enter class marks (comma-separated) and instantly find the topper and
  lowest scorer.
- Generate a random class of 30 students for a quick demo.
- Shows Divide & Conquer comparison count vs Naive comparison count for
  the entered data.
- Run a performance test on random datasets of size 10, 100, 1000, and
  10000, comparing D&C comparisons, Naive comparisons, and the theoretical
  formula (3n/2 - 2).
- Simple error handling for invalid or empty input.

## How to Run
```
python main.py
```
Requires Python 3 with Tkinter (included in standard Python installation).

## Files Included
- `main.py` — Divide & Conquer Min-Max implementation + Tkinter GUI application.
- `README.md` — This file.
