"""
Practice Problem 4 — Impulse response <-> step response round trip.

Relationship between an impulse response h[n] and its step response s[n]:
    s[n] = Σ_{k ≤ n} h[k]        (running sum / accumulator)  ==  h * u
    h[n] = s[n] - s[n-1]         (first difference)           <- inverse of the sum

This is the SAME identity used in Problem A, but here we go the OTHER direction:
start from a KNOWN h[n], build s[n] by convolving with a unit step, then recover
h[n] back by first-differencing s[n]. We should land exactly on the original h.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from signal_lti import DiscreteSignal, LTISystem


def make_signal(start_time, values):
    sig = DiscreteSignal(start_time, start_time + len(values) - 1)
    for i, v in enumerate(values):
        sig.set_value_at_time(start_time + i, float(v))
    return sig


def unit_step(start_time, end_time):
    """u[n] = 1 for n >= 0 (within the finite window [start_time, end_time])."""
    u = DiscreteSignal(start_time, end_time)
    for n in range(start_time, end_time + 1):
        u.set_value_at_time(n, 1.0 if n >= 0 else 0.0)
    return u


def first_difference(sig):
    """sig[n] - sig[n-1] using only Signal operations."""
    return sig.add(sig.shift(1).multiply(-1.0))


def main():
    # A known impulse response.
    h = make_signal(0, [1, -2, 3, 1])

    # ---- Build the step response s = h * u ----
    # The unit step must be long enough to cover the accumulation window.
    u = unit_step(0, 12)
    s = LTISystem(h).output(u)

    # ---- Recover the impulse response by first-differencing s ----
    h_recovered = first_difference(s)

    print("Original h[n]:", [round(v, 4) for v in h.values],
          "over", list(h.times()))
    print("Step response s[n] (windowed running sum):",
          [round(v, 4) for v in s.values])

    # Compare h_recovered with h over h's own support [0, 3].
    # NOTE: a FINITE step u[0..12] = u[n] - u[n-13], so the recovered signal is
    #   h[n] - h[n-13]: a clean copy of h at n=0..3 plus a delayed echo at n>=13.
    # Within h's support the reconstruction is exact; the echo only appears where
    # the finite window ends (this is why a true accumulator needs an infinite step).
    ok = all(abs(h.get_value_at_time(n) - h_recovered.get_value_at_time(n)) < 1e-9
             for n in h.times())
    print("Recovered h over its support:",
          [round(h_recovered.get_value_at_time(n), 4) for n in h.times()])
    print("Recovered h matches original on [0, 3]:", ok)


if __name__ == "__main__":
    main()
