"""
Minimal reference solutions for the 8 practice questions in EXAM_PRACTICE_QUESTIONS.md.

Each question gets the smallest set of functions that answers it, plus a qN()
runner that prints the numbers from the answer key.

Run all:      python practice_solutions.py
Run one:      python practice_solutions.py 5

In the real exam you must paste DiscreteSignal / LTISystem into your own file.
Here they are imported to keep this file short.
"""

import numpy as np

from signal_lti import DiscreteSignal, LTISystem


# =============================================================================
# Shared helpers -- write these first in any exam.
# =============================================================================

def make_signal(start, values):
    """Build a DiscreteSignal from a list, starting at index `start`."""
    sig = DiscreteSignal(start, start + len(values) - 1)
    for i, v in enumerate(values):
        sig.set_value_at_time(start + i, float(v))
    return sig


def from_dict(start, end, table):
    """Sparse build: only the listed {index: value} pairs are nonzero."""
    sig = DiscreteSignal(start, end)
    for t, v in table.items():
        sig.set_value_at_time(t, float(v))
    return sig


def show(sig, name=""):
    print(f"{name:26s} n={sig.start_time}..{sig.end_time}  {np.round(sig.values, 6).tolist()}")


def max_abs_diff_in_range(s1, s2, start, end):
    """Largest |s1[n] - s2[n]| for start <= n <= end."""
    worst = 0.0
    for n in range(start, end + 1):
        d = abs(s1.get_value_at_time(n) - s2.get_value_at_time(n))
        if d > worst:
            worst = d
    return worst


def max_abs_diff(s1, s2):
    """Same, over the UNION of both supports."""
    return max_abs_diff_in_range(
        s1, s2,
        min(s1.start_time, s2.start_time),
        max(s1.end_time, s2.end_time),
    )


def convolve(sig_a, sig_b):
    """a * b, using LTISystem as a convolution engine (no numpy.convolve)."""
    return LTISystem(sig_a).output(sig_b)


def reverse(sig):
    """y[n] = x[-n].  NOTE: the range flips to [-end, -start]."""
    out = DiscreteSignal(-sig.end_time, -sig.start_time)
    for n in sig.times():
        out.set_value_at_time(-n, sig.get_value_at_time(n))
    return out


def first_difference(sig):
    """y[n] = x[n] - x[n-1], using only signal operations."""
    return sig.add(sig.shift(1).multiply(-1))


DELTA = make_signal(0, [1.0])


# =============================================================================
# Q1 -- Causality and BIBO stability as generic tests
# =============================================================================

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


def system_c(input_signal):
    """y[n] = x[n+1] -- a one-step advance (non-causal)."""
    return input_signal.shift(-1)


def q1():
    h_a = make_signal(0, [1, 0.5, 0.25])
    h_b = make_signal(-1, [0.5, 1, 0.5])
    probe = make_signal(0, [1, 2, -1])          # zero for n < 0

    print(f"leak A (h starts at 0)  : {test_causality(LTISystem(h_a).output, probe, 0)}")
    print(f"leak B (h starts at -1) : {test_causality(LTISystem(h_b).output, probe, 0)}")
    print(f"leak C (advance)        : {test_causality(system_c, probe, 0)}")
    print(f"sum|h_A| = {absolute_sum(h_a)}   sum|h_B| = {absolute_sum(h_b)}")
    print("Conclusion: only System A is causal. An LTI system is causal iff "
          "h.start_time >= 0; h_B has a sample at n=-1 and C reads x[n+1], so both\n"
          "            produce output before the input starts. Both are BIBO stable "
          "(finite sum|h|), so causality and stability are independent properties.")


# =============================================================================
# Q2 -- The non-LTI zoo: which property fails
# =============================================================================

def test_linearity(apply_system, x1, x2, a, b):
    """max| S{a*x1 + b*x2} - (a*S{x1} + b*S{x2}) |.  Works for ANY callable."""
    lhs = apply_system(x1.multiply(a).add(x2.multiply(b)))
    rhs = apply_system(x1).multiply(a).add(apply_system(x2).multiply(b))
    return max_abs_diff(lhs, rhs)


def test_time_invariance(apply_system, x, k):
    """max| S{x[n-k]} - y[n-k] |: shift-then-apply vs apply-then-shift."""
    return max_abs_diff(apply_system(x.shift(k)), apply_system(x).shift(k))


def system_p(sig):
    """y[n] = x[n]^2."""
    out = DiscreteSignal(sig.start_time, sig.end_time)
    for n in sig.times():
        v = sig.get_value_at_time(n)
        out.set_value_at_time(n, v * v)
    return out


def system_q(sig):
    """y[n] = x[-n].  Output range is [-end, -start], NOT [start, end]."""
    return reverse(sig)


def system_r(sig):
    """y[n] = 2*x[n] + 1."""
    out = DiscreteSignal(sig.start_time, sig.end_time)
    for n in sig.times():
        out.set_value_at_time(n, 2 * sig.get_value_at_time(n) + 1)
    return out


