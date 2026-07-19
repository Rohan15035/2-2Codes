# Signals Lab — Code Syntax Cheat Sheet

Every NumPy / Matplotlib / Python idiom used to solve the questions in this directory,
grouped by purpose. Each entry says **what it does**, **why it is used here**, and shows a
minimal example. The "Seen in" note points to a file that uses it.

Files this covers: `Online1_A/set2.py`, `Online1_B/set1.py`, `Online1_D/*`, `Online1_E/*`,
`solutions/solution_A/B/C.py`, `practice_exam/P1..P3` and their `answer_key/`.

---

## 0. Program skeleton

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    ...

if __name__ == "__main__":   # run main() only when this file is executed directly
    main()
```

Type hints are optional but appear in the solutions for clarity:

```python
def interpolate_signal(t: np.ndarray, x: np.ndarray, tq: np.ndarray) -> np.ndarray:
    ...
```
*Seen in:* every file.

---

## 1. Building the time / index axis

| Idiom | Meaning | Example |
| --- | --- | --- |
| `np.linspace(a, b, N)` | `N` points from `a` to `b`, **both endpoints included** | `t = np.linspace(-np.pi, np.pi, 1000)` |
| `np.arange(a, b, step)` | values `a, a+step, …`, **`b` excluded** | `n = np.arange(-25, 26)` → −25…25 |
| `np.arange(t_min, t_max + dt/2, dt)` | include the last endpoint despite float error (the `dt/2` guard) | `Online1_B/set1.py` |
| `np.pi` | the constant π | `T_MIN, T_MAX = -np.pi, np.pi` |

- **Continuous signal** → sample on a fine grid with `linspace`.
- **Discrete signal** → integer index axis with `arange`.
- A grid `linspace(-c, c, N)` is **symmetric about 0**: `t[N-1-i] = -t[i]`. This is what makes
  time reversal a pure array flip (see §4).

*Seen in:* `Online1_A/set2.py` (`linspace`), `Online1_B/set1.py` (`arange` endpoint trick),
`solution_B` (`arange` index range).

---

## 2. Boolean masks (select / zero-out samples)

```python
x[(t < T_MIN) | (t > T_MAX)] = 0      # force out-of-range values to 0
mask = (t >= a) & (t <= b)            # True where t is inside [a, b]
x[mask]                               # keep only the in-range samples
```

- `&` = AND, `|` = OR, applied **element-wise**; wrap each comparison in `()` (operator
  precedence). `~mask` is NOT.
- Assigning through a mask (`x[mask] = 0`) edits only those positions.
- Indexing with a mask (`x[mask]`) returns just the selected values.

*Seen in:* `base_signal` in every question (zeroing outside `[-pi, pi]`), `Online1_E/energy_solution.py`
(interval mask), `P3_solution.py` (`n >= 0`, `n == 1`).

---

## 3. Element-wise math on arrays (vectorization)

```python
x = np.exp(-0.4 * t) * np.cos(2 * t) + 0.5 * t   # no loop needed
y = alpha * x                                     # amplitude scaling
xe = 0.5 * (x + xr)                               # array + array, scalar * array
```

NumPy applies `+  -  *  /  **`, `np.sin`, `np.cos`, `np.exp`, `np.abs` to **every element at
once**. Prefer this over Python `for` loops.

*Seen in:* `base_signal` everywhere, `Online1_A/set2.py` (`alpha*x[::-1]`), `solution_C`.

---

## 4. Time reversal — `x[::-1]`

```python
def time_reverse(x):
    return x[::-1]        # reverse the sample array  ->  x(-t)
