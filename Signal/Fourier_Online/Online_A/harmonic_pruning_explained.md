# Energy-Based Harmonic Pruning — the concept

*Companion notes for `fs_redrawer.py` (Online A). All numbers below come from
the actual run on `svgs/heart.svg` with N = 150, 1000 samples.*

---

## 1. The idea in one paragraph

A closed drawing is stored as 2N+1 = 301 complex Fourier coefficients. But those
301 numbers are not equally important: a handful of them carry almost all of the
signal's **energy**, and the rest are fine detail. Because the Fourier basis is
*orthogonal*, energy is **separable** — each harmonic owns a private slice of the
total, and the slices simply add up. That lets you rank harmonics by their slice,
keep only the biggest ones until you have (say) 99% of the energy, and throw the
rest away. For the heart, **6 of 301 harmonics carry 99.26% of the energy** — a
50× compression, and the error you pay is *exactly* the energy you discarded.

---

## 2. The setup: a drawing is a complex periodic signal

The SVG path is sampled into a complex-valued signal over one period:

```
f(t) = x(t) + j·y(t),        t ∈ [0, T],   T = 2π
```

Each sample is a point on the curve, encoded as a complex number. Since the curve
is closed, `f(0) = f(T)` — it is genuinely periodic, so a Fourier series applies.

Its Fourier coefficients are

```
c_n = (1/T) ∫₀ᵀ f(t) · e^(-j·n·ω·t) dt,        ω = 2π/T
```

and the reconstruction is

```
f̂(t) = Σ_{n=-N}^{N} c_n · e^(j·n·ω·t)
```

### Why negative harmonics exist here

For a **real** signal you only need `n ≥ 0`, because `c_{-n} = conj(c_n)` carries
no new information. Our signal is **complex** (x *and* y are independent), so
`c_n` and `c_{-n}` are unrelated and both must be kept.

Geometrically, each term `c_n·e^(jnωt)` is a **circle**:

| quantity | meaning |
|---|---|
| `\|c_n\|` | radius of the circle |
| `arg(c_n)` | its starting angle |
| `n` | how many turns per period — **sign = direction** |

Positive `n` spins counter-clockwise, negative `n` spins clockwise. Stack all
301 circles tip-to-tail and the final tip traces the drawing — that is the
epicycle animation. **Pruning = deleting the smallest circles from that chain.**

---

## 3. The enabling fact: Parseval's theorem

The total energy of the signal, measured in the time domain, equals the sum of
squared coefficient magnitudes in the frequency domain:

```
E_total = (1/T) ∫₀ᵀ |f(t)|² dt  =  Σ_{n=-N}^{N} |c_n|²
```

Verified numerically on the heart:

```
(1/T) ∫ |f(t)|² dt  = 0.6353372
Σ |c_n|²            = 0.6353371     ✓
```

This is *the* reason the whole task works. Orthogonality of `{e^(jnωt)}` means
the harmonics do not interfere in the energy budget — there are no cross terms.
So the phrase "the energy of harmonic *n*" is meaningful, and defining

```
E_n = |c_n|²          (energy of harmonic n)
```

gives a legitimate, additive importance score for each harmonic.

---

## 4. The key theorem: discarded energy *is* the error

Let `D` be the set of harmonics you zero out. Then the residual is just those
deleted terms:

```
f(t) − f̂(t) = Σ_{n ∈ D} c_n · e^(j·n·ω·t)
```

Apply Parseval to that residual:

```
MSE = (1/T) ∫₀ᵀ |f(t) − f̂(t)|² dt  =  Σ_{n ∈ D} |c_n|²  =  (1 − r) · E_total
```

**The mean squared error equals the energy you threw away.** Not approximately —
exactly. This is why "preserve a fraction *r* of the energy" is a principled
compression knob rather than a heuristic: choosing *r* is *directly choosing your
error budget*.

