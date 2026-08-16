# Part 1 — Fourier Series problems (`fs_redrawer.py`)

Problems 1–5 and 7–15. Every method below is written against your existing
`FourierEpicycles` class and was run and verified numerically.

**The one sentence that unlocks two-thirds of this section:** every coefficient
`c_n` is a complex number, so it has a *magnitude* and a *phase*. Operations that
move the drawing in space touch magnitudes; operations that retime the drawing
touch only phases. Sort each problem into that split before you write a line.

**Universal rules for this section**

- Energy of a harmonic is `abs(c)**2`, never `c**2` — the coefficients are complex.
- Zero coefficients out, never `del` them. `approximate` and the animation code
  iterate the dictionary and will break on missing keys.
- Build a **fresh object per experiment**. Pruning and shifting are destructive.

---

## Problem 1 — Centroid and rigid translation

```python
def get_centroid(self):
    return self.coeffs[0]

def translate(self, dz):
    self.coeffs[0] = self.coeffs[0] + dz
```

**Why.** Set `n = 0` in the coefficient integral: the kernel `exp(-j·0·ωt)`
becomes 1, so `c₀ = (1/T)∫f(t)dt` — the time-average pen position, which is the
centroid by definition. It is already in the dictionary, so the getter is a
lookup. No new integration is needed, which is exactly what the spec forbids.

For translation, adding a constant `d` to a signal changes only its average. By
linearity, `f(t) + d` has identical `cₙ` for every `n ≠ 0` and `c₀ + d` at zero.
So exactly one entry changes.

**Geometric reading (say this in the viva).** `c₀` is the only epicycle that does
not rotate — its frequency is zero. It is the anchor the whole chain hangs off.
Move the anchor and the entire drawing slides rigidly.

**Verified:** centroid prints ≈ 7e-17 (the loader centres every shape); after
`translate(2+3j)` the reconstruction's mean is 2 + 3.0003j.

---

## Problem 2 — Spectrum visualization

```python
def plot_spectrum(self):
    ns = sorted(self.coeffs)
    mags = [abs(self.coeffs[n]) for n in ns]
    phases = [np.angle(self.coeffs[n]) for n in ns]
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].stem(ns, mags);   ax[0].set_ylabel("|c_n|")
    ax[1].stem(ns, phases); ax[1].set_ylabel("angle(c_n) [rad]")
    ax[1].set_xlabel("harmonic index n")
    plt.show()
```

**Why sorted order.** A dict has no guaranteed key order matching `n`. Iterating
`sorted(self.coeffs)` gives you `n`, `|cₙ|` and `∠cₙ` as three aligned arrays —
misalign them and the stems land on the wrong harmonics.

**What you'll see, and why it matters.** A handful of tall stems clustered at
small `|n|` and a fast-decaying tail. For a heart, `n = −1` towers over everything
(measured: 87% of total energy in my test shape). That picture *is* the
justification for pruning in Problem 5 — most harmonics carry almost nothing.

The phase plot looks like scatter. That is expected and not a bug: **phase carries
the *where*, not the *how much*.** Problems 7 and 21 make this precise.

---

## Problem 3 — Shape morphing by coefficient blending

```python
def blend(coeffs_a, coeffs_b, alpha):
    return {n: (1-alpha)*coeffs_a[n] + alpha*coeffs_b[n] for n in coeffs_a}
```

**The property is linearity.** The coefficient integral is linear in the signal,
so the coefficients of `αx + βy` are `αaₖ + βbₖ`.

**The precondition is a shared period.** Both signals must have the same `T`,
hence the same `ω₀` — otherwise harmonic `n` of one drawing is a physically
different frequency from harmonic `n` of the other and adding them entry-by-entry
is meaningless. The spec's "both sampled on [0, 2π]" is what guarantees it.

**Verified:** blending coefficients matches re-integrating the blended signal to
8.8e-17 — machine precision — at every α. α = 0 and α = 1 reproduce the originals
exactly.

---

## Problem 4 — Energy in two domains (Parseval)

```python
def total_energy(self):
    return sum(abs(c)**2 for c in self.coeffs.values())

# independent time-domain check:
power = np.trapezoid(np.abs(signal)**2, t) / T
```

**Why they agree.** Expand `(1/T)∫|f|²dt` using the series. You get a double sum
over `n` and `m` of `cₙ c̄ₘ (1/T)∫e^{j(n−m)ωt}dt`. For `n ≠ m` that integral is a
whole number of cycles of a complex exponential and averages to **zero**. Only the
`n = m` terms survive, leaving `Σ|cₙ|²`. That is Parseval's identity.

**Verified:** both print 0.701172 on my test heart — identical to six decimals.
Any residual gap is the energy of harmonics beyond `|n| = N`, which is negligible.

