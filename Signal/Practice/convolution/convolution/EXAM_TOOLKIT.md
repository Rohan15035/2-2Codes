# Exam Toolkit — Creative Ways to Drive `DiscreteSignal` and `LTISystem`

Every snippet here has been run against your actual [signal_lti.py](signal_lti.py). Outputs shown in comments are real.

The whole class API is tiny. Everything below is built from just these:

| `DiscreteSignal` | `LTISystem` |
|---|---|
| `.start_time`, `.end_time`, `.values` | `.impulse_response` |
| `.times()` → `np.arange(start, end+1)` | `.output_range(x)` → `(n_min, n_max)` |
| `.get_value_at_time(t)` → **0.0 outside range** | `.output(x)` → full convolution |
| `.set_value_at_time(t, v)` → **raises outside range** | `.output_at_time(x, n)` → one sample |
| `.shift(k)` → `x[n-k]` | `.output_by_superposition(x)` |
| `.add(other)` → union range | `.get_response_components(x)` |
| `.multiply(scalar)` | `.get_contributions_at_time(x, n)` |
| `.nonzero_samples(tol)` | |

**The single most important fact:** `get_value_at_time` returns `0.0` outside the support, but `set_value_at_time` *raises*. Reading is safe everywhere; writing is not. Almost every trick below exploits the free zero-padding on reads.

---

## 0. The helper to write first, every time

Write this in the first 30 seconds of the exam. Everything else depends on it.

```python
def make_signal(start, values):
    """Build a DiscreteSignal from a list, starting at index `start`."""
    sig = DiscreteSignal(start, start + len(values) - 1)
    for i, v in enumerate(values):
        sig.set_value_at_time(start + i, float(v))
    return sig
```

Note `start + len(values) - 1` — you don't have to count the end index by hand, which is where range-off-by-one mistakes come from under time pressure.

A printing helper is worth another 20 seconds:

```python
def show(sig, name=""):
    print(f"{name}: n={sig.start_time}..{sig.end_time}  {np.round(sig.values, 6).tolist()}")
```

---

## 1. Building signals

### Standard test signals
```python
delta  = make_signal(0, [1.0])                    # δ[n]
step   = make_signal(0, [1.0] * 11)               # u[n], stored window 0..10
ramp   = make_signal(0, list(range(11)))          # n·u[n]
pulse  = make_signal(-2, [1.0] * 5)              # rectangular pulse on -2..2
alt    = make_signal(0, [(-1.0) ** n for n in range(8)])   # (-1)^n
expo   = make_signal(0, [0.8 ** n for n in range(10)])     # a^n u[n]
```

### Sparse signals — write only the samples you care about
```python
def from_dict(start, end, table):
    sig = DiscreteSignal(start, end)
    for t, v in table.items():
        sig.set_value_at_time(t, float(v))
    return sig

sparse = from_dict(-1, 4, {0: 1.0, 3: -2.0})
# n=-1..4  [0.0, 1.0, 0.0, 0.0, -2.0, 0.0]
```

### Build an impulse response as a sum of shifted deltas
This is the literal reading of `h[n] = δ[n] + 0.6·δ[n-2] − 0.4·δ[n-3]`, and it's often faster and less error-prone than counting zeros in a list:

```python
h = DiscreteSignal(0, 3)                      # accumulator over the final range
for k, c in [(0, 1.0), (2, 0.6), (3, -0.4)]:
    h = h.add(delta.shift(k).multiply(c))
# n=0..3  [1.0, 0.0, 0.6, -0.4]
```

Seeding the accumulator over the **full intended range** matters: `add` takes the union of supports, so the seed pins down the final range even if the first or last coefficient is zero.

---

## 2. The three operators as an algebra

`shift`, `add`, `multiply` are closed over signals, so you can chain them into any linear expression.

| Math | Code |
|---|---|
| `a·x[n]` | `x.multiply(a)` |
| `x[n-k]` | `x.shift(k)` |
| `x[n+k]` | `x.shift(-k)` |
| `x[n] + y[n]` | `x.add(y)` |
| `x[n] − y[n]` | `x.add(y.multiply(-1))` ← **no `.subtract()` exists** |
| `a·x1[n] + b·x2[n]` | `x1.multiply(a).add(x2.multiply(b))` |
| `x[n] − x[n-1]` | `x.add(x.shift(1).multiply(-1))` |

```python
a, b = 2.0, -3.0
combo = x1.multiply(a).add(x2.multiply(b))     # a·x1 + b·x2 in one line
```

