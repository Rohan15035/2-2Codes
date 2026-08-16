# Practice 5 — Cross-Correlation via Convolution

**File:** `problem5_correlation_via_convolution.py`

## Problem
Use convolution to locate a short pattern `{1, 2, 1}` inside a longer signal
`x = {0,0,0,0, 1,2,1, 0,0,0}`. The correlation peaks where the pattern best lines up.

## The idea
Cross-correlation and convolution differ by a **time reversal**:
```
corr_xy[n] = Σ_k x[k] · y[k − n]  =  ( x * y_reversed )[n],   where y_reversed[n] = y[−n]
```
So we can reuse the exact same `LTISystem` convolution — we just flip the pattern in time
first. Correlation is the standard tool for **pattern / template matching**: the output is
largest at the lag where the template overlaps a matching piece of the signal.

## How the code solves it
Time-reversal maps index `n → −n`, which flips the sign of the range:
```python
def time_reverse(sig):
    g = DiscreteSignal(-sig.end_time, -sig.start_time)   # range flips sign
    for n in sig.times():
        g.set_value_at_time(-n, sig.get_value_at_time(n))
    return g
```
Then correlation is one convolution:
```python
corr = LTISystem(time_reverse(pattern)).output(x)
```
The peak lag is found with `max(..., key=...)`:
```python
best_n = max(corr.times(), key=lambda n: corr.get_value_at_time(n))
```

## Expected output
```
corr[n]: [0, 0, 0, 0, 1, 4, 6, 4, 1, 0, 0, 0]  over [-2 ... 9]
Peak correlation at lag n = 4  value = 6.0
```
The peak value `6 = 1·1 + 2·2 + 1·1` occurs when the pattern sits exactly on top of the
matching region — pointing to index 4, where `{1,2,1}` lives in `x`. The symmetric shape
around the peak (`1, 4, 6, 4, 1`) is the autocorrelation of `{1,2,1}` because here the
buried pattern is identical to the template.

## Python notes
- `key=lambda n: corr.get_value_at_time(n)` tells `max` to compare indices *by their
  signal value*, not by the index number itself.
- Negative start/end times are fine — `DiscreteSignal` supports any integer range.
