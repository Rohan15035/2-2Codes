"""
Problem B (B1/B2): Combination of LTI systems.

Block diagram:

        +------+
   x -->|  h1  |---+
        +------+   |      +------+
                  (+)---->|  h3  |--> y
        +------+   |      +------+
   x -->|  h2  |---+
        +------+

So x is fed to h1 AND h2 in parallel, their outputs are ADDED, and that sum is
passed through h3 in series.

Two ways to get y:
  (1) Block by block:
        y1 = x * h1
        y2 = x * h2
        y_parallel = y1 + y2
        y = y_parallel * h3
  (2) Single equivalent system with impulse response:
        h_combined = (h1 + h2) * h3
        y = x * h_combined

Both use LTI properties:
  - Parallel systems add:            h_parallel = h1 + h2
  - Series (cascade) systems convolve: h_series  = h_parallel * h3
We reuse DiscreteSignal / LTISystem from signal_lti.py and verify y matches.
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


def make_signal(start_time, end_time, samples):
    """Build a DiscreteSignal. `samples` is a dict {time: value}."""
    sig = DiscreteSignal(start_time, end_time)
    for t, v in samples.items():           # .items() iterates (key, value) pairs
        sig.set_value_at_time(t, v)
    return sig


def max_abs_difference(a, b):
    n_min = min(a.start_time, b.start_time)
    n_max = max(a.end_time, b.end_time)
    worst = 0.0
    for n in range(n_min, n_max + 1):
        diff = abs(a.get_value_at_time(n) - b.get_value_at_time(n))
        worst = max(worst, diff)
    return worst


def save_plot(sig, title, path):
    fig, ax = plt.subplots(figsize=(8, 3))
    sig.plot(title, ax=ax)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)


def main():
    out_dir = os.path.join(HERE, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    # ---- Input and the three impulse responses (same as the template) ----
    x = make_signal(0, 2, {0: 1.0, 2: -1.0})       # x[0]=1, x[2]=-1
    h1 = make_signal(0, 0, {0: 1.0})               # identity
    h2 = make_signal(1, 1, {1: 0.5})               # half-gain delay by 1
    h3 = make_signal(0, 1, {0: 1.0, 1: 1.0})       # x[n] + x[n-1]

    sys1 = LTISystem(h1)
    sys2 = LTISystem(h2)
    sys3 = LTISystem(h3)

    # ---- Method 1: block by block ----
    y1 = sys1.output(x)                # x * h1
    y2 = sys2.output(x)                # x * h2
    y_parallel = y1.add(y2)            # add the two branch outputs
    y_final_1 = sys3.output(y_parallel)  # push the sum through h3
    save_plot(y_final_1, "Output via block-by-block system",
              os.path.join(out_dir, "1_block_by_block.png"))

    # ---- Method 2: single combined impulse response ----
    # h_combined = (h1 + h2) convolved with h3
    h_parallel = h1.add(h2)
    h_combined = sys3.output(h_parallel)   # convolve (h1+h2) with h3
    save_plot(h_combined, "Combined impulse response h_combined",
              os.path.join(out_dir, "2_h_combined.png"))

    sys_combined = LTISystem(h_combined)
    y_final_2 = sys_combined.output(x)
    save_plot(y_final_2, "Output via combined impulse response",
              os.path.join(out_dir, "3_combined_output.png"))

    # ---- Verify the two outputs are the same signal ----
    difference = max_abs_difference(y_final_1, y_final_2)
    print("h_combined samples:", list(h_combined.times()), "->",
          [round(v, 4) for v in h_combined.values])
    print("y range:", (y_final_1.start_time, y_final_1.end_time))
    print("y values:", [round(v, 4) for v in y_final_1.values])
    print(f"Max |y1 - y2| = {difference:.3e}")
    print("Outputs are equal:", difference < 1e-9)
    print(f"Figures saved in: {out_dir}")


if __name__ == "__main__":
    main()
