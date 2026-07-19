"""ANSWER KEY -- P3  Even/odd decomposition of a discrete signal + energy check."""

import numpy as np
import matplotlib.pyplot as plt

M = 15
n = np.arange(-M, M + 1)


def x_of_n(n):
    return (n >= 0) * (0.8 ** np.abs(n)) + 0.5 * (n == 1) - 0.3 * (n == -2)


def time_reverse(x):
    # Symmetric index range about 0  ->  x[-n] is the reversed array.
    return x[::-1]


def even_odd_decompose(x):
    xr = time_reverse(x)
    xe = 0.5 * (x + xr)
    xo = 0.5 * (x - xr)
    return xe, xo


def energy(x):
    return float(np.sum(np.abs(x) ** 2))


def stem_plot(ax, n, x, label):
    markerline, stemlines, baseline = ax.stem(n, x, label=label)
    baseline.set_visible(False)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("n")
    ax.set_ylabel("Amplitude")


def main():
    x = x_of_n(n)
    xe, xo = even_odd_decompose(x)

    # reconstruction check
    print("max|(xe+xo) - x| =", np.max(np.abs((xe + xo) - x)))     # ~0

    # energy split: E_x == E_xe + E_xo  (cross-term of even*odd sums to 0)
    print("E_x            =", energy(x))
    print("E_xe + E_xo    =", energy(xe) + energy(xo))
    print("difference     =", energy(x) - (energy(xe) + energy(xo)))  # ~0

    fig, ax = plt.subplots(figsize=(9, 4))
    stem_plot(ax, n, x, "x[n]")
    stem_plot(ax, n, xe, "xe[n] (even)")
    stem_plot(ax, n, xo, "xo[n] (odd)")
    ax.set_title("P3: even/odd decomposition of a discrete signal")
    ax.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
