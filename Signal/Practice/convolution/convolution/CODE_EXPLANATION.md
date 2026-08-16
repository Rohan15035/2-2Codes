# Discrete-Time Convolution — Code Explanation

This document explains the two source files in this folder:

- [signal_lti.py](signal_lti.py) — the **library**: a finite discrete-time signal type and an LTI system built on a finite impulse response.
- [main.py](main.py) — the **driver**: reads a problem from a text file, runs convolution two different ways, cross-checks them, renders figures, and writes a report.

---

## 1. The math being implemented

A discrete-time LTI system is completely described by its impulse response `h[n]`. For any input `x[n]`, the output is the **convolution sum**:

```
y[n] = Σ  x[k] · h[n − k]
       k
```

The code computes this quantity in **two independent ways**, and then checks they agree:

| Method | Where | Idea |
|---|---|---|
| **Superposition (shift-and-scale)** | `LTISystem.output_by_superposition` | Decompose `x` into scaled impulses. Each sample `x[k]` produces a copy of `h` shifted to `k` and scaled by `x[k]`. Add all the copies. |
| **Direct convolution sum** | `LTISystem.output` | For each output index `n`, loop over `k` and accumulate `x[k]·h[n−k]`. |

They are mathematically the same identity read in two directions — one accumulates whole signals, the other accumulates one output sample at a time. Agreement between them (reported as a max-absolute-difference of ~`1e-16`) is the built-in correctness check.

If `x` lives on `[x_start, x_end]` and `h` lives on `[h_start, h_end]`, then `y` lives on:

```
[x_start + h_start ,  x_end + h_end]
```

so `len(y) = len(x) + len(h) − 1`. This is `LTISystem.output_range`.

---

## 2. `signal_lti.py`

### 2.1 `readable_time_ticks(time_values, max_labels=18)` — [signal_lti.py:4](signal_lti.py#L4)

A plotting helper, not signal math. Given a list of time indices, it returns a thinned-out subset so the x-axis does not become an unreadable smear of labels.

- If there are `≤ max_labels` values, it returns them unchanged.
- Otherwise it takes every `step`-th value, where `step = ceil(len / max_labels)`.
- It then force-appends the final time index if the stride happened to skip it, so the axis always shows where the signal ends.

