# Part 2 — CFT problems (`cft_edge_detector.py`)

Problems 6 and 16–24. Written against your existing `CFT2D`, `FrequencyFilter`
and `InverseCFT2D`. Every method below was run and verified on a deliberately
**non-square** 31×27 test image, so any row/column swap would have shown up.

---

## The one helper that carries this entire section

Almost every problem here is "compute each entry's distance from the spectrum
centre, build a mask, multiply." Write this once:

```python
def _distance_grid(shape):
    rows, cols = shape
    ci, cj = rows // 2, cols // 2
    i, j = np.meshgrid(np.arange(rows), np.arange(cols), indexing='ij')
    return np.sqrt((i - ci)**2 + (j - cj)**2)
```

`indexing='ij'` is load-bearing: it makes the first output vary down **rows**,
matching the `[row, col] = [v, u]` layout of your spectrum. The default `'xy'`
transposes it and everything silently breaks on non-square images.

This replaces the given `high_pass`'s double Python loop with one vectorised
multiply — faster, and less to get wrong under time pressure.

**Three disciplines that get marked:**

1. **Work on copies.** `real.copy()` before mutating; never touch the caller's array.
2. **Respect strict-vs-inclusive inequalities exactly as written** (`r_low < d ≤ r_high`),
   or boundary rings get double-counted or dropped.
3. **A filter is an entrywise weight, and weights need not be 0/1.** Problem 18
   depends on this.

---

## Problem 6 — Band filters, complementarity, DC manipulation *(Section B's real online)*

### Task 1 — band-pass and band-stop

```python
def band_pass(self, real, imag, rlow, rhigh):
    d = _distance_grid(real.shape)
    m = (d > rlow) & (d <= rhigh)
    return real * m, imag * m

def band_stop(self, real, imag, rlow, rhigh):
    d = _distance_grid(real.shape)
    m = ~((d > rlow) & (d <= rhigh))
    return real * m, imag * m
```

Build the ring mask once and negate it for the stop-band. Deriving one from the
other by `~` is what *guarantees* Task 2 rather than merely hoping for it.

### Task 2 — complementarity check

```python
def check_complementarity(self, I_bp, I_bs, I_recon):
    delta = np.max(np.abs(I_bp + I_bs - I_recon))
    return bool(delta < 1e-9), delta
```

**One line of algebra is the whole story.** The two masks *partition* the entries —
every entry is in exactly one — so `F_bp + F_bs = F` **exactly**, entry by entry.
The inverse transform is linear in the spectrum, so the reconstructions add the
same way.

> **The graded trap:** compare against the **round-tripped** `I_recon`, never
> against the original image. Forward+inverse discretization error is far larger
> than 1e-9 — but it is *common to all three arrays and cancels in δ*.

**Verified:** δ = 4.4e-16 → `True`.

### Task 3 — DC manipulation

```python
def shift_brightness(self, real, imag, shift_amount):
    r, i = real.copy(), imag.copy()
    r[r.shape[0]//2, r.shape[1]//2] += shift_amount
    return r, i
```

**Why it brightens uniformly.** `F(0,0) = ∬I dx dy` is the total brightness.
Lifting that one spectrum sample by `A` adds a constant `A·Δu·Δv` — the sample's
integration cell — to **every** reconstructed pixel.

For a `[−1,1]²` image, `Δu = Δv = ½`, so `shift_amount = 2.0` brightens every pixel
by exactly **0.5**.

**Verified:** mean difference 0.500000, **std 2.4e-16** — the shift is genuinely
uniform, not just uniform on average. That std is the number to quote. Hence the
entry point must clip to [0, 1].

---

## Problem 16 — Low-pass and its complement

```python
def low_pass(self, real, imag, cutoff):
    d = _distance_grid(real.shape)
    m = (d <= cutoff)              # d == 0 (DC) is included
    return real * m, imag * m
```

**Prediction before running:** keeps smooth shading, kills edges → a **blurred**
image. Blurry but clean.

**Boundary care:** if you build this from a band mask with a lower edge, that edge
must sit **below zero** so the DC entry (`d = 0`) is retained. Excluding DC
silently darkens the whole result — you would have removed the average brightness.

### Task 2 — high-pass without calling `high_pass`

The disk and its exterior partition the entries, so entry by entry:

```
F_hp = F − F_lp
```

```python
real_hp = real - real_lp
imag_hp = imag - imag_lp
```

