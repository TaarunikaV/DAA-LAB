# Matrix Pipeline Cost Optimizer (Matrix Chain Multiplication - DP)

A small GUI application that finds the **cheapest order to multiply a chain
of matrices** (e.g. transformation matrices in a graphics/data pipeline)
using the **Matrix Chain Multiplication Dynamic Programming algorithm**.

## Main Features
- Enter matrix chain dimensions (p0, p1, ..., pn) and compute:
  - Minimum number of scalar multiplications needed.
  - Optimal parenthesization (multiplication order).
- Displays the list of matrices formed from the entered dimensions.
- Shows the full DP cost table `m[i][j]` used to derive the optimal order.
- "Load Example" button to quickly demo with a sample matrix chain.
- Simple error handling for invalid or insufficient input.

## How to Run
```
python main.py
```
Requires Python 3 with Tkinter (included in standard Python installation).

## Files Included
- `main.py` — Matrix Chain Multiplication DP implementation + Tkinter GUI application.
- `README.md` — This file.