> ⚠️ `x1 * 2`, `x1 + x2`, `x1 - x2` all **fail** — `DiscreteSignal` defines no `__mul__`, `__add__` or `__sub__`. This is the single most common exam crash.

### First difference without an LTI system
```python
diff = x.add(x.shift(1).multiply(-1))          # y[n] = x[n] − x[n−1]
```
Useful when a question says "compute the first difference of the step response" and you don't want to spin up a whole `LTISystem`.

---

## 3. Using `LTISystem` in non-obvious ways

### 3a. Probe with an impulse to *recover* the impulse response
```python
sys_a = LTISystem(h)
recovered = sys_a.output(delta)                # == h, exactly
```
Because `x * δ = x`. This is how you extract `h` from a system you were handed as a black box — and how you check that a system someone built is the one you think it is.

### 3b. Convolve two impulse responses to get the **equivalent cascade system**
```python
h1 = make_signal(0, [1.0, -1.0])               # first difference
h2 = make_signal(0, [1.0] * 5)                 # truncated step
h_eq = LTISystem(h1).output(h2)                # h1 * h2
# n=0..5  [1.0, 0.0, 0.0, 0.0, 0.0, -1.0]
```
`LTISystem.output` doesn't care that its argument is "an impulse response" — a signal is a signal. **Convolving two `h`s gives the cascade's equivalent `h`.** One `LTISystem` object, used to do algebra on impulse responses.

Read that result: it's `δ[n] − δ[n−5]`, not `δ[n]`. The `−1` at `n=5` is exactly the truncation artifact of storing only 5 samples of `u[n]` — which is why the finite-window questions insist you compare on a restricted observation window.

### 3c. Commutativity, for free
```python
LTISystem(h1).output(h2)     # h1 * h2
LTISystem(h2).output(h1)     # h2 * h1   → identical
```
Swapping which signal plays "system" and which plays "input" changes nothing. Good sanity check, and an easy exam task in itself.

### 3d. Cascade
```python
def cascade(sys1, sys2, x):
    mid = sys1.output(x)
    return mid, sys2.output(mid)
```
The whole point: **system 2 is fed system 1's output**, not `x`. Equivalent single system: `LTISystem(LTISystem(h1).output(h2))`.

### 3e. Parallel combination
```python
h_par = h1.add(h2)                             # equivalent h of parallel branches
lhs = LTISystem(h_par).output(x)
rhs = LTISystem(h1).output(x).add(LTISystem(h2).output(x))
# lhs == rhs   (distributivity of convolution over addition)
```

### 3f. `output_at_time` — one sample, no full convolution
```python
y5 = sys_a.output_at_time(x, 5)
```
When a question only asks "what is `y[5]`?", this skips computing the whole signal.

### 3g. `get_contributions_at_time` — show your working
```python
for k, xk, h_nk, term in sys_a.get_contributions_at_time(x, 3):
    print(f"  x[{k}]={xk} · h[{3-k}]={h_nk} → {term}")
```
Returns the individual `x[k]·h[n−k]` products. If a question asks you to *explain* or *tabulate* how an output sample arises, this prints the derivation for you.

### 3h. Two independent computations = a free correctness check
```python
y1 = sys_a.output(x)                    # direct convolution sum
y2 = sys_a.output_by_superposition(x)   # shift-and-scale superposition
assert max_absolute_difference(y1, y2) < 1e-9
```
Different code paths, same math. Cheap insurance that your `h` and ranges are right.

---

## 4. Helpers the class doesn't have (write these when needed)

### Time reversal `x[−n]`
```python
def reverse(sig):
    out = DiscreteSignal(-sig.end_time, -sig.start_time)   # range flips too!
    for n in sig.times():
        out.set_value_at_time(-n, sig.get_value_at_time(n))
    return out
# reverse of n=1..3 [1,2,3]  →  n=-3..-1 [3,2,1]
```
Needed for **cross-correlation**: `r_xy[n] = Σ x[k]·y[k−n] = (x * reverse(y))[n]`.

### Restrict to a window (essential for finite-window questions)
```python
def window(sig, start, end):
    out = DiscreteSignal(start, end)
    for n in range(start, end + 1):
        out.set_value_at_time(n, sig.get_value_at_time(n))
    return out
```
Works even when `[start, end]` sticks out past the signal — the zero-padded getter fills the gaps.

