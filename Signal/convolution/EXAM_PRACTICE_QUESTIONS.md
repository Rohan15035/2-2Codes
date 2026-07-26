# CSE220 — Convolution Online: Practice Question Set

Eight practice questions written in the same shape as the two real papers you have:

- **[A1_A2.pdf](Convolution_A1_A2/Convolution_A1_A2/A1_A2.pdf)** — *generic property testers*: write functions that accept **any** system as a callable, apply them to one genuine LTI system and one hand-written non-LTI system, print the max-difference numbers, conclude which property fails.
- **[spec.pdf](online-B/online-B/spec.pdf)** — *cascade / system algebra*: connect systems with repeated `LTISystem.output` calls, verify an identity, respect a finite stored window, compare only on the graded observation range.

Every question below follows the same house rules:

> **Total Marks: 10 · Total Time: 30–40 minutes**
> Reuse your `DiscreteSignal` and `LTISystem` classes from the offline.
> **Do NOT use `numpy.convolve`, `scipy.signal`, or any built-in convolution routine.**
> Finish with a `print` statement stating your conclusion.
> Rename your file as `2305xxx.py` and submit in Moodle.

**Every answer key below was produced by actually running the code against your `signal_lti.py`** — the numbers are real, not estimated.

Recipes for anything you get stuck on are in [EXAM_TOOLKIT.md](EXAM_TOOLKIT.md).

| # | Style | Topic | Difficulty |
|---|---|---|---|
| 1 | A | Causality & BIBO stability as generic tests | ●●○○○ |
| 2 | A | Non-LTI zoo — which property fails, three ways | ●●○○○ |
| 3 | B | Commutativity & associativity of cascades | ●●○○○ |
| 4 | B | Parallel branches & distributivity | ●●○○○ |
| 5 | B | Echo canceller — inverse system by truncated series | ●●●●● |
| 6 | B | Step response ↔ impulse response roundtrip | ●●●○○ |
| 7 | A/B | Matched filter — detection via time-reversed convolution | ●●●●○ |
| 8 | B | Block diagram → single equivalent impulse response | ●●●○○ |

---

## Question 1 — Causality and Stability as Generic Tests

A discrete-time system is **causal** if the output at time `n` depends only on inputs at times `≤ n`. Equivalently: if `x[n] = 0` for all `n < n₀`, then `y[n] = 0` for all `n < n₀`. An LTI system is **BIBO stable** iff its impulse response is absolutely summable, `Σ|h[n]| < ∞`.

**Given**

```
h_A[n] :  n = 0...2,    values = [1, 0.5, 0.25]
h_B[n] :  n = -1...1,   values = [0.5, 1, 0.5]
probe[n] : n = 0...2,   values = [1, 2, -1]        (zero for n < 0)
System C is defined directly on samples:  y_C[n] = x[n+1]   (a one-step advance)
```

**Tasks**

- Implement `test_causality(apply_system, probe_signal, n0)`, returning the largest `|y[n]|` found at any `n < n0`. It must work for **any** callable mapping a `DiscreteSignal` to a `DiscreteSignal` — do not assume `apply_system` is an `LTISystem`.
- Implement `absolute_sum(impulse_response)` returning `Σ|h[n]|`, using only `DiscreteSignal` operations.
- Implement `system_c(input_signal)` as a plain function.
- Run the causality test on all three systems (A and B via `LTISystem.output`, C via `system_c`) with the given probe and `n0 = 0`. Print all three leak values.
- Print `Σ|h[n]|` for `h_A` and `h_B`.
- In a `print` statement, state which systems are causal and why the non-causal ones leak output before `n = 0`.

<details><summary><b>Answer key</b></summary>

```
leak causal (h_A)   : 0.0        → causal
leak noncausal (h_B): 0.5        → NOT causal
leak advance (C)    : 1.0        → NOT causal
sum|h_A| = 1.75      sum|h_B| = 2.0     → both BIBO stable
```

