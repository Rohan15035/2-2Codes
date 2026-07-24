"""
Practice Problem 2 — Smoothing filter vs. edge detector.

Two classic FIR filters applied to the same signal:
    - 3-point moving average  h_avg[n] = {1/3, 1/3, 1/3}   -> SMOOTHS the signal
    - first difference        h_diff[n] = {1, -1}          -> detects EDGES/jumps

Input is a step-like signal with one spike:
    x[n] = 0,0, 1,1,1, 5, 1,1,1, 0,0     (the 5 is a spike; the 0->1 is an edge)

We convolve x with each filter and read off what each does.
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


def show(sig, name):
    print(f"{name}: " + ", ".join(f"{v:+.3f}" for v in sig.values))


def main():
    x = make_signal(0, [0, 0, 1, 1, 1, 5, 1, 1, 1, 0, 0])

    # Moving-average smoother: h_avg = 1/3 for three taps.
    h_avg = make_signal(0, [1 / 3, 1 / 3, 1 / 3])
    y_smooth = LTISystem(h_avg).output(x)

    # First-difference edge detector: h_diff = {1, -1} => y[n] = x[n] - x[n-1].
    h_diff = make_signal(0, [1, -1])
    y_edge = LTISystem(h_diff).output(x)

    show(x, "x[n]       ")
    show(y_smooth, "smoothed   ")   # spike gets spread out and lowered
    show(y_edge, "edges (dx) ")     # nonzero only where x changes

    # The edge detector is nonzero exactly at the rising/falling transitions.
    edges = [n for n in y_edge.times()
             if abs(y_edge.get_value_at_time(n)) > 1e-9]
    print("Transition indices detected:", edges)


if __name__ == "__main__":
    main()
