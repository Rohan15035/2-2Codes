# Practice 3 — Echo Systems & Commutativity

**File:** `problem3_echo_and_commutativity.py`

## Problem
1. Apply a single **echo** system `h[n] = δ[n] + 0.5·δ[n−3]` to `x = {1, 2, 3}`.
2. Cascade two different echoes and show the order doesn't matter:
   `(x*h1)*h2 == (x*h2)*h1 == x*(h1*h2)`.

## The idea
An echo response is the original impulse (`δ[n]`) plus a delayed, scaled copy
(`gain·δ[n−delay]`). Convolving with it copies the input, then adds a quieter, delayed copy.

Two fundamental laws of convolution:
- **Commutative:** `a * b = b * a` → cascading systems in either order gives the same output.
- **Associative:** `(x*h1)*h2 = x*(h1*h2)` → a chain of systems equals one combined system
  whose impulse response is the convolution of the individual ones.

## How the code solves it
```python
def echo_response(gain, delay):
    h = DiscreteSignal(0, delay)
    h.set_value_at_time(0, 1.0)        # original
    h.set_value_at_time(delay, gain)   # echo
    return h
```
Then it convolves in both orders and also builds the single combined system
`h_comb = LTISystem(h1).output(h2)` (convolving one impulse response with the other), and
checks all three outputs are identical.

## Expected output
```
echo out : [1.0, 2.0, 3.0, 0.5, 1.0, 1.5]      # original, then half-strength echo at n=3
Cascade order (h1 then h2): [1.0, 2.0, 3.25, 1.0, 1.75, 1.625, 0.25, 0.375]
Cascade order (h2 then h1): [1.0, 2.0, 3.25, 1.0, 1.75, 1.625, 0.25, 0.375]
Single combined system    : [1.0, 2.0, 3.25, 1.0, 1.75, 1.625, 0.25, 0.375]
All three equal: True
```

## Python notes
- Building `h` with explicit `DiscreteSignal(0, delay)` reserves indices `0…delay`; only
  two are set, the rest stay `0`.
- Passing an impulse response *as if it were an input* (`LTISystem(h1).output(h2)`) is the
  clean way to convolve two `h`'s — convolution treats both operands the same.
