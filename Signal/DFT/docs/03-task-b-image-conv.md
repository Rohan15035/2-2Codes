# 3 — Task B: Blurring an Image in the Frequency Domain (`image_conv.py`)

The same theorem as Task A, with two indices instead of one. Digits become
pixels, the polynomial becomes an image, and the convolution becomes a blur.

---

## 1 Theory

### 1.1 A blur is a convolution

Every output pixel of a blur is a weighted average of the input pixels around
it, the weights given by a kernel `h`:

```
(I ∗ h)[r,c] = sum_i sum_j  I[r−i, c−j] · h[i,j]
```

Done directly this costs **O(N²K²)** for an `N × N` image and a `K × K` kernel:
each of the `N²` output pixels sums `K²` terms. For a 512×512 image and a 19×19
bokeh kernel that is ~95 million multiply-adds.

The kernels (built by the provided `image_utils.make_kernel`, all normalised to
sum to 1 so brightness is preserved):

- **gaussian** — the familiar soft blur.
- **motion** — a straight streak, as if the camera moved during exposure.
- **bokeh** — a filled disc. This is what a real lens does out of focus: a
  focused lens maps each point of the scene to a point on the sensor, but a
  defocused one spreads that point into a small image of the aperture. So the
  kernel *is* the disc, and every bright point becomes a bright disc of the
  same radius. It is why the night skyline dissolves into overlapping circles
  rather than a smooth haze — the window lights are near-point sources, and
  each becomes a copy of the kernel.

### 1.2 The 2D DFT, and why it is two passes of 1D transforms

An image is a 2D signal, so it has a 2D spectrum:

```
F[u,v] = sum_{r=0}^{P-1} sum_{c=0}^{Q-1}  f[r,c] · exp(-2πi(ur/P + vc/Q))
```

Evaluated as written this is hopeless — `PQ` outputs, each a sum over `PQ`
inputs, so **O(N⁴)**. But the exponential *factorises*:

```
exp(-2πi(ur/P + vc/Q)) = exp(-2πi·ur/P) · exp(-2πi·vc/Q)
```

and only the second factor involves `c`, so it pulls out of the inner sum:

```
F[u,v] = sum_r exp(-2πi·ur/P) · [ sum_c f[r,c]·exp(-2πi·vc/Q) ]
                                  └──── 1D DFT of row r ────┘
```

The bracket is just the 1D DFT of row `r`; the outer sum is then a 1D DFT down
each column of those results. This is **separability**: transform every row,
then transform every column of what you got. The order does not matter.

The cost is `2N` transforms of length `N`:

| Route | Cost |
|---|---|
| Direct 2D double sum | O(N⁴) |
| Row-column with naive DFT | O(N³) |
| Row-column with radix-2 FFT | O(N² log N) |

The inverse works the same way.

The pointwise multiply is also where the intuition lives: each spatial
frequency of the image is simply *scaled* by the kernel's response at that
frequency. A blur kernel has a spectrum close to 1 near the origin and near 0
far from it, so low frequencies pass through untouched while fine detail is
multiplied away. **Blurring is low-pass filtering**, and here you can watch it
happen entry by entry.

### 1.3 Padding and cropping — in two dimensions

The padding rule applies per axis. The full linear convolution of an `(H,W)`
image with a `(kh,kw)` kernel is `(H+kh−1, W+kw−1)`, so zero-pad both to at
least that, and to the next power of two per axis for radix-2.

Two dimensions add one wrinkle. The kernel is placed at the **origin** of the
padded array, not at its centre, so the result comes out displaced by half a
kernel. The fix is to crop the `(H,W)` window starting at `(kh//2, kw//2)`:

```python
full[kh // 2 : kh // 2 + H,  kw // 2 : kw // 2 + W]
```

Skip that offset and the whole image comes out shifted diagonally — a bug that
looks like a rendering glitch rather than a maths error.

### 1.4 The deliberate mistake: circular convolution

