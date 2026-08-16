# Code Walkthrough — what was added to `fs_redrawer.py`

*Line-by-line explanation of the pruning code, written for someone who knows the
maths but not every Python/NumPy idiom. For the theory behind it, see
[harmonic_pruning_explained.md](harmonic_pruning_explained.md).*

---

## Overview: four additions

| # | Where | What |
|---|---|---|
| 1 | end of `calculate_all_coefficients` | save a backup copy of the full spectrum |
| 2 | new method | `prune_harmonics_by_energy(r)` — **Task 1** |
| 3 | new method | `evaluate_reconstruction_error()` — **Task 2** |
| 4 | `if __name__ == "__main__":` | the four-ratio loop, the table, the plots |

Everything above the class (`calculate_cn`, `approximate`, …) is unchanged from
the offline assignment.

---

## 1. The backup copy

```python
        # Pristine snapshot of the full 2N+1 spectrum. Pruning is destructive
        # (it zeroes coefficients in self.coeffs), so keeping the originals
        # here lets prune_harmonics_by_energy() be called repeatedly with
        # different target ratios without recomputing every integral.
        self.full_coeffs = dict(self.coeffs)
```

**The problem it solves.** Pruning *destroys* data — it replaces coefficients
with zero. After pruning to r = 0.96, only 2 of the 301 coefficients still exist;
the other 299 are gone. If the next loop iteration (r = 0.98) then tried to rank
harmonics, it would be ranking a spectrum that is 99% zeros and would produce
nonsense.

So we keep two dictionaries:

- `self.full_coeffs` — the **truth**, computed once, never modified.
- `self.coeffs` — the **current working version**, freely overwritten by pruning.

**Syntax note.** `dict(x)` makes a *copy* of dictionary `x`. Without the copy,
`self.full_coeffs = self.coeffs` would just be a second name for the *same*
dictionary, and zeroing one would zero the other — the classic Python
reference-vs-copy trap.

---

## 2. `prune_harmonics_by_energy` — Task 1

### 2a. Check the input

```python
        r = float(energy_ratio)
        if r <= 0.0 or r > 1.0:
            raise ValueError("energy_ratio must be in (0, 1]")
```

`r` is a *fraction of the total energy*, so it only makes sense in (0, 1].
r = 0 would mean "keep enough harmonics to have 0% of the energy" — answer: none,
which is useless. r > 1 is impossible to satisfy. Crashing with a clear message
beats returning silent garbage.

### 2b. Start from the backup

```python
        # Always start from the untouched spectrum, never from an
        # already-pruned one.
        source = self.full_coeffs
```

`source` is just a short name for the backup. Everything below reads from
`source` and writes to `self.coeffs`, so each call is independent of the previous
one. This is what lets the main loop run all four ratios on one object.

### 2c. Compute each harmonic's energy

```python
        # Step 1: energy of every harmonic, E_n = |c_n|^2, and their sum.
        energies = {}
        total = 0.0
        for n in source:
            energies[n] = abs(source[n]) ** 2
            total += energies[n]
```

Builds a second dictionary, `energies`, that mirrors the coefficient dictionary
but stores a **real number** per harmonic instead of a complex one:

```
source  = { -150: (-0.0000+0.0000j), ..., -1: (0.31+0.71j), ... }   complex
energies= { -150:  8.9e-10,          ..., -1:  0.599,       ... }   real
```

**Syntax notes.**

- `for n in source:` loops over a dictionary's **keys** (here, the harmonic
  numbers −150 … 150). To get the value you write `source[n]`.
- `abs()` on a *complex* number returns its **modulus** `√(re² + im²)`, not a sign
  flip. So `abs(source[n]) ** 2` is exactly `|c_n|²`.
- `total += x` is shorthand for `total = total + x`.

**The concept.** `E_n = |c_n|²` is the energy carried by harmonic *n*. Parseval's
theorem guarantees these add up to the signal's true energy:
`Σ|c_n|² = (1/T)∫|f(t)|²dt`. Because the Fourier basis is **orthogonal**, there
are no cross terms — each harmonic owns an independent slice of the budget. That
is the only reason a per-harmonic "importance score" is meaningful at all.

