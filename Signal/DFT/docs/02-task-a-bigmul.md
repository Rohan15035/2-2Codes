# 2 — Task A: Multiplying Enormous Integers (`bigmul.py`)

Multiply two integers of up to 20 000 decimal digits without using Python's
big-integer multiply — that appears exactly once, at the end, to check the
answer.

---

## 1 Theory

### 1.1 Digits are polynomial coefficients

Write an integer in base `B` as digits `a₀, a₁, …, a_{n-1}`, least significant
first:

```
A = sum_i a_i · B^i
```

Read that as a **polynomial** `A(x) = Σ aᵢxⁱ` evaluated at `x = B`. Multiplying
two integers is then multiplying two polynomials, and the coefficients of a
polynomial product are the **linear convolution** of the coefficient arrays:

```
p_m = sum_{i+j=m} a_i · c_j  =  (a ∗ c)[m]
```

Worked example — `1234 × 5678` in base 10, so `a = [4,3,2,1]`, `c = [8,7,6,5]`:

```
p = [32, 52, 61, 60, 34, 16, 5]
```

for instance `p₂ = a₀c₂ + a₁c₁ + a₂c₀ = 24 + 21 + 16 = 61`. These are not
digits yet — they are far larger than the base. A **carry sweep** from the
least significant end fixes that: 32 leaves digit 2 and carries 3; 52+3 = 55
leaves 5 carries 5; and so on, giving `[2,5,6,6,0,0,7]`, read the other way
`7 006 652`.

That is the whole algorithm. The only expensive part is the convolution — and
the convolution theorem makes it `O(N log N)`.

### 1.2 Limbs: packing several digits per coefficient

Nothing forces one decimal digit per coefficient. Packing 4 digits gives base
`B = 10⁴`, so `123456789` becomes `[6789, 2345, 1]`. Each packed coefficient is
a **limb**. A 20 000-digit operand is 20 000 coefficients in base 10 but only
5 000 in base 10⁴ — the transform is a quarter as long.

### 1.3 Why not pack more? The mantissa.

The FFT works in double-precision floating point, but the true convolution
coefficients are *integers*, so the final step rounds. Rounding only recovers
the right integer if that integer was representable in the first place. A
double carries a 53-bit mantissa, holding integers exactly up to
`2⁵³ ≈ 9.007 × 10¹⁵`. Each coefficient is a sum of at most `n` products of two
limbs:

```
p_max  ≤  n · (B − 1)²
```

| Base | `(B−1)²` | `p_max` at n = 5 000 | Safe? |
|---|---|---|---|
| `10⁴` | ~10⁸ | ~5.0 × 10¹¹ | yes, ~4 orders of headroom |
| `10⁹` | ~10¹⁸ | — | **no** — a single product already exceeds 2⁵³ |

