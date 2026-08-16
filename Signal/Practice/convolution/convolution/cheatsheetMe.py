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



 energy = float(np.sum(t.values ** 2))
DELTA = make_signal(0, [1.0])

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

def unit_step(start_time, end_time):
    """u[n] = 1 for n >= 0 (within the finite window [start_time, end_time])."""
    u = DiscreteSignal(start_time, end_time)
    for n in range(start_time, end_time + 1):
        u.set_value_at_time(n, 1.0 if n >= 0 else 0.0)
    return u

def test_causality(apply_system, probe_signal, n0):
    """Largest |y[n]| at any n < n0. Zero => no output before the input starts."""
    y = apply_system(probe_signal)
    leaks = [abs(y.get_value_at_time(n)) for n in range(y.start_time, n0)]
    return max(leaks) if leaks else 0.0

def absolute_sum(impulse_response):
    """Sum |h[n]|.  Finite => BIBO stable."""
    total = 0.0
    for n in impulse_response.times():
        total += abs(impulse_response.get_value_at_time(n))
    return total

def system_p(sig):
    """y[n] = x[n]^2."""
    out = DiscreteSignal(sig.start_time, sig.end_time)
    for n in sig.times():
        v = sig.get_value_at_time(n)
        out.set_value_at_time(n, v * v)
    return out

def system_r(sig):
    """y[n] = 2*x[n] + 1."""
    out = DiscreteSignal(sig.start_time, sig.end_time)
    for n in sig.times():
        out.set_value_at_time(n, 2 * sig.get_value_at_time(n) + 1)
    return out


def block_diagram_response(h1, h2, h3):
    """Two parallel branches (h1, h2) summed, then cascaded into h3."""
    return convolve(h1.add(h2), h3)


def cross_correlate(x, template):
    """r[n] = sum_k x[k]*t[k-n] = (x * reverse(t))[n]."""
    return LTISystem(reverse(template)).output(x)


def peak_index(sig):
    """Time index of the largest-magnitude sample."""
    return int(sig.times()[np.argmax(np.abs(sig.values))])