### 2d. Guard against an all-zero signal

```python
        if total == 0.0:            # all-zero signal: nothing worth keeping
            self.coeffs = {}
            for n in source:
                self.coeffs[n] = 0j
            return 0, 0.0
```

If the signal is identically zero, `total` is 0 and the final
`kept_energy / total` would crash with a division by zero. This never happens for
a real drawing, but the guard makes the method safe to call on anything.

### 2e. Rank by energy, biggest first

```python
        # Step 2: list the harmonics with the most energetic one first.
        ranked = sorted(energies, key=lambda n: energies[n], reverse=True)
```

`ranked` is a plain list of harmonic numbers, ordered from most to least
energetic. For the heart it begins:

```
[-1, 2, -3, -2, -4, 1, 0, 4, 3, 6, -6, ...]
```

**Syntax note — how to read this line.** `sorted(energies, ...)` sorts the
dictionary's **keys**. Normally that would sort them numerically (−150, −149, …).
The `key=` argument overrides that: *"don't compare the harmonic numbers
themselves — compare `energies[n]`, the energy of each."* The `lambda n: ...` is
just a throwaway one-line function meaning "given `n`, give back `energies[n]`".
`reverse=True` flips it to descending.

Read the whole line as: **order the harmonic numbers by their energy, largest
first.**

**The concept.** Note that positive and negative harmonics compete in one shared
ranking — `n = −1` and `n = +1` are separate entries and are kept or dropped
independently. For the heart, `−1` is ranked first (94.3% of all energy) while
`+1` only appears sixth. That asymmetry is real: our signal is complex, so
`c_{-n}` is *not* the conjugate of `c_n` and carries genuinely different
information.

### 2f. Collect harmonics until the target is met

```python
        # Step 3: walk down that list, keeping harmonics until the energy
        # collected reaches the target. If round-off keeps the running sum a
        # hair below the target (possible when r == 1.0), the loop simply
        # runs out of harmonics and every one of them is kept.
        target = r * total
        kept = []
        kept_energy = 0.0
        for n in ranked:
            kept.append(n)
            kept_energy += energies[n]
            if kept_energy >= target:
                break
```

This is the heart of the algorithm, and it is deliberately boring: take the next
most energetic harmonic, add its energy to a running total, stop as soon as
you have enough.

**Dry run for r = 0.96** (real numbers from the heart):

```
total  = 0.6353371
target = 0.96 × 0.6353371 = 0.6099236

iteration 1:  n = -1   kept_energy = 0.5990179    0.5990179 >= 0.6099236 ?  No  -> continue
iteration 2:  n =  2   kept_energy = 0.6100016    0.6100016 >= 0.6099236 ?  Yes -> break

kept = [-1, 2]     ->  retained = 2
actual ratio = 0.6100016 / 0.6353371 = 0.960123
```

Two harmonics out of 301. Notice the achieved ratio (0.9601) **overshoots** the
target (0.96) — energy arrives in discrete lumps, so you land on or above the
target, never exactly on it.

**Why this loop is the optimal answer, not a guess.** Because the harmonics are
orthogonal, the squared error caused by deleting a set of them equals the sum of
their energies. Minimising error for a given number of kept harmonics therefore
means maximising kept energy, which means keeping the biggest ones. Greedy is
provably optimal here — no clever search is needed, sorting *is* the optimisation.

**The r = 1.00 subtlety (worth knowing).** When r = 1.0, `target` equals the total
energy — and floating-point addition is not perfectly associative, so the running
`kept_energy` can end a few bits *below* `total` even after adding everything. In
that case `kept_energy >= target` never becomes true, the `break` never fires, and
the loop simply ends after visiting all 301 harmonics — leaving `kept` with all of
them, which is the correct answer. The naive loop handles this for free; an
index-based binary search would need an explicit off-by-one fix.

### 2g. Write the result back