### Max absolute difference, on a chosen range
```python
def max_abs_diff_in_range(s1, s2, start, end):
    worst = 0.0
    for n in range(start, end + 1):
        d = abs(s1.get_value_at_time(n) - s2.get_value_at_time(n))
        if d > worst:
            worst = d
    return worst
```
And the whole-support version, when no window is specified:
```python
def max_abs_diff(s1, s2):
    start = min(s1.start_time, s2.start_time)
    end   = max(s1.end_time,   s2.end_time)
    return max_abs_diff_in_range(s1, s2, start, end)
```
Taking the **union** of supports matters — using only one signal's range would silently ignore a mismatch living outside it.

### Scalar summaries
```python
total   = float(np.sum(sig.values))                  # Σ x[n]  (DC gain if applied to h)
abs_sum = float(np.sum(np.abs(sig.values)))          # Σ|h[n]| → BIBO stable iff finite
energy  = float(np.sum(sig.values ** 2))
peak_n  = int(sig.times()[np.argmax(np.abs(sig.values))])   # index of largest sample
```
`peak_n` is how you answer "at what lag does the template match?" in a matched-filter question.

### Running sum without a huge stored step
```python
def running_sum(sig):
    out = DiscreteSignal(sig.start_time, sig.end_time)
    total = 0.0
    for n in sig.times():
        total += sig.get_value_at_time(n)
        out.set_value_at_time(n, total)
    return out
```
Exact, no truncation window to reason about. Use it to *check* an accumulator built as `LTISystem(step)`.

---

## 5. Systems as plain functions (the non-LTI half of the exam)

An `LTISystem` can only ever express convolution. Anything else — squaring, time-varying gain, decimation — must be a plain function that takes a signal and returns a signal.

```python
def system_scaler(sig):                  # y[n] = n·x[n]   (linear, NOT time-invariant)
    out = DiscreteSignal(sig.start_time, sig.end_time)
    for n in sig.times():
        out.set_value_at_time(n, n * sig.get_value_at_time(n))
    return out

def system_square(sig):                  # y[n] = x[n]²    (time-invariant, NOT linear)
    out = DiscreteSignal(sig.start_time, sig.end_time)
    for n in sig.times():
        v = sig.get_value_at_time(n)
        out.set_value_at_time(n, v * v)
    return out

def system_reverse(sig):                 # y[n] = x[−n]    (linear, NOT time-invariant)
    return reverse(sig)

def system_bias(sig):                    # y[n] = 2x[n] + 1 (TI, NOT linear — affine)
    out = DiscreteSignal(sig.start_time, sig.end_time)
    for n in sig.times():
        out.set_value_at_time(n, 2 * sig.get_value_at_time(n) + 1)
    return out
```

> 🔴 **The trap that will cost you marks.** Inside these loops, `n` is a *time index*, but `sig.values` is a *0-based array*. Writing `sig.values[n]` on a signal starting at `n = −2` silently wraps around via Python negative indexing, and on a shifted signal it throws `IndexError: index 5 is out of bounds`. **Always** go through `get_value_at_time` / `set_value_at_time` inside these functions.
>
> ```python
> out.values[n] = n * sig.values[n]                            # ✗ WRONG
> out.set_value_at_time(n, n * sig.get_value_at_time(n))       # ✓ RIGHT
> ```

---

## 6. Passing systems around as values

Generic testers must accept *any* signal→signal callable, LTI or not. Three ways to hand one over:

```python
sys_a = LTISystem(h)

test_linearity(sys_a.output, x1, x2, a, b)      # ✓ bound method, NO parentheses
test_linearity(system_square, x1, x2, a, b)     # ✓ plain function object
test_linearity(lambda s: system_square(s), ...) # ✓ lambda, for adapting signatures

test_linearity(sys_a, ...)                      # ✗ LTISystem object is not callable
test_linearity(sys_a.output(x1), ...)           # ✗ parentheses = already called
```

**No parentheses = pass the recipe. Parentheses = pass the cooked meal.**

Lambdas let you build a system on the fly, which is the fastest way to test a variant:

```python
delayed   = lambda s: s.shift(2)                                  # pure delay
amplified = lambda s: s.multiply(3.0)                             # gain
combo     = lambda s: sys_a.output(s).add(s.multiply(-1))         # h-branch minus direct path
smooth_3  = lambda s: LTISystem(make_signal(0, [1/3]*3)).output(s)
```