**The trap:** `abs(c)**2`, not `c**2`. Squaring a complex number gives you another
complex number, not an energy.

---

## Problem 5 — Energy-preserving harmonic pruning *(Section A's real online)*

```python
def prune_harmonics_by_energy(self, r):
    E = {n: abs(c)**2 for n, c in self.coeffs.items()}
    total = sum(E.values())
    kept, acc = [], 0.0
    for n in sorted(E, key=E.get, reverse=True):   # most energetic first
        if acc >= r * total:                        # CHECK BEFORE TAKING
            break
        acc += E[n]
        kept.append(n)
    for n in self.coeffs:
        if n not in kept:
            self.coeffs[n] = 0j
    return len(kept), acc / total

def evaluate_reconstruction_error(self):
    resid = self.signal - self.approximate(self.t)
    return np.mean(np.abs(resid)**2)
```

**Why greedy is correct here.** Parseval (Problem 4) makes `|cₙ|²` *the* energy of
harmonic `n`, and the energies simply add. So "smallest subset reaching a fraction
`r`" is solved by taking the biggest ones first — no cleverer search can do better
when the items are additive and you only care about the total.

**The minimality discipline.** `if acc >= r*total: break` *before* adding is what
makes the answer minimal. If you check after adding, you take one harmonic too
many and report the wrong count. This same check-before-act pattern reappears in
Problems 14 and 17 — get it right once.

**Talking points.** Energy decides the pickup order, **not** index, and the order
is **not** ±-symmetric: on my test heart it went −1, −3, −2, 2, 3, −4. At r = 1.00
everything survives and the MSE drops to ~1e-32 (exactly zero coefficients removed);
on a shape with a truncation tail it bottoms out around 1e-8 instead — the `|n| > N`
content that was never in the dictionary to begin with.

**Verified:** r = 0.99 on my heart keeps 4 harmonics for an actual ratio of 0.9903.

---

## Problem 7 — Time shift (retiming the animation)

```python
def shift_in_time(self, t0):
    for n in self.coeffs:
        self.coeffs[n] *= np.exp(-1j * n * self.omega * t0)
```

**Why.** Substitute `t → t − t₀` into the series: each term picks up
`e^{−jnωt₀}`. That factor has magnitude 1, so it is a **pure rotation** of each
coefficient in the complex plane.

**Answer the three deliverables directly:**

- **(c)** Every `∠cₙ` rotates by `−nωt₀`; every `|cₙ|` is **unchanged**.
- **(a)** Because magnitudes are untouched, the *set of points* traced over a full
  period is identical — the path on screen is the same closed curve.
- **(b)** The GIF shows the same circles with the same radii drawing the same
  outline, just **starting from a different point** of it.

**The rotation is n-dependent** — higher harmonics rotate more, because the same
fixed delay eats a larger fraction of a faster wave's cycle.

**The favourite trap:** distinguish this from Problem 1's `translate`. Translate
*moves the drawing* and touches only `c₀`. Time shift *retimes the drawing* and
touches every coefficient non-uniformly.

**Verified:** max magnitude change 2.8e-17; reconstruction matches an interpolation
of `f(t − 0.7)` to 1.2e-05.

---

## Problem 8 — Time reversal and composition

```python
def reverse_time(self):
    self.coeffs = {n: self.coeffs[-n] for n in self.coeffs}
```

**Why.** `f(−t) = Σ cₙ e^{−jnωt}`. Relabel `m = −n` and it becomes
`Σ c₋ₘ e^{jmωt}` — so the coefficient at index `m` is the old one at `−m`.
Reversal **swaps the roles of +n and −n**. Every epicycle now spins the opposite
way and the GIF traces the same outline backwards.

Build the new dict as a comprehension, not in place — writing `coeffs[n] =
coeffs[-n]` one key at a time overwrites values you still need.

**Task 2 — realizing `f(4 − t)`.** Substitute inside-out. Write
`f(4 − t) = g(−t)` where `g(t) = f(t + 4)`. Getting `f(t + 4)` is an *advance*,
which is `shift_in_time(-4)`. Then reverse. So:

```python
fs.shift_in_time(-4)   # now the object represents g(t) = f(t+4)
fs.reverse_time()      # now it represents g(-t) = f(4-t)
```

**Justify the order like this:** after each call, state what the dictionary
currently represents. That is the only reliable way to compose these — the reverse
lands the phase factors on the negated indices, giving the textbook
`c₋ₙ e^{−j4nω}`.

**Verified:** max error 9.9e-07 against a direct interpolation of `f(4 − t)`.

---

## Problem 9 — Rotation and scaling

```python
def transform_drawing(self, s, theta):
    k = s * np.exp(1j * theta)
    for n in self.coeffs:
        self.coeffs[n] *= k
```