```python
        # Step 4: zero everything, then write the survivors back unchanged.
        self.coeffs = {}
        for n in source:
            self.coeffs[n] = 0j          # 0j is just complex zero
        for n in kept:
            self.coeffs[n] = source[n]

        return len(kept), kept_energy / total
```

Two passes: fill the dictionary entirely with zeros, then overwrite the survivors
with their original values.

- **Why keep all 301 keys** instead of storing only the survivors? Because
  `approximate()` and the provided animation code loop over `self.coeffs` and
  expect the full harmonic range. A zero coefficient contributes
  `0 · e^(jnωt) = 0`, so it is mathematically identical to being absent — and the
  spec explicitly says discarded coefficients should be *set to zero*.
- **Survivors are copied verbatim** — pruning deletes terms, it never rescales
  the ones it keeps. Their coefficients are still the correct Fourier
  coefficients of the original signal.

**Syntax notes.** `0j` is Python's literal for complex zero (`0 + 0i`);
writing plain `0` would make the dictionary mix ints and complex numbers.
`return len(kept), kept_energy / total` returns **two values at once** as a tuple,
which the caller unpacks with `retained, actual_ratio = fs.prune_...`.

---

## 3. `evaluate_reconstruction_error` — Task 2

```python
        f_hat = self.approximate(self.t)
        squared_errors = np.abs(self.signal - f_hat) ** 2
        return float(np.mean(squared_errors))
```

Three lines, one per symbol in the formula:

```
MSE = (1/M) · Σᵢ |f(tᵢ) − f̂(tᵢ)|²
```

1. `self.approximate(self.t)` rebuilds the curve at all 1000 sample times **from
   whatever is currently in `self.coeffs`**. That coupling is deliberate: call
   this *after* pruning and you measure the *pruned* reconstruction.
2. `self.signal - f_hat` subtracts the two 1000-element complex arrays elementwise
   — NumPy does the loop for you. `np.abs(...)` then gives the modulus of each
   complex difference, and `** 2` squares it. Since
   `|Δ|² = Δx² + Δy²`, a single number captures the error in **both** coordinates
   at that point.
3. `np.mean(...)` averages the 1000 values; `float(...)` converts NumPy's scalar
   into an ordinary Python number for clean printing.

**The concept — why MSE pairs so neatly with energy.** The difference between the
true signal and the pruned one is *literally the deleted harmonics*:

```
f(t) − f̂(t) = Σ_{n discarded} c_n · e^(jnωt)
```

Apply Parseval to that residual and you get

```
MSE = Σ_{n discarded} |c_n|²  =  (1 − r) · E_total
```

**The error equals the energy you threw away.** Your run confirms it: at r = 0.99
the measured MSE is `4.7005e-03` and `(1 − 0.992609) × 0.6353371 = 4.6959e-03` —
agreeing to 0.1%. (The tiny gap is because the code averages 1000 discrete
samples while the identity is a continuous time-average.)

This is what makes `r` a *guarantee* rather than a tuning knob: choosing the
energy ratio is directly choosing the error budget.

---

## 4. The main block

```python
    TARGET_RATIOS = [0.96, 0.98, 0.99, 1.00]

    t, z = load_svg_path(svg_path, num_points=1000)
    fs = FourierEpicycles(t, z, n_harmonics=N_HARMONICS)
    fs.calculate_all_coefficients()

    print("Target Ratio | Harmonics Retained | Actual Energy Ratio | MSE")
    print("-" * 66)

    saved = []
    for r in TARGET_RATIOS:
        retained, actual_ratio = fs.prune_harmonics_by_energy(r)
        mse = fs.evaluate_reconstruction_error()

        print(f"{r:12.2f} | {retained:18d} | {actual_ratio:19.4f} | {mse:.6e}")

        fig, ax = plt.subplots(figsize=(5, 5))
        plot_comparison(fs, z, ax=ax)
        ax.get_lines()[1].set_label(f"Reconstruction ({retained} harmonics)")
        ax.legend(loc="upper right")
        ax.set_title(...)
        out_path = f"{stem}_pruned_{r:.2f}.png"
        fig.savefig(out_path, dpi=120)
        plt.close(fig)
        saved.append(out_path)
```