def q2():
    x1 = make_signal(-2, [1, 0, 2, -1, 3])
    x2 = make_signal(-1, [2, -3, 0, 1, 1])
    a, b, k = 2.0, -3.0, 3

    print(f"{'system':12s}{'linearity':>12s}{'time-inv':>12s}")
    for name, f in [("P square", system_p), ("Q reverse", system_q), ("R 2x+1", system_r)]:
        print(f"{name:12s}{test_linearity(f, x1, x2, a, b):12g}"
              f"{test_time_invariance(f, x1, k):12g}")
    print("Conclusion: P is time-invariant but not linear ((a*x)^2 != a*x^2).")
    print("            Q is linear but not time-invariant (reversal maps a delay to an advance).")
    print("            R is time-invariant but not linear -- the +1 means the zero input")
    print("            does not map to the zero output, so it is affine, not linear.")


# =============================================================================
# Q3 -- Commutativity and associativity
# =============================================================================

def q3():
    h1 = make_signal(0, [1, 0, 0.5])
    h2 = make_signal(0, [1 / 3, 1 / 3, 1 / 3])
    h3 = make_signal(0, [1, -1])

    show(convolve(h1, h2), "h1*h2")
    print(f"commutativity difference : {max_abs_diff(convolve(h1, h2), convolve(h2, h1))}")

    left = convolve(convolve(h1, h2), h3)
    right = convolve(h1, convolve(h2, h3))
    show(left, "(h1*h2)*h3")
    print(f"associativity difference : {max_abs_diff(left, right)}")
    print(f"length check: {len(convolve(h1, h2))} == {len(h1)} + {len(h2)} - 1")
    print("Conclusion: both differences are 0 (up to ~1e-16 rounding), so convolution is")
    print("            commutative and associative -- the ORDER of boxes in a cascade")
    print("            does not change the overall system.")


# =============================================================================
# Q4 -- Parallel branches and distributivity
# =============================================================================

def parallel_response(h1, h2):
    """Equivalent impulse response of two branches driven by the same input."""
    return h1.add(h2)


def q4():
    h1 = make_signal(0, [1, 0, 0.5])
    h2 = make_signal(0, [1 / 3, 1 / 3, 1 / 3])
    x = make_signal(-2, [1, 0, 2, -1, 3])

    h_par = parallel_response(h1, h2)
    show(h_par, "h1+h2")

    via_sum_of_h = LTISystem(h_par).output(x)
    via_sum_of_y = LTISystem(h1).output(x).add(LTISystem(h2).output(x))
    show(via_sum_of_h, "x*(h1+h2)")
    print(f"distributivity difference : {max_abs_diff(via_sum_of_h, via_sum_of_y)}")

    # h2 moved to n=2..4: add() takes the UNION of supports and relies on
    # get_value_at_time returning 0.0 outside each range, so the gap is filled
    # with zeros automatically -- no manual padding anywhere.
    h2_late = make_signal(2, [1 / 3, 1 / 3, 1 / 3])
    show(parallel_response(h1, h2_late), "h1 + h2(shifted)")
    print("Conclusion: x*(h1+h2) = (x*h1) + (x*h2). Parallel branches ADD their")
    print("            impulse responses.")


# =============================================================================
# Q5 -- Echo canceller: inverse system by truncated series
# =============================================================================

def echo_response(alpha, delay):
    """h[n] = delta[n] + alpha*delta[n-D], built from shifted impulses."""
    h = DiscreteSignal(0, delay)
    return h.add(DELTA).add(DELTA.shift(delay).multiply(alpha))


def truncated_inverse(alpha, delay, terms):
    """g[n] = sum_{m=0..M} (-alpha)^m * delta[n - m*D]."""
    g = DiscreteSignal(0, delay * terms)
    for m in range(terms + 1):
        g = g.add(DELTA.shift(delay * m).multiply((-alpha) ** m))
    return g


def q5():
    alpha, delay, terms = 0.6, 3, 4
    obs_start, obs_end = 0, 14
    x = make_signal(0, [2, -1, 3, 1, -2, 0, 4])

    h = echo_response(alpha, delay)
    g = truncated_inverse(alpha, delay, terms)
    show(h, "h (echo)")
    show(g, "g (truncated inverse)")

    eq = convolve(h, g)
    show(eq, "h*g")
    residual_n = (terms + 1) * delay
    print(f"residual sample: n={residual_n}  value={eq.get_value_at_time(residual_n)}"
          f"  (= alpha^{terms + 1})")

    recovered = LTISystem(g).output(LTISystem(h).output(x))
    show(recovered, "recovered x")
    print(f"difference on n={obs_start}..{obs_end} : "
          f"{max_abs_diff_in_range(recovered, x, obs_start, obs_end)}")
    print(f"difference on full range   : {max_abs_diff(recovered, x)}")
    print(f"Conclusion: the series telescopes to h*g = delta[n] + alpha^(M+1)*delta[n-(M+1)D],")
    print(f"            so cancellation is EXACT for n < (M+1)*D = {residual_n}. The full-range")
    print("            difference is the truncation tail, not an error. Raising M shrinks the")
    print("            residual geometrically AND pushes it further out in time.")


