# Solution Notes — The Two Onlines

Not a full walkthrough. Just the code segments that actually earn marks, and what part of the problem each one answers.

| Paper | File | Status |
|---|---|---|
| **A1/A2** — linearity & time-invariance testers | [Convolution_A1_A2/.../template.py](Convolution_A1_A2/Convolution_A1_A2/template.py) | ⚠️ **`system_b` is broken — crashes.** See §A4 |
| **B** — accumulator ⟷ first-difference cascade | [online-B/online-B/template.py](online-B/online-B/template.py) | ✅ fixed and verified |

---

# Paper A — Generic Property Testers

**The problem:** prove that a real LTI system satisfies linearity and time-invariance, and that `y[n] = n·x[n]` does not. The testers must work for *any* system, so they cannot mention `LTISystem`.

## A1. Testing linearity

```python
def test_linearity(apply_system, x1, x2, a, b):
    lhs = apply_system(x1.multiply(a).add(x2.multiply(b)))          # S{a·x1 + b·x2}
    rhs = apply_system(x1).multiply(a).add(apply_system(x2).multiply(b))
    return max_absolute_difference(lhs, rhs)
```

**Solves:** the whole linearity task in three lines.

It is a direct transcription of the definition `T{a·x1 + b·x2} = a·T{x1} + b·T{x2}` — build the left side, build the right side, measure the gap. The only translation work is that `DiscreteSignal` has no operators: `a*x1 + b*x2` must be written `x1.multiply(a).add(x2.multiply(b))`. Chaining works because both methods return new signals.

Returning a **number** rather than a boolean is what makes it a useful answer: `0.0` means the property holds, and the size of a nonzero value tells you how badly it fails.

## A2. Testing time-invariance

```python
def test_time_invariance(apply_system, x, k):
    return max_absolute_difference(apply_system(x.shift(k)), apply_system(x).shift(k))
```

**Solves:** the time-invariance task.

"Shift then apply" versus "apply then shift" — the definition `T{x[n−k]} = y[n−k]` is literally the two orderings of `.shift(k)` and `apply_system(...)`. If they commute, the system is time-invariant.

Note this works only because `shift` returns a new signal rather than mutating in place; otherwise the second call would see an already-shifted input.

## A3. Passing the system in

```python
system_a = LTISystem(h)

diff_linear_a = test_linearity(system_a.output, x1, x2, a, b)   # bound method, no ()
diff_linear_b = test_linearity(system_b, x1, x2, a, b)          # plain function object
```

**Solves:** the "must work for any `apply_system` callable" requirement.

`system_a.output` **without parentheses** is the function object, with `self` already bound to `system_a`. The tester later calls `apply_system(sig)`, which runs `system_a.output(sig)`.

The two ways to get this wrong:
- `test_linearity(system_a, ...)` — an `LTISystem` object is not callable.
- `test_linearity(system_a.output(x1), ...)` — parentheses call it *now*, passing a `DiscreteSignal` where a function was expected.

This is why the paper spends a whole page on "passing a function as a parameter": the same tester has to accept a bound method from one system and a plain `def` from another, and only the no-parentheses form makes both work.

## A4. ⚠️ System B — the live bug

```python
def system_b(input_signal):
    output = DiscreteSignal(input_signal.start_time, input_signal.end_time)
    for i in input_signal.times():
        output.values[i] = i * input_signal.values[i]     # ✗ BROKEN
    return output
```

Running the file right now gives:

```
=== System B: y[n] = n * x[n] ===
IndexError: index 5 is out of bounds for axis 0 with size 5
```

**What's wrong:** `i` is a **time index**, but `.values` is a **0-based array**. For `x1` on `n = −2…2`, `values[-2]` is Python's negative indexing — it silently reads the *second-to-last* element instead of the first. No error, just wrong numbers. Then `test_time_invariance` passes in `x1.shift(3)`, whose times are `1…5`, and `values[5]` is off the end of a 5-element array — crash.

**The fix** — go through the accessors, which do the `t − start_time` translation for you:

```python
def system_b(input_signal):
    output = DiscreteSignal(input_signal.start_time, input_signal.end_time)
    for n in input_signal.times():
        output.set_value_at_time(n, n * input_signal.get_value_at_time(n))
    return output
```

With that fix the results are:

```
System A:  linearity 0.0        time-invariance 0.0        → genuine LTI
System B:  linearity 0.0        time-invariance 9.0        → linear, NOT time-invariant
```

**The conclusion the paper asks for:** System B *is* linear — scaling and adding inputs scales and adds outputs, because the multiplier `n` doesn't depend on `x`. It **fails time-invariance**, because the gain applied to a sample depends on *where* the sample sits. Delay the input and each sample gets multiplied by a different `n` than before, so `S{x[n−k]} ≠ y[n−k]`.

The `main()` also still ends with an unwritten conclusion — the last bullet of the paper. Write it.

---

# Paper B — Accumulator and First Difference

**The problem:** show that a running-sum accumulator followed by a first difference is the identity system, using a non-impulse input, without ever constructing `h1 * h2` explicitly.

## B1. The cascade

