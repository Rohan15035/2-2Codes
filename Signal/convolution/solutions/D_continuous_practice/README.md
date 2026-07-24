# Problem D — Continuous-Time Convolution (Impulse Decomposition)

**File:** `solution_D.py`

## ⚠️ This problem CANNOT reuse `signal_lti.py`

| | `signal_lti.py` (`DiscreteSignal`) | This problem (`ContinuousSignal`) |
|---|---|---|
| A signal is… | a finite **array of samples** at integer indices | a **function** `x(t)` of a real variable |
| Stored as… | `np.zeros(N)` | a Python function you can call at any `t` |
| Shift means… | move array elements | build a new function `x(t − shift)` |

Because the underlying representation is completely different, this folder ships its own
`ContinuousSignal` and `LTIContinuous` classes. Everything else in the assignment set
does reuse your discrete code — only this continuous practice needs fresh code.

## What the problem asks

Approximate a continuous input `x(t)` as a sum of tall, thin **rectangular impulses** and
show the approximation improves as the width `Δ` shrinks. (Output computation is **not**
required here — only the input decomposition.)

The model:
```
δ_Δ(t) = 1/Δ  for 0 ≤ t < Δ,  else 0        (a unit-area pulse of width Δ)
x(t) ≈ Σ_k  x(t_k)·Δ · δ_Δ(t − t_k),   t_k = k·Δ
```
Each coefficient `c_k = x(t_k)·Δ`, and since `δ_Δ` has height `1/Δ`, the term
`c_k·δ_Δ` has height `x(t_k)` on its little interval → a **staircase** version of `x(t)`.

## How the code solves it

**`ContinuousSignal`** wraps a function and returns *new functions* for each operation:
```python
def shift(self, shift):
    return ContinuousSignal(lambda t: self.func(t - shift))   # x(t - shift)
```
> `lambda t: ...` is a tiny anonymous function. Here `shift` builds and returns a brand
> new signal whose function evaluates the old one at `t - shift`. This is how you "delay"
> a continuous signal without any array.

**`linear_combination_of_impulses(x, Δ)`** builds one unit pulse, then for each
`t_k = k·Δ` in the window `[−3, 3]` returns the shifted pulse and its coefficient
`c_k = x(t_k)·Δ`:
```python
def unit_pulse(t):
    return np.where((t >= 0) & (t < delta), 1.0/delta, 0.0)   # 1/Δ on [0,Δ)
```
> `np.where(cond, a, b)` is a **vectorized if/else**: for every element of the array `t`
> it picks `a` where `cond` is True and `b` elsewhere — no Python loop needed.

**`reconstruct`** sums `Σ c_k·δ_Δ(t − t_k)` into one signal — the staircase `x̂(t)`.

**`main()`** builds `x(t)=e^{−t}u(t)` and `h(t)=u(t)`, then saves three figures.

## Result when you run it

```
Reconstruction check (smaller delta -> smaller error):
  delta = 0.5    max|x_hat - x| = 0.3933
  delta = 0.1    max|x_hat - x| = 0.0929
  delta = 0.05   max|x_hat - x| = 0.0523
  delta = 0.01   max|x_hat - x| = 0.0503
```

The error shrinks as `Δ` shrinks — the staircase converges to the smooth curve.
Figures are saved in `continuous_practice/` exactly as the spec requires:

- `figure1_input.png` — `x(t)` over `[−3, 3]`
- `figure2_components.png` — the component pulses `c_k·δ_Δ(t − t_k)` and the reconstruction
- `figure3_varying_delta.png` — `x(t)` vs `x̂(t)` for `Δ = 0.5, 0.1, 0.05, 0.01`

## Note on the `Δ = 0.05` vs `0.01` error

The reported error barely improves from `Δ=0.05` to `0.01`. That is not a bug — it comes
from the jump discontinuity of `x(t)` at `t=0`: near a step, any staircase is off by
about half a sample no matter how fine `Δ` is. Away from the jump the fit keeps improving,
which is what the overlay plot in `figure3` shows.
