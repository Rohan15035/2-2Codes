# CSE 220 — Practice Exam (Signals & Their Properties)

Three fresh problems in the same style and difficulty as the real online. Each is
worth **10 marks / 30 minutes**. Fill in the matching template, then check
yourself against `answer_key/`.

| #   | Template to edit                      | Skill it drills              | Based on  |
| --- | ------------------------------------- | ---------------------------- | --------- |
| P1  | `P1_time_scaling_template.py`         | interpolation + axis remap   | Problem A |
| P2  | `P2_periodicity_aliasing_template.py` | discrete sinusoid properties | Problem B |
| P3  | `P3_even_odd_discrete_template.py`    | reversal + decomposition     | Problem C |

> Rules of thumb for full marks: every plot needs **title, xlabel, ylabel,
> legend, grid**; print a **numeric check** (MSE / max-abs-error) to prove your
> result; values that fall outside the defined range should be **ignored**
> (set them to `NaN`).

---

## P1 — Time scaling by a real factor with linear interpolation

You are given a base signal `x(t)` sampled on a uniform grid
`t = linspace(-5, 5, 5001)`. Implement time scaling

$$ y(t) = x(a\,t), \qquad a > 0 \text{ (a real number, not necessarily an integer).}$$

Because `x` is only known at the sample times, `x(a·t[i])` usually lands
**between** two stored samples, so you must interpolate.

**Tasks**

1. (given) Build `t` and `x(t)`.
2. Implement `interpolate_signal(t_original, x_original, t_query)` using
   **linear interpolation**: if a query time lies a fraction `f` of the way from
   the left sample `xL` to the right sample `xR`, return `(1 - f)·xL + f·xR`.
   A query that lands exactly on a sample returns that sample. Query times
   outside `[t_min, t_max]` return `NaN`.
3. Implement `time_scale(t, x, a)` returning `y(t) = x(a·t)` using
   `interpolate_signal`.
4. Plot `x(t)` and `y(t)` on the same figure for `a = 0.5` (expansion) **and**,
   in a second figure, for `a = 2.0` (compression). Explain in one line why one
   stretches and the other squeezes, and why part of the compressed signal is
   missing.

**Marks:** linear interpolation 4 · time scaling 3 · both plots + explanation 3

---

## P2 — Periodicity and aliasing of a discrete-time sinusoid

For `x[n] = A·cos(Ω₀·n + φ)` on `n = arange(-25, 26)`:

**Tasks**

1. Implement `sinusoid(n, A, Omega0, phi)`.
2. A discrete sinusoid is periodic **only** when `Ω₀ / (2π)` is rational, i.e.
   `Ω₀·N = 2π·m` for some integers `N > 0`, `m`. Implement
   `fundamental_period(Omega0, max_N=1000)` that returns the smallest such `N`
   (or `None` if none is found up to `max_N`). Verify it with the provided
   `mse(...)`: for the found `N`, `mse(x[n], x[n+N])` over the overlapping range
   must be ≈ 0.
3. **Aliasing.** Using `mse`, demonstrate that shifting the frequency by `2π`
   changes nothing: `cos(Ω₀ n)` and `cos((Ω₀ + 2π) n)` are the **same** sequence
   (MSE ≈ 0), whereas `cos((Ω₀ + 0.5) n)` is a **different** sequence (MSE > 0).
4. Plot: (a) `x[n]` with a marker every `N` samples showing one period; (b) the
   three frequency variants from Task 3 as stems, so the alias overlaps the
   original. Be ready to explain why discrete frequency is only unique over an
   interval of length `2π`.

Use `Ω₀ = π/4` (periodic) and also try `Ω₀ = 1.0` (not periodic) to see
`fundamental_period` return `None`.

**Marks:** sinusoid 1 · fundamental_period 4 · aliasing demonstration 3 · plots 2

---

## P3 — Even/odd decomposition of a discrete signal + energy check

You are given a discrete signal `x[n]` on a symmetric index range
`n = arange(-M, M+1)`.

**Tasks**

1. (given) Build `n` and `x[n]`.
2. Implement `time_reverse(x)` returning the samples of `x[-n]`.
3. Using **only** `time_reverse`, implement `even_odd_decompose(x)` returning
   `xe[n] = ½(x[n] + x[-n])` and `xo[n] = ½(x[n] - x[-n])`.
4. Verify two properties with a printed number:
   - reconstruction: `max|(xe + xo) - x| ≈ 0`;
   - **energy split**: `E_x = E_xe + E_xo`, where `E = Σ |·|²`
     (the cross-term cancels because one part is even and the other odd).
5. Plot `x[n]`, `xe[n]`, `xo[n]` as stems on one figure, and confirm visually
   that `xe` is symmetric and `xo` is anti-symmetric about `n = 0`.

**Marks:** time_reverse 2 · even/odd decomposition 3 · reconstruction + energy
checks 3 · plot 2
