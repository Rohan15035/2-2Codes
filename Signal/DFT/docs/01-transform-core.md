# 1 — The Transform Core (`transforms.py`)

The shared engine behind both tasks. Written once, imported by `bigmul.py` and
`image_conv.py`. Three engines live here, all exposing the same two methods
(`transform`, `inverse`) plus a `name` attribute, so the applications can hold
any of them without knowing which.

| Class | `name` | Valid lengths | Cost |
|---|---|---|---|
| `DFTAnalyzer` | `dft` | any `N` | O(N²) |
| `FFTTransformer` | `fft` | powers of two only | O(N log N) |
| `ArbitraryLengthFFT` | `arbitrary` | any `N` | O(N log N) |

---

## 1.1 Theory: what the DFT actually is

The Discrete Fourier Transform rewrites a length-`N` signal in a different
basis — the basis of complex exponentials:

```
Analysis    X[k] = sum_{n=0}^{N-1}  x[n] · exp(-2πi·k·n/N)
Synthesis   x[n] = (1/N) · sum_{k=0}^{N-1}  X[k] · exp(+2πi·k·n/N)
```

The reason this basis is worth the trouble is **shift-invariance**. Delaying a
complex exponential `exp(2πikn/N)` by one sample multiplies it by the constant
`exp(-2πik/N)` — it does not turn into a different function. Convolution is
built entirely out of shifts and sums, so in the time domain every output
sample depends on every input sample (hopelessly tangled), while in the
frequency domain each component is only ever *scaled*, never mixed with its
neighbours. The whole convolution therefore decouples into `N` independent
scalar multiplications:

```
a ∗ c  =  IDFT( DFT{a} · DFT{c} )          ← the convolution theorem
```

That identity is the entire offline. Task A and Task B are the same three
steps — transform, multiply pointwise, transform back — applied to digits and
to pixels.

Evaluating the analysis sum literally costs `N` multiply-adds per output and
there are `N` outputs, so **O(N²)**. Using it to compute a convolution buys you
nothing: you have replaced an `N²` convolution with an `N²` transform. The FFT
is what makes the change of basis cheap enough to be worth doing.

### Cooley-Tukey, decimation in time

Split the input by parity. Writing `W_N = exp(-2πi/N)`:

```
X[k] = sum_{n even} x[n] W_N^{kn}  +  sum_{n odd} x[n] W_N^{kn}
     = E[k]  +  W_N^k · O[k]
```

where `E` and `O` are the length-`N/2` DFTs of the even- and odd-indexed
samples. Because `E` and `O` are periodic with period `N/2` and
`W_N^{k+N/2} = -W_N^k`, one pair of sub-transforms produces *two* outputs:

```
X[k]        = E[k] + W_N^k · O[k]
X[k + N/2]  = E[k] - W_N^k · O[k]        (k = 0 .. N/2-1)
```

That pair is a **butterfly**, and `W_N^k` is a **twiddle factor**. The
recurrence `T(N) = 2·T(N/2) + O(N)` gives **O(N log N)** — `log₂N` stages of
`N/2` butterflies each.

### Why bit-reversal

Recursing on "even indices first, then odd" repeatedly partitions by
successively higher-order bits. After `log₂N` levels, the element that ends up
in position `j` of the fully-split array is the one whose index is `j` with its
bits written backwards. An *iterative* implementation therefore permutes the
input into bit-reversed order once up front, after which every stage is a
regular, in-place sweep of adjacent butterflies.

### The inverse costs nothing extra

Analysis and synthesis differ only in the sign of the exponent and the `1/N`
factor. So the same butterfly machinery serves both — flip the sign of the
twiddles and divide by `N` at the end. No second copy of the algorithm.

### Bluestein: O(N log N) for *any* length (bonus)

Radix-2 needs a power of two. Bluestein's chirp-z removes that restriction via
the algebraic identity

```
2kn = k² + n² − (k−n)²
```