By linearity of the inverse, the same identity survives reconstruction:

```
I_hp = I_recon − I_lp        i.e.  "edges = image minus its blur"
```

That is the classic **unsharp mask** from image processing — worth naming out loud.

**Verified:** spectrum identity exact (0.00e+00); image identity 5.7e-16.

---

## Problem 17 — Data-driven cutoff selection

```python
def cutoff_for_energy(self, real, imag, r):
    d = _distance_grid(real.shape).astype(int)      # integer ring index
    E = real**2 + imag**2
    ring = np.bincount(d.ravel(), weights=E.ravel())  # one pass
    cum = np.cumsum(ring)
    cum = cum / cum[-1]
    return int(np.searchsorted(cum, r))
```

**Bucket → accumulate → threshold.** Floor each entry's distance to an integer ring
index, sum energy into one bucket per ring in a **single pass** (`np.bincount` with
`weights` — this is what the spec means by "no fresh scan per candidate ρ"), take
the cumulative sum outward, normalise, and `searchsorted` for the first radius
reaching `r`.

**The deliverable — how this combines both onlines.** It is Problem 5's
*greedy-cumulative-threshold* skeleton wearing Problem 6's *radial geometry*. One
algorithm, two exam costumes. And **2D Parseval** is what licenses calling
`ℜ² + ℑ²` "energy" in the first place.

**Verified:** on my smooth test image the disk `d ≤ 5` already held 98.7% of total
energy; ρ = 6 was returned for r = 0.99. A natural photo concentrates even harder —
which is the whole reason a small cutoff like 15 works.

---

## Problem 18 — Diagnosing and curing the ripples

### Task 1 — diagnosis

The faint ripples radiating from strong edges are **not an integration bug**. They
follow from the filter's *shape*.

The chain of reasoning, which is what gets marked:

1. The hard 0/1 disk in `high_pass` is a **rectangle profile** in frequency.
2. The **rect ↔ sinc** pair works in both directions: a sharp box in one domain is
   an oscillating, slowly-decaying sinc in the other.
3. Masking the spectrum with a hard edge therefore **convolves the image with a
   sinc-like kernel**, whose side lobes print rings around every strong edge.

**Name the design choice precisely:** the hard binary cutoff — the abrupt 0-to-1
transition at `d = cutoff`. This is the 2D sibling of Gibbs (Problem 14): both are
sharp truncation in frequency.

### Task 2 — cure

```python
def gaussian_high_pass(self, real, imag, sigma):
    d = _distance_grid(real.shape)
    H = 1 - np.exp(-d**2 / (2 * sigma**2))
    return real * H, imag * H
```

**Why it works: use a mask with no edge.** `H` rises smoothly from 0 at DC toward
1. A Gaussian's transform is again a Gaussian — **no side lobes, so no rings.**

**Does complementarity survive for `{H, 1−H}`?** **Yes.** `H + (1−H) = 1`
everywhere by construction, and linearity of the inverse does the rest. The check
needs the weights to **sum to one** — it never needed them to be in `{0,1}`.

**Verified:** Gaussian pair reconstructs to the round trip within 7.8e-16.

---

## Problem 19 — The rectangle transform, numerically

```python
t = np.linspace(-5, 5, 20001)
x = np.where(np.abs(t) <= 1, 1.0, 0.0)          # width-2 centered rect
omega = np.linspace(-10, 10, 401)
X = np.array([np.trapezoid(x * np.cos(o * t), t) for o in omega])
```

**Why one real integral suffices.** The imaginary part is `−∫x sin(ωt)dt`. For an
**even real** signal, `x·sin(ωt)` is even × odd = **odd**, and an odd integrand over
a symmetric interval vanishes. So `Im{X} ≡ 0` by symmetry and only the cosine
integral is needed.

That is the same even/odd bookkeeping as your offline's cosine/sine split — worth
pointing out, because it is the 1D shadow of why your `imag` array is what it is.

**Verified:** max deviation from `2sin(ω)/ω` was 5.0e-04 at 20001 samples — pure
trapezoid discretization error, and it shrinks as you sample more finely. At
`ω = 0` the analytic value is `T = 2` (the sinc's removable singularity — guard the
division).

**Task 2 — duality.** Width 6 gives `2sin(3ω)/ω`; the first zero moves from
`ω = π ≈ 3.142` to `π/3 ≈ 1.047`.

