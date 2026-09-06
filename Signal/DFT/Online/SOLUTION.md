# CSE 220 — Online on DFT and FFT — Solution Notes

Both online problems were solved on top of the existing offline submission. Only
the six `TODO` blocks inside the two supplied templates were written; every
offline file (`transforms.py`, `image_conv.py`, `image_utils.py`, `io_utils.py`,
`bench_utils.py`) is byte-identical to the offline submission, as the question
papers require.

| | Question | Template | Marks | Result |
|---|---|---|---|---|
| **A1/A2** | Fourier Hybrid Image | `hybrid_image_template.py` | 10 | `verification: MATCH`, max error `4.219e-15` |
| **B1/B2** | Fourier Magnitude–Phase Swap | `magnitude_phase_swap_template.py` | 10 | `verification: MATCH`, worst error `1.179e-12` |

Both are far below the `1e-9` threshold at which the runners raise
`RuntimeError`.

## Folder layout

```
Online/
  hybrid_image_template.py            <- A1/A2, three TODOs completed
  magnitude_phase_swap_template.py    <- B1/B2, three TODOs completed
  transforms.py  image_conv.py                    unmodified offline files
  image_utils.py io_utils.py bench_utils.py       (provided, not touched)
  images/                             sunset512, skyline512, skyline256, nebula512
  cmd.txt                             the exact commands that produced outputs/
  outputs/
    lab_hybrid_student/               A1/A2 required run (grayscale, fft)
    lab_phase_swap_student/           B1/B2 required run (grayscale, fft)
    lab_hybrid_student_rgb/           the same, --color
    lab_phase_swap_student_rgb/       the same, --color
    bonus/lab_hybrid_arbitrary/       ArbitraryLengthFFT engine
    bonus/lab_phase_swap_arbitrary/   ArbitraryLengthFFT engine
```

The templates were copied into this folder rather than into `Testing/` so that
the offline deliverables stay exactly as submitted. Both templates import
`transform_2d`, `inverse_2d`, `convolve_image` and `next_power_of_two` from the
offline code, so this folder must contain those files for them to run.

## Before anything was written

As the papers instruct, the unmodified templates were run first to observe the
indicated incomplete TODO:

```
NotImplementedError: TODO 3: process a grayscale image      (hybrid)
NotImplementedError: TODO 3: process grayscale images       (phase swap)
```

---

# Question A1/A2 — Fourier Hybrid Image

A hybrid image takes its smooth content from one photograph and its edges from
another, so it reads as the high-frequency source from nearby and as the
low-frequency source from a distance. With `L`, `H`, `G` the padded spectra of
the low source, the high source and the Gaussian kernel, and `Δ` the spectrum of
an impulse aligned with the kernel centre, the paper specifies

```
Y = L·G + H·(Δ − G)
```

`L·G` is the blur (the smooth part). `H·Δ` is the *unblurred* high image, shifted
so that it lines up with the cropped convolutions, so `H·(Δ − G)` is
"high image minus its own blur" — exactly the detail the Gaussian removes.

### TODO 1 — `choose_transform_shape` (2 marks)

