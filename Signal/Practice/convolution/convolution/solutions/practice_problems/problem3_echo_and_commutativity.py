"""
Practice Problem 3 — Echo systems and commutativity of convolution.

An "echo" system adds a delayed, quieter copy of the input:
    h_echo[n] = δ[n] + a·δ[n - D]     (original + gain a, delayed by D)

Task 1: apply a single echo (a = 0.5, D = 3) to a short signal.
Task 2: cascade TWO different echoes and show the order does not matter:
        (x * h1) * h2  ==  (x * h2) * h1  ==  x * (h1 * h2)
This demonstrates convolution is COMMUTATIVE and ASSOCIATIVE.
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


def echo_response(gain, delay):
    """h[n] = δ[n] + gain·δ[n - delay], as a DiscreteSignal on [0, delay]."""
    h = DiscreteSignal(0, delay)
    h.set_value_at_time(0, 1.0)          # the original
    h.set_value_at_time(delay, gain)     # the echo
    return h


def max_abs_difference(a, b):
    n_min = min(a.start_time, b.start_time)
    n_max = max(a.end_time, b.end_time)
    return max(abs(a.get_value_at_time(n) - b.get_value_at_time(n))
               for n in range(n_min, n_max + 1))


def main():
    x = make_signal(0, [1, 2, 3])

    # ---- Task 1: single echo, gain 0.5, delay 3 ----
    h1 = echo_response(0.5, 3)
    y1 = LTISystem(h1).output(x)
    print("x[n]      :", list(x.values), "over", list(x.times()))
    print("echo out  :", [round(v, 4) for v in y1.values], "over", list(y1.times()))
    # You should see the original {1,2,3} then the half-strength echo {0.5,1,1.5}
    # starting 3 samples later.

    # ---- Task 2: two echoes in cascade, in both orders ----
    h2 = echo_response(0.25, 2)

    order_ab = LTISystem(h2).output(LTISystem(h1).output(x))   # (x*h1)*h2
    order_ba = LTISystem(h1).output(LTISystem(h2).output(x))   # (x*h2)*h1

    # Combined single system: h_comb = h1 * h2
    h_comb = LTISystem(h1).output(h2)
    combined = LTISystem(h_comb).output(x)                     # x*(h1*h2)

    print("\nCascade order (h1 then h2):", [round(v, 4) for v in order_ab.values])
    print("Cascade order (h2 then h1):", [round(v, 4) for v in order_ba.values])
    print("Single combined system    :", [round(v, 4) for v in combined.values])
    print("All three equal:",
          max_abs_difference(order_ab, order_ba) < 1e-9 and
          max_abs_difference(order_ab, combined) < 1e-9)


if __name__ == "__main__":
    main()
