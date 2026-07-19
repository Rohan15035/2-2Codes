# CSE 220 — Signals & Their Properties: Approach Notes

Study notes for the three online problems. Each section tells you **what is asked**,
**the math**, **the coding trick**, and the **traps** that cost marks.

The full worked code is in [`solutions/`](solutions/):

| Problem | PDF | Template | Solution |
|---|---|---|---|
| A | Spec_A1_A2 | `template (2).py` | `solutions/solution_A_time_subscaling.py` |
| B | Online_1_Spec_B1_B2 | `Online_B_Template (2).py` | `solutions/solution_B_shift_vs_phase.py` |
| C | Online_1_C1_C2 | `template.py` | `solutions/solution_C_time_reversal_even_odd.py` |

---

## The one idea behind everything

A "continuous-time" signal on the computer is really an **array of samples on a
uniform grid** `t = linspace(T_MIN, T_MAX, N)`. Every operation
(`x(t/k)`, `x(-t)`, `x[n-n0]`, …) is a **remapping of the time axis**:

> To build `y(t) = x(g(t))`, for each output index `i` you need the value of `x`
> at the time `g(t[i])`. If that time is not exactly a stored sample, you must
> **interpolate**.

Keep the grid spacing `dt = t[1] - t[0]` and the start `t0 = t[0]` handy; the
index of any time `τ` is `pos = (τ - t0) / dt`.

---

## Problem A — Time sub-scaling `y(t) = x(t/k)` (10 marks)

**Asked:** implement `interpolate_signal(...)` (4), `time_scale(...)` (4), and plot (2).

### Math
- `y(t) = x(t/k)` with `k` a positive integer is **time expansion** (the signal
  stretches out): the feature of `x` at time `1` appears in `y` at time `k`.
- Output sample `i` must equal `x` evaluated at `t[i] / k`.

### Interpolation rule (given by the problem)
A missing value is the **average of the nearest left and right stored samples**:
`y(1) = 0.5·(x(0) + x(1))`. This is exactly correct here because for `k=2` the
query times land either **on** a sample (even index) or **exactly halfway**
between two (odd index).

### Coding recipe
```python
pos   = (t_query - t0) / dt      # fractional sample position
left  = floor(pos); right = ceil(pos)
y     = 0.5 * (x[left] + x[right])    # left==right => exact sample, no averaging
```
- `time_scale` is a one-liner once interpolation exists: query the original
  signal at `t/k`.
- Out-of-range query times → `NaN` (matplotlib skips them → "ignore values
  beyond the range").

### Traps
- **Off-by-one / exact samples:** when `pos` is an integer, `floor==ceil`, so the
  average returns the sample itself. Good — but floating-point noise in `dt` can
  make an integer look like `1999.9999`. Snap it: `if |pos - round(pos)| < 1e-6: pos = round(pos)`. (This is why `y(0)` must equal `x(0)` exactly.)
- Don't confuse `x(t/k)` (expansion) with `x(k·t)` (compression).
- Label both curves and add a legend (the 2 plotting marks).

---

## Problem B — Time shift vs. phase change in `x[n] = A·cos(Ω₀n + φ)` (10 marks)

**Asked:** `sinusoid` (1), `time_shift_sinusoid` (2), `phase_change_sinusoid` (2),
show shift→phase (2), show phase→shift (3).

### The three functions
```
x[n]                = A cos(Ω0 n + φ)
time shift by n0    = A cos(Ω0 (n - n0) + φ)
phase change by φ0  = A cos(Ω0 n + φ + φ0)
```

### The key identity (expand the shift)
```
A cos(Ω0 (n - n0) + φ) = A cos(Ω0 n + φ - Ω0 n0)
```
So a **time shift of `n0` is identical to a phase change of `φ0 = -Ω0·n0`.**

### Part 4 — "does a time shift correspond to a phase change?" → **YES, always.**
Pick any integer `n0`, set `φ0_equiv = -Ω0·n0`, and the two signals coincide:
`MSE ≈ 0` (≈1e-31). Demonstrate with a stem plot + the MSE print.

### Part 5 — "does a phase change correspond to a time shift?" → **NOT in general.**
Inverting the identity needs `n0 = -φ0 / Ω0`, but **`n0` must be an integer.**
A time shift can only realize phases that are multiples of `Ω0` (mod 2π). For an
arbitrary `φ0` (e.g. `1.0` rad with `Ω0 = π/4`), the best integer shift still
leaves `MSE > 0` (≈0.023). That non-zero MSE *is* the demonstration.

### Traps
- Sign of the phase: `x[n-n0]` gives `-Ω0 n0`, **not** `+Ω0 n0`.
- The asymmetry between Part 4 and Part 5 is the whole point — be ready to say
  *"time shift ⇒ phase change always; phase change ⇒ time shift only if
  `-φ0/Ω0` is an integer."*
- Discrete sinusoids are only periodic in `n` when `Ω0/2π` is rational; that's
  the same "integer" flavour of constraint.

---

## Problem C — Time reversal and even/odd decomposition (10 marks)

**Asked:** plot `x(t)` (1), `time_reverse` (2), even/odd built from it (4), plot
`x(-t)`, `xe`, `xo` (3).

### Why reversal = flipping the array
The grid `linspace(-4, 4, 4001)` is **symmetric about 0** with an **odd** number
of points (so `t = 0` is included and `t[i] = -t[N-1-i]`). Therefore
```
x(-t)[i] = x(-t[i]) = x(t[N-1-i]) = x[N-1-i]   ⟹   time_reverse(x) = x[::-1]
```

### Even/odd (must be built only from `time_reverse`)
```
xe(t) = ½ ( x(t) + x(-t) )     # even  (symmetric):      xe[::-1] == xe
xo(t) = ½ ( x(t) - x(-t) )     # odd   (anti-symmetric): xo[::-1] == -xo
xe + xo = x                    # always — use as a sanity check
```

### Traps
- `x[::-1]` is only "time reversal about 0" **because the grid is symmetric and
  centred**. On a non-symmetric grid you would have to re-sample/interpolate.
- Reversing a NumPy array returns a **view**; if you plan to mutate, `.copy()`.
  (Here we only read, so it's fine.)
- Verify `max|(xe + xo) - x| ≈ 0` — a cheap correctness check worth doing in the
  exam.
- Two figures are required: one `x(t)`+`x(-t)`, one `x(t)`+`xe`+`xo`.

---

## 90-second exam checklist

1. `dt = t[1]-t[0]`, `t0 = t[0]` — you'll need them for any axis remap.
2. Remap: `y(t)=x(g(t))` ⟶ query `x` at `g(t[i])`; interpolate if between samples.
3. Symmetric grid ⟶ `x(-t) == x[::-1]`.
4. `xe = ½(x + x_rev)`, `xo = ½(x - x_rev)`, and `xe + xo == x`.
5. Shift ↔ phase: `x[n-n0] = A cos(Ω0 n + φ - Ω0 n0)` ⟹ `φ0 = -Ω0 n0`.
6. Every plot: **title, xlabel, ylabel, legend, grid** (free marks).
7. Sanity-print an MSE or a max-abs-error to prove correctness.