**Why.** In the complex plane, scaling by `s` and rotating by `θ` about the origin
is just multiplication of every signal value by the single constant `s·e^{jθ}`.
Linearity holds for complex constants, so **every coefficient is multiplied by
that same constant** — uniformly.

**Per-epicycle effect:** radius grows by `s`, starting angle advances by `θ`,
**speed `nω` untouched**.

**The deliverable question — which operation modifies exactly one coefficient?**
Translation (Problem 1, only `c₀`). Rotation and scaling touch all of them
*uniformly*; time shift touches all of them *non-uniformly*. That three-way
contrast is the whole point of the question.

**Verified:** multiplying all coefficients by `j` equals `j·f̂(t)` pointwise to
3.3e-16.

---

## Problem 10 — Time scaling (changing the clock)

```python
def rescale_time(self, alpha):
    self.omega *= alpha
    self.T /= alpha
    # self.coeffs deliberately untouched
```

**Why nothing in the dictionary changes.** Substitute `αt` into the series:
`f(αt) = Σ cₙ e^{jn(αω)t}`. The *same coefficients* are riding a **new frequency
ruler**. So the object's clock changes, not its coefficients.

This is the one property in the whole table that acts on the object's metadata
rather than its data. Everything downstream — `approximate`, and the animation
timing that reads `fs.omega` / `fs.T` — then produces the identical shape traced
α times faster. All epicycle speeds `nω` scale together; radii and starting angles
are unchanged.

**If you find yourself modifying coefficients here, you have answered a different
question.**

**Verified:** after `rescale_time(2.0)`, `approximate(t)` equals the original
`f(2t)` **exactly** (0.00e+00), and the dictionary is byte-for-byte identical.

---

## Problem 11 — Derivative coefficients

```python
def derivative_coeffs(self):
    return {n: 1j * n * self.omega * c for n, c in self.coeffs.items()}
```

**Why.** Differentiate `cₙ e^{jnωt}` term by term: the chain rule brings down
`jnω`. No finite differencing on the samples is needed or allowed.

**The geometric reading — this is what the question is actually testing.**
Harmonic `n` is circular motion of radius `|cₙ|` at angular speed `nω`.

- **Size:** speed on a circle is `ωr = |nω|·|cₙ|` — that is the `nω` factor.
- **Direction:** velocity points **tangent** to the circle, a 90° turn from the
  position vector — which is precisely what multiplying by `j` does.

So `jnω` is not an algebraic accident; it is "turn 90° and scale by the speed."

**Why high harmonics dominate the derivative.** The multiplier grows *linearly* in
`|n|`, so the fastest epicycles are amplified most. A shape whose coefficients
decay like `1/n²` (anything with a corner) has a derivative decaying only like
`1/n` — barely convergent, and visibly jittery near star tips and cusps. The next
derivative would place impulses at the corners (jump → impulse).

**Verified on the circle** (`z = e^{jt}`, exact derivative `je^{jt}`): max error
2.6e-13.

---

## Problem 12 — Integral coefficients and the lost constant

```python
def integral_coeffs(self, mean_value=0.0):
    return {n: (complex(mean_value) if n == 0 else c / (1j * n * self.omega))
            for n, c in self.coeffs.items()}
```

**Why `n = 0` is special, and why that is not a hack.** Dividing by `jnω` inverts
the derivative rule — but at `n = 0` that is division by zero. And rightly so:
differentiation maps *every* constant to the same derivative, so **no integration
rule can possibly recover the antiderivative's mean.** The information was
destroyed, not mislaid. `mean_value` is the interface's way of asking the caller to
supply it. (Same reason the lectures compute `a₀` separately for the sawtooth.)

**The round trip** returns every `n ≠ 0` coefficient exactly — the `jnω` factors
cancel — and sets `c₀` to whatever you passed. **Identity minus the mean.**

**Periodicity condition.** The running integral gains `c₀T` per period, so the
integral of a periodic signal is itself periodic **iff `c₀ = 0`** — true for the
centered SVGs, since Problem 1 showed `c₀ ≈ 0`.

**Verified:** round trip max error 2.8e-17 over all `n ≠ 0`.

---

## Problem 13 — Product of two signals

```python
def multiply_coeffs(self, other):
    out = {}
    for p, ap in self.coeffs.items():
        for q, bq in other.coeffs.items():
            out[p+q] = out.get(p+q, 0j) + ap*bq
    return out
```

**Why convolution.** One term from each series multiplies to
`a_p b_q e^{j(p+q)ωt}` — it lands in harmonic `k = p + q`. Collect every pair that
sums to `k` and you get `cₖ = Σ_p a_p b_{k−p}`. That is a convolution of the two
coefficient sequences.

