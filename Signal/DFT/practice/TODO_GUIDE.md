# TODO Guide — Practice Onlines (DFT / FFT)

This file explains **only the `# TODO (student)` blocks** in `problems/*.py`.
Everything else in those files — the `run()` runner, `_make_engine()`, `_resolve()`,
report/image writing, and the helpers marked *"Provided"* — is already written and
should not be touched. The offline modules (`bigmul.py`, `transforms.py`,
`image_conv.py`, `image_utils.py`, `io_utils.py`) are imported from the parent
folder and must not be modified either.

Every one of the 10 problems has exactly **3 TODOs**, and they always follow the
same three-layer shape:

| TODO | Layer | What it does |
|------|-------|--------------|
| 1 | **Setup** | Pick the transform length / shape, or build a multiplier mask |
| 2 | **Spectral core** | Pad → transform → combine spectra → **one** inverse → `.real` → crop |
| 3 | **Wrapper** | Convert inputs, dispatch grayscale/RGB, carry digits, unwrap indices |

---

## Part 0 — Patterns that repeat in every file

Learn these five once and most TODOs become mechanical.

### 0.1 The transform-length rule

Linear convolution of two sequences of length `n` and `m` produces `n + m - 1`
coefficients. The transform must have **at least** that many slots, or the tail
wraps around onto the head (that wraparound is the whole point of A3).

```
need = n + m - 1                    # two factors
need = n + q + r - 2                # three factors (A1)
need = 2n - 1                       # a square (A5)
```

Then round according to the engine:

```python
if engine.name == "arbitrary":
    return need                     # Bluestein: any length works
return next_power_of_two(need)      # radix-2 FFT needs 2^k
```

> **Per-file detail:** in the A-series the `dft` engine is also rounded up to a
> power of two (it falls through to the same `next_power_of_two`). In **B2** the
> rounding is guarded by `if engine.name == "fft"`, so `dft` and `arbitrary` both
> use the exact full size there. Copy the shape shown in each file's comment.

### 0.2 The spectral-core recipe

```python
fa = np.zeros(N, dtype=np.complex128); fa[:len(a)] = a     # zero-pad
A  = engine.transform(fa)                                   # forward
...                                                         # combine spectra
coeffs = engine.inverse(SPECTRUM).real[:need]               # ONE inverse, real part, crop
return np.rint(coeffs).astype(np.int64), N                  # round (integers only)
```

Three rules that are graded:

1. **One inverse transform.** Anything you can express as a product/sum of
   spectra must come back in a single `engine.inverse(...)` call.
2. **`.real` always.** The inputs are real, so the imaginary part is only
   floating-point noise.
3. **`np.rint` before `astype(np.int64)`** for integer work. A plain cast
   truncates, and `1999.9999` silently becomes `1999`.

### 0.3 Engine dispatch

`_make_engine(name)` is provided. The three engines share one interface —
`.transform(x)`, `.inverse(spectrum)`, `.name` — so your code never branches on
the engine except to choose the length.

| `name` | Class | Length constraint |
|--------|-------|-------------------|
| `dft` | `DFTAnalyzer` | any N (direct O(N²) sums) |
| `fft` | `FFTTransformer` | power of two (radix-2) |
| `arbitrary` | `ArbitraryLengthFFT` | any N (Bluestein chirp) |

### 0.4 Grayscale / RGB dispatch (all of B1–B5, always TODO 3)

Identical body in five files:

```python
image = np.asarray(image, dtype=np.float64)
if image.ndim == 2:
    return work_on_one_plane(image, ...)
if image.ndim == 3 and image.shape[2] == 3:
    planes = [work_on_one_plane(image[:, :, c], ...) for c in range(image.shape[2])]
    return np.stack(planes, axis=-1)
raise ValueError("images must be grayscale or RGB")
```

The `np.stack(..., axis=-1)` puts the channels back on the **last** axis so the
output keeps the input's shape. (B4 sums the per-channel surfaces instead of
stacking; B5 stacks two lists, one for `low` and one for `high`.)

### 0.5 Index unwrapping (A4, B4)

A DFT output of length `N` stores lag `k` at index `k mod N`, so the upper half
of the array holds the **negative** lags:

```python
if k > N // 2:
    k -= N
```

The same logic in B5 says bin `u` of an `H`-point DFT carries frequency
`min(u, H - u)`.

---

# Part A — Big-integer problems (`a1`–`a5`)