The required `wraparound.png` shows what happens when you *don't* pad:
transform at exactly `(H,W)` with the kernel wrapped around the origin. The
result is circular convolution, and in two dimensions the wrap is plainly
visible — content that should have fallen off one edge of the picture
reappears on the opposite edge. The provided images are 256×256 and 512×512,
both powers of two, so this path works with radix-2 directly.

Comparing the two outputs side by side is the point of `comparison.png`. The
correct linear convolution also darkens slightly toward the border, because
zero padding treats the world outside the frame as black.

---

## 2 Implementation

### Sizing — [image_conv.py:44](../2305126/image_conv.py#L44), [:50](../2305126/image_conv.py#L50)

Two small helpers keep the padding rule in exactly one place, used by both
`convolve_plane` and the report:

```python
rows, cols = linear_shape(image_shape, kernel_shape)
if engine.name == "fft":
    return next_power_of_two(rows), next_power_of_two(cols)
return rows, cols
```

The naive DFT and Bluestein transform at the exact linear size; only radix-2
rounds up. For a 512×512 image with a 19×19 kernel that is 530×530 versus
1024×1024 — the padded area nearly doubles.

### `transform_2d` / `inverse_2d` — [:61](../2305126/image_conv.py#L61), [:85](../2305126/image_conv.py#L85)

Separability, directly:

```python
rows    = np.array([engine.transform(row)    for row    in plane])
columns = np.array([engine.transform(column) for column in rows.T])
return columns.T
```

Iterating a 2D array yields its rows, so `rows.T` iterates *columns*; the final
`.T` puts the result back the right way round. `inverse_2d` is the identical
shape with `engine.inverse`. Because the engines share an interface, these two
functions work unchanged for all three.

### `convolve_plane` — [:95](../2305126/image_conv.py#L95)

The two branches differ only in how the arrays are prepared:

```python
if circular:
    padded_plane = plane
    padded_kernel = np.zeros((H, W))
    padded_kernel[:kh, :kw] = kernel
    padded_kernel = np.roll(padded_kernel, (-(kh // 2), -(kw // 2)), axis=(0, 1))
else:
    P, Q = transform_shape(plane.shape, kernel.shape, engine)
    padded_plane  = np.zeros((P, Q));  padded_plane[:H, :W]   = plane
    padded_kernel = np.zeros((P, Q));  padded_kernel[:kh, :kw] = kernel
```

The `np.roll` wraps the kernel's centre onto the origin — the array-index
equivalent of centring it, and permitted since a roll is a permutation, not a
transform. After that both branches share one pipeline:

```python
spectrum = transform_2d(padded_plane, engine) * transform_2d(padded_kernel, engine)
full = inverse_2d(spectrum, engine).real
```

and only the linear branch crops.

### `convolve_image` — [:158](../2305126/image_conv.py#L158)

Grayscale `(H,W)` passes straight through; colour `(H,W,3)` has each plane
convolved independently and re-stacked. Convolution is linear and the channels
do not interact, so this is exact, not an approximation.

### `convolve_plane_direct` — [:174](../2305126/image_conv.py#L174)

The correctness oracle: four nested loops, no vectorisation, deliberately slow
and obviously right.

```python
for r in range(H):
    for c in range(W):
        total = 0.0
        for i in range(kh):
            rr = r + kh // 2 - i
            if 0 <= rr < H:
                for j in range(kw):
                    cc = c + kw // 2 - j
                    if 0 <= cc < W:
                        total += pixels[rr][cc] * weights[i][j]
```

The bounds checks implement zero padding — out-of-range pixels contribute
nothing, which is exactly "treated as zero". Hoisting the row check out of the
`j` loop skips `kw` tests per out-of-range row. Working from `.tolist()` rather
than indexing NumPy scalars is several times faster while staying pure Python,
which matters only because this function is also a benchmark curve.

### `run_single` — [:224](../2305126/image_conv.py#L224)

Produces `blurred.png`, `wraparound.png`, `kernel.png`, `comparison.png` and
`report.txt`, then verifies:

```python
corner = image[:VERIFY_CROP, :VERIFY_CROP] if image.ndim == 2 \
    else image[:VERIFY_CROP, :VERIFY_CROP, 0]
error = float(np.max(np.abs(convolve_plane(corner, kernel, engine)
                            - convolve_plane_direct(corner, kernel))))
```

