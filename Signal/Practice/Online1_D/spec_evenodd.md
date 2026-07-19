# CSE 220 — Online on Signals and Their Properties (Practice Set D)

**Total Marks: 10  ·  Total Time: 30 Minutes**

In this assignment, you need to implement the **even/odd decomposition** of a sampled
continuous-time signal in Python, and use it to rebuild the signal with a weight.
You also need to plot the graphs of each of these signals.

Let the base signal be `x(t)` (provided in the template file). You will compute and plot:

```
x(t),   xe(t),   xo(t),   y(t) = xe(t) + a * xo(t)
```

Recall (Lecture 1):

```
xe(t) = 1/2 ( x(t) + x(-t) )      (the even part,  xe(-t) =  xe(t))
xo(t) = 1/2 ( x(t) - x(-t) )      (the odd  part,  xo(-t) = -xo(t))
x(t)  = xe(t) + xo(t)             (always reconstructs the original)
```

## Tasks

- ★ Generate the time axis `t` and compute `x(t)`. **(given)**
- ★ Implement `time_reverse(t, x)` that returns the samples of `x(-t)`.
  Assume the signal is bounded between `-pi` and `pi`, values outside the range are `0`.
  - The time grid `t = linspace(-pi, pi, N)` is **symmetric about 0**, so `t[N-1-i] = -t[i]`.
    Time reversal is therefore just a **reversal of the sample array** — no interpolation needed.
    For example: `x(-t)` at `t = 1` equals `x(-1)`; at `t = -1` it equals `x(1)`, and so on.
- ★ Implement `even_odd_decompose(t, x)` that returns `(xe, xo)` using **only** `time_reverse`.
- ★ Implement `reconstruct(xe, xo, a)` that returns `y(t) = xe(t) + a * xo(t)`.
  - `a =  1`  → `y(t) = x(t)`   (original signal)
  - `a = -1`  → `y(t) = x(-t)`  (time-reversed signal, since `xe - xo = x(-t)`)
  - `a =  0`  → `y(t) = xe(t)`  (even part only)
- ★ Print the reconstruction check `max|(xe + xo) - x|` (should be ≈ 0).
- ★ Plot (with proper labels and legend) on the same figure: `x(t)`, `xe(t)`, `xo(t)`, `y(t)`.
- ★ In the main function, make an **infinite loop** that takes `a` repeatedly and shows a plot on
  each iteration. The program ends upon receiving `'q'`.

## Marks Distribution

- Implementing time reversal: **3**
- Implementing even/odd decomposition: **4**
- Reconstruction + completing the loop: **3**