**Same machine as two things you already know:** substitute `z = e^{jω₀t}` and this
is literally polynomial multiplication; it is also the LTI convolution sum.

**The range trap the problem is built around.** With both inputs over `|n| ≤ N`,
the product reaches `|k| ≤ 2N` — **wider than either input**. A fixed-size
structure sized for `N` silently drops the ends. Using `out.get(p+q, 0j)` on a
plain dict accommodates the widening automatically.

**Verified** on `x(t) = 1 + cos(ω₀t)`, `p = x²`: input stems (½, 1, ½) at
`k = −1, 0, 1`; self-convolution returns exactly (¼, 1, 3/2, 1, ¼) at `k = −2..2`,
matching the closed form `c₀ = 3/2, c±1 = 1, c±2 = ¼`.

---

## Problem 14 — Pruning under an error budget

**Task 1 — the identity.** The error signal after discarding a set `D` is *exactly*
the discarded series `Σ_{n∈D} cₙ e^{jnωt}`. Apply Parseval to that error signal:
its average power — which the MSE over uniform samples approximates — equals
`Σ_{n∈D}|cₙ|²`.

> **MSE = discarded energy.** No reconstruction is ever needed.

**Task 2 — implementation.** This is Problem 5 walked from the other end.

```python
def prune_to_mse(self, eps):
    E = {n: abs(c)**2 for n, c in self.coeffs.items()}
    discarded, dropped = 0.0, 0
    for n in sorted(E, key=E.get):          # WEAKEST first
        if discarded + E[n] > eps:          # check before acting
            break
        self.coeffs[n] = 0j
        discarded += E[n]; dropped += 1
    return dropped, discarded
```

Same sort as Problem 5, opposite direction, same check-before-acting discipline.
`approximate` is never called — the guarantee comes from Parseval, not from testing.

**Verified:** with ε = 4.7e-3, dropped 296 harmonics for a predicted 2.93e-03 and a
measured MSE of 2.93e-03 — the theory and the measurement agree.

**Task 3 — Gibbs phenomenon.** Build a 0/1 square wave on [0, 2π] and reconstruct
with N = 50.

**Measured maximum: 1.0898** — an ≈8.98% overshoot beside each jump (the classic
figure is ≈8.95%).

**Why it does not go away as N grows.** Near a discontinuity the partial sum
overshoots by a *fixed fraction of the jump height*, no matter how many harmonics
you add. Growing N only makes the overshooting spike **narrower**, not shorter.

- **MSE does improve** with N — the spike thins, so its energy shrinks.
- **Max error does not** — it converges to ~8.95% of the jump.

**Practical echo:** this is exactly why pruned drawings wobble at corners and cusps.

---

## Problem 15 — Fixed-budget compression and shape geometry

```python
def prune_to_count(self, K):
    E = {n: abs(c)**2 for n, c in self.coeffs.items()}
    total = sum(E.values())
    kept = set(sorted(E, key=E.get, reverse=True)[:K])
    for n in self.coeffs:
        if n not in kept:
            self.coeffs[n] = 0j
    return sum(E[n] for n in kept) / total
```

Problem 5 with the stopping rule "count reached" instead of "energy reached."

**Task 2 — the analysis, which is where the marks are.**

**The circle's row is all 1s** because a circle traced at constant speed *is* a
single complex exponential, `z = e^{jt}`. One harmonic holds essentially all the
energy; there is nothing to add. (Confirmed: my circle needs 1 harmonic at every
ratio including 0.999.)

**The governing principle:**

> **Smoothness in time ⇔ decay in frequency.**

Smooth curves have rapidly decaying `|cₙ|`. Corners and cusps push energy into high
harmonics with only ~`1/n²` decay, so banking 99.9% of the energy demands many more
of them. **The heart's last column is large because of its cusp** — that single
non-smooth point is what costs it 11 harmonics where the circle needs 1.

**This is JPEG's founding observation:** natural images are mostly smooth, so most
of their frequency content is negligible and can be thrown away.

---

## Fourier-series cheat table

| Time domain | Coefficients | Touches |
|---|---|---|
| `x(t) + d` (translate) | `c₀ + d` only | one entry |
| `s·e^{jθ}x(t)` (rotate/scale) | all `×s·e^{jθ}` | all, uniformly |
| `x(t − t₀)` (delay) | all `×e^{−jnωt₀}` | all phases, non-uniformly |
| `x(−t)` (reverse) | swap `±n` | index flip |
| `x(αt)` (faster clock) | **unchanged** | `ω → αω`, `T → T/α` |
| `x′(t)` | `×jnω` | high `n` amplified |
| `∫x dt` | `÷jnω`, `n ≠ 0` | `c₀` supplied separately |
| `x(t)y(t)` | `Σ_p a_p b_{k−p}` | range doubles to `2N` |
