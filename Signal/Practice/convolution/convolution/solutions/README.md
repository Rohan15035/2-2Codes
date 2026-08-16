# Convolution Solutions — Overview

This folder solves every problem in the `convolution` assignment folders by
**reusing your two template files**:

- `signal_lti.py` — the `DiscreteSignal` and `LTISystem` classes (your Offline 1 code).
- `main.py` — the driver that reads problems from files and runs convolution.

A **copy of `signal_lti.py` lives in this folder** so every solution can import it.

| Folder | Original problem | Reuses `signal_lti.py`? |
|--------|------------------|--------------------------|
| `A_step_response/` | A1/A2 — output from the **step response** | ✅ Yes |
| `B_combined_systems/` | B1/B2 — **combination** of LTI systems (parallel + series) | ✅ Yes |
| `C_supersignal/` | C1/C2 — **superposition** of multiple signals | ✅ Yes |
| `D_continuous_practice/` | Continuous-time impulse decomposition | ❌ **No — needs new code** (see its README) |
| `practice_problems/` | 5 extra problems I generated for you | ✅ Yes |

**Why D can't reuse your code:** `signal_lti.py` stores a signal as a *finite array
of samples at integer indices*. The continuous problem needs a signal defined by a
*mathematical function of a real variable* `x(t)`. Those are fundamentally different
data structures, so problem D has its own standalone `ContinuousSignal` class.

Run any solution like this:

```bash
cd A_step_response
python solution_A.py
```

Each script prints a short report and saves plots into its own `outputs/` folder.

---

## How `signal_lti.py` works (the toolbox you reuse)

### `DiscreteSignal(start_time, end_time)`
A signal that lives on integer indices `start_time … end_time`. Internally it holds
a NumPy array `values` of length `end_time - start_time + 1`.

Key methods:

| Method | Meaning | Math |
|--------|---------|------|
| `get_value_at_time(t)` | value at index `t` (0 if outside range) | `x[t]` |
| `set_value_at_time(t, v)` | store a value | `x[t] = v` |
| `shift(k)` | move the signal right by `k` | `x[n-k]` |
| `add(other)` | sample-by-sample sum | `x[n] + y[n]` |
| `multiply(scalar)` | scale by a number | `a·x[n]` |
| `times()` | array of the integer indices | — |

> **Careful with `shift`:** `shift(1)` moves samples to *later* times, which
> represents `x[n-1]` (a one-sample **delay**). This is exactly what you need for a
> first difference `x[n] - x[n-1]`.

### `LTISystem(impulse_response)`
Wraps an impulse response `h[n]` and computes the output `y = x * h` (convolution):

| Method | Meaning |
|--------|---------|
| `output(x)` | full output signal via convolution sum `y[n] = Σ x[k]·h[n-k]` |
| `output_by_superposition(x)` | same result by adding shifted/scaled copies of `h` |
| `output_range(x)` | the `[n_min, n_max]` the output occupies |

The output length rule: if `x` spans `[a, b]` and `h` spans `[c, d]`, then `y` spans
`[a+c, b+d]`. **No `numpy.convolve` is used** — the sum is done by hand, which is what
every assignment requires.

---

## Python syntax cheat-sheet (used throughout these solutions)

You said Python syntax is shaky, so here is every non-obvious construct you'll see.

### Imports and running files
```python
from signal_lti import DiscreteSignal, LTISystem   # grab names from another file
import numpy as np                                  # import with a short alias

if __name__ == "__main__":     # code here runs ONLY when you execute this file
    main()                     # ...not when it's imported by another file
```

### Making `signal_lti.py` importable from a subfolder
```python
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))  # folder of THIS script
sys.path.insert(0, os.path.join(HERE, ".."))       # add parent folder to search path
```
- `__file__` = path to the current `.py` file.
- `os.path.dirname(p)` = the folder containing `p`.
- `os.path.join(a, "..")` = "a, then one level up".
- `sys.path` = list of folders Python searches for `import`; `insert(0, ...)` puts ours first.

### Lists, tuples, dicts
```python
nums = [1, 2, 3]              # list  — ordered, changeable, nums[0] == 1
pair = (2.0, sig)            # tuple — like a list but fixed; often used to group values
table = {0: 1.0, 2: -1.0}   # dict  — key -> value lookups, table[0] == 1.0
```

### Loops and iteration helpers
```python
for t, v in table.items():        # loop over dict as (key, value) pairs
for i, v in enumerate(values):    # enumerate -> (0, values[0]), (1, values[1]), ...
for c, s in zip(coeffs, sigs):    # zip -> pairs up two lists element by element
```

### Comprehensions (compact loops that build a list)
```python
squares = [n * n for n in range(5)]          # [0, 1, 4, 9, 16]
evens   = [n for n in range(10) if n % 2 == 0]
```

### Functions, defaults, and unpacking
```python
def add(signal, coefficient=1.0):   # coefficient has a DEFAULT; can be omitted
    ...

a, b = map(int, "3 5".split())      # split "3 5" -> ["3","5"], int each, unpack to a,b
```

### `lambda` — a one-line anonymous function (used a lot in problem D)
```python
step = lambda t: np.where(t >= 0, 1.0, 0.0)   # same as: def step(t): return ...
```

### Reading a text file
```python
with open("data.txt", "r", encoding="utf-8") as f:  # `with` auto-closes the file
    first_line = f.readline()        # read one line as a string
```

### NumPy bits you'll meet
```python
np.array([1, 2, 3], dtype=float)   # make an array of floats
np.linspace(-3, 3, 1000)           # 1000 evenly spaced points from -3 to 3
np.where(cond, a, b)               # pick a where cond is True, else b (elementwise)
np.allclose(u, v, atol=1e-6)       # True if arrays are equal within a tolerance
```

Each problem's own `README.md` explains the *signal-processing* reasoning step by step.