Shared background: `to_limbs(text, base_digits)` returns `(sign, array)` where the
number is written in base `10^base_digits`, least-significant limb first.
`from_limbs(sign, coeffs, base_digits)` performs the **carry** and returns the
decimal string. Multiplying two numbers = convolving their limb arrays.
Default `BASE_DIGITS = 4`.

---

## A1 — `a1_triple_product.py` — product of THREE big integers

**Goal:** `A * B * C` using exactly **one** inverse transform.

### TODO 1 — `choose_transform_length(len_a, len_b, len_c, engine)`

A product of three polynomials with `n`, `q`, `r` coefficients has
`n + q + r - 2` coefficients (each multiplication costs `-1`, and there are two
multiplications). So `need = len_a + len_b + len_c - 2`, then apply §0.1.

### TODO 2 — `multiply_three_transform(a, b, c, engine)`

Zero-pad all three limb arrays to `N`, take **three forward transforms**,
multiply the three spectra pointwise, and invert **once**:

```python
spectrum = engine.transform(fa) * engine.transform(fb) * engine.transform(fc)
coeffs   = engine.inverse(spectrum).real[:need]
```

Return `(np.rint(coeffs).astype(np.int64), N)`.

### TODO 3 — `multiply_three(text_a, text_b, text_c, method)`

Convert each operand with `to_limbs(text, TRIPLE_BASE_DIGITS)`, keep the three
signs, convolve, then carry with the **same** base and re-attach the sign:

```python
product = from_limbs(sign_a * sign_b * sign_c, coeffs, TRIPLE_BASE_DIGITS)
```

**Why `TRIPLE_BASE_DIGITS = 2` and not the usual 4** — this is the point of the
problem. A triple-product coefficient is a sum of ~`n²/2` products of *three*
limbs, so it reaches about `(n²/2)(B-1)³`. With `B = 10⁴` that overflows the
53-bit double mantissa the FFT relies on; `B = 10²` keeps every coefficient
exact. Using the base-4 default here is the classic way to get a `MISMATCH`.

---

## A2 — `a2_sum_of_products.py` — `a*b + c*d` with ONE inverse

**Goal:** exploit **linearity** of the DFT.

### TODO 1 — `choose_transform_length(len_a, len_b, len_c, len_d, engine)`

Two independent products share one transform length, so take the larger
requirement: `need = max(len_a + len_b - 1, len_c + len_d - 1)`, then §0.1.

### TODO 2 — `sum_of_products_transform(a, b, c, d, engine)`

Pad and transform all four arrays (four forward transforms), then add **in the
frequency domain** before inverting — because `IDFT(A·B + C·D) = a*b + c*d`:

```python
coeffs = engine.inverse(A*B + C*D).real[:need]
```

One inverse for both products. Computing two separate inverses and adding the
results in the time domain gives the same numbers but misses the point of the
exercise.

### TODO 3 — `sum_of_products(text_a, text_b, text_c, text_d, method)`

Convert all four with `to_limbs` (default base). **Raise `ValueError` if any sign
is negative** — `from_limbs` carries a magnitude plus a single sign, so it cannot
represent a sum whose two products have opposite signs. Then convolve and carry
with sign `+1`: `from_limbs(1, coeffs)`.

---

## A3 — `a3_circular_wraparound.py` — circular vs. linear convolution

**Goal:** demonstrate *why* padding matters, by deliberately not padding enough.
Nothing here is "wrong output" — the wraparound **is** the answer.

### TODO 1 — `short_length(len_a, len_b, engine)`

`N = max(len_a, len_b)` — enough to hold either input, deliberately far too
little for the `len_a + len_b - 1` product coefficients. Round up for the
non-arbitrary engines as in §0.1.

### TODO 2 — `circular_convolve(a, b, N, engine)`

The standard recipe with **no cropping**: pad both arrays to exactly `N`,
transform, multiply, invert, `.real`, `np.rint(...).astype(np.int64)`. All `N`
slots are the result. Multiplying two spectra of length `N` is *by definition*
circular convolution modulo `N`.

### TODO 3 — `fold(linear, N)`

The mathematical model of what TODO 2 physically did: take the full linear
convolution and add each coefficient back onto slot `m mod N`.

```python
out = np.zeros(N, dtype=np.int64)
for m in range(len(linear)):
    out[m % N] += linear[m]
return out
```

The runner checks `circular_convolve(...) == fold(linear, N)` — proving that a
too-short transform doesn't lose information, it *aliases* it.

---

## A4 — `a4_shift_correlation.py` — cross-correlation to find a shift

**Goal:** recover an unknown lag between two limb sequences.

### TODO 1 — `choose_transform_length(len_a, len_b, engine)`

