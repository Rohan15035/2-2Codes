"""
Practice Problem 1 — Basic convolution ("flip and slide").

Given two finite sequences
    x[n] = {1, 2, 3}  starting at n = 0
    h[n] = {1, 1, 1}  starting at n = 0   (a length-3 running sum)
compute y[n] = (x * h)[n] two ways and confirm they agree:
    (a) LTISystem.output(x)          -- the library's convolution sum
    (b) a hand-written convolution   -- to see exactly what the sum does

Convolution sum:   y[n] = Σ_k  x[k] · h[n - k]
Output support:    x on [a,b], h on [c,d]  ->  y on [a+c, b+d].
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from signal_lti import DiscreteSignal, LTISystem


def make_signal(start_time, values):
    """Build a DiscreteSignal starting at `start_time` from a list of values."""
    sig = DiscreteSignal(start_time, start_time + len(values) - 1)
    for i, v in enumerate(values):
        sig.set_value_at_time(start_time + i, float(v))
    return sig


def manual_convolution(x, h):
    """Compute y = x * h directly from the definition, by hand."""
    n_min = x.start_time + h.start_time
    n_max = x.end_time + h.end_time
    y = DiscreteSignal(n_min, n_max)
    for n in range(n_min, n_max + 1):
        total = 0.0
        for k in range(x.start_time, x.end_time + 1):
            total += x.get_value_at_time(k) * h.get_value_at_time(n - k)
        y.set_value_at_time(n, total)
    return y


def main():
    x = make_signal(0, [1, 2, 3])
    h = make_signal(0, [1, 1, 1])

    y_lib = LTISystem(h).output(x)      # library convolution
    y_manual = manual_convolution(x, h)  # hand-written convolution

    print("x[n]:", list(x.values), "over", list(x.times()))
    print("h[n]:", list(h.values), "over", list(h.times()))
    print("y[n] (library):", [round(v, 4) for v in y_lib.values])
    print("y[n] (manual): ", [round(v, 4) for v in y_manual.values])

    diff = max(abs(y_lib.get_value_at_time(n) - y_manual.get_value_at_time(n))
               for n in range(y_lib.start_time, y_lib.end_time + 1))
    print("Match:", diff < 1e-9)
    # Expected y = {1, 3, 6, 5, 3}: partial then full then trailing sums.


if __name__ == "__main__":
    main()