> **Main-lobe width scales as 1/T. Short in time ⇔ wide in frequency.**

The extreme cases bracket the whole course: the one-pixel image (Problem 21) is
infinitely narrow and has a perfectly flat spectrum; the constant image is
infinitely wide and is a single point at DC.

---

## Problem 20 — Injecting oscillation into an image

```python
modulated = img.image * np.cos(2*np.pi*u0*img.x)[np.newaxis, :]   # u0 = 20
```

`img.x` varies along **columns**, so shape the cosine `(1, W)` and broadcast it
down the rows. No Python loops.

**Prediction, before you run it.** `cos = ½(e⁺ + e⁻)` splits the spectrum into two
half-strength copies:

```
½F(u − u₀, v) + ½F(u + u₀, v)
```

So the central energy blob **vanishes from the centre and reappears as two blobs at
u = ±u₀**, unchanged in `v` — displaced **horizontally** in the plot, because
columns are the `u` axis. Each is half the original strength.

**Verified:** with `u₀ = 5` on my grid (`Δu` such that `u₀/Δu = 10`), the four
strongest bins landed at columns 3 and 23 with the centre column at 13 — exactly
±10 columns off centre, as predicted.

**Consequence for filtering (the actual deliverable).** Content that used to be
"low frequency" now sits `u₀/Δu` pixels from the centre. So **a high-pass now keeps
what it previously killed**, and a band-pass ring can be aimed to select exactly the
modulated content.

> Modulation moves signals between the kept and killed zones of every radial filter.

---

## Problem 21 — The one-pixel image

**The theory.** A single bright pixel is a sampled impulse. Sifting collapses the
transform integral to a single evaluation:

```
F(u,v) = C · e^{−j2π(u·x₀ + v·y₀)},   C = Δx·Δy   (the pixel's area weight)
```

### Task 1 — centered pixel (`x₀ = y₀ = 0`)

The exponent is zero, so `F ≡ C`: a **real constant**.

- `real` = constant `C` everywhere
- `imag` ≈ **0** everywhere
- magnitude **perfectly flat** — `plot_magnitude` shows a featureless field

**Verified:** `real.std() = 0.00e+00`, `real.mean() = 0.005128`, and independently
`Δx·Δy = 0.005128` — an exact match. `max|imag| = 0.00e+00`.

**Why this is Problem 19's duality at its extreme:** the narrowest possible signal
needs **all frequencies equally**.

### Task 2 — off-centre pixel

Now `real = C·cos(2π(ux₀+vy₀))` and `imag = −C·sin(·)`.

| Array | Verdict | Why |
|---|---|---|
| `real` | **changed** | becomes a striped cosine pattern |
| `imag` | **changed** | becomes a striped sine pattern, no longer zero |
| magnitude | **invariant** | `√(ℜ²+ℑ²) = C√(cos²+sin²) = C`, still flat |

**Verified:** magnitude std 7.2e-19 (flat to machine precision) while `real` std
rose to 0.0036 (visibly striped).

> **Position is stored entirely in phase.**

This is the exact 2D twin of Problem 7 — "delay changes every phase, no magnitude."
If an examiner asks why your `plot_magnitude` throws away the phase, this is the
answer: it throws away *where*, and keeps *how much*.

---

## Problem 22 — Hidden redundancy (conjugate symmetry)

**The relationship.** Conjugating the transform integral flips the sign of the
exponent. For a **real** image `I`, conjugating `I` does nothing, so the conjugated
integral is identical to evaluating the original at `(−u, −v)`:

```
F(−u, −v) = conj( F(u, v) )
```

That is the 2D version of `a₋ₖ = conj(aₖ)` for real 1D signals.

**Translating to your arrays.** Because `self.u` and `self.v` are *symmetric*
linspaces, negating a frequency is exactly reversing an index. So:

```python
assert np.allclose(real, real[::-1, ::-1])      # real part is SYMMETRIC
assert np.allclose(imag, -imag[::-1, ::-1])     # imag part is ANTISYMMETRIC
```

**Verified:** 2.8e-15 and 1.6e-16 respectively.

**The optimization this licenses.** Compute only half the `(v, u)` grid and fill the
rest by flip-and-negate — nearly **2×** on the forward transform. The same idea
inverts.

**The self-check it provides.** If a fresh implementation breaks either identity,
**hunt for a sign error in the sine term** — that is almost always what it is. This
is a genuinely useful debugging tool under exam pressure, and worth saying so.