Lags run from `-(len_a - 1)` to `len_b - 1`, i.e. `len_a + len_b - 1` distinct
values — the same count as linear convolution, so the same rule:
`need = len_a + len_b - 1`, then §0.1.

### TODO 2 — `cross_correlate(a, b, engine)`

Correlation is convolution with a **time-reversed** `a`, and for a real sequence
time reversal is **conjugation** in the frequency domain:

```python
spectrum = np.conj(engine.transform(fa)) * engine.transform(fb)
c = engine.inverse(spectrum).real
```

Result: `c[k] = Σ_i a[i] · b[i + k]`, with lag `k` stored at index `k mod N`.
No cropping — every slot is a lag.

### TODO 3 — `find_shift(text_a, text_b, method)`

Use the **limb magnitudes only** (discard the signs returned by `to_limbs`),
correlate, take `k = int(np.argmax(c))`, then unwrap per §0.5
(`if k > N // 2: k -= N`). Return `(k, int(c.max()), N)`. The peak value comes
from the array itself — unwrapping only relabels the index, it doesn't move data.

The runner builds `b = a · BASE^shift`, so `b`'s limbs are `a`'s moved up by
exactly `shift` slots and the peak must land there.

---

## A5 — `a5_fourth_power.py` — `a⁴` by squaring twice

**Goal:** one forward transform per square, and a lesson about carrying.

### TODO 1 — `square_length(n, engine)`

A square has `2n - 1` coefficients: `need = 2*n - 1`, then §0.1.

### TODO 2 — `square_transform(a, engine)`

Squaring needs the transform of `a` **once**; reuse it:

```python
A = engine.transform(fa)
coeffs = engine.inverse(A * A).real[:need]
```

Calling `engine.transform` twice on the same padded array is the mistake the
docstring warns about — it doubles the work for an identical result.

### TODO 3 — `fourth_power(text, method)`

The critical step sits between the two squarings:

```python
_, limbs   = to_limbs(text)
square, N1 = square_transform(limbs, engine)
_, reduced = to_limbs(from_limbs(1, square))     # CARRY, then re-split
fourth, N2 = square_transform(reduced, engine)
return from_limbs(1, fourth), (N1, N2), (len(limbs), len(reduced))
```

`square` holds **un-carried** coefficients that are far larger than the base.
Feeding them straight into the second square would multiply already-oversized
numbers and blow past the double mantissa. `from_limbs` carries them into a
proper decimal string, and `to_limbs` splits that back into in-range limbs.
An even power is never negative, so the sign is `1` throughout.

---

# Part B — Image / 2D problems (`b1`–`b5`)

Shared background: `transform_2d(plane, engine)` and `inverse_2d(spectrum, engine)`
apply the chosen 1D engine along rows then columns. Images are `float64`,
grayscale `(H, W)` or RGB `(H, W, 3)`. **TODO 3 is the grayscale/RGB dispatch of
§0.4 in every one of these files** — only B4 and B5 vary, as noted.

---

## B1 — `b1_spectral_shift.py` — shift an image with a phase ramp

**Goal:** a translation in space is a **linear phase** in frequency.

### TODO 1 — `phase_ramp(shape, shift_rows, shift_cols)`

Delaying `x[n]` by `s` multiplies `X[u]` by `exp(-2πj·u·s/N)`. In 2D the two
exponents add:

```python
u = np.arange(height, dtype=np.float64)[:, np.newaxis]   # column vector
v = np.arange(width,  dtype=np.float64)[np.newaxis, :]   # row vector
return np.exp(-2j*np.pi*(u*shift_rows/height + v*shift_cols/width))
```

The `np.newaxis` pair makes this broadcast into a full `(H, W)` multiplier
without a loop. Negative shifts need no special handling — the exponent just
changes sign.

### TODO 2 — `shift_plane(plane, shift_rows, shift_cols, engine)`

**No padding here.** The shift is meant to wrap, which is exactly what the
circular nature of the DFT gives for free:

```python
spectrum = transform_2d(plane, engine) * phase_ramp(plane.shape, shift_rows, shift_cols)
return inverse_2d(spectrum, engine).real
```

The runner compares against `np.roll` and expects agreement to `1e-9`.

### TODO 3 — grayscale/RGB dispatch, §0.4.

---

## B2 — `b2_unsharp_mask.py` — sharpening in the frequency domain

**Goal:** build `plane + amount·(plane - blur(plane))` entirely as one spectral
expression. This one is a **linear** (padded) convolution, not circular.

### TODO 1 — `choose_transform_shape(image_shape, kernel_shape, engine)`

