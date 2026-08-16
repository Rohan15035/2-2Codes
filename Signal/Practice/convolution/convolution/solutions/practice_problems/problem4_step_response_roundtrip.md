# Practice 4 — Impulse ↔ Step Response Round Trip

**File:** `problem4_step_response_roundtrip.py`

## Problem
Starting from a **known** impulse response `h = {1, −2, 3, 1}`:
1. Build the step response `s[n]` (the running sum of `h`) by convolving with a unit step.
2. Recover `h[n]` back by first-differencing `s`.

This is the inverse direction of Problem A.

## The identities
```
s[n] = Σ_{k ≤ n} h[k]  = (h * u)[n]     accumulator / running sum
h[n] = s[n] − s[n−1]                     first difference (undoes the sum)
```
Summation and differencing are inverse operations — differencing a running sum returns
the original sequence.

## How the code solves it
```python
u = unit_step(0, 12)              # u[n] = 1 for n >= 0, within a finite window
s = LTISystem(h).output(u)        # running sum via convolution
h_recovered = first_difference(s) # s[n] - s[n-1]
```
where `first_difference(sig) = sig.add(sig.shift(1).multiply(-1.0))`.

## The finite-step subtlety (important!)
A *finite* window step equals `u[n] − u[n−13]`. So the recovered signal is really
`h[n] − h[n−13]`: a **clean copy of `h` at `n = 0…3`** plus a delayed echo starting at
`n = 13` where the window ends. That is why we compare only over `h`'s support `[0, 3]`,
where the reconstruction is exact. A perfectly clean round trip everywhere would need a
truly infinite step — a real limitation of finite-length signals, worth stating in an exam.

## Expected output
```
Original h[n]: [1.0, -2.0, 3.0, 1.0]
Step response s[n]: [1.0, -1.0, 2.0, 3.0, 3.0, ... 3.0, 2.0, 4.0, 1.0]
Recovered h over its support: [1.0, -2.0, 3.0, 1.0]
Recovered h matches original on [0, 3]: True
```
Notice `s` climbs to the total sum `3` and holds — then wobbles at the far edge where the
window closes.

## Python notes
- `all(condition for n in ...)` returns `True` only if the condition holds for every `n`.
- `sig.shift(1)` is a one-sample delay, i.e. `sig[n−1]`.
