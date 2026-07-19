"""
Solution A  --  Spec_A1_A2
Time sub-scaling of a sampled continuous-time signal:  y(t) = x(t / k)

Key idea
--------
The signal is stored as SAMPLES on a uniform grid t.  To build y(t) = x(t/k)
we must, for every output time t[i], read the value of x at the time  t[i]/k.
That time usually falls BETWEEN two stored samples, so we interpolate it as the
average of the nearest left and right samples (as the assignment specifies).
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Time axis
# ----------------------------
T_MIN, T_MAX, N = -4.0, 4.0, 4001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Base signal x(t): sum of two sinusoids (given)."""
    return (
        np.sin(2 * np.pi * 0.5 * t)
        + 0.5 * np.sin(2 * np.pi * 1.5 * t)
    )


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def interpolate_signal(
    t_original: np.ndarray,
    x_original: np.ndarray,
    t_query: np.ndarray,
) -> np.ndarray:
    """
    Return the value of the sampled signal (t_original, x_original) at each time
    in t_query, using the AVERAGE of the nearest left and right samples.

    A query time that lands exactly on a stored sample returns that sample
    (because then left == right).  A query time outside the stored range is
    marked NaN so it is simply ignored by the plot.
    """
    t0 = t_original[0]
    dt = t_original[1] - t_original[0]          # uniform sample spacing
    M = len(x_original)

    # Position of each query time measured in units of samples.
    pos = (t_query - t0) / dt

    # Snap away tiny floating-point error so a query that lands exactly on a
    # sample is treated as exact (e.g. y(0) = x(0), not an average of neighbours).
    pos_round = np.round(pos)
    pos = np.where(np.abs(pos - pos_round) < 1e-6, pos_round, pos)

    left = np.floor(pos).astype(int)            # nearest sample to the left
    right = np.ceil(pos).astype(int)            # nearest sample to the right

    y = np.full(t_query.shape, np.nan, dtype=float)

    valid = (left >= 0) & (right < M)           # keep only in-range queries
    y[valid] = 0.5 * (x_original[left[valid]] + x_original[right[valid]])
    return y


def time_scale(t: np.ndarray, x: np.ndarray, k: int) -> np.ndarray:
    """
    Time sub-scaling:  y(t) = x(t / k).

    Output sample i must equal x evaluated at time t[i]/k, so we simply ask
    interpolate_signal for the original signal at the query times t / k.
    """
    t_query = t / k
    return interpolate_signal(t, x, t_query)


def plot_pair(t: np.ndarray, x: np.ndarray, y: np.ndarray, title: str) -> None:
    """Plot x(t) and y(t) on the same figure."""
    plt.figure()
    plt.plot(t, x, label="x(t)")
    plt.plot(t, y, label="y(t) = x(t/k)")
    plt.title(title)
    plt.xlabel("t")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()


# ----------------------------
# Main
# ----------------------------
def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)

    k = 2   # sub-scaling (expansion) factor
    y = time_scale(t, x, k)

    plot_pair(t, x, y, title=f"Time Sub-scaling: y(t) = x(t / {k})")
    plt.show()


if __name__ == "__main__":
    main()