# =============================================================================
# Q6 -- Step response <-> impulse response roundtrip
# =============================================================================

def q6():
    h = make_signal(0, [1, 0.5, 0.25])
    u = make_signal(0, [1.0] * 12)

    s = LTISystem(h).output(u)
    show(s, "s = h*u")

    h_rec = first_difference(s)          # s.add(s.shift(1).multiply(-1))
    show(h_rec, "s[n]-s[n-1]")

    print(f"difference on n=0..2     : {max_abs_diff_in_range(h_rec, h, 0, 2)}")
    print(f"difference on full range : {max_abs_diff(h_rec, h)}")
    # The tail at n=12..14 is -h delayed by 12: the stored u[n] stops at n=11, so
    # what was really convolved was the pulse u[n]-u[n-12]. Its rising edge gives
    # +h, its falling edge gives -h.
    print("Conclusion: h[n] = s[n] - s[n-1] and s[n] = sum_{k<=n} h[k]. Accumulation and")
    print("            first differencing are inverse operations; h is recovered exactly")
    print("            on its own support, and the tail is the finite-window artifact.")


# =============================================================================
# Q7 -- Matched filter: detection by time-reversed convolution
# =============================================================================

def cross_correlate(x, template):
    """r[n] = sum_k x[k]*t[k-n] = (x * reverse(t))[n]."""
    return LTISystem(reverse(template)).output(x)


def peak_index(sig):
    """Time index of the largest-magnitude sample."""
    return int(sig.times()[np.argmax(np.abs(sig.values))])


def q7():
    t = make_signal(0, [1, -1, 2])
    x = from_dict(0, 14, {1: 0.5, 4: 1, 5: -1, 6: 2, 9: -0.5, 11: 0.3})
    show(x, "x")

    r = cross_correlate(x, t)
    show(r, "r = x * reverse(t)")

    n_peak = peak_index(r)
    energy = float(np.sum(t.values ** 2))
    print(f"peak index : {n_peak}   peak value : {r.get_value_at_time(n_peak)}")
    print(f"template energy sum t[n]^2 : {energy}")
    # Peak value == template energy: correlation is maximised when the template
    # lines up with an exact copy of itself. Any other lag only partly overlaps.
    print(f"Conclusion: the template occurs at n = {n_peak}, because that is where the")
    print("            correlation peaks, and the peak equals the template energy --")
    print("            the signature of a perfect (unscaled) match.")


# =============================================================================
# Q8 -- Block diagram to a single equivalent system
# =============================================================================

def block_diagram_response(h1, h2, h3):
    """Two parallel branches (h1, h2) summed, then cascaded into h3."""
    return convolve(h1.add(h2), h3)


def q8():
    h1 = make_signal(0, [1, 0, 0.5])
    h2 = make_signal(0, [1 / 3, 1 / 3, 1 / 3])
    h3 = make_signal(0, [1, -1])
    x = make_signal(-2, [1, 0, 2, -1, 3])

    # Route 1: simulate the diagram box by box.
    branch_sum = LTISystem(h1).output(x).add(LTISystem(h2).output(x))
    y_direct = LTISystem(h3).output(branch_sum)

    # Route 2: collapse the diagram first, then one convolution.
    h_eq = block_diagram_response(h1, h2, h3)
    y_equiv = LTISystem(h_eq).output(x)

    show(h_eq, "h_eq = (h1+h2)*h3")
    show(y_direct, "y (box by box)")
    print(f"difference between routes : {max_abs_diff(y_direct, y_equiv)}")
    # Predicted range: h1+h2 spans 0..2, *h3 (0..1) -> h_eq on 0..3,
    # *x (-2..2) -> y on -2..5, i.e. 5 + 4 - 1 = 8 samples.
    print(f"predicted y range -2..5, actual {y_direct.start_time}..{y_direct.end_time}")
    print("Conclusion: ((x*h1) + (x*h2))*h3 = x*((h1+h2)*h3). Parallel branches add their")
    print("            impulse responses, cascaded blocks convolve theirs -- so any")
    print("            feedback-free diagram collapses to one equivalent h.")


# =============================================================================

QUESTIONS = {
    1: ("Causality & BIBO stability", q1),
    2: ("Non-LTI zoo", q2),
    3: ("Commutativity & associativity", q3),
    4: ("Parallel branches & distributivity", q4),
    5: ("Echo canceller (inverse system)", q5),
    6: ("Step <-> impulse roundtrip", q6),
    7: ("Matched filter", q7),
    8: ("Block diagram -> single system", q8),
}


def main():
    import sys

    wanted = [int(a) for a in sys.argv[1:]] or sorted(QUESTIONS)
    for number in wanted:
        title, runner = QUESTIONS[number]
        print(f"\n{'=' * 70}\nQ{number} -- {title}\n{'=' * 70}")
        runner()


if __name__ == "__main__":
    main()