The oracle runs on a 64×64 corner only — at O(N²K²) in pure Python a full
512×512 image would take minutes. As in Task A, a failure exits nonzero rather
than being reported quietly.

---

## 3 Results

All four required runs verify, and the reports match `expected_outputs/`:

| Run | Image | Kernel | Engine | Linear | Transform | max&#124;spectral−direct&#124; |
|---|---|---|---|---|---|---|
| skyline_bokeh | 512² RGB | bokeh 19² | fft | 530² | 1024² | 3.331e-15 |
| sunset_motion | 512² gray | motion 41² | fft | 552² | 1024² | 2.776e-16 |
| skyline256_gaussian_dft | 256² gray | gaussian 21² | dft | 276² | 276² | 2.220e-15 |
| nebula_bokeh | 512² RGB | bokeh 27² | fft | 538² | 1024² | 2.109e-15 |

All ~1e-15 against a 1e-9 bar. The third run drives the identical pipeline with
the naive DFT instead of the FFT, and that is the point of including it: re-run
with `--engine fft` and both `blurred.png` and `wraparound.png` come out
**byte-identical** (0 differing pixels of 65 536). Same theorem, same answer,
very different running time.

Against the reference images: the grayscale outputs are pixel-exact; the colour
ones differ by at most 1/255 on a few dozen of 786 432 pixels — rounding at the
8-bit quantisation boundary.

### Benchmark — `outputs/task_b/benchmark/`

**Study 1 — fixed 15×15 kernel, growing image:**

```
     N   Naive DFT   Radix-2 FFT   Direct spatial
    16    0.013195      0.019202         0.006812
    32    0.044261      0.050130         0.031906
    64    0.227069      0.116122         0.136038
   128    1.334132      0.279901         0.564384
   256   15.150195      0.730081         2.330260
   512          --      2.045476         9.871539
```

- **Naive DFT** grows by ~6× then ~11× per doubling, bracketing the predicted
  **O(N³)**, and blows the 8-second budget at N=256.
- **Radix-2 FFT** grows 2.4× to 2.8× per doubling — well under the 4× of a
  plain `N²`, because each doubling of `N` only sometimes crosses a
  power-of-two boundary in the padded size: **O(N² log N)**.
- **Direct spatial** grows 4× per doubling: **O(N²)** at fixed kernel.

Note that at N=16 the FFT is the *slowest* of the three. Padding a 30×30
linear-convolution size up to 32×32 and running 192 length-32 transforms (three
2D transforms, two passes each, 32 lines per pass) costs more than the 57 600
multiply-adds direct convolution needs at that size. Constant factors decide small cases; asymptotics
decide large ones. By N=512 the FFT is 4.8× faster than direct convolution and
the naive DFT is off the chart entirely.

**Study 2 — fixed 256×256 image, growing kernel:**

```
     K   Direct spatial   Radix-2 FFT
     3         0.129171      0.743213
     7         0.541933      0.723547
    15         2.306737      0.725992
    31         9.011826      0.700657
    63               --      0.723773
```

This is the sharper result. Direct convolution grows as `K²` — quadrupling with
each near-doubling of the kernel. The FFT route is **completely flat**: 0.70 s
to 0.74 s across a 21× range of kernel widths. The reason is structural, not
incidental — the kernel is zero-padded to the same transform size whatever its
width, so a 63×63 kernel costs precisely what a 3×3 one costs. The two cross
somewhere between K=15 and K=31, and past that the frequency-domain route wins
by an unbounded margin.

### Bonus — `outputs/bonus/task_b/`

With `--engine arbitrary`, Bluestein transforms at the exact linear size:
530×530 instead of 1024×1024 for `skyline_bokeh`. That is 280 900 versus
1 048 576 samples — the padded area drops by **73%**. Both bonus runs verify
MATCH.

---

**Previous:** [Task A — big-integer multiplication](02-task-a-bigmul.md) ·
[The transform core](01-transform-core.md)