Full convolution size per axis, then a power of two **per axis, `fft` only**:

```python
full_height, full_width = rows + krows - 1, cols + kcols - 1
if engine.name == "fft":
    full_height, full_width = next_power_of_two(full_height), next_power_of_two(full_width)
return full_height, full_width
```

### TODO 2 — `sharpen_plane(plane, kernel, amount, engine)`

Two helpers are **provided**: `_pad_top_left` (places an array at the origin of a
zero complex array) and `centred_delta_spectrum` (the DFT of an impulse sitting
at the kernel's centre — the "identity filter", already carrying the same
half-kernel delay the blur introduces).

```python
combined = plane_spectrum * (delta_spectrum + amount*(delta_spectrum - kernel_spectrum))
full = inverse_2d(combined, engine).real
row, column = kernel.shape[0] // 2, kernel.shape[1] // 2
return full[row:row + plane.shape[0], column:column + plane.shape[1]]
```

Two things to get right:

- The whole filter `δ + amount·(δ − G)` is assembled **before** the single
  inverse transform.
- The crop offset is the kernel's **half-size**, which discards the leading
  convolution ramp and re-centres the output on the original pixels.

### TODO 3 — grayscale/RGB dispatch, §0.4.

---

## B3 — `b3_deblur.py` — inverse filtering (spectral division)

**Goal:** undo a *circular* Gaussian blur by dividing spectra. Convolution is
multiplication in frequency, so deconvolution is division.

### TODO 1 — `wrapped_kernel_spectrum(kernel, shape, engine)`

The kernel must be positioned so its **centre tap sits at index (0, 0)** —
otherwise the division reconstructs a shifted image. Embed it at the top-left of
a zero array the size of the plane, then roll that centre back to the origin:

```python
padded = np.zeros(shape, dtype=np.float64)
padded[:krows, :kcols] = kernel
padded = np.roll(padded, (-(krows // 2), -(kcols // 2)), axis=(0, 1))
return transform_2d(padded, engine)
```

This mirrors exactly what `convolve_plane(..., circular=True)` does when it
blurs — which is why the inverse matches to `1e-9`.

### TODO 2 — `deblur_plane(blurred, kernel, engine, epsilon=1e-12)`

Divide `Y` by `G`, but **never divide by a vanishing bin** — a Gaussian spectrum
decays toward zero, and dividing there amplifies pure noise into garbage:

```python
restored = np.zeros_like(blurred_spectrum)
reliable = np.abs(kernel_spectrum) > epsilon
restored[reliable] = blurred_spectrum[reliable] / kernel_spectrum[reliable]
return inverse_2d(restored, engine).real
```

Bins that fail the test are left at **0**, not divided. The boolean-mask
assignment does this without a Python loop.

### TODO 3 — grayscale/RGB dispatch, §0.4 (variable named `blurred`).

---

## B4 — `b4_phase_correlation.py` — recover an unknown 2D shift

**Goal:** phase correlation — throw away all magnitude information and keep only
the phase difference, which is a pure impulse at the shift.

### TODO 1 — `unit_cross_power(spectrum_a, spectrum_b, epsilon=1e-12)`

`cross = conj(A) · B` carries the phase difference; normalising by `|cross|`
leaves only that phase, so image content cancels and a clean peak survives:

```python
cross = np.conj(spectrum_a) * spectrum_b
magnitude = np.abs(cross)
result = np.zeros_like(cross)
reliable = magnitude > epsilon
result[reliable] = cross[reliable] / magnitude[reliable]
return result
```

Same guarded-division pattern as B3 TODO 2.

### TODO 2 — `correlation_surface(plane_a, plane_b, engine)`

Transform both planes (**no padding** — the shift wraps), form the unit
cross-power spectrum, invert **once**, keep `.real`. An exact circular shift
produces a unit impulse at `(shift_rows mod H, shift_cols mod W)`.

### TODO 3 — `find_shift(image_a, image_b, engine)`

This is the one dispatch that differs from §0.4:

- Reject mismatched shapes with `ValueError`.
- Grayscale → one surface. RGB → **the sum** of the three channel surfaces
  (`sum(correlation_surface(...) for c in range(3))`), not a stack — the three
  channels vote for the same peak, and summing sharpens it.
- Locate the peak with `np.unravel_index(int(np.argmax(surface)), surface.shape)`
  and unwrap **both** axes independently (§0.5): `if row > height // 2: row -= height`,
  and the same for `col` against `width`.
- Return `(row, col, surface)`.

The runner divides the surface by the channel count before comparing with the
ideal impulse — which is why summing (not averaging) is what the code expects.

