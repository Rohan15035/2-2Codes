"""
Problem A (A1/A2): Working with the STEP RESPONSE of an LTI system.

We are given the step response s[n] of an LTI system (instead of the impulse
response h[n]). We must:

  1. Read s[n] and plot it.
  2. Recover the impulse response:  h[n] = s[n] - s[n-1]      (s[-1] = 0)
  3. Read x[n] and compute the first difference:
        dx[n] = x[n] - x[n-1]                                 (x[-1] = 0)
  4. Compute the output using ONLY the step response:
        y_s[n] = (dx * s)[n]
  5. Verify against the impulse-response method:
        y_h[n] = (x * h)[n]
     and show y_s == y_h.

We reuse the DiscreteSignal / LTISystem classes from signal_lti.py (Offline 1).
No numpy.convolve is used -- LTISystem.output() does the convolution by hand.
"""

import os
import sys

# --- make signal_lti.py importable, no matter where we run this from ----------
# __file__ is the path of THIS script. dirname() gives its folder.
# os.path.join(..., "..") goes one level up (to the "solutions" folder), where
# the copy of signal_lti.py lives. sys.path is the list of folders Python
# searches for imports; inserting at position 0 makes it look there first.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

# matplotlib needs a writable cache dir; keep it local so it never fails.
os.environ.setdefault("MPLCONFIGDIR", os.path.join(HERE, ".mpl-cache"))

import matplotlib

matplotlib.use("Agg")  # "Agg" = save figures to files, never open a window.
import matplotlib.pyplot as plt

from signal_lti import DiscreteSignal, LTISystem


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def read_signal_from_file(filename):
    """Read a signal file in the format:
        line 1:  nstart nend
        line 2:  one value per index from nstart..nend
    and return a DiscreteSignal.
    """
    with open(filename, "r", encoding="utf-8") as f:
        # f.readline() reads one line as a string, e.g. "-10 30\n".
        # .split() breaks it on whitespace -> ["-10", "30"].
        # map(int, ...) converts each piece to int; we unpack into two names.
        nstart, nend = map(int, f.readline().split())
        values = list(map(float, f.readline().split()))

    sig = DiscreteSignal(nstart, nend)
    for i, v in enumerate(values):          # enumerate gives (index, value) pairs
        sig.set_value_at_time(nstart + i, v)
    return sig


def first_difference(sig):
    """Return d[n] = sig[n] - sig[n-1], using ONLY Signal operations.

    sig[n-1] is the same signal shifted RIGHT by one sample -> sig.shift(1).
    Subtracting is "add the negative": sig + (-1) * sig.shift(1).
    """
    shifted = sig.shift(1)                   # this is sig[n-1]
    neg_shifted = shifted.multiply(-1.0)     # this is -sig[n-1]
    return sig.add(neg_shifted)              # sig[n] + (-sig[n-1])


def max_abs_difference(a, b):
    """Largest |a[n] - b[n]| over every index either signal touches.
    Used to prove two outputs are the same signal.
    """
    n_min = min(a.start_time, b.start_time)
    n_max = max(a.end_time, b.end_time)
    worst = 0.0
    for n in range(n_min, n_max + 1):
        diff = abs(a.get_value_at_time(n) - b.get_value_at_time(n))
        if diff > worst:
            worst = diff
    return worst


def save_plot(sig, title, path):
    fig, ax = plt.subplots(figsize=(8, 3))
    sig.plot(title, ax=ax)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------
def main():
    out_dir = os.path.join(HERE, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    # ---- Part 1: read and plot the step response s[n] ----
    s = read_signal_from_file(os.path.join(HERE, "step_response.txt"))
    save_plot(s, "Step response s[n]", os.path.join(out_dir, "1_step_response.png"))

    # ---- Part 2: recover impulse response h[n] = s[n] - s[n-1] ----
    h = first_difference(s)
    save_plot(h, "Recovered impulse response h[n] = s[n] - s[n-1]",
              os.path.join(out_dir, "2_impulse_response.png"))

    # ---- Part 3: read x[n] and compute dx[n] = x[n] - x[n-1] ----
    x = read_signal_from_file(os.path.join(HERE, "input_signal.txt"))
    dx = first_difference(x)
    save_plot(x, "Input x[n]", os.path.join(out_dir, "3_input.png"))
    save_plot(dx, "First difference dx[n] = x[n] - x[n-1]",
              os.path.join(out_dir, "4_first_difference.png"))

    # ---- Part 4: output using ONLY the step response:  y_s = dx * s ----
    system_s = LTISystem(s)          # treat s as the impulse response of a system
    y_s = system_s.output(dx)        # convolve dx with s
    save_plot(y_s, "Output y_s[n] = (dx * s)[n]",
              os.path.join(out_dir, "5_output_via_step.png"))

    # ---- Part 5: verify with impulse-response method:  y_h = x * h ----
    system_h = LTISystem(h)
    y_h = system_h.output(x)
    save_plot(y_h, "Output y_h[n] = (x * h)[n]",
              os.path.join(out_dir, "6_output_via_impulse.png"))

    # ---- Report ----
    difference = max_abs_difference(y_s, y_h)
    print("Output range (y_s):", (y_s.start_time, y_s.end_time))
    print("Output range (y_h):", (y_h.start_time, y_h.end_time))
    print(f"Max |y_s - y_h| = {difference:.3e}")
    if difference < 1e-9:
        print("SUCCESS: both methods give the same output signal.")
    else:
        print("MISMATCH: the two outputs differ.")
    print(f"Figures saved in: {out_dir}")


if __name__ == "__main__":
    main()