---

## Problem 23 — Photometric editing in the frequency domain

```python
def scale_brightness(self, real, imag, factor):
    r, i = real.copy(), imag.copy()
    ci, cj = r.shape[0]//2, r.shape[1]//2
    r[ci, cj] *= factor;  i[ci, cj] *= factor
    return r, i

def boost_contrast(self, real, imag, gamma):
    ci, cj = real.shape[0]//2, real.shape[1]//2
    r, i = real*gamma, imag*gamma
    r[ci, cj], i[ci, cj] = real[ci, cj], imag[ci, cj]   # restore DC
    return r, i
```

**The clean split the problem is built on:**

- **DC carries the mean brightness.**
- **Every other entry carries deviations from the mean.**

So scaling DC by a factor scales the mean level → **brightness** (multiplicative,
versus Problem 6's `shift_brightness`, which is additive). Scaling everything
*except* DC → scales every deviation while pinning the mean → **contrast**.

**Implementation discipline for contrast:** scale-everything-then-restore-DC is
cleaner and safer than trying to mask the centre out. Save the centre values first.

**Verified:** `boost_contrast(2.0)` gave a reconstruction std ratio of exactly
**2.0000** against the original — deviations doubled, as designed.

**Post-processing the entry point must apply:** `γ > 1` pushes pixels outside
[0, 1], so **clipping is mandatory**.

**The unifying view worth ending on:** `high_pass` is `boost_contrast` pushed to
the extreme — DC *and its neighbourhood* scaled by **zero**.

---

## Problem 24 — Multi-band split with a guarantee

```python
def multi_band_split(self, real, imag, radii):
    edges = [-1.0] + list(radii) + [np.inf]
    d = _distance_grid(real.shape)
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (d > a) & (d <= b)
        out.append((real * m, imag * m))
    return out
```

**The half-open convention is the entire guarantee.** Consecutive half-open annuli
`(r₀, r₁], (r₁, r₂], …` mean every entry's distance falls in **exactly one**
interval, so the masks sum to the all-ones array **by construction, not by luck**.
That is precisely what the spec means by "for any `radii`."

**The two sentinel edges do specific jobs:**

- **First edge `−1`** must sit below zero so that `d = 0` (the DC entry) belongs to
  the lowest band. Start at 0 with a strict `>` and you orphan DC.
- **Last edge `∞`** so the array's **corners** — which are further from the centre
  than any listed radius — are not orphaned either.

**The k-band check** generalises Problem 6: sum all returned `real` arrays (and all
`imag`) and assert equality with the input. Or reconstruct each band and check the
images sum to the round trip.

**Energy shares:** per-mask sums of `ℜ² + ℑ²` over the total (2D Parseval again).

**Verified:** 4 bands from `radii = [2, 6, 12]`, entrywise sum error **exactly
0.00e+00** for both arrays; shares 0.9563 / 0.0333 / 0.0089 / 0.0015.

**Typical decomposition of a photo, worth naming:** low band = blurry base, mid =
shapes and soft edges, high = fine texture. That is **JPEG's keep / quantize / drop
trio**.

---

## CFT cheat table

| Operation | Spectrum edit | Result |
|---|---|---|
| `high_pass(c)` | zero `d ≤ c` | edges |
| `low_pass(c)` | zero `d > c` | blur |
| `band_pass(a,b)` | keep `a < d ≤ b` | scale-selective |
| `shift_brightness(A)` | `+A` at DC | every pixel `+A·Δu·Δv` |
| `scale_brightness(f)` | `×f` at DC | multiplicative brightness |
| `boost_contrast(γ)` | `×γ` everywhere but DC | contrast |
| `gaussian_high_pass(σ)` | `×(1−e^{−d²/2σ²})` | edges, **no ringing** |
| modulate by `cos(2πu₀x)` | two half copies at `u = ±u₀` | shifts content across filters |

**Identities to have memorised:**

- `F_hp = F − F_lp`, and after inversion `I_hp = I_recon − I_lp` (unsharp mask)
- `F(−u,−v) = conj(F(u,v))` → `real` symmetric, `imag` antisymmetric under `[::-1,::-1]`
- One pixel at `(x₀,y₀)` → `F = Δx·Δy·e^{−j2π(ux₀+vy₀)}`; magnitude flat, position in phase
- Complementarity always compares against the **round trip**, never the original
