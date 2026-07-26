import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from signal_lti import DiscreteSignal, LTISystem

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





def echo_response(gain, delay):
    """h[n] = δ[n] + gain·δ[n - delay], as a DiscreteSignal on [0, delay]."""
    h = DiscreteSignal(0, delay)
    h.set_value_at_time(0, 1.0)          # the original
    h.set_value_at_time(delay, gain)     # the echo
    return h


order_ab = LTISystem(h2).output(LTISystem(h1).output(x))   # (x*h1)*h2
order_ba = LTISystem(h1).output(LTISystem(h2).output(x))   # (x*h2)*h1

# Combined single system: h_comb = h1 * h2
h_comb = LTISystem(h1).output(h2)
combined = LTISystem(h_comb).output(x)                     # x*(h1*h2)

def time_reverse(sig):
    """Return g[n] = sig[-n]. Index n maps to -n, so the range flips sign."""
    g = DiscreteSignal(-sig.end_time, -sig.start_time)
    for n in sig.times():
        g.set_value_at_time(-n, sig.get_value_at_time(n))
    return g


def first_difference(sig):
    """y[n] = x[n] - x[n-1], using only signal operations."""
    return sig.add(sig.shift(1).multiply(-1))