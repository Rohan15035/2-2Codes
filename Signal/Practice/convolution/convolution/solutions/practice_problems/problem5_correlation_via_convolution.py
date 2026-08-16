"""
Practice Problem 5 — Cross-correlation using convolution.

Cross-correlation measures how much one signal resembles a shifted copy of another.
It is closely related to convolution:
        corr_xy[n] = Σ_k x[k]·y[k - n]  =  ( x  *  y_reversed )[n]
where y_reversed[n] = y[-n] is y flipped in time.

So we can reuse the SAME LTISystem convolution machinery to compute correlation:
just time-reverse one signal first. We use correlation to locate a short pattern
inside a longer signal (the correlation peaks where the pattern best lines up).
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


def time_reverse(sig):
    """Return g[n] = sig[-n]. Index n maps to -n, so the range flips sign."""
    g = DiscreteSignal(-sig.end_time, -sig.start_time)
    for n in sig.times():
        g.set_value_at_time(-n, sig.get_value_at_time(n))
    return g


def cross_correlation(x, pattern):
    """corr[n] = (x * reverse(pattern))[n], via the LTI convolution."""
    return LTISystem(time_reverse(pattern)).output(x)


def main():
    # A longer signal containing the pattern {1, 2, 1} around n = 4..6.
    x = make_signal(0, [0, 0, 0, 0, 1, 2, 1, 0, 0, 0])
    pattern = make_signal(0, [1, 2, 1])

    corr = cross_correlation(x, pattern)

    print("x[n]     :", list(x.values))
    print("pattern  :", list(pattern.values))
    print("corr[n]  :", [round(v, 4) for v in corr.values],
          "over", list(corr.times()))

    # The correlation is largest at the lag where the pattern best aligns.
    best_n = max(corr.times(), key=lambda n: corr.get_value_at_time(n))
    print("Peak correlation at lag n =", int(best_n),
          "value =", round(corr.get_value_at_time(best_n), 4))
    print("Interpretation: the pattern's start best lines up with x at index",
          int(best_n), "(matching where {1,2,1} sits in x).")


if __name__ == "__main__":
    main()