The leak values are not arbitrary. `h_B` starts at `n = −1`, so `y[−1] = x[0]·h_B[−1] = 1 × 0.5 = 0.5`. System C is `x[n+1]`, so `y[−1] = x[0] = 1`. **Causality is a property of where `h` starts** — an LTI system is causal iff `h.start_time ≥ 0`. Stability is about the *magnitudes*, and is entirely independent: `h_B` is unstable-free but non-causal, which shows the two properties are orthogonal.
</details>

---

## Question 2 — The Non-LTI Zoo

*(A direct extension of A1/A2 — same testers, three systems instead of one.)*

**Given**

```
x1[n] : n = -2...2,  values = [1, 0, 2, -1, 3]
x2[n] : n = -1...3,  values = [2, -3, 0, 1, 1]
a = 2,   b = -3,   k = 3

System P:  y[n] = x[n]²          (squarer)
System Q:  y[n] = x[-n]          (time reversal)
System R:  y[n] = 2·x[n] + 1     (amplifier with DC offset)
```

**Tasks**

- Implement `test_linearity(apply_system, x1, x2, a, b)` returning `max| S{a·x1 + b·x2} − (a·S{x1} + b·S{x2}) |`.
- Implement `test_time_invariance(apply_system, x, k)` returning `max| S{x[n−k]} − y[n−k] |`.
- Implement `system_p`, `system_q`, `system_r` as plain functions using only `DiscreteSignal` operations. Note that System Q **changes the signal's time range** — think about what the output range must be before you allocate it.
- Run both tests on all three systems and print all six numbers in a table.
- In a `print` statement, state for each system exactly which property it satisfies and which it violates.

<details><summary><b>Answer key</b></summary>

```
System     linearity      time-invariance
square     188            0
reverse    0              3
bias 2x+1  4              0
```