Checked against the run (`MSE` from `evaluate_reconstruction_error`, predicted
value from the energy identity):

| r | measured MSE | (1 − r_actual) · E_total | ratio |
|---|---|---|---|
| 0.96 | 2.5451e-02 | 2.5336e-02 | 1.0046 |
| 0.98 | 1.0945e-02 | 1.0913e-02 | 1.0029 |
| 0.99 | 4.7005e-03 | 4.6959e-03 | 1.0010 |

The ~0.3% gap is discretization: the code's MSE is a **discrete sample average**
`(1/M)Σᵢ|f(tᵢ) − f̂(tᵢ)|²` over 1000 points, while the identity is a continuous
time-average. They converge as M grows.

### Why "keep the top-k" is optimal

Since the error is `Σ_{n∈D}|c_n|²`, minimising error for a fixed number of kept
harmonics means **maximising the kept energy**, which means keeping the largest
`|c_n|²` values. Greedy is exactly optimal here (standard exchange argument: swap
any kept harmonic for a discarded larger one and the retained energy strictly
improves). No dynamic programming, no search — just sort.

This is the same principle behind JPEG, MP3 and PCA/SVD truncation.

---

## 5. The algorithm

Implemented in `prune_harmonics_by_energy(r)`:

1. **Score** — `E_n = |c_n|²` for all 2N+1 harmonics.
2. **Total** — `E_total = Σ E_n`.
3. **Rank** — sort harmonics by `E_n` descending (`np.argsort(-energies)`).
4. **Accumulate** — running sum `cumulative = np.cumsum(...)` down that ranking.
5. **Cut** — find the first index where `cumulative ≥ r · E_total`
   (`np.searchsorted`); that prefix is the minimal retained set.
6. **Zero** — every harmonic outside the prefix gets `c_n = 0`.
7. **Report** — return `(retained_count, cumulative[k-1] / E_total)`.

Note the ranking is over **all** harmonics jointly, positive and negative
together — `n = -1` and `n = +1` compete on equal footing and are kept or dropped
independently (see the table in §6, where `-1` is kept first and `+1` only sixth).

Two implementation details worth knowing:

- **`r = 1.00` and floating point.** Summing 301 floats sequentially
  (`cumsum`) can land a few ULPs below `np.sum`'s pairwise total, so
  `cumulative ≥ 1.0 · E_total` may never test true. `searchsorted` then returns
  `len(...)`, and clamping `k = min(k, len)` keeps all 301 — which is the correct
  answer. Without that clamp you get an off-by-one crash or a wrong count.
- **Pruning is destructive.** Zeroing coefficients loses the originals, so
  `calculate_all_coefficients()` stores a pristine `self.full_coeffs` and every
  prune restarts from it. That is what makes the four ratios runnable in one loop
  without recomputing 301 numerical integrals each time.

---

## 6. What actually happened to the heart

### The spectrum is brutally top-heavy

| rank | n | \|c_n\| | share of E_total | cumulative |
|---|---|---|---|---|
| 1 | **−1** | 0.7740 | 94.283% | 94.283% |
| 2 | **+2** | 0.1048 | 1.729% | 96.012% |
| 3 | **−3** | 0.0945 | 1.406% | 97.418% |
| 4 | **−2** | 0.0741 | 0.864% | 98.282% |
| 5 | **−4** | 0.0632 | 0.629% | 98.912% |
| 6 | **+1** | 0.0471 | 0.349% | 99.261% |
| 7 | 0 | 0.0434 | 0.297% | 99.558% |
| … | … | … | … | … |