With `B = 10⁹` the coefficients cannot be represented *before any summing
happens at all*, and rounding would hand back confidently wrong digits. That is
the trade: bigger base, shorter transform, less headroom. `BASE_DIGITS = 4`
([bigmul.py:37](../2305126/bigmul.py#L37)) sits comfortably inside the bound.

### 1.4 Padding, here

The product of an `n`-limb and a `q`-limb number has `n + q − 1` coefficients —
four digits times four digits gave seven coefficients above. A length-`N` DFT
only knows `N` output slots, so multiplying two length-`N` spectra pointwise
gives **circular** convolution: anything past the last slot wraps around and is
*added back* onto the start. In the worked example a length-4 transform would
have folded `p₄, p₅, p₆` back onto `p₀, p₁, p₂` and produced a plausible-looking
but entirely wrong number.

So: pad to `N ≥ n + q − 1`, and to a power of two on top of that for radix-2.

---

## 2 Implementation

### `to_limbs` — [bigmul.py:47](../2305126/bigmul.py#L47)

Sign is split off first and never touches the transform:

```python
sign = 1
if digits[:1] in ("+", "-"):
    sign = -1 if digits[0] == "-" else 1
    digits = digits[1:]
```

`digits[:1]` (a slice, not an index) is safe on an empty string. The magnitude
is then chopped from the *right* in `base_digits`-sized pieces, which is what
makes the array little-endian:

```python
for end in range(len(digits), 0, -base_digits):
    limbs.append(int(digits[max(0, end - base_digits):end]))
```

`max(0, …)` handles the leading partial limb (`123456789` → the final piece is
just `1`). Trailing zero limbs are stripped, and zero is normalised so that
`-0` can never be produced.

### `from_limbs` — [bigmul.py:86](../2305126/bigmul.py#L86)

The carry sweep, on un-reduced convolution output:

```python
for i in range(len(values)):
    total = values[i] + carry
    values[i] = total % base
    carry = total // base
while carry:
    values.append(carry % base)
    carry //= base
```

Note the `while` rather than an `if`: the final carry out of the top limb can
itself exceed the base. Reassembly zero-pads **every** limb to exactly
`base_digits` and strips leading zeros afterwards:

```python
text = "".join("%0*d" % (base_digits, v) for v in reversed(values))
text = text.lstrip("0") or "0"
return "-" + text if sign < 0 and text != "0" else text
```

Padding every limb is what keeps interior zeros intact — limb `[42]` in the
middle of a number is the four digits `0042`, and writing it as `42` would
silently delete two digits. The `or "0"` covers an all-zero result, and the
final guard prevents `"-0"`.

### `multiply_transform` — [bigmul.py:117](../2305126/bigmul.py#L117)

The pipeline, and the padding decision:

```python
length = a.size + b.size - 1
N = length if engine.name == "arbitrary" else next_power_of_two(length)
```

This is where `engine.name` earns its keep: Bluestein transforms at the exact
linear-convolution size, while `dft` and `fft` round up to a power of two. Then
zero-pad, transform both, multiply pointwise, invert, and round:

```python
spectrum = engine.transform(padded_a) * engine.transform(padded_b)
coefficients = np.rint(engine.inverse(spectrum).real[:length])
return coefficients.astype(np.int64), N
```

`.real` discards an imaginary part that is pure rounding noise (the inputs are
real, so the exact result is real); `np.rint` recovers the integers, which §1.3
guarantees are representable; slicing `[:length]` drops the padding zeros.

### `multiply_schoolbook` — [bigmul.py:163](../2305126/bigmul.py#L163)

The optional O(n²) baseline, one NumPy row-update per limb of `a`:

```python
for i in range(a.size):
    coefficients[i:i + b.size] += a[i] * b
```

Returns the same un-carried coefficient array as `multiply_transform`, so the
rest of the pipeline is shared. Overflow is not a concern: the largest possible
accumulation, 32 768 limbs of ~10⁸, is ~3.3 × 10¹² against int64's 9.2 × 10¹⁸.

### `multiply` / `run_single` — [:181](../2305126/bigmul.py#L181), [:203](../2305126/bigmul.py#L203)

`multiply` dispatches on method and returns `(product, N, limbs_a, limbs_b)`.
`run_single` writes `product.txt` and `report.txt`, and does the one permitted
big-integer operation:

```python
expected = int(text_a) * int(text_b)
verdict = "MATCH" if product == str(expected) else "MISMATCH"
...
if verdict != "MATCH":
    raise SystemExit("VERIFICATION FAILED for %s with engine %s" % (path, method))
```

A mismatch is never silently swallowed — it is written to the report *and*
exits nonzero.

---

## 3 Results

All four inputs verify, and `product.txt`/`report.txt` are byte-identical to
`expected_outputs/` (modulo CRLF, since the provided `io_utils.py` writes text
mode on Windows):

| Input | Digits | Limbs | Engine | N | Product digits | |
|---|---|---|---|---|---|---|
| 1 | 12 / 9 (one negative) | 3 / 3 | dft | 8 | 21 | MATCH |
| 2 | 200 / 200 | 50 / 50 | dft | 128 | 400 | MATCH |
| 3 | 2048 / 2048 | 512 / 512 | fft | 1024 | 4095 | MATCH |
| 4 | 20000 / 20000 | 5000 / 5000 | fft | 16384 | 40000 | MATCH |

Cross-checks: inputs 1 and 2 give a byte-identical product through `dft`,
`arbitrary` and `schoolbook`; inputs 3 and 4 through `fft` and `arbitrary`.
Every engine agrees with every other on every input it was run on.

### Benchmark — `outputs/task_a/benchmark/`

```
      digits    Naive DFT  Radix-2 FFT   Schoolbook
---------------------------------------------------
         128     0.001019     0.000452     0.000155
         512     0.015730     0.000829     0.000598
        1024     0.066130     0.001210     0.001306
        4096     1.169212     0.003116     0.007146
       16384           --     0.009540     0.047143
       65536           --     0.041807     0.454043
      131072           --     0.093927     1.603896
```

Reading the slopes (on the log-log plot, slope *is* the exponent):

- **Naive DFT** quadruples per doubling — textbook **O(n²)**. It is 375× slower
  than the FFT at 4096 digits and falls off the chart beyond that.
- **Radix-2 FFT** multiplies by ~2.25 per doubling, the signature of
  **O(n log n)** (pure `O(n)` would be 2.0).
- **Schoolbook** is the interesting curve. It is *faster than the FFT* through
  about 512 digits and level with it at 1024 — a NumPy-assisted O(n²) with a
  tiny constant beats an O(n log n) with a large one at small sizes. Past the crossover the asymptotics
  take over decisively: by 131 072 digits the FFT is **17× faster**.

That crossover is the honest lesson of the plot: complexity classes describe
behaviour in the limit, and the limit may be further out than your inputs.

### Bonus — `outputs/bonus/task_a/`

With `--engine arbitrary`, Bluestein transforms at the exact linear-convolution
size instead of padding to a power of two:

| Input | Radix-2 N | Bluestein N | Saved |
|---|---|---|---|
| 1 | 8 | 5 | 38% |
| 2 | 128 | 99 | 23% |
| 3 | 1024 | 1023 | ~0% |
| 4 | 16384 | 9999 | **39%** |

Input 3 shows the catch from the other side: 1023 sits just *under* 1024, so
radix-2 padding is nearly free there. It is lengths that land just *over* a
power of two — input 4's 9999, one past 8192 — that pay for almost twice the
transform they need. All four
verify MATCH.

---

**Previous:** [The transform core](01-transform-core.md) ·
**Next:** [Task B — image convolution](03-task-b-image-conv.md)
