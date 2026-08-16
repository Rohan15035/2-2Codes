"""
Problem C (C1/C2): Superposition of multiple signals.

A "SuperSignal" is just a bookkeeping object that stores several component
signals together with a scalar coefficient for each one, e.g.

        x(n) = 2 * x1(n) - 1 * x2(n)

is a SuperSignal with components [(2.0, x1), (-1.0, x2)].

Tasks:
  1. A SuperSignal class holding components (given in template, kept here).
  2. output_super(system, supersignal): return the LTI output for the whole
     combination.
  3. A main() that tests it.

Key idea -- LINEARITY of LTI systems:
        output( a*x1 + b*x2 )  ==  a*output(x1) + b*output(x2)
So we can compute the output two equivalent ways and check they agree:
  (A) collapse the SuperSignal into a single input signal, then convolve once;
  (B) convolve each component separately, scale, and add.
We reuse DiscreteSignal / LTISystem from signal_lti.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
os.environ.setdefault("MPLCONFIGDIR", os.path.join(HERE, ".mpl-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from signal_lti import DiscreteSignal, LTISystem


class SuperSignal:
    """Holds several (coefficient, DiscreteSignal) pairs."""

    def __init__(self):
        self.components = []               # start with an empty list

    def add(self, signal, coefficient=1.0):
        # Append a tuple. coefficient defaults to 1.0 if the caller omits it.
        self.components.append((coefficient, signal))

    def combine(self):
        """Collapse into one ordinary DiscreteSignal: sum of coeff * signal."""
        if not self.components:            # "if the list is empty"
            return DiscreteSignal(0, 0)
        total = None
        for coeff, sig in self.components:
            scaled = sig.multiply(coeff)   # coeff * sig
            total = scaled if total is None else total.add(scaled)
        return total


# We don't want to edit signal_lti.py, so we EXTEND LTISystem with a subclass.
# "class Child(Parent)" means Child inherits everything from Parent and can add
# new methods. output_super is the new method the problem asks for.
class LTISystemSuper(LTISystem):
    def output_super(self, super_signal):
        """Return the system output for a SuperSignal input."""
        combined_input = super_signal.combine()   # a + b + ...
        return self.output(combined_input)         # one convolution


def max_abs_difference(a, b):
    n_min = min(a.start_time, b.start_time)
    n_max = max(a.end_time, b.end_time)
    worst = 0.0
    for n in range(n_min, n_max + 1):
        worst = max(worst, abs(a.get_value_at_time(n) - b.get_value_at_time(n)))
    return worst


def save_plot(sig, title, path):
    fig, ax = plt.subplots(figsize=(8, 3))
    sig.plot(title, ax=ax)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)


def main():
    out_dir = os.path.join(HERE, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    # ---- Component signals ----
    x1 = DiscreteSignal(0, 0)
    x1.set_value_at_time(0, 1.0)           # x1[0] = 1

    x2 = DiscreteSignal(2, 2)
    x2.set_value_at_time(2, 1.0)           # x2[2] = 1

    # ---- Build the SuperSignal x(n) = 2*x1(n) - x2(n) ----
    x = SuperSignal()
    x.add(x1, 2.0)
    x.add(x2, -1.0)

    # ---- Impulse response and system ----
    h = DiscreteSignal(0, 1)
    h.set_value_at_time(0, 1.0)
    h.set_value_at_time(1, 0.5)
    system = LTISystemSuper(h)

    # ---- Method A: output of the collapsed SuperSignal ----
    combined_input = x.combine()
    y_super = system.output_super(x)
    save_plot(combined_input, "Combined input x[n] = 2*x1 - x2",
              os.path.join(out_dir, "1_combined_input.png"))
    save_plot(y_super, "Output via output_super",
              os.path.join(out_dir, "2_output_super.png"))

    # ---- Method B: superposition done by hand (to verify linearity) ----
    y_manual = None
    for coeff, sig in x.components:
        branch = system.output(sig).multiply(coeff)   # coeff * (sig * h)
        y_manual = branch if y_manual is None else y_manual.add(branch)

    difference = max_abs_difference(y_super, y_manual)
    print("Combined input:", [round(v, 4) for v in combined_input.values],
          "over", list(combined_input.times()))
    print("Output y:", [round(v, 4) for v in y_super.values],
          "over", list(y_super.times()))
    print(f"Max |output_super - manual superposition| = {difference:.3e}")
    print("Linearity holds:", difference < 1e-9)
    print(f"Figures saved in: {out_dir}")


if __name__ == "__main__":
    main()
