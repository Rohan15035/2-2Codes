# Problem A (A1/A2) — Output from the Step Response

**File:** `solution_A.py`  ·  **Data:** `step_response.txt`, `input_signal.txt`

## What the problem asks

Normally an LTI system is described by its **impulse response** `h[n]`. Here you are
instead given the **step response** `s[n]` (the output when the input is the unit step
`u[n]`). You must compute the output for any input `x[n]` using the identities:

```
h[n]  = s[n] - s[n-1]        (with s[-1] = 0)   ← recover impulse response
Δx[n] = x[n] - x[n-1]        (with x[-1] = 0)   ← first difference of input
y[n]  = (Δx * s)[n]                              ← output using ONLY s[n]
```

Then verify against the ordinary method `y[n] = (x * h)[n]`.

## Why these identities are true (the intuition)

- The step is the running sum of the impulse: `s[n] = Σ_{k≤n} h[k]`. Undoing a running
  sum is a **first difference**, so `h[n] = s[n] - s[n-1]`.
- Convolution is linear and shift-invariant, so differencing the input is the same as
  differencing the system. That lets you swap the difference onto `x`:
  `y = x * h = x * (s - s_shifted) = (x - x_shifted) * s = Δx * s`.

So you never need `h` to get the output — differencing `x` and convolving with `s` is
enough. We compute `h` anyway just to **verify** both routes agree.

## How the code solves it (step by step)

1. **Read the files** — `read_signal_from_file` parses the two-line format
   (`nstart nend` then the samples) into a `DiscreteSignal`.

2. **Recover `h[n] = s[n] - s[n-1]`** — the helper `first_difference(sig)` does
   `sig + (-1)·sig.shift(1)` using **only** `DiscreteSignal` operations:
   ```python
   shifted     = sig.shift(1)          # sig[n-1]
   neg_shifted = shifted.multiply(-1)  # -sig[n-1]
   return sig.add(neg_shifted)         # sig[n] - sig[n-1]
   ```
   `shift(1)` is a one-sample delay, which is exactly `s[n-1]`.

3. **Compute `Δx[n]`** — the *same* `first_difference` helper applied to `x`.

4. **Output via step response** — `LTISystem(s).output(dx)` convolves `Δx` with `s`
   (the hand-written convolution sum in `signal_lti.py`, **no `numpy.convolve`**).

5. **Verify** — `LTISystem(h).output(x)` gives the classic answer. The two output
   signals occupy the *same* index range and their max absolute difference is `~1e-16`
   (floating-point zero) → they are the same signal.

## Result when you run it

```
Output range (y_s): (-20, 61)
Output range (y_h): (-20, 61)
Max |y_s - y_h| = 2.220e-16
SUCCESS: both methods give the same output signal.
```

Plots are written to `outputs/`: step response, recovered `h[n]`, input, `Δx[n]`, and
both outputs.

## Mapping to the original template (`template_conv_online.py`)

The template defines empty `Signal` / `LTI_System` classes with `Signal(INF)` (a
symmetric `-INF…INF` range). We **reuse your `DiscreteSignal` / `LTISystem`** instead,
which use explicit `start_time…end_time`. The three TODO functions map directly:

| Template TODO | Our implementation |
|---------------|--------------------|
| `first_difference(sig)` | `first_difference()` in `solution_A.py` |
| `impulse_from_step_response(s)` | `first_difference(s)` (same operation) |
| `output_using_step_response(x, s)` | `LTISystem(s).output(first_difference(x))` |