Things worth noticing:

- **The 301 integrals run once**, before the loop. Pruning is pure bookkeeping on
  numbers already computed — it never touches `calculate_cn` again. That is only
  possible because of the backup copy from §1.
- **Order matters inside the loop:** prune first, *then* evaluate. The error
  function reads the current `self.coeffs`, so swapping the two lines would
  measure the previous iteration's reconstruction.
- **`ax.get_lines()[1]`** grabs the second line drawn on the plot (index 0 is the
  grey original, index 1 is the crimson reconstruction) so its legend label can be
  corrected. The provided `plot_comparison` hardcodes `N=150`, which is misleading
  once only 6 harmonics are non-zero — and `epicycle_animation.py` is provided
  code we should not edit, so we fix the label from outside instead.
- **`plt.close(fig)`** releases each figure; without it matplotlib keeps every
  figure in memory and warns after a while.

**Syntax note on the f-strings.** In `f"{r:12.2f}"` the part after the colon is a
format spec: `12` = pad to 12 characters wide (keeps the table columns aligned),
`.2f` = 2 decimal places. Similarly `{retained:18d}` means "an integer, 18 wide",
and `{mse:.6e}` means "scientific notation, 6 decimals" — which is why the MSE
prints as `2.545104e-02`. `f"{stem}_pruned_{r:.2f}.png"` uses the same trick to
produce `heart_pruned_1.00.png` rather than Python's default `1.0`.

---

## 5. Python/NumPy idioms used, in one table

| Code | Meaning |
|---|---|
| `dict(x)` | make a copy of dictionary `x` (not a second name for it) |
| `for n in some_dict:` | loop over the dictionary's **keys** |
| `abs(c)` where `c` is complex | modulus `√(re² + im²)` |
| `total += x` | `total = total + x` |
| `sorted(d, key=lambda n: d[n], reverse=True)` | sort keys by their value, biggest first |
| `lambda n: expr` | a small unnamed function of `n` |
| `list.append(x)` | add `x` to the end of a list |
| `break` | leave the loop immediately |
| `0j` | complex zero |
| `return a, b` | return two values; caller writes `x, y = f()` |
| `np.abs(arr)` | modulus of *every* element, no loop needed |
| `np.mean(arr)` | average of all elements |
| `f"{x:8.3f}"` | format `x` as a float, width 8, 3 decimals |

---

## 6. Sanity checks that were run

The implementation was verified independently (not just by eyeballing the table).
For every ratio it confirms:

1. the reported count equals the actual number of non-zero coefficients;
2. the reported ratio matches an independent recomputation of kept ÷ total;
3. the achieved ratio really does meet the target;
4. **minimality** — removing the weakest kept harmonic drops below the target, so
   no smaller set would have worked;
5. the kept set is exactly the top-k by `|c_n|`;
6. kept coefficients are bit-identical to the originals, all others exactly zero;
7. the MSE matches a from-scratch recomputation;
8. pruning loosely *after* pruning aggressively restores the full spectrum
   (proving the backup copy works);
9. invalid ratios (0, −0.1, 1.5) raise `ValueError`.

All pass.

---

## 7. Results this code produces

```
Target Ratio | Harmonics Retained | Actual Energy Ratio | MSE
------------------------------------------------------------------
        0.96 |                  2 |              0.9601 | 2.545104e-02
        0.98 |                  4 |              0.9828 | 1.094460e-02
        0.99 |                  6 |              0.9926 | 4.700460e-03
        1.00 |                301 |              1.0000 | 5.781795e-08
```

Plus `heart_pruned_0.96.png`, `heart_pruned_0.98.png`, `heart_pruned_0.99.png`,
`heart_pruned_1.00.png`.

**One caveat for the report:** the r = 1.00 row is *not* a pruning result —
nothing was discarded, so its `5.78e-08` is the leftover error of truncating the
series at N = 150 (energy living beyond harmonic 150) plus numerical integration
error. It is the noise floor the other three rows sit on top of.