Substituting into the analysis sum and setting `w[n] = exp(-πi·n²/N)`:

```
X[k] = w[k] · sum_n ( x[n]·w[n] ) · conj(w[k−n])
```

The sum is a **convolution** of two chirp sequences. Evaluate *that* with a
radix-2 FFT of any length `M ≥ 2N−1` and the transform of an awkward length `N`
costs `O(M log M) = O(N log N)`. Note the pleasing circularity: the convolution
theorem is used to compute a transform, which is itself used to compute
convolutions.

---

## 2 Implementation

### `next_power_of_two` — [transforms.py:25](../2305126/transforms.py#L25)

```python
size = 1
while size < int(n):
    size *= 2
return size
```

Doubling from 1 returns 1 for `n ≤ 1` and is exact on powers of two
(`next_power_of_two(8) == 8`), which matters — padding an already-valid length
up to the next power would double the work for nothing.

### `DFTAnalyzer` — [transforms.py:42](../2305126/transforms.py#L42)

Two pieces: a twiddle **table**, and the double loop that uses it.

**`_twiddle_table`** ([:59](../2305126/transforms.py#L59)) stores `N` values,
not `N²`:

```python
self._tables[key] = np.exp(sign * 2j * np.pi * np.arange(N) / N).tolist()
```

**`_sums`** ([:66](../2305126/transforms.py#L66)) is the definition, written out:

```python
for k in range(N):
    total = 0j
    for n in range(N):
        total += values[n] * table[(k * n) % N]
    out.append(total)
```

Because `exp(-2πi·kn/N)` is periodic in `kn` with period `N`, the product `k·n`
can be reduced mod `N` and used as an index into the small table. This is the
"precomputed table indexed by `(k*n) % N`" the skeleton docstring suggests. It
also *improves accuracy*: the phase never grows large, so it is never a big
floating-point number rounded down to a small one.

`transform` and `inverse` are then one line each, differing only in sign and
the `1/N` factor ([:82](../2305126/transforms.py#L82),
[:96](../2305126/transforms.py#L96)).

> #### Design note: why this is a literal loop and not a matrix product
>
> The first version built the full `N × N` twiddle matrix and called
> `matrix.dot(x)`. Mathematically identical, and defensible under the
> docstring's "or a NumPy expression". It was also **wrong for this
> assignment**: NumPy routes that through BLAS, so the "naive" DFT came out
> *faster than the FFT* in the Task B benchmark (0.15 s vs 0.27 s at N=256),
> inverting the exact comparison the offline is built to demonstrate. The
> literal double loop restores honest O(N²) behaviour with an honest constant.
> The lesson is real: **an O(N²) algorithm with a hand-tuned constant can beat
> an O(N log N) one at any fixed size** — which is also why the schoolbook
> multiply stays competitive up to ~1000 digits in Task A.

### `FFTTransformer` — [transforms.py:116](../2305126/transforms.py#L116)

Iterative radix-2 DIT. Subclasses `DFTAnalyzer` so both are interchangeable.

**`_bit_reversed_order`** ([:140](../2305126/transforms.py#L140)) builds the
permutation by shifting bits out of the index and into the accumulator,
one bit position per iteration, vectorised across all `N` indices at once:

```python
for bit in range(N.bit_length() - 1):
    order = (order << 1) | ((index >> bit) & 1)
```

After `log₂N` iterations, bit `b` of `index` sits at position `bits-1-b` of
`order` — the reversal. Cached per `N`.

**`_butterflies`** ([:150](../2305126/transforms.py#L150)) is the whole
algorithm, one stage per loop iteration:

```python
a = a[self._bit_reversed_order(N)]
half = 1
while half < N:
    twiddles = np.exp(sign * 1j * np.pi * np.arange(half) / half)
    blocks = a.reshape(-1, 2 * half)
    even = blocks[:, :half]
    odd  = blocks[:, half:] * twiddles
    a = np.concatenate((even + odd, even - odd), axis=1).reshape(N)
    half *= 2
```

Reshaping to `(-1, 2*half)` lays every block of the stage out as its own row,
so all `N/2` butterflies of that stage execute as **three whole-array NumPy
operations**. The left columns are the even sub-transform, the right columns
the odd; `even ± twiddle·odd` is the butterfly pair, written back in place.

This satisfies the stated requirements directly:

- **Twiddles once per stage** — `twiddles` is built in the loop body, outside
  any per-butterfly loop. There is no per-butterfly loop at all.
- **Power-of-two enforcement** — `N & (N-1)` is nonzero for any non-power of
  two, raising `ValueError` ([:154](../2305126/transforms.py#L154)).
- **One copy of the butterflies** — `inverse` calls the same `_butterflies`
  with `sign=+1` and divides by `N` ([:174](../2305126/transforms.py#L174)).

### `ArbitraryLengthFFT` — [transforms.py:187](../2305126/transforms.py#L187)

Bluestein, built on the inherited `_butterflies`.

**`_chirp`** ([:206](../2305126/transforms.py#L206)) tabulates `exp(-πi·n²/N)`:

```python
self._chirps[N] = np.exp(-1j * np.pi * ((n * n) % (2 * N)) / N)
```

The `% (2*N)` is load-bearing, not decoration. `exp(-πi(n²+2N)/N)` equals
`exp(-πi·n²/N)`, so the reduction is exact — but without it, `n²` reaches
`~10⁸` for the 20 000-digit input and the phase argument reaches `~3×10⁴`,
costing roughly five significant digits of precision. Reduced mod `2N` the
argument stays inside one turn and the table is accurate to full precision.

**`transform`** ([:213](../2305126/transforms.py#L213)) short-circuits to the
radix-2 path when `N` is already a power of two, then:

```python
M = next_power_of_two(2 * N - 1)

signal = np.zeros(M, dtype=np.complex128)
signal[:N] = x * chirp

weights = np.zeros(M, dtype=np.complex128)
weights[:N] = chirp.conjugate()
weights[M - N + 1:] = chirp[:0:-1].conjugate()
```

`weights` carries the two-sided sequence `conj(w[m])` for `m = -(N-1) .. N-1`.
Since `w[m]` depends on `m²`, negative indices mirror the positive ones, and
they are placed at the *end* of the array — index `M-N+1` is where `m = -(N-1)`
lands under mod-`M` arithmetic. Padding to `M ≥ 2N-1` is what stops the
circular convolution from wrapping (the same padding rule as both tasks).

Three radix-2 transforms then do the work, and the result is de-chirped:

```python
spectrum  = self._butterflies(signal, -1) * self._butterflies(weights, -1)
convolved = self._butterflies(spectrum, +1)[:N] / M
return convolved * chirp
```

**`inverse`** ([:236](../2305126/transforms.py#L236)) uses the conjugation
identity rather than a second chirp implementation:

```
IDFT(X) = conj( DFT( conj(X) ) ) / N
```

---

## 3 Verification

The skeleton's own self-test, plus arbitrary-length agreement:

```
dft vs fft (N=64)   : 9.44e-15
dft round-trip      : 1.56e-15
arbitrary vs dft    : 0.00e+00 (N=1,2)  …  4.28e-14 (N=256)
arbitrary round-trip: ≤ 3.46e-15
FFTTransformer.transform(np.zeros(6)) → ValueError: FFT length must be a power of two, got 6
```

All three engines agree to ~1e-14 — floating-point noise, well under the 1e-9
bar. Each is exercised end-to-end by the tasks. Task A inputs 1 and 2 produce a
byte-identical product through `dft`, `arbitrary` and `schoolbook`, and inputs
3 and 4 through `fft` and `arbitrary`; in Task B the `dft` and `fft` engines
produce pixel-identical images from the same pipeline.

---

**Next:** [Task A — big-integer multiplication](02-task-a-bigmul.md) ·
[Task B — image convolution](03-task-b-image-conv.md)
