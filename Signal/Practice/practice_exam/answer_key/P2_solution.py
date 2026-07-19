"""ANSWER KEY -- P2  Periodicity and aliasing of a discrete-time sinusoid."""

import numpy as np
import matplotlib.pyplot as plt


def sinusoid(n, A, Omega0, phi):
    return A * np.cos(Omega0 * n + phi)


def fundamental_period(Omega0, max_N=1000):
    # Periodic iff Omega0*N = 2*pi*m for integers N>0, m.
    # Use a STRICT tolerance: when Omega0 is a rational multiple of pi the pi
    # cancels and m is an exact integer, whereas an irrational frequency (e.g.
    # Omega0 = 1.0) only ever comes *close* to an integer and must return None.
    for N in range(1, max_N + 1):
        m = Omega0 * N / (2 * np.pi)
        if np.isclose(m, round(m), rtol=0.0, atol=1e-9):
            return N
    return None


def mse(a, b):
    return float(np.mean((a - b) ** 2))


def stem_plot(ax, n, x, label):
    markerline, stemlines, baseline = ax.stem(n, x, label=label)
    baseline.set_visible(False)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("n")
    ax.set_ylabel("Amplitude")


def main():
    A, phi = 1.0, 0.0
    n = np.arange(-25, 26)

    # ---- Periodicity ----
    Omega0 = np.pi / 4
    x = sinusoid(n, A, Omega0, phi)

    N = fundamental_period(Omega0)
    print("fundamental period N =", N)                 # -> 8 for pi/4

    # verify: x[n] == x[n+N] over the overlapping range
    print("periodicity MSE  =", mse(x[:-N], x[N:]))     # ~0

    print("period for Omega0=1.0 :", fundamental_period(1.0))  # -> None (not periodic)

    # ---- Aliasing: discrete frequency is unique only over a 2*pi span ----
    x_base = sinusoid(n, A, Omega0, phi)
    x_alias = sinusoid(n, A, Omega0 + 2 * np.pi, phi)
    x_diff = sinusoid(n, A, Omega0 + 0.5, phi)
    print("MSE(base, +2pi) =", mse(x_base, x_alias))    # ~0  (same sequence)
    print("MSE(base, +0.5) =", mse(x_base, x_diff))     # >0  (different)

    # ---- Plots ----
    fig1, ax1 = plt.subplots(figsize=(9, 4))
    stem_plot(ax1, n, x, "x[n] = cos(pi/4 n)")
    # mark one period starting at n=0
    one = (n >= 0) & (n < N)
    ax1.plot(n[one], x[one], "o", ms=10, mfc="none", label=f"one period (N={N})")
    ax1.set_title("P2a: periodicity of a discrete sinusoid")
    ax1.legend()
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(9, 4))
    stem_plot(ax2, n, x_base, "cos(Omega0 n)")
    stem_plot(ax2, n, x_alias, "cos((Omega0+2pi) n)  [alias, overlaps]")
    stem_plot(ax2, n, x_diff, "cos((Omega0+0.5) n)  [different]")
    ax2.set_title("P2b: adding 2pi to the frequency changes nothing")
    ax2.legend()
    fig2.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
