"""
Solution C  --  Online_1_C1_C2
Time reversal of a sampled signal, then even/odd decomposition.

Key idea
--------
The time grid t is SYMMETRIC about 0 (linspace(-4, 4, 4001), an odd number of
points that includes t = 0).  Therefore t[i] and t[N-1-i] are exact negatives
of each other, and x(-t) is obtained simply by REVERSING the sample array:

        x(-t)[i] = x( -t[i] ) = x( t[N-1-i] ) = x[N-1-i]      ->   x[::-1]

Even / odd parts:
        xe(t) = 1/2 ( x(t) + x(-t) )      (symmetric)
        xo(t) = 1/2 ( x(t) - x(-t) )      (anti-symmetric)
and  xe + xo = x  always.
"""

import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -4.0, 4.0, 4001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Base signal x(t) (given): an asymmetric mix so even & odd parts are both non-trivial."""
    # 1) Triangular pulse centered at 0
    tri0 = np.zeros_like(t, dtype=float)
    m0 = np.abs(t) <= 1.0
    tri0[m0] = 1.0 - np.abs(t[m0])

    # 2) Windowed ramp (odd-ish component)
    ramp = np.zeros_like(t, dtype=float)
    m1 = np.abs(t) <= 1.0
    ramp[m1] = t[m1]

    # 3) Shifted triangular pulse (breaks symmetry)
    tri_shift = np.zeros_like(t, dtype=float)
    u = t - 1.2
    m2 = np.abs(u) <= 1.0
    tri_shift[m2] = 1.0 - np.abs(u[m2])

    return tri0 + 0.6 * ramp + 0.4 * tri_shift


def time_reverse(x: np.ndarray) -> np.ndarray:
    """
    Given samples x(t) on a grid symmetric about 0, return samples of x(-t).
    Reversing the array flips the time axis.
    """
    return x[::-1]


def even_odd_decompose(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Even / odd decomposition, built ONLY from time_reverse (as required).
        xe = 1/2 (x + x(-t))
        xo = 1/2 (x - x(-t))
    """
    xr = time_reverse(x)
    xe = 0.5 * (x + xr)
    xo = 0.5 * (x - xr)
    return xe, xo


# ----------------------------
# Provided plotting (do not modify)
# ----------------------------
def plot_three(t: np.ndarray, x: np.ndarray, xe: np.ndarray, xo: np.ndarray):
    plt.figure()
    plt.plot(t, x, label="x(t)")
    plt.plot(t, xe, label="xe(t)")
    plt.plot(t, xo, label="xo(t)")
    plt.title("Even–Odd Decomposition")
    plt.xlabel("t")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()


def plot_pair(t: np.ndarray, x: np.ndarray, xr: np.ndarray):
    plt.figure()
    plt.plot(t, x, label="x(t)")
    plt.plot(t, xr, label="x(-t)")
    plt.title("Time Reversal")
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

    # Time reverse and even/odd components
    xr = time_reverse(x)
    xe, xo = even_odd_decompose(x)

    # Sanity check: xe + xo must reconstruct x exactly.
    print("max |(xe + xo) - x| =", np.max(np.abs((xe + xo) - x)))

    # Plots
    plot_pair(t, x, xr)          # x(t) and x(-t)
    plot_three(t, x, xe, xo)     # x(t), xe(t), xo(t)
    plt.show()


if __name__ == "__main__":
    main()
