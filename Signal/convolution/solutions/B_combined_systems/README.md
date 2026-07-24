# Problem B (B1/B2) — Combination of LTI Systems

**File:** `solution_B.py`

## What the problem asks

Given the block diagram:

```
        +------+
   x -->|  h1  |---+
        +------+   |      +------+
                  (+)---->|  h3  |--> y
        +------+   |      +------+
   x -->|  h2  |---+
        +------+
```

`x` goes into `h1` **and** `h2` in **parallel**; their outputs are **added**; the sum
goes through `h3` in **series (cascade)**.

Do it two ways and show they match:
1. **Block by block** — actually push signals through each block.
2. **One equivalent system** — find a single `h_combined` for the whole diagram.

## The two LTI rules you need

- **Parallel adds:** two systems fed the same input and summed behave like one system
  with `h_parallel = h1 + h2`.
- **Cascade convolves:** feeding one system's output into another is one system with
  `h_series = h_a * h_b`.

Putting them together:

```
h_combined = (h1 + h2) * h3
y = x * h_combined
```

## How the code solves it

**Signals** (from the template): `x[0]=1, x[2]=-1`; `h1=δ[n]` (identity);
`h2 = 0.5·δ[n-1]`; `h3[0]=h3[1]=1` (i.e. `y[n]=x[n]+x[n-1]`).

**Method 1 — block by block:**
```python
y1 = sys1.output(x)            # x * h1
y2 = sys2.output(x)            # x * h2
y_parallel = y1.add(y2)        # add the two branches
y_final_1 = sys3.output(y_parallel)   # push the sum through h3
```

**Method 2 — combined impulse response:**
```python
h_parallel = h1.add(h2)                 # h1 + h2
h_combined = sys3.output(h_parallel)    # (h1 + h2) * h3   ← convolution of two h's
y_final_2  = LTISystem(h_combined).output(x)
```
> Note the neat trick: convolving `h3` with `(h1+h2)` is done by treating `sys3` as an
> LTI system and passing `(h1+h2)` in as if it were an input. Convolution doesn't care
> which operand is the "signal" and which is the "impulse response" — it's commutative.

**Verify:** `max |y_final_1 - y_final_2|` is exactly `0`.

## Result when you run it

```
h_combined samples: [0, 1, 2] -> [1.0, 1.5, 0.5]
y range: (0, 4)
y values: [1.0, 1.5, -0.5, -1.5, -0.5]
Max |y1 - y2| = 0.000e+00
Outputs are equal: True
```

Check `h_combined` by hand: `h1+h2 = {0:1, 1:0.5}`, convolved with `h3 = {0:1, 1:1}`
gives `{0:1, 1:1.5, 2:0.5}` ✓.

Plots (`outputs/`): block-by-block output, `h_combined`, and the combined output.

## Mapping to the original template (`template.py`)

The template asks you to define `Signal`/`LTI_System` and fill in `y_final_1` and
`h_combined`. We reuse `DiscreteSignal`/`LTISystem`; `y_final_1` is the block-by-block
chain and `h_combined = (h1+h2) * h3`.