[hybrid_image_template.py:34-42](hybrid_image_template.py#L34-L42)

```python
full_height = image_shape[0] + kernel_shape[0] - 1
full_width = image_shape[1] + kernel_shape[1] - 1

if engine.name == "fft":
    # Adjust both dimensions to lengths supported by the radix-2 engine.
    return next_power_of_two(full_height), next_power_of_two(full_width)

# Other engines can use the minimum dimensions calculated above.
return full_height, full_width
```

This is the offline linear-convolution padding rule: an `R × C` image against a
`Kr × Kc` kernel needs `(R + Kr − 1) × (C + Kc − 1)` samples, otherwise the
periodic product wraps content around the opposite edge. `FFTTransformer` is
radix-2 and raises `ValueError` on any non-power-of-two length, so each axis is
independently rounded up with `next_power_of_two`. `DFTAnalyzer` and
`ArbitraryLengthFFT` handle any length and use the minimum.

This deliberately reproduces `image_conv.transform_shape` rather than importing
it, because the runner's oracle calls `convolve_image`, which pads by that rule —
if the two disagreed the comparison would be between two different transform
sizes. For the required run this gives `512 + 31 − 1 = 542`, rounded up to
**1024 × 1024**.

### TODO 2 — `hybrid_plane` (5 marks)

[hybrid_image_template.py:81-90](hybrid_image_template.py#L81-L90)

```python
combined = (low_spectrum * kernel_spectrum
            + high_spectrum * (delta_spectrum - kernel_spectrum))

full = inverse_2d(combined, engine).real
row, column = kernel.shape[0] // 2, kernel.shape[1] // 2
return full[row:row + low_plane.shape[0],
            column:column + low_plane.shape[1]]
```

Three points the marking scheme asks for:

* **Combine in the frequency domain, then invert once.** Multiplication is
  pointwise, so `L·G + H·(Δ − G)` is assembled while everything is still a
  spectrum. There is exactly **one** call to `inverse_2d`, not three; the
  linearity of the DFT is what makes that legal. The template's own comment
  ("The submitted `hybrid_image` must combine the spectra first") makes this the
  graded distinction between the answer and the oracle.
* **`.real`.** The inputs are real, so the result is mathematically real and the
  imaginary part is only float roundoff (~1e-16). The offline `convolve_plane`
  discards it at the same point.
* **The crop.** The kernel sits at the origin of the padded array, so the
  convolution is offset by half the kernel. Taking rows `kh//2 … kh//2+H−1` and
  columns `kw//2 … kw//2+W−1` undoes that; omitting it shifts the picture
  diagonally. The centred `Δ` is placed at the same `(kh//2, kw//2)`, so the
  unblurred term lands under the identical crop — that is the whole reason the
  provided helper exists.

The runner then rebuilds the same image the slow way
(`convolve_image(low) + high − convolve_image(high)`, two full convolutions) and
compares. They agree to **4.219e-15**.

### TODO 3 — `hybrid_image` (3 marks)

[hybrid_image_template.py:102-109](hybrid_image_template.py#L102-L109)

```python
return hybrid_plane(low_image, high_image, kernel, engine)
...
planes = [hybrid_plane(low_image[:, :, c], high_image[:, :, c],
                       kernel, engine)
          for c in range(3)]
return np.stack(planes, axis=2)
```

A 2D grayscale input is one plane. A colour input is three planes that must be
processed **independently** and stacked back on `axis=2`, preserving the
`(H, W, 3)` shape — the same dispatch the offline `convolve_image` uses.

### Result

`outputs/lab_hybrid_student/report.txt`:

```
image shape          : (512, 512)
kernel               : Gaussian 31 x 31
engine               : fft
transform shape      : 1024 x 1024
max |combined - reference| : 4.219e-15
verification         : MATCH
```

`comparison.png` shows the blurred sunset carrying the skyline's edges: at full
zoom the city dominates, and shrinking the image leaves the tree.

---

# Question B1/B2 — Fourier Magnitude–Phase Swap

Every DFT coefficient carries a magnitude (how strong a spatial frequency is)
and a phase (where its oscillation sits). This problem exchanges the two between
images to show which half actually holds the recognisable structure. With
`A = DFT2{a}` and `B = DFT2{b}`,

```
S_AB = |A| · phase(B)          S_BA = |B| · phase(A)
```

### TODO 1 — `unit_phase` (3 marks)

[magnitude_phase_swap_template.py:33-36](magnitude_phase_swap_template.py#L33-L36)

```python
result = np.ones_like(spectrum)
reliable = magnitude > epsilon
result[reliable] = spectrum[reliable] / magnitude[reliable]
return result
```

`Z/|Z|` is the phase-only value of `Z`, but it is undefined when `Z` is zero.
`spectrum` was already cast to `complex128` above, so `np.ones_like` gives an
array pre-filled with the neutral phase `1+0j`; the boolean mask then divides
**only** at bins that are safely above `epsilon`, and every other bin keeps that
neutral value. Division by zero never happens — the mask is applied to both
sides of the division, so the unsafe entries are never evaluated, not merely
overwritten afterwards.

The paper's requirement that the function "must never divide by zero" rules out
computing `spectrum / magnitude` first and patching up the `NaN`s.

### TODO 2 — `swap_plane_spectra` (4 marks)

[magnitude_phase_swap_template.py:53-60](magnitude_phase_swap_template.py#L53-L60)

```python
swapped_ab = np.abs(spectrum_a) * unit_phase(spectrum_b)
swapped_ba = np.abs(spectrum_b) * unit_phase(spectrum_a)

result_ab = inverse_2d(swapped_ab, engine).real
result_ba = inverse_2d(swapped_ba, engine).real
return result_ab, result_ba
```

A real magnitude scaling a unit-magnitude complex number produces a coefficient
with the modulus of one image and the argument of the other. Note that this
never exchanges whole complex spectra — the paper explicitly forbids that, and it
is why the magnitude has to be taken with `np.abs` and the phase through
`unit_phase` instead of swapping `spectrum_a` and `spectrum_b` outright.

`.real` is taken because the results are only real up to roundoff. That they are
real at all is worth stating: for a real image, `A[−k] = conj(A[k])`, so `|A|` is
even and `phase(B)[−k] = conj(phase(B)[k])`. Their product inherits the
conjugate symmetry, and a conjugate-symmetric spectrum inverts to a real signal.
The `epsilon` fallback does not break this, because `|B|` is even and so a bin
and its mirror are always masked together.

The runner's energy check passes for the same reason, via Parseval:
`Σ result_ab² = (1/N) Σ |S_AB|² = (1/N) Σ |A|² = Σ a²`. The measured relative
energy error is `1.962e-16`, which confirms `.real` threw away nothing but noise.

### TODO 3 — `swap_images` (3 marks)

[magnitude_phase_swap_template.py:74-84](magnitude_phase_swap_template.py#L74-L84)

```python
return swap_plane_spectra(image_a, image_b, engine)
...
pairs = [swap_plane_spectra(image_a[:, :, c], image_b[:, :, c], engine)
         for c in range(3)]
result_ab = np.stack([pair[0] for pair in pairs], axis=2)
result_ba = np.stack([pair[1] for pair in pairs], axis=2)
return result_ab, result_ba
```

Grayscale forwards the pair straight through. For RGB, each call returns an
`(ab, ba)` tuple for one channel, so the three `ab` planes are stacked into one
image and the three `ba` planes into the other, both keeping the original
`(H, W, 3)` shape.

### Result

`outputs/lab_phase_swap_student/report.txt`:

```
image shape          : (512, 512)
engine               : fft
worst relative magnitude error : 1.128e-16
worst phase-vector error       : 1.179e-12
worst relative energy error    : 1.962e-16
verification         : MATCH
```

`comparison.png` shows the classic outcome: **each output looks like the image
that donated its phase.** Magnitude-sunset + phase-skyline is a recognisable
city; magnitude-skyline + phase-sunset is a recognisable tree. The phase carries
the structure; the magnitude only tints the contrast.

---

## Verification performed

Beyond the two required runs, every code path in the six TODO blocks was
exercised. The grayscale/RGB dispatch and all three engines were checked on
16×16 crops (the naive `DFTAnalyzer` is O(N²) per 1D transform, so a 512×512
run through it is not practical), and the full-size images were run through
`fft` and the bonus `arbitrary` engine:

| Run | Engine | Input | Verdict |
|---|---|---|---|
| Hybrid, 512×512, Gaussian 31 | `fft` | grayscale | MATCH, 4.219e-15 |
| Hybrid, 512×512, Gaussian 31 | `fft` | RGB | MATCH, 4.552e-15 |
| Hybrid, 512×512, Gaussian 31 | `arbitrary` | grayscale | MATCH, 6.550e-15 |
| Hybrid, 16×16, Gaussian 5 | `dft` | grayscale + RGB | MATCH, ≤2.8e-15 |
| Swap, 512×512 | `fft` | grayscale | MATCH, ≤1.179e-12 |
| Swap, 512×512 | `fft` | RGB | MATCH, ≤1.010e-11 |
| Swap, 512×512 | `arbitrary` | grayscale | MATCH, ≤1.179e-12 |
| Swap, 16×16 | `dft` | grayscale + RGB | MATCH, ≤4.3e-12 |

The two verifications are independent of the submitted code: the hybrid runner
rebuilds the image with two ordinary `convolve_image` blurs, and the swap runner
re-transforms the reconstructions and checks magnitude, phase and energy
separately.

**Bonus.** Both templates also run under the offline `ArbitraryLengthFFT`
(Bluestein chirp-z). It is the more interesting of the two for the hybrid, where
it transforms at the exact linear-convolution size **542 × 542** instead of
padding up to 1024 × 1024 — a quarter of the samples — and still verifies to
6.550e-15. For the swap, 512 is already a power of two, so the engine takes its
radix-2 fast path and the numbers are identical to the `fft` run.

## Constraints observed

* No `numpy.fft`, `scipy.fft`, `scipy.signal`, `numpy.convolve`, or any library
  transform/convolution. Every transform goes through the offline `transforms.py`
  via `transform_2d` / `inverse_2d`; NumPy is used only for array arithmetic
  (`np.abs`, `np.ones_like`, `np.stack`, masking, pointwise multiply).
* No offline file was modified — verified byte-identical against the offline
  submission.
* Only the marked TODO blocks were edited. Every provided helper
  (`centred_delta_spectrum`, `_pad_top_left`, `_normalise_for_display`,
  `_plane_verification`, both `run` functions) is untouched, and the surrounding
  instruction comments were left in place.
* Both grayscale and RGB inputs work in both templates.

## One limitation worth flagging

In the swap task the image is transformed at its **native** size — a
magnitude–phase exchange has no linear-convolution padding to hide behind, and
zero-padding would change the spectrum being swapped. So the radix-2 `fft`
engine requires power-of-two image dimensions there, and raises
`ValueError: FFT length must be a power of two` on, say, a 24×24 crop. This
comes from the provided (non-TODO) line `transform_2d(plane_a, engine)`, not
from the submitted code; the supplied images are 256×256 and 512×512, and the
`dft` and `arbitrary` engines accept any size. The hybrid task is unaffected,
since it pads to a power of two anyway.