> **Note:** it calls `.append()`, so the argument must be a **Python list**, not a NumPy array. Both call sites (`DiscreteSignal.plot` at [signal_lti.py:111](signal_lti.py#L111) and `plot_color_blocks` at [main.py:196](main.py#L196)) correctly pass `list(signal.times())`.

### 2.2 `class DiscreteSignal` — [signal_lti.py:17](signal_lti.py#L17)

A finite-support signal over an **integer index range**, stored as a dense NumPy array plus the integer index of the first sample.

```
self.start_time   # integer index of values[0]
self.end_time     # integer index of values[-1]
self.values       # np.ndarray, length = end_time - start_time + 1
```

The whole class rests on one mapping:

```
array position  =  time index  −  start_time
```

Everything outside `[start_time, end_time]` is defined to be zero.

#### `__init__(start_time, end_time)` — [signal_lti.py:21](signal_lti.py#L21)
Allocates a zero-filled signal covering the inclusive range. You then fill it via `set_value_at_time`, or by assigning `values` wholesale (which is what `make_signal` in `main.py` does).

#### `__len__()` — [signal_lti.py:27](signal_lti.py#L27)
Number of stored samples (the length of the support window, *not* the number of nonzero samples).

#### `times()` — [signal_lti.py:33](signal_lti.py#L33)
Returns `np.arange(start_time, end_time + 1)` — the integer indices, aligned one-to-one with `values`. Used everywhere as the iteration domain.

#### `get_value_at_time(t)` — [signal_lti.py:37](signal_lti.py#L37)
Reads a sample. **Out-of-range reads return `0.0` instead of raising.** This is the single most important convenience in the file: it is what lets `add` and the convolution loops treat signals of different supports uniformly, without any manual zero-padding.

#### `set_value_at_time(t, value)` — [signal_lti.py:43](signal_lti.py#L43)
Writes a sample, and **raises `IndexError`** if `t` is out of range. Deliberately asymmetric with the getter: reading outside the support is meaningful (it's zero), but writing outside it is a bug, since the array cannot grow.

#### `shift(k)` — [signal_lti.py:50](signal_lti.py#L50)
Returns `x[n − k]`: a new signal whose range is `[start+k, end+k]` and whose `values` array is a **copy** of the original.

The samples themselves are untouched — only the labelling of the window moves. That is the payoff of storing `(start_time, values)` instead of an absolute-indexed buffer: a shift is O(n) copy and zero arithmetic. The `.copy()` matters; without it, the shifted signal would alias the original's buffer and a later `multiply`/write would corrupt both.

(The commented-out `for` loop at [signal_lti.py:54-56](signal_lti.py#L54-L56) is an equivalent hand-rolled version of `values.copy()`.)

#### `add(other)` — [signal_lti.py:65](signal_lti.py#L65)
Pointwise sum over the **union** of the two supports:

```
new_start = min(self.start, other.start)
new_end   = max(self.end,   other.end)
```

then loops over every `t` in the union and stores `self[t] + other[t]`. The explicit `if start <= t <= end` guards are technically redundant — `get_value_at_time` already returns `0.0` outside the range — but they make the "treat missing samples as zero" intent explicit.

Returns a new signal; neither operand is mutated.

#### `multiply(scalar)` — [signal_lti.py:81](signal_lti.py#L81)
Returns a scaled copy over the same range, using NumPy broadcasting (`scalar * self.values`). The range is unchanged because scaling cannot move support.

> The `raise NotImplementedError` at [signal_lti.py:87](signal_lti.py#L87) is **dead code** — it sits after the `return`. It's a leftover from the assignment template. Harmless, but it can be deleted.

#### `nonzero_samples(tolerance=1e-12)` — [signal_lti.py:90](signal_lti.py#L90)
Returns `(times, values)` for samples whose magnitude exceeds `tolerance`, via a boolean mask. Useful for inspection/debugging. **Currently unused by `main.py`.**

The `1e-12` threshold (rather than `!= 0`) is the standard float-comparison hygiene: after a chain of multiplies and adds, an exact algebraic zero often lands at `1e-17`.

#### `plot(title, save_path=None, ax=None)` — [signal_lti.py:94](signal_lti.py#L94)
Draws the signal as a **stem plot** — the correct visual idiom for discrete-time data, since it shows samples as isolated points rather than implying a continuous curve between them.

- `matplotlib` is imported *inside* the method, so importing `signal_lti` stays cheap and dependency-free for non-plotting use.
- If no `ax` is given it makes its own figure; otherwise it draws into a caller-supplied axis. This is what lets `main.py` compose a 3-panel figure.
- Adds a zero line, grid, axis labels, and the thinned ticks from `readable_time_ticks`.
- Returns the axis for further customization.

### 2.3 `class LTISystem` — [signal_lti.py:120](signal_lti.py#L120)

Wraps a single `DiscreteSignal` — the impulse response `h[n]` — and derives everything else from it.

#### `__init__(impulse_response)` — [signal_lti.py:124](signal_lti.py#L124)
Stores `h` by reference. **Note:** no defensive copy, so mutating the impulse response after construction changes the system.

#### `output_range(input_signal)` — [signal_lti.py:129](signal_lti.py#L129)
Returns `(h_start + x_start, h_end + x_end)`, the support bounds derived in §1. Note it does **not** require `h` to start at 0 — a non-causal impulse response with a negative `start_time` works and correctly produces output before `n = 0`.

#### `get_response_components(input_signal)` — [signal_lti.py:136](signal_lti.py#L136)
The heart of the superposition view. For each `k` in the input's range:

1. read `x[k]`;
2. **skip it** if `|x[k]| ≤ 1e-12` (a zero input sample contributes nothing — this is the main speedup for sparse inputs);
3. otherwise build `x[k] · h[n − k]` as `h.shift(k).multiply(x[k])`;
4. collect `(k, component)`.

Returning the components as a list — rather than summing internally — is what makes this method useful for teaching and for plotting the individual contributions.

#### `output_by_superposition(input_signal)` — [signal_lti.py:147](signal_lti.py#L147)
Sums all components.

The subtle detail: it seeds the accumulator with a **zero signal spanning the full output range** before adding anything. Since `add` takes the union of supports, this guarantees the result has exactly the theoretical range `[x_start+h_start, x_end+h_end]` — even when the first and last input samples are zero and therefore contributed no component at all. Without that seed, an input like `[0, 1, 0]` would produce an output window narrower than the formula predicts, and the cross-check in `main.py` would fail on a shape mismatch.

#### `get_contributions_at_time(input_signal, n)` — [signal_lti.py:157](signal_lti.py#L157)
For a **single** output index `n`, returns every nonzero product term as a 4-tuple `(k, x[k], h[n−k], x[k]·h[n−k])`.

The guard `h_start <= n − k <= h_end` is the explicit form of "`h` is zero outside its support" — it skips index pairs that cannot contribute. Terms below `1e-12` are dropped.

Returning the full breakdown (not just the sum) makes it possible to print or plot *why* a given output sample has the value it does.

#### `output_at_time(input_signal, n)` — [signal_lti.py:171](signal_lti.py#L171)
Sums the contribution terms for index `n`. That is literally `y[n] = Σ_k x[k]·h[n−k]`.

#### `output(input_signal)` — [signal_lti.py:180](signal_lti.py#L180)
Loops `n` over the full output range, calls `output_at_time` for each, and assembles the result signal. (Another dead `raise NotImplementedError` at [signal_lti.py:188](signal_lti.py#L188).)

#### Cost comparison

With `N = len(x)` and `M = len(h)`:

- `output` — `O(N · (N + M))`: for each of the `N+M−1` output indices it scans all `N` input indices, including the ones that cannot contribute. Simple, allocation-free.
- `output_by_superposition` — `O(K · (N + M))` where `K` is the number of *nonzero* input samples, but each `add` allocates and rebuilds a full-length signal, so the constant factor is much larger.

Neither is optimized (a real implementation would use `np.convolve`, or FFT for large inputs). They are written for clarity and for mutual verification, which is the point of the exercise.

---

## 3. `main.py`

### 3.1 Environment setup — [main.py:1-13](main.py#L1-L13)

```python
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-cache")
matplotlib.use("Agg")
```

- `MPLCONFIGDIR` redirects matplotlib's font cache, avoiding warnings on machines where the home directory is read-only (grading containers, CI).
- `matplotlib.use("Agg")` selects the **headless raster backend** — no GUI window, files only. It must be called *before* `import matplotlib.pyplot`, which is why the imports are split across lines 6–10 instead of grouped at the top.

> On Windows, `/tmp/matplotlib-cache` resolves to `\tmp\matplotlib-cache` on the current drive. Harmless, but it's a Linux-shaped path — `tempfile.gettempdir()` would be portable.

### 3.2 Signal construction

#### `make_signal(start_time, end_time, values)` — [main.py:17](main.py#L17)
Builds a `DiscreteSignal` and replaces its `values` array wholesale with `np.array(values, dtype=float)`.

The `dtype=float` is load-bearing: an integer array would silently truncate later results (e.g. a `1/3` moving-average scale would land on `0`).

> ⚠️ **The big `# BUG:` comment at [main.py:18-24](main.py#L18-L24) is stale.** It describes a version that did `values.copy()` on a plain Python list. Line 26 already does the correct `np.array(values, dtype=float)` — the fix the comment recommends. The comment should be deleted; as written it will confuse the next reader into thinking there is a live defect.
>
> There is also a dead `raise NotImplementedError` at [main.py:28](main.py#L28).

A real (if minor) gap: `make_signal` never checks that `len(values) == end_time − start_time + 1`. Passing a mismatched list produces a signal whose `values` length disagrees with its declared range, which surfaces later as a confusing `IndexError` in `set_value_at_time` or a wrong-length plot.

#### `signal_from_samples(start_time, end_time, samples)` — [main.py:32](main.py#L32)
An alternative builder that accepts either a `dict` (`{time: value}`, sparse) or a list/array (dense, offset from `start_time`), leaving unspecified indices at zero. It's a convenience for defining sparse signals by hand — **currently unused by the rest of `main.py`.**

### 3.3 The impulse-response catalogue — [main.py:43-92](main.py#L43-L92)

Six factory functions, each returning one `DiscreteSignal`:

| Name | `h[n]` | Range | Effect |
|---|---|---|---|
| `impulse_identity` | `h[0] = 1` | `0..0` | Passthrough: `y = x`. The convolution identity. |
| `impulse_moving_average_3` | `1/3, 1/3, 1/3` | `0..2` | Smoothing / low-pass |
| `impulse_moving_average_5` | five × `1/5` | `0..4` | Stronger smoothing |
| `impulse_moving_average_7` | seven × `1/7` | `0..6` | Stronger still |
| `impulse_weighted_smoothing` | `0.5, 0.3, 0.2` | `0..2` | Smoothing weighted toward the present sample |
| `impulse_first_difference` | `1, −1` | `0..1` | Discrete derivative / high-pass: `y[n] = x[n] − x[n−1]` |

The three moving averages all delegate to a shared `impulse_moving_average(length)` at [main.py:49](main.py#L49), which builds `[1/length] * length`. The coefficients sum to 1, so a constant input passes through unchanged (unity DC gain).

`BUILT_IN_IMPULSES` at [main.py:81](main.py#L81) is a table of `(slug, description, factory)`. Storing the **factory** rather than a built signal means each run gets a fresh object, and nothing is constructed unless the input file actually asks for built-in mode.

Since every built-in `h` starts at `n = 0`, all of these systems are **causal** — output at `n` depends only on inputs at or before `n`.

### 3.4 Input file parsing — [main.py:95-138](main.py#L95-L138)

#### File format

```
<x_start> <x_end>
<x values, whitespace separated>
<mode>                     # either "custom" / "built-in" / "builtin"
<h_start> <h_end>          # only if mode == custom
<h values>                 # only if mode == custom
```

Blank lines and lines starting with `#` are stripped by `read_nonempty_lines` ([main.py:95](main.py#L95)) *before* parsing, so the format is comment-friendly and the parsers can address lines by a simple running index.

#### The parsers

- **`parse_signal(lines, index)`** — [main.py:105](main.py#L105) — consumes exactly two lines and returns `(signal, next_index)`. Threading the index through the return value is what lets the callers chain parsers without a cursor object.
- **`parse_impulse_response(lines, index)`** — [main.py:111](main.py#L111) — branches on the mode keyword:
  - `custom` → parse one more signal, return a single case tagged `"convolution"`.
  - `built-in` / `builtin` → return **all six** built-ins, each with a prefix like `builtin_4_moving_average_7` (the number keeps output files sorting in catalogue order).
  - anything else → `ValueError`.

  Either way it returns a **uniform list** of `(file_prefix, description, impulse_response)`, so `main()` has exactly one code path regardless of mode.
- **`read_problem_from_file(file_path)`** — [main.py:129](main.py#L129) — runs both parsers in sequence and then asserts `index == len(lines)`, rejecting trailing junk. That check catches the common mistake of a malformed file that happens to parse a valid prefix.

### 3.5 Verification — `max_absolute_difference` — [main.py:150](main.py#L150)

Walks `first_signal.times()`, compares against the same index in the second signal, and returns the largest absolute gap — the L∞ norm of the error.

Because it iterates only over the *first* signal's range and relies on the getter's out-of-range `0.0`, it would silently ignore any extra samples the second signal has beyond that range. In practice both arguments come from the same `output_range`, so the ranges are identical.

The vectorized one-liner is present but commented out at [main.py:152](main.py#L152); the explicit loop is equivalent and does not assume the two `values` arrays are the same length. Dead `raise NotImplementedError` at [main.py:164](main.py#L164).

**How to read the result:** the two methods perform the same additions in a *different order*, and floating-point addition is not associative. So the expected difference is not exactly `0` but a few multiples of machine epsilon (`~1e-16`). Anything meaningfully larger than that indicates a genuine bug, not rounding.

### 3.6 Visualization

#### `normalized_grayscale_rgb(signal)` — [main.py:167](main.py#L167)
Min-max normalizes the sample values into `0..255` and stacks the result into an RGB triple, producing a grayscale strip where dark = minimum and light = maximum.

The `np.isclose(minimum, maximum)` branch handles the constant-signal case, which would otherwise divide by zero; it paints a uniform mid-gray `128` instead.

#### `plot_color_blocks(signal, title, ax)` — [main.py:192](main.py#L192)
Renders the signal as a **1×N image strip** — an intensity view rather than a stem plot, which makes broad shape and smoothing effects easy to see at a glance for long signals.

Two details:
- `interpolation="nearest"` keeps each sample a hard-edged block instead of blurring between them (a blur would misrepresent discrete data).
- `imshow` indexes by **array position**, not by time index, so the tick labels from `readable_time_ticks` must be translated back into positions via `time_values.index(label)` ([main.py:197](main.py#L197)). White vertical lines at each `boundary − 0.5` draw the sample borders.

#### `plot_signals_as_stems(...)` — [main.py:181](main.py#L181)
A 3-panel stacked figure: `x[n]`, `h[n]`, `y[n]`. It delegates all drawing to `DiscreteSignal.plot`, passing each subplot axis — this is exactly the composition case the `ax` parameter exists for. `plt.close(fig)` after saving prevents figure accumulation across the six built-in cases.

#### `plot_signals_as_color_blocks(...)` — [main.py:211](main.py#L211)
A 2-panel input-vs-output intensity comparison. `h` is omitted here — it is typically only 2–7 samples long, so a color strip of it carries no useful information.

#### `save_visualizations(...)` — [main.py:221](main.py#L221)
Creates `<out_dir>/plot/` and `<out_dir>/color/`, writes `<file_prefix>.png` into each, and returns both paths so they can be cited in the report.

#### `clear_old_figures(out_dir)` — [main.py:240](main.py#L240)
Deletes stale `.png` files plus `results.txt` / `report.txt` from `out_dir` and from the two subfolders, so a run with fewer cases cannot leave orphaned images from a previous run lying around. It is deliberately narrow — it only removes files matching those specific patterns, never directories.

### 3.7 Reporting — [main.py:141-294](main.py#L141-L294)

- **`print_signal(signal, name)`** — [main.py:141](main.py#L141) — formats every sample as `n = <int>, value = <10.4f>`, aligned into columns.
- **`build_report_section(...)`** — [main.py:258](main.py#L258) — one section per impulse response: title, underline, the three signals, the output range, the max-absolute-difference verification number, and the two figure paths.
- **`build_report(...)`** / **`write_report(...)`** — [main.py:284](main.py#L284) — join the sections under an input-file header and write `<out_dir>/report.txt`.

All three build strings and return them rather than printing directly, so the same text can be both written to disk and echoed to stdout without being generated twice.

### 3.8 CLI and orchestration

#### `parse_arguments()` — [main.py:297](main.py#L297)

```
python main.py <input_file> [--out-dir outputs]
```

`input_file` is required and positional; `--out-dir` defaults to `outputs`.

#### `main()` — [main.py:313](main.py#L313)

The whole pipeline:

1. Parse args; create and clean the output directory.
2. Read the input file → one input signal and a list of impulse-response cases.
3. **For each case:**
   - build an `LTISystem` from `h`;
   - compute `y` by **superposition**;
   - compute `y` by the **direct convolution sum**;
   - compare the two (`max_absolute_difference`);
   - save the stem figure and the color figure;
   - append a report section.
4. Assemble the report, write it, print it, and print a summary line.

The `if __name__ == "__main__":` guard at [main.py:356](main.py#L356) keeps all of this from running if the module is imported.

---

## 4. Worked example

Input file:

```
0 2
1 2 3
custom
0 1
1 -1
```

So `x[n] = {1, 2, 3}` on `n = 0..2`, and `h[n] = {1, −1}` on `n = 0..1` (first difference).

**Output range:** `[0+0, 2+1] = [0, 3]` → 4 samples.

**Direct sum** (`y[n] = Σ x[k]·h[n−k]`):

| `n` | contributing terms | `y[n]` |
|---|---|---|
| 0 | `x[0]·h[0] = 1·1` | `1` |
| 1 | `x[0]·h[1] + x[1]·h[0] = 1·(−1) + 2·1` | `1` |
| 2 | `x[1]·h[1] + x[2]·h[0] = 2·(−1) + 3·1` | `1` |
| 3 | `x[2]·h[1] = 3·(−1)` | `−3` |

**Superposition** — three components, then summed:

```
k=0:  1 · h shifted to 0  →   1, -1,  0,  0
k=1:  2 · h shifted to 1  →   0,  2, -2,  0
k=2:  3 · h shifted to 2  →   0,  0,  3, -3
                             ------------------
                       sum =  1,  1,  1, -3     ✓
```

Both agree; `max_absolute_difference` reports ~`0`. The result `{1, 1, 1, −3}` is the expected discrete derivative of a ramp: constant `1` while the ramp rises, then a large negative spike where the finite signal drops back to zero.

---

## 5. Design notes and known rough edges

**What the design gets right**

- **`(start_time, values)` representation.** Storing the window offset separately from the samples makes `shift` trivial and lets signals with different supports be combined without manual padding.
- **Asymmetric bounds handling.** Reads outside the support return `0.0` (mathematically true); writes outside it raise (always a bug). This one decision removes nearly all the boundary logic from the convolution code.
- **Two independent implementations plus a numeric cross-check.** Self-verifying without a test suite.
- **Factories in the built-in table.** Fresh objects per run; nothing built unless requested.
- **Uniform `(prefix, description, signal)` case list.** `main()` has a single loop for both custom and built-in modes.

**Rough edges worth cleaning up**

| Issue | Location | Notes |
|---|---|---|
| Stale `# BUG:` comment describing an already-fixed defect | [main.py:18-24](main.py#L18-L24) | Actively misleading — delete it. |
| Dead `raise NotImplementedError` after `return` | [signal_lti.py:87](signal_lti.py#L87), [signal_lti.py:188](signal_lti.py#L188), [main.py:28](main.py#L28), [main.py:45](main.py#L45), [main.py:51](main.py#L51), [main.py:72](main.py#L72), [main.py:78](main.py#L78), [main.py:164](main.py#L164) | Template leftovers; unreachable. |
| No length validation in `make_signal` | [main.py:17](main.py#L17) | `len(values)` is never checked against `end − start + 1`; a mismatch fails confusingly later. |
| Unused helpers | `signal_from_samples` ([main.py:32](main.py#L32)), `DiscreteSignal.nonzero_samples` ([signal_lti.py:90](signal_lti.py#L90)) | Fine to keep as API surface, but nothing exercises them. |
| Linux-shaped temp path on Windows | [main.py:4](main.py#L4) | `tempfile.gettempdir()` would be portable. |
| `LTISystem` stores `h` by reference | [signal_lti.py:124](signal_lti.py#L124) | Mutating the impulse response after construction changes the system. |
| Unused local in `output_at_time` | [signal_lti.py:175](signal_lti.py#L175) | The loop unpacks `k, xk, hn_k` but only uses `term`. |
| Redundant range guards in `add` | [signal_lti.py:73-76](signal_lti.py#L73-L76) | `get_value_at_time` already returns `0.0` out of range. |
