# Practice 2 — Smoothing Filter vs. Edge Detector

**File:** `problem2_smoothing_and_edges.py`

## Problem
Apply two FIR filters to the same signal and interpret what each does:
- 3-point moving average `h_avg = {1/3, 1/3, 1/3}` → **smooths**
- first difference `h_diff = {1, -1}` (i.e. `y[n] = x[n] − x[n−1]`) → **detects edges**

Input: `x = {0,0, 1,1,1, 5, 1,1,1, 0,0}` — a flat step region with a spike at the middle.

## The idea
- **Averaging** replaces each sample with the mean of itself and its neighbours, so sharp
  changes get blurred and the spike is spread out and lowered.
- **Differencing** outputs zero wherever the signal is constant and a nonzero value only at
  a jump — a simple edge detector.

## How the code solves it
Both are just convolutions with the right impulse response:
```python
y_smooth = LTISystem(h_avg).output(x)
y_edge   = LTISystem(h_diff).output(x)
```
The transition indices are found with a **list comprehension + filter**:
```python
edges = [n for n in y_edge.times() if abs(y_edge.get_value_at_time(n)) > 1e-9]
```

## Expected output
```
x[n]       : 0, 0, 1, 1, 1, 5, 1, 1, 1, 0, 0
smoothed   : 0, 0, .333, .667, 1, 2.333, 2.333, 2.333, 1, .667, .333, 0, 0
edges (dx) : 0, 0, +1, 0, 0, +4, -4, 0, 0, -1, 0, 0
Transition indices detected: [2, 5, 6, 9]
```
The edge output is nonzero exactly at the rising edge (`+1` at n=2), both sides of the
spike (`+4`, `−4` at n=5,6), and the falling edge (`−1` at n=9). The spike (`5`) barely
moves the smoother because it is averaged with its small neighbours.

## Python notes
- `1/3` in Python 3 is true float division (`0.333…`), not integer division.
- `f"{v:+.3f}"` formats a number with a sign and 3 decimals — handy for lining up columns.