```

`x[::-1]` reverses an array. On a grid **symmetric about 0**, `x[::-1][i] = x(-t[i])`, so this
is exactly the time-reversed signal — **no interpolation required**. This is why the base grid
is `linspace(-pi, pi, N)`.

- Even part: `xe = 0.5 * (x + x[::-1])`
- Odd part:  `xo = 0.5 * (x - x[::-1])`

*Seen in:* `Online1_A/set2.py`, `Online1_D/evenodd_solution.py`, `solution_C`, `P3_solution.py`.

---

## 5. Interpolation (time scaling & shifting) — `x(alpha*t + beta)`

The key move: build **query times**, then read `x` at those times by interpolating between
stored samples.

```python
dt  = t[1] - t[0]                       # uniform sample spacing
pos = (t_query - t[0]) / dt             # query time measured in "sample units"

left  = np.floor(pos).astype(int)       # nearest sample index to the left
right = np.ceil(pos).astype(int)        # nearest sample index to the right

y = np.full(t_query.shape, 0.0)         # (or np.nan) default for out-of-range
valid = (left >= 0) & (right < len(t))  # keep only in-range queries

# average-of-neighbours interpolation (Online1_B spec):
y[valid] = 0.5 * (x[left[valid]] + x[right[valid]])

# OR true linear interpolation (practice P1):
f = pos - left                          # fraction between left and right
y[valid] = (1 - f[valid]) * x[left[valid]] + f[valid] * x[right[valid]]
```

Then the transform is just choosing the query times:

```python
t_query = alpha * t + beta              # y(t) = x(alpha*t + beta)
t_query = t / k                         # y(t) = x(t / k)
```

Gotchas:
- `np.floor` / `np.ceil` return **floats** → convert with `.astype(int)` before indexing.
- **Out-of-range** queries: initialize `y` with `0.0` (spec says values outside `[-pi,pi]` are 0)
  or `np.nan` (to leave a gap in the plot). Do **not** leave them as an index that overflows.
- When using the fraction `f`, index it with the **same mask**: `f[valid]`, or the shapes mismatch.
- Snap tiny float error so an exact hit stays exact: `pos = np.where(np.abs(pos-np.round(pos))<1e-6, np.round(pos), pos)`.

*Seen in:* `Online1_B/set1.py`, `solution_A`, `practice_exam/P1` (+ its two documented bugs).

---

## 6. Array creation helpers

| Idiom | Meaning |
| --- | --- |
| `np.full(shape, fill, dtype=float)` | new array of given shape filled with a value |
| `np.full_like(a, fill, dtype=float)` | same shape/type as `a`, filled with a value |
| `np.zeros_like(a)` / `np.zeros(shape)` | all-zeros array |
| `np.round(pos)` | round to nearest integer (still float) |
| `np.where(cond, a, b)` | element-wise "if cond then a else b" |
| `arr.shape`, `len(arr)` | dimensions / length |

*Seen in:* interpolation code in `Online1_B`, `solution_A`, `P1`.

---

## 7. Numeric summaries (energy, power, error checks)

```python
E   = np.sum(np.abs(x) ** 2)            # discrete energy  E = sum |x|^2
E   = np.sum(np.abs(x[mask]) ** 2)*dt   # sampled continuous energy (Riemann sum)
P   = E / (b - a)                       # average power over [a, b]
mse = np.mean((a - b) ** 2)             # mean squared error between two sequences
err = np.max(np.abs((xe + xo) - x))     # max absolute reconstruction error (~0)
```

- `np.abs(x)**2` works for real **and** complex signals (matches the lecture's `|x|^2`).
- `float(np.sum(...))` casts the 0-d NumPy result to a plain Python float for clean printing.
- `np.isclose(m, round(m), atol=1e-9)` — safe "is this (almost) an integer?" test
  (used for discrete periodicity).

*Seen in:* `Online1_E/energy_solution.py`, `solution_B`/`P2` (`mse`), `solution_C`/`P3`
(reconstruction & energy-split checks).

---

## 8. The interactive main loop

The online questions all use an **infinite loop** that reads a parameter, quits on `'q'`, and
plots each iteration.

```python
while True:
    raw = input("Enter value (or 'q' to quit): ").strip()   # .strip() drops stray spaces
    if raw.lower() == 'q':                                   # .lower() accepts 'q' or 'Q'
        break

    alpha = float(raw)                       # single value

    a_str, b_str = raw.split(',')            # OR two comma-separated values
    a, b = float(a_str), float(b_str)        # convert BOTH to float (input() gives str)

    y = transform_signal(t, x, alpha)
    ...plot...
