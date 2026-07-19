"""
PRACTICE P2  --  Periodicity and aliasing of a discrete-time sinusoid
        x[n] = A cos(Omega0 n + phi)

Fill in every function marked TODO, and complete the demonstrations in main().
See QUESTIONS.md for the full problem statement and marks.
"""

import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# 1) Signal + property functions
# -----------------------------
def sinusoid(n: np.ndarray, A: float, Omega0: float, phi: float) -> np.ndarray:
    """x[n] = A cos(Omega0 n + phi)."""
        return A*np.cos(Omega0*n+phi)
    raise NotImplementedError  # TODO


def fundamental_period(Omega0: float, max_N: int = 1000) -> int | None:
    """
    Smallest integer N > 0 with  Omega0 * N = 2*pi*m  for some integer m.
    Return that N, or None if no such N exists up to max_N.

    Hint: for each candidate N, check whether (Omega0 * N) / (2*pi) is an integer.
    Use a STRICT tolerance, e.g. np.isclose(m, round(m), rtol=0, atol=1e-9): a
    rational multiple of pi gives an EXACT integer, but an irrational frequency
    (e.g. Omega0 = 1.0) only comes close and must return None.
    """

    N=Omega0/(np.pi*2)
    raise NotImplementedError  # TODO


# -----------------------------
# 2) Utility (given)
# -----------------------------
def mse(a: np.ndarray, b: np.ndarray) -> float:
    """Mean squared error between two equal-length sequences."""
    return float(np.mean((a - b) ** 2))


def stem_plot(ax, n, x, label):
    markerline, stemlines, baseline = ax.stem(n, x, label=label)
    baseline.set_visible(False)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("n")
    ax.set_ylabel("Amplitude")


# -----------------------------
# 3) Main experiment
# -----------------------------
def main():
    A, phi = 1.0, 0.0
    n = np.arange(-25, 26)

    # ---- Periodicity ----
    Omega0 = np.pi / 4
    x = sinusoid(n, A, Omega0, phi)

    N = fundamental_period(Omega0)      # TODO uses your function
    print("fundamental period N =", N)

    # TODO: verify periodicity with mse(x[n], x[n+N]) over the overlapping range.
    #       Print the MSE (should be ~0).

    # TODO: also call fundamental_period(1.0) and show it returns None.

    # ---- Aliasing ----
    # TODO: build three sequences and compare with mse:
    #   x_base  = cos(Omega0 n)
    #   x_alias = cos((Omega0 + 2*pi) n)      -> should equal x_base   (MSE ~ 0)
    #   x_diff  = cos((Omega0 + 0.5)  n)      -> should differ         (MSE > 0)
    #   Print both MSE values.

    # ---- Plots ----
    # TODO: (a) stem plot of one period of x[n];
    #       (b) stem plot of x_base, x_alias, x_diff on one figure.

    plt.show()


if __name__ == "__main__":
    main()