- **P (squarer)** — time-invariant (squaring doesn't care about `n`), **not linear**: `(a·x)² ≠ a·x²`.
- **Q (reversal)** — linear (it just relabels indices, and relabelling commutes with scaling and adding), **not time-invariant**: `S{x[n−k]} = x[−n−k]` but `y[n−k] = x[−n+k]`. These differ by a shift of `2k`, which is why the number `3` appears for `k = 3`.
- **R (affine)** — time-invariant, **not linear**. The `+1` is the culprit: a linear system must map the zero signal to zero, and R maps it to the constant 1. This is the classic trap — "linear" in the everyday sense (a straight line) is *not* linearity in the systems sense.

For System Q, the output range is `[−end, −start]`, not `[start, end]`. Allocating `DiscreteSignal(sig.start_time, sig.end_time)` and then writing to `−n` will raise `IndexError`.
</details>

---

## Question 3 — Convolution is Commutative and Associative

Cascading LTI systems has an equivalent single impulse response given by convolution. Because convolution is commutative and associative, **the order of the boxes in a cascade does not matter**.

**Given**

```
h1[n] : n = 0...2,  values = [1, 0, 0.5]      (direct path + half-amplitude echo at lag 2)
h2[n] : n = 0...2,  values = [1/3, 1/3, 1/3]  (3-point moving average)
h3[n] : n = 0...1,  values = [1, -1]          (first difference)
```

**Tasks**

- Compute `h1 * h2` and `h2 * h1` **without** any dedicated convolution helper — use `LTISystem(h1).output(h2)` and `LTISystem(h2).output(h1)`. Print both and their max absolute difference.
- Compute `(h1 * h2) * h3` and `h1 * (h2 * h3)`. Print both and their max absolute difference.
- Verify the range arithmetic: print the start/end of each result and confirm `len(h1 * h2) = len(h1) + len(h2) − 1`.
- In a `print` statement, state what these two numbers demonstrate about cascade ordering.

<details><summary><b>Answer key</b></summary>

```
h1*h2      : n=0..4  [0.333333, 0.333333, 0.5, 0.166667, 0.166667]
commutativity difference : 0.0
(h1*h2)*h3 : n=0..5  [0.333333, 0.0, 0.166667, -0.333333, 0.0, -0.166667]
associativity difference : 5.55e-17
```

`5.55e-17` is a rounding residue, not a mismatch — the two groupings perform the same additions in a different order and float addition isn't associative. Anything under `1e-9` means "equal".

The key insight for the code: **`LTISystem.output` does not care that its argument is "an impulse response"** — a signal is a signal. Feeding `h2` into `LTISystem(h1)` is how you convolve two impulse responses when you're forbidden from using `np.convolve`.
</details>

---

## Question 4 — Parallel Branches and Distributivity

When two LTI systems are driven by the same input and their outputs are **added**, the combination is a single LTI system with impulse response `h1 + h2`.

**Given**

```
h1[n] : n = 0...2,  values = [1, 0, 0.5]
h2[n] : n = 0...2,  values = [1/3, 1/3, 1/3]
x[n]  : n = -2...2, values = [1, 0, 2, -1, 3]
```

**Tasks**

- Build the parallel-equivalent impulse response `h_par = h1 + h2` using `DiscreteSignal.add`. Print it.
- Compute the output two ways: (i) one `LTISystem(h_par)` applied to `x`; (ii) `LTISystem(h1).output(x)` added to `LTISystem(h2).output(x)`. Print both.
- Print the max absolute difference between them.
- Now change `h2` to start at `n = 2` instead of `n = 0` and re-run. Print the new `h_par` range and explain in a comment why `add` gives the right answer without you padding anything by hand.
- In a `print` statement, state the distributive law you have just verified.

<details><summary><b>Answer key</b></summary>

```
h1+h2 : n=0..2  [1.333333, 0.333333, 0.833333]
distributivity difference : 1.11e-16
```

The law is `x * (h1 + h2) = (x * h1) + (x * h2)`.

The last task is the real lesson: `add` takes the **union** of the two supports and relies on `get_value_at_time` returning `0.0` outside each signal's range. With `h2` moved to `n = 2…4`, `h_par` automatically spans `0…4` with the gap filled by zeros. You never write padding logic — the zero-returning getter is the padding.
</details>

---

## Question 5 — Echo Canceller (Inverse System by Truncated Series)

A recording picks up a single delayed echo:

```
h[n] = δ[n] + α·δ[n−D]          with α = 0.6, D = 3
```

The exact inverse is an infinite series, `g[n] = Σ_{m≥0} (−α)^m · δ[n − mD]`, which cannot be stored. Truncate it at `m = M`.

**Given**

```
α = 0.6,  D = 3,  M = 4
x[n] : n = 0...6,  values = [2, -1, 3, 1, -2, 0, 4]
OBSERVATION_START = 0,  OBSERVATION_END = 14
```

**Tasks**

- Build `h[n]` on `n = 0…D` as a sum of shifted, scaled impulses (do **not** hand-type the zeros).
- Build the truncated inverse `g[n]` on `n = 0…M·D` the same way.
- Compute the equivalent cascade response `h * g` and print it. Identify, by index and value, the single sample that stops it from being exactly `δ[n]`.
- Pass `x` through the echo system, then through `g`. Print the recovered signal.
- Print the max absolute difference between the recovered signal and `x` over the observation window, **and** over the full support. Explain why the two numbers differ.
- In a `print` statement, state the relationship between `M` and the length of the window over which cancellation is exact.

<details><summary><b>Answer key</b></summary>

```
h      : n=0..3   [1.0, 0.0, 0.0, 0.6]
g      : n=0..12  [1, 0, 0, -0.6, 0, 0, 0.36, 0, 0, -0.216, 0, 0, 0.1296]
h*g    : n=0..15  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.07776]

recovery difference on n = 0...14 : 4.44e-16     ← exact
recovery difference on full range : 0.31104      ← truncation tail
```

The series telescopes: every intermediate term cancels, leaving `h * g = δ[n] + α^(M+1)·δ[n − (M+1)D]`. Here `0.6⁵ = 0.07776` at `n = 15`.

So cancellation is **exact** for `n < (M+1)·D = 15`, and the leftover echo appears only from `n = 15` onward. The full-range difference of `0.31104` is `0.07776 × 4` — the residual acting on `x[6] = 4`. That number is not a bug; it's the truncation you chose when you picked `M`. Doubling `M` shrinks the residual geometrically (`α^(M+1)`) *and* pushes it further out in time.

This is the same finite-window logic as spec B's `h2[n] = u[n]` stored on `0…10` — an infinite impulse response, truncated just far enough that the graded window is exact.
</details>

---

## Question 6 — Step Response ↔ Impulse Response Roundtrip

The step response is `s[n] = (h * u)[n]`. Since `u[n] − u[n−1] = δ[n]`, differencing the step response returns the impulse response: `h[n] = s[n] − s[n−1]`.

**Given**

```
h[n] : n = 0...2,  values = [1, 0.5, 0.25]
u[n] : stored on n = 0...11
```

**Tasks**

- Compute the step response `s = LTISystem(h).output(u)` and print it.
- Recover the impulse response by first differencing `s`, using **only** `DiscreteSignal` operations (`shift`, `multiply`, `add`) — no `LTISystem`, no loop over samples.
- Print the recovered signal in full, then print the max absolute difference against the true `h` over `n = 0…2`, and separately over the full support.
- Explain in a comment what the extra nonzero samples at the tail of the recovered signal are.
- In a `print` statement, state the impulse ↔ step response relationship in both directions.

<details><summary><b>Answer key</b></summary>

```
s              : n=0..13  [1, 1.5, 1.75, 1.75, ..., 1.75, 0.75, 0.25]
s[n] − s[n−1]  : n=0..14  [1, 0.5, 0.25, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -0.5, -0.25]

difference on n = 0...2 : 0.0        ← exact recovery
difference on full range : 1.0       ← truncation tail
```

The one-liner is `s.add(s.shift(1).multiply(-1))`.

The tail `[−1, −0.5, −0.25]` at `n = 12…14` is a **mirror image of `h`, negated**. It appears because the stored `u[n]` stops at `n = 11`, so the finite pulse you actually convolved was `u[n] − u[n−12]`, and its response contains a falling edge as well as a rising one. The rising edge gives you `h`; the falling edge gives you `−h`, delayed by 12.

Both directions of the relationship: `s[n] = Σ_{k≤n} h[k]` (running sum), and `h[n] = s[n] − s[n−1]` (first difference). Accumulation and differencing are inverse operations — the same fact spec B asks you to demonstrate from the other side.
</details>

---

## Question 7 — Matched Filter (Detection by Time-Reversed Convolution)

Cross-correlation of `x` with a template `t` equals convolution with the **time-reversed** template:

```
r[n] = Σ_k x[k]·t[k−n] = (x * t̃)[n],   where t̃[n] = t[−n]
```

The peak of `r` marks where the template sits inside `x`.

**Given**

```
t[n] : n = 0...2,  values = [1, -1, 2]
x[n] : n = 0...14, all zeros except
       x[1] = 0.5,  x[4] = 1,  x[5] = -1,  x[6] = 2,  x[9] = -0.5,  x[11] = 0.3
```

**Tasks**

- Implement `reverse(signal)` returning `t[−n]`. Be careful with the output range — it is **not** the same as the input range.
- Build `x` using a sparse construction (a dict of `{index: value}`), not a 15-element list.
- Compute `r = LTISystem(reverse(t)).output(x)` and print it.
- Find and print the index of the largest-magnitude sample of `r`, and its value.
- Print `Σ t[n]²` and compare it with the peak value. Explain the relationship in a comment.
- In a `print` statement, state at which index the template occurs in `x` and how you know.

<details><summary><b>Answer key</b></summary>

```
r = x * reverse(t) : n=-2..14
    [0, 1, -0.5, 0.5, 2, -3, 6, -3, 2, -1, 0.5, 0.1, -0.3, 0.3, 0, 0, 0]
peak index : 4     peak value : 6.0
Σ t[n]²    : 6.0
```

`reverse(t)` spans `n = −2…0`, so `r` starts at `n = −2` — forgetting that the reversed signal's range flips is the usual mistake here.

The peak lands at `n = 4`, exactly where the copy of `[1, −1, 2]` begins in `x`. And the peak value `6.0` equals the template's energy `Σt² = 1 + 1 + 4 = 6`. That is the defining property of a matched filter: correlation is maximised when the template aligns with itself, and the maximum equals the template energy. Every other lag gives a smaller value because the template is only partially overlapping.
</details>

---

## Question 8 — Block Diagram to a Single Equivalent System

```
                ┌──────────┐
          ┌────►│    h1    ├────┐
          │     └──────────┘    │
   x[n] ──┤                     ⊕──►┌──────────┐
          │     ┌──────────┐    │   │    h3    ├──► y[n]
          └────►│    h2    ├────┘   └──────────┘
                └──────────┘
```

Two parallel branches feed a summing junction, whose output drives a third system.

**Given**

```
h1[n] : n = 0...2,  values = [1, 0, 0.5]
h2[n] : n = 0...2,  values = [1/3, 1/3, 1/3]
h3[n] : n = 0...1,  values = [1, -1]
x[n]  : n = -2...2, values = [1, 0, 2, -1, 3]
```

**Tasks**

- Compute `y[n]` by following the diagram literally: two `output` calls, one `add`, one more `output`.
- Derive the single equivalent impulse response `h_eq` for the whole block diagram and build it with `add` and `output` calls. Print it and its range.
- Compute `y[n]` a second way, as `LTISystem(h_eq).output(x)`.
- Print the max absolute difference between the two computations.
- Predict the output range from `h1`, `h2`, `h3` and `x` **before** printing it, and check your prediction in a comment.
- In a `print` statement, write the algebraic identity your two computations verify.

<details><summary><b>Answer key</b></summary>

```
h_eq = (h1 + h2) * h3 : n=0..3  [1.333333, -1.0, 0.5, -0.833333]
difference between the two routes : 8.88e-16
```

The identity is `((x * h1) + (x * h2)) * h3 = x * ((h1 + h2) * h3)` — distributivity followed by associativity.

Range prediction: `h1 + h2` spans `0…2`; convolving with `h3` (`0…1`) gives `h_eq` on `0…3`; convolving with `x` (`−2…2`) gives `y` on `−2…5`, i.e. `5 + 4 − 1 = 8` samples.

The general recipe for any feedback-free block diagram: **parallel branches add their impulse responses, cascaded blocks convolve theirs.** Collapsing the diagram first is usually less code than simulating it box by box, and it's the version an exam wants you to justify.
</details>

---

## Exam strategy

**Time allocation for a 30-minute paper.** Roughly 5 minutes reading and writing helpers, 15 minutes on the tasks, 5 minutes on plots and the conclusion, 5 minutes spare.

**The order that avoids most crashes**

1. Paste in `DiscreteSignal` and `LTISystem` unchanged. Do not edit them.
2. Write `make_signal` and `max_abs_diff_in_range` immediately, before reading the tasks in detail.
3. Build the given signals and **print them right away** to check ranges and values against the paper.
4. Do the tasks in the order the paper lists them — the marks are usually one per bullet.
5. Never leave `conclusion = None`.

**The five mistakes that cost the most marks**

| Mistake | Cost |
|---|---|
| `sig.values[n]` with a time index instead of `get_value_at_time(n)` | wrong answers on any signal not starting at 0; `IndexError` on shifted signals |
| `a * signal` instead of `signal.multiply(a)` | `TypeError` |
| Feeding the original `x` to both boxes of a cascade | tests the wrong thing entirely |
| Comparing over the full support instead of the observation window | a correct system reports a large error |
| Leaving the conclusion unwritten | free marks lost |

**Sanity checks that cost nothing**

- `system.output(delta)` must return `h` exactly.
- `output(x)` and `output_by_superposition(x)` must agree to `~1e-16`.
- Output length must equal `len(x) + len(h) − 1`.
- If a "max difference" comes out *exactly* `0.0` on a test that should be non-trivial, suspect your comparison function before you believe it.
