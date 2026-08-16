# Practice 1 — Basic Convolution ("Flip and Slide")

**File:** `problem1_basic_convolution.py`

## Problem
Given `x[n] = {1, 2, 3}` (from `n=0`) and `h[n] = {1, 1, 1}` (from `n=0`), compute
`y[n] = (x * h)[n]`. Do it with `LTISystem.output` **and** by hand, and confirm they match.

## The convolution sum
```
y[n] = Σ_k  x[k] · h[n - k]
```
For each output index `n` you flip `h` in time, slide it to position `n`, multiply
overlapping samples, and add. If `x` covers `[a, b]` and `h` covers `[c, d]`, then `y`
covers `[a+c, b+d]` — here `[0,2] + [0,2] = [0,4]`, so `y` has 5 samples.

## How the code solves it
`manual_convolution` implements the sum with two loops — the outer over output index `n`,
the inner over `k`:
```python
for n in range(n_min, n_max + 1):
    total = 0.0
    for k in range(x.start_time, x.end_time + 1):
        total += x.get_value_at_time(k) * h.get_value_at_time(n - k)
    y.set_value_at_time(n, total)
```
`get_value_at_time` returns `0.0` outside a signal's range, so you never index out of
bounds — the "flip and slide" edges are handled automatically.

## Expected output
```
y[n] (library): [1.0, 3.0, 6.0, 5.0, 3.0]
y[n] (manual):  [1.0, 3.0, 6.0, 5.0, 3.0]
Match: True
```
Read the result as growing partial sums (`1`, `1+2`, `1+2+3`) then shrinking tail sums
(`2+3`, `3`) — exactly what a length-3 running-sum filter does.

## Python notes
- `enumerate(values)` → `(index, value)` pairs, used to place each sample.
- A **generator expression** inside `max(...)` computes the biggest difference without
  building a list: `max(abs(...) for n in range(...))`.