```python
def cascade(first_system, second_system, input_signal):
    intermediate_output = first_system.output(input_signal)
    final_output = second_system.output(intermediate_output)
    return intermediate_output, final_output

accumulator_output, difference_output = cascade(accumulator, differentiator, x)
```

**Solves:** the "connect them using repeated calls to `LTISystem.output`" task.

The entire content is that the second call takes `intermediate_output`, **not** `input_signal`. Feed both systems the same `x` and you have built two parallel systems that answer a different question altogether. Returning both outputs matters because the paper asks you to print and plot the intermediate `v[n]` as well as the final `y[n]`.

## B2. The unit step under a finite window

```python
h1 = make_signal(0, 1, [1.0, -1.0])      # δ[n] − δ[n−1]
h2 = make_signal(0, 10, np.ones(11))     # u[n], stored on n = 0...10
```

**Solves:** the "store enough samples of `h2`" task, and the finite-window note.

`h2[n] = u[n]` is `1` for **every** `n ≥ 0` — `np.ones`, not `np.arange`. (A ramp `[0,1,2,…]` would make the system a weighted running sum, and nothing downstream would work.)

Why exactly 11 samples: computing `y[n]` for `n ≤ 8` requires `v` up to `n = 8`, and `v[n] = Σ_k x[k]·h2[n−k]` with `x` supported on `−2…2` reaches `h2` at index at most `8 − (−2) = 10`. So `n = 0…10` isn't an approximation on the graded window — it's exact.

**The general rule:** to report `y` correctly on `[N₀, N₁]` with input supported on `[x₀, x₁]`, store an infinite `h` out to index `N₁ − x₀`.

## B3. Comparing on the observation window only

```python
max_difference = max_absolute_difference_in_range(
    difference_output, x, OBSERVATION_START, OBSERVATION_END
)
```

**Solves:** the "compute the maximum absolute difference between the first-difference response and `x[n]` over `n = −2…8`" task.

Two decisions, both load-bearing:

- **Which signals.** The claim is `(h1 * h2)[n] = δ[n]`, so the thing to verify is *final output vs. the original input*. Comparing the two intermediate signals against each other tests nothing.
- **Which range.** The full supports run to `n = 19`. Past `n = 8`, the truncated `h2` makes `v[n]` drift from the true running sum, so `y[n]` out there is a truncation artifact. Comparing over it reports a big error for a system that is perfectly correct — which is exactly why the spec says *"Compare results only on OBSERVATION_START…OBSERVATION_END."*

## B4. The comparison helper

```python
def max_absolute_difference_in_range(first_signal, second_signal, start_time, end_time):
    worst = 0.0
    for n in range(start_time, end_time + 1):
        diff = abs(first_signal.get_value_at_time(n) - second_signal.get_value_at_time(n))
        if diff > worst:
            worst = diff
    return worst
```

**Solves:** the reusable verification metric every one of these papers asks for.

It reads through `get_value_at_time`, so it works even when the requested range extends past either signal — the out-of-range zeros are the correct mathematical values, not padding hacks.

Two mistakes worth remembering because they are silent:

- `np.abs(a, b)` is **not** absolute difference. numpy's second positional argument is `out`, the destination array — so this asks numpy to write `|a|` into `b` and raises `TypeError: return arrays must be of ArrayType`.
- `if diff < worst` starting from `worst = 0` can never grow, so the function always returns `0.0`. That is the most dangerous possible bug here, because `0.0` is precisely the value that makes `Identity test passed: True` print. **A test that can only ever pass is worse than no test.**

## B5. The result

```
x[n] =  2, -1,  3,  1, -2,  0, 0, 0, 0, 0, 0
v[n] =  2,  1,  4,  5,  3,  3, 3, 3, 3, 3, 3      ← running sum of x
y[n] =  2, -1,  3,  1, -2,  0, 0, 0, 0, 0, 0      ← equals x
maximum absolute difference: 0.0
```

`v` is the cumulative sum; differencing it returns `x`. This is the discrete version of the fundamental theorem of calculus. Algebraically, `(h1 * h2)[n] = u[n] − u[n−1] = δ[n]`, so the cascade is the identity and the two systems are inverses under zero initial conditions.

Note that `v[n]` settles to `3 = Σx[k]` and stays there — a running sum of a finite signal is eventually constant at the total. Good quick check that your accumulator is right.

---

# What carries over to the next paper

Five things showed up in both papers and will show up again:

1. **`make_signal(start, values)`** — write it first, every time.
2. **A max-absolute-difference function** returning a number, not a boolean. Every task is graded on that number.
3. **Systems passed as callables** — `system.output` with no parentheses for LTI, a plain `def` for anything else.
4. **`get_value_at_time` / `set_value_at_time`, never `.values[n]`** inside a loop over `times()`. This is the bug in Paper A and it is the easiest one to repeat.
5. **A printed conclusion.** Both papers award marks for it, and both templates ship with it blank.

Recipes: [EXAM_TOOLKIT.md](EXAM_TOOLKIT.md) · Practice: [EXAM_PRACTICE_QUESTIONS.md](EXAM_PRACTICE_QUESTIONS.md)