### The two generic property testers
```python
def test_linearity(apply_system, x1, x2, a, b):
    lhs = apply_system(x1.multiply(a).add(x2.multiply(b)))          # S{a·x1 + b·x2}
    rhs = apply_system(x1).multiply(a).add(apply_system(x2).multiply(b))
    return max_abs_diff(lhs, rhs)

def test_time_invariance(apply_system, x, k):
    lhs = apply_system(x.shift(k))                                  # S{x[n−k]}
    rhs = apply_system(x).shift(k)                                  # y[n−k]
    return max_abs_diff(lhs, rhs)
```
Both return `0.0` (to ~1e-16) when the property holds, and something visibly large when it doesn't. Note neither one mentions `LTISystem` anywhere — that's what makes them generic.

### The same pattern extends to other properties
```python
def test_causality(apply_system, sig, n0):
    """sig must be zero for n < n0. Output must then also be zero for n < n0."""
    y = apply_system(sig)
    return max(abs(y.get_value_at_time(n)) for n in range(y.start_time, n0))

def test_memoryless(apply_system, sig):
    """A memoryless system's response to a lone impulse stays at that one index."""
    y = apply_system(sig)
    leak = [abs(y.get_value_at_time(n)) for n in y.times() if n != sig.start_time]
    return max(leak) if leak else 0.0
```

---

## 7. Range arithmetic — know these cold

| Operation | Resulting range |
|---|---|
| `x.shift(k)` | `[x0+k, x1+k]` |
| `x.add(y)` | `[min(x0,y0), max(x1,y1)]` (union) |
| `x.multiply(c)` | unchanged |
| `LTISystem(h).output(x)` | `[h0+x0, h1+x1]`, length `len(x)+len(h)−1` |
| cascade of `h1` then `h2` | `[h1₀+h2₀+x0, h1₁+h2₁+x1]` |

**Finite-window rule of thumb.** If `x` is supported on `[x0, x1]` and you must report `y` correctly on `[N0, N1]`, an infinite `h` (like `u[n]`) needs to be stored out to index `N1 − x0`. In spec B: `8 − (−2) = 10`, which is exactly why the template stores `h2[n]` for `n = 0…10`. Beyond the observation window the truncation shows up as a spurious tail — that's why you compare on the window only.

---

## 8. Pitfall checklist

| Symptom | Cause | Fix |
|---|---|---|
| `TypeError: unsupported operand type(s) for *` | `2 * signal` | `signal.multiply(2)` |
| `IndexError: index 5 is out of bounds` | `sig.values[n]` with time index `n` | `sig.get_value_at_time(n)` |
| Silently wrong values, no error | `sig.values[-2]` wraps to the end | same fix |
| `TypeError: return arrays must be of ArrayType` | `np.abs(a, b)` — 2nd arg is `out`, not an operand | `abs(a - b)` |
| Max difference always exactly `0.0` | inverted comparison `if d < worst` | `if d > worst` |
| Integer truncation (`1/3` → `0`) | int-dtype values list | `float(v)` or `dtype=float` |
| Both shifted signals share values | forgot `.copy()` | already handled inside `shift` |
| Huge difference outside the window | finite-window truncation of `u[n]` | compare on the observation range only |
| `IndexError` from `set_value_at_time` | writing outside the allocated range | allocate the correct range up front |

---

## 9. A 60-second exam skeleton

```python
import numpy as np
import matplotlib.pyplot as plt
# ... paste DiscreteSignal + LTISystem ...

def make_signal(start, values): ...
def max_abs_diff_in_range(s1, s2, start, end): ...
def show(sig, name): ...

def main():
    tolerance = 1e-9
    N0, N1 = -2, 8                       # observation window

    x  = make_signal(-2, [2, -1, 3, 1, -2])
    h1 = make_signal(0, [1.0, -1.0])
    h2 = make_signal(0, [1.0] * 11)

    sys1, sys2 = LTISystem(h1), LTISystem(h2)

    y = sys2.output(sys1.output(x))      # or cascade(...)
    d = max_abs_diff_in_range(y, x, N0, N1)

    print("y:", [(n, y.get_value_at_time(n)) for n in range(N0, N1 + 1)])
    print(f"max abs difference: {d}")
    print("Conclusion: ...")             # ← never leave this as None; marks live here
    print("Test passed:", d < tolerance)

if __name__ == "__main__":
    main()
```

Both sample specs award marks for a printed conclusion sentence. Write it even if your numbers came out wrong — state what you observed and what it implies.