The single harmonic `n = −1` carries **94.3%** of the energy on its own. That is
why `r = 0.96` retains only **2** harmonics — the first one nearly satisfies the
target by itself. (It is `n = −1`, not `+1`, simply because this path is traced
clockwise once per period; a big clockwise circle is the heart's "average shape".)

### Results

| Target r | Retained | Actual ratio | MSE | Kept harmonics |
|---|---|---|---|---|
| 0.96 | 2 | 0.9601 | 2.5451e-02 | −1, 2 |
| 0.98 | 4 | 0.9828 | 1.0945e-02 | −1, 2, −3, −2 |
| 0.99 | 6 | 0.9926 | 4.7005e-03 | −1, 2, −3, −2, −4, 1 |
| 1.00 | 301 | 1.0000 | 5.7818e-08 | all |

**Compression:** 6 complex numbers instead of 301 — a **50× reduction** (12 floats
vs. 602) for a 0.74% energy loss.

Note that "actual ratio" always *overshoots* the target (0.9601 ≥ 0.96). Energy
arrives in discrete lumps, so you land on or above the target, never exactly on
it — and the granularity is coarse when one harmonic dominates.

### Why coefficients decay so fast

| n | max(\|c_n\|, \|c_{−n}\|) |
|---|---|
| 1 | 7.74e-01 |
| 10 | 6.13e-03 |
| 100 | 6.22e-05 |
| 150 | 2.98e-05 |

Roughly `|c_n| ~ 1/n²`, hence `E_n ~ 1/n⁴` — energy collapses fourth-order fast.
The decay rate is set by the **smoothness** of the curve: the heart is smooth
almost everywhere except the bottom cusp and the top notch, and a corner in an
otherwise smooth path is exactly what produces `1/n²`. A perfect circle would
have a single non-zero coefficient; a shape with more corners would decay slower
and prune worse.

---

## 7. Reading the results honestly

Three things worth saying out loud in a report:

**(a) The r = 1.00 row is not a pruning result.** Nothing is discarded, so the
residual MSE of `5.78e-08` is not pruning error at all — it is the **truncation
error of stopping at N = 150** (energy living in harmonics `|n| > 150`) plus
numerical quadrature error from `np.trapezoid`. It is the noise floor of the
representation, and it is the baseline the other rows sit on top of.

**(b) High energy ratio ≠ visually faithful.** At r = 0.99 the reconstruction is
unmistakably a heart, but the bottom cusp is rounded off and the top notch is a
shallow dimple. Those sharp features are built from *many* high-order harmonics,
each carrying negligible energy — precisely the ones pruning deletes first. Energy
is a global, `L²` measure; it is blind to localized geometric detail. So:

> Energy-based pruning preserves the *gross shape* efficiently and sacrifices
> *sharp local features* first.

**(c) MSE inherits that blindness.** MSE is an average over the whole period, so a
large error confined to a small arc (the cusp) barely moves the number. A shape
metric like Hausdorff distance or curvature error would penalize the rounded cusp
far more than MSE does. MSE is the right metric for *this* task because it is the
one the energy identity predicts exactly — not because it matches human judgment.

---

## 8. Quick reference — what each piece does

| Symbol / method | Meaning |
|---|---|
| `f(t)` | ground-truth sampled drawing, `x + jy` |
| `c_n` | Fourier coefficient of harmonic `n`; a circle of radius `\|c_n\|` |
| `E_n = \|c_n\|²` | energy of harmonic `n` (additive, thanks to orthogonality) |
| `E_total = Σ E_n` | total signal energy (= time-domain energy, by Parseval) |
| `r` | target fraction of energy to preserve — your **error budget** |
| `prune_harmonics_by_energy(r)` | keeps the minimal top-energy set reaching `r`, zeros the rest |
| `evaluate_reconstruction_error()` | `(1/M) Σ \|f(tᵢ) − f̂(tᵢ)\|²`, which ≈ `(1−r)·E_total` |

**The one-sentence takeaway:** because the Fourier basis is orthogonal, energy is
additive per harmonic (Parseval), so ranking harmonics by `|c_n|²` and keeping a
cumulative-energy prefix is provably the best possible compression for a given
squared-error budget — and the error you incur is exactly the energy you dropped.
