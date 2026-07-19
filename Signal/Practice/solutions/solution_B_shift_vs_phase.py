"""
Solution B  --  Online_1_Spec_B1_B2
Time shift vs. phase change in a discrete-time sinusoid  x[n] = A cos(Omega0 n + phi)

Core relationship
-----------------
A cos( Omega0 (n - n0) + phi )  =  A cos( Omega0 n + phi - Omega0*n0 )

So a TIME SHIFT of n0 is ALWAYS equivalent to a PHASE CHANGE of
        phi0 = -Omega0 * n0.                                   (Part A)

The converse is NOT always true.  A phase change phi0 can be reproduced by a
time shift only if  phi0 = -Omega0 * n0 (mod 2*pi)  for some INTEGER n0.
Because n0 must be an integer, an arbitrary phi0 cannot generally be matched,
so the best integer shift leaves a non-zero MSE.                (Part B)
"""

import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# 1) Signal-building functions
# -----------------------------
def sinusoid(n: np.ndarray, A: float, Omega0: float, phi: float) -> np.ndarray:
    """x[n] = A cos(Omega0 n + phi)."""
    return A * np.cos(Omega0 * n + phi)


def time_shift_sinusoid(n: np.ndarray, A: float, Omega0: float, phi: float, n0: int) -> np.ndarray:
    """Time shift by n0 samples:  x[n - n0] = A cos(Omega0 (n - n0) + phi)."""
    return A * np.cos(Omega0 * (n - n0) + phi)


def phase_change_sinusoid(n: np.ndarray, A: float, Omega0: float, phi: float, phi0: float) -> np.ndarray:
    """Add phi0 to the phase:  A cos(Omega0 n + phi + phi0)."""
    return A * np.cos(Omega0 * n + phi + phi0)


# -----------------------------
# 2) Utility functions (given)
# -----------------------------
def mse(a: np.ndarray, b: np.ndarray) -> float:
    """Mean squared error between two sequences of equal length."""
    return float(np.mean((a - b) ** 2))


def stem_plot(ax, n, x, label):
    """A nicer stem plot for discrete-time sequences."""
    markerline, stemlines, baseline = ax.stem(n, x, label=label)
    baseline.set_visible(False)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("n")
    ax.set_ylabel("Amplitude")


# -----------------------------
# 3) Main experiment
# -----------------------------
def main():
    # Base sinusoid parameters
    A = 1.0
    Omega0 = np.pi / 4
    phi = 0.0

    # Index range
    n = np.arange(-20, 21)  # -20, -19, ..., 20

    # Original signal
    x = sinusoid(n, A, Omega0, phi)

    # ---------- Part A: time shift  ->  equivalent phase change ----------
    n0 = 3                       # integer time shift
    x_time = time_shift_sinusoid(n, A, Omega0, phi, n0)

    # A time shift of n0 is the same as a phase change of -Omega0*n0.
    phi0_equiv = -Omega0 * n0
    x_phase_equiv = phase_change_sinusoid(n, A, Omega0, phi, phi0_equiv)

    err_A = mse(x_time, x_phase_equiv)
    print("[Part A] MSE between time-shifted and equivalent phase-changed:", err_A)
    print(f"         (a shift of n0={n0} equals a phase change of {phi0_equiv:.3f} rad)\n")

    fig1, ax1 = plt.subplots(figsize=(9, 4))
    stem_plot(ax1, n, x, "original x[n]")
    stem_plot(ax1, n, x_time, f"time shift by n0={n0}")
    stem_plot(ax1, n, x_phase_equiv, f"phase change by phi0={phi0_equiv:.3f}")
    ax1.set_title("Part A: a time shift is exactly a phase change (MSE = 0)")
    ax1.legend()
    fig1.tight_layout()

    # ---------- Part B: phase change  ->  best matching time shift ----------
    phi0 = 1.0                   # an ARBITRARY phase change (not a multiple of Omega0)
    x_phase = phase_change_sinusoid(n, A, Omega0, phi, phi0)

    # Search over integer shifts to see whether any time shift matches this phase change.
    k_min, k_max = -12, 12
    best_k = None
    best_err = None

    for k in range(k_min, k_max + 1):
        x_time_k = time_shift_sinusoid(n, A, Omega0, phi, k)
        e = mse(x_time_k, x_phase)
        if (best_err is None) or (e < best_err):
            best_err = e
            best_k = k

    print(f"[Part B] Best matching integer shift in [{k_min},{k_max}] is k={best_k} with MSE={best_err}")
    print("         MSE != 0  ->  an arbitrary phase change canNOT be reproduced by an integer time shift.")
    print(f"         (a shift can only make phases that are multiples of Omega0={Omega0:.3f} rad)\n")

    x_time_best = time_shift_sinusoid(n, A, Omega0, phi, best_k)

    fig2, ax2 = plt.subplots(figsize=(9, 4))
    stem_plot(ax2, n, x_phase, f"phase change by phi0={phi0:.3f}")
    stem_plot(ax2, n, x_time_best, f"best time shift k={best_k}")
    ax2.set_title("Part B: an arbitrary phase change has no exact integer time shift (MSE > 0)")
    ax2.legend()
    fig2.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