print("Exiting.")
```

Common mistakes (all real, from earlier drafts in this repo):
- `alpha, beta = input(...)` unpacks a string **character by character** and leaves them as
  **strings** → `alpha*t` then crashes. Always `split(',')` **and** `float(...)`.
- Forgetting the `'q'` check → the loop never ends and the "Exiting." line is unreachable.

*Seen in:* `Online1_A/set2.py`, `Online1_B/set1.py`, `Online1_D`, `Online1_E`.

---

## 9. Plotting — continuous signals (`plt.plot`)

```python
plt.figure(figsize=(9, 5))
plt.plot(t, x, label="x(t)")
plt.plot(t, y, label=f"y(t) = x({alpha}t + {beta})", linewidth=2, linestyle="--")
plt.fill_between(t[mask], 0, np.abs(x[mask])**2, alpha=0.3, label="|x|^2")  # shaded region
plt.title("...")
plt.xlabel("t"); plt.ylabel("Amplitude")
plt.legend()                 # needs label=... on each plot
plt.grid(True)
plt.tight_layout()           # stop labels being clipped
plt.show()                   # opens the window (blocks until closed)
```

- Full marks per the rubric = **title + xlabel + ylabel + legend + grid** on every figure.
- f-strings put live values into labels/titles: `f"Energy = {E:.4f}"` (`.4f` = 4 decimals).

*Seen in:* `Online1_A/B/D/E`, `solution_A`, `solution_C`.

---

## 10. Plotting — discrete signals (`stem`)

```python
fig, ax = plt.subplots(figsize=(9, 4))       # figure + axes object

markerline, stemlines, baseline = ax.stem(n, x, label="x[n]")
baseline.set_visible(False)                   # hide the y=0 baseline for a cleaner look

ax.plot(n[one], x[one], "o", ms=10, mfc="none", label="markers")  # ring markers
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.set_title("...")
ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
plt.show()
```

- `stem` draws lollipop stems — the right choice for **discrete** `x[n]`.
- `plt.subplots()` returns `(fig, ax)`; call methods on `ax` (`ax.set_title`, `ax.legend`, …).
- Marker style string `"o"`, `ms` = marker size, `mfc="none"` = hollow marker.

*Seen in:* `solution_B`, `practice_exam/P2`, `P3`.

---

## 11. copy vs view (aliasing pitfall)

```python
b = a.copy()   # independent array — editing b does NOT change a
c = a.view()   # shares memory — editing c DOES change a
```

Relevant because `x[::-1]` and mask indexing can return **views**; use `.copy()` if you need to
mutate a result without disturbing the original.

*Seen in:* `prac.ipynb` (experiment cell).

---

## 12. Transformation → code quick reference

| Operation (lecture) | Formula | Code on a symmetric grid |
| --- | --- | --- |
| Amplitude scaling | `alpha * x(t)` | `alpha * x` |
| Time reversal | `x(-t)` | `x[::-1]` |
| Time shift | `x(t - t0)` | interpolate at `t_query = t - t0` |
| Time scaling | `x(alpha * t)` | interpolate at `t_query = alpha * t` |
| Scale + shift | `x(alpha*t + beta)` | interpolate at `t_query = alpha*t + beta` |
| Even part | `½(x(t) + x(-t))` | `0.5 * (x + x[::-1])` |
| Odd part | `½(x(t) - x(-t))` | `0.5 * (x - x[::-1])` |
| Energy | `∫\|x\|² dt` | `np.sum(np.abs(x)**2) * dt` |
| Average power | `E / (b - a)` | `energy / (b - a)` |
