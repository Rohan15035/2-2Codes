# CSE 220 — Online on Signals and Their Properties (Practice Set E)

**Total Marks: 10  ·  Total Time: 30 Minutes**

In this assignment, you need to compute the **energy** and **average power** of a sampled
continuous-time signal over a user-chosen interval `[a, b]`, in Python, and plot the signal
together with the region whose energy you measured.

Let the base signal be `x(t)` (provided in the template file). Recall (Lecture 1):

```
Energy         E[a,b] = integral_a^b |x(t)|^2 dt
Average power  P[a,b] = 1/(b - a) * integral_a^b |x(t)|^2 dt = E[a,b] / (b - a)
```

Because `x(t)` is stored as **samples** on a uniform grid, approximate the integral by the
Riemann sum (square the samples, add them up, multiply by the sample spacing `dt`):

```
E[a,b] ≈ ( sum over samples t in [a,b] of |x(t)|^2 ) * dt
```

## Tasks

- ★ Generate the time axis `t` and compute `x(t)`. **(given)**
- ★ Implement `energy(t, x, a, b)` returning `E[a,b]` using the Riemann-sum approximation.
  - Assume the signal is bounded between `-pi` and `pi`; values outside are `0`.
  - Use a **boolean mask** `(t >= a) & (t <= b)` to select the samples inside the interval.
- ★ Implement `average_power(t, x, a, b)` returning `P[a,b] = E[a,b] / (b - a)`.
- ★ On each iteration print the numeric `E` and `P`.
- ★ Plot (with proper labels and legend) on the same figure: `x(t)`, and the shaded area
  `|x(t)|^2` over `[a, b]` (use `plt.fill_between`).
- ★ In the main function, make an **infinite loop** that takes `a` and `b` repeatedly
  (comma-separated, e.g. `0,3.14159`) and shows a plot on each iteration.
  The program ends upon receiving `'q'`.

> Sanity check: for `x(t) = sin(t)` on `[0, pi]`, `E ≈ pi/2 ≈ 1.5708` and `P ≈ 0.5`.

## Marks Distribution

- Implementing energy: **4**
- Implementing average power: **2**
- Plot (shaded `|x|^2`) + completing the loop: **4**