---

## B5 — `b5_ideal_filter.py` — ideal low-pass / high-pass split

**Goal:** split a spectrum into a disc and its complement, with `low + high`
reconstructing the original exactly.

### TODO 1 — `radial_mask(shape, radius)`

The spectrum is **not** `fftshift`-ed, so the negative frequencies live in the
upper half of each axis. Bin `u` of an `H`-point DFT therefore has frequency
`min(u, H - u)`:

```python
freq_rows = np.minimum(u, height - u).astype(np.float64)[:, np.newaxis]
freq_cols = np.minimum(v, width  - v).astype(np.float64)[np.newaxis, :]
distance = np.sqrt(freq_rows**2 + freq_cols**2)
return (distance <= radius).astype(np.float64)
```

Return **`float64`, not bool** — the mask gets multiplied into a complex spectrum
and used as `1.0 - mask`, both of which want a numeric dtype.

### TODO 2 — `split_plane(plane, radius, engine)`

One forward transform, two inverses (the two halves are genuinely different
signals, so two inverses is correct here):

```python
spectrum = transform_2d(plane, engine)
mask = radial_mask(plane.shape, radius)
low  = inverse_2d(spectrum * mask, engine).real
high = inverse_2d(spectrum * (1.0 - mask), engine).real
return low, high
```

Because the two masks sum to `1` everywhere, `low + high == plane` exactly — the
"complementarity" check in the runner.

### TODO 3 — `split_image(image, radius, engine)`

Like §0.4, but each plane returns a **pair**, so stack twice:

```python
pairs = [split_plane(image[:, :, c], radius, engine) for c in range(image.shape[2])]
low  = np.stack([pair[0] for pair in pairs], axis=-1)
high = np.stack([pair[1] for pair in pairs], axis=-1)
return low, high
```

Grayscale returns `split_plane(...)` directly, since that is already a
`(low, high)` pair.

---

# Quick reference — every TODO at a glance

| File | TODO 1 | TODO 2 | TODO 3 |
|------|--------|--------|--------|
| **A1** triple product | `N` for `n+q+r-2` | `A·B·C`, one inverse | base 10², signs multiplied, carry |
| **A2** sum of products | `N` for `max(n+m-1, …)` | `A·B + C·D`, one inverse | reject negatives, carry with `+1` |
| **A3** wraparound | deliberately short `N` | circular conv, no crop | `out[m % N] += linear[m]` |
| **A4** correlation | `N` for `n+m-1` lags | `conj(A)·B`, one inverse | argmax + unwrap negative lag |
| **A5** fourth power | `N` for `2n-1` | one forward, `A·A` | square → **carry** → square |
| **B1** spectral shift | `exp(-2πj(u·s_r/H + v·s_c/W))` | spectrum × ramp, no padding | gray/RGB stack |
| **B2** unsharp mask | padded shape, `fft` → pow-2 | `P·(δ + amt·(δ − G))`, crop | gray/RGB stack |
| **B3** deblur | kernel rolled to origin | `Y/G` where `abs(G) > ε`, else 0 | gray/RGB stack |
| **B4** phase correlation | `conj(A)·B` normalised to unit magnitude | surface, no padding | **sum** channels, unwrap both axes |
| **B5** ideal filter | `min(u, H−u)` radial mask | `×mask` and `×(1−mask)` | stack lows and highs separately |

---

# Common mistakes checklist

- [ ] Forgot `.real` after the inverse transform.
- [ ] Cast to `int64` without `np.rint` first (truncation, off-by-one digits).
- [ ] Cropped to `N` instead of to `need` — trailing zeros, or worse, kept alias garbage.
- [ ] Used two inverse transforms where the problem asks for one (A1, A2, A4, A5).
- [ ] Called `engine.transform` twice on the same array in A5 TODO 2.
- [ ] Used the default `BASE_DIGITS` instead of `TRIPLE_BASE_DIGITS` in A1 → mantissa overflow.
- [ ] Skipped the carry between the two squarings in A5 → mantissa overflow.
- [ ] Padded in B1/B4 — those shifts are supposed to wrap; padding breaks the match.
- [ ] Divided by a near-zero bin in B3/B4 instead of zeroing it.
- [ ] Forgot to roll the kernel centre to `(0, 0)` in B3 → restored image is offset.
- [ ] Returned a bool mask from B5 TODO 1 instead of `float64`.
- [ ] Stacked RGB on `axis=0` instead of `axis=-1` → shape no longer matches the input.
- [ ] Unwrapped only one axis in B4 TODO 3.
