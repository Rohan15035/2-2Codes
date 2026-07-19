"""
PRACTICE P1  --  Time scaling by a real factor with LINEAR interpolation
        y(t) = x(a * t),   a > 0  (real, not necessarily integer)

Fill in every function marked TODO.  Do not change x_of_t or the grid.
See QUESTIONS.md for the full problem statement and marks.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Time axis  (given)
# ----------------------------
T_MIN, T_MAX, N = -5.0, 5.0, 5001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Base signal x(t) (given): a smooth, decaying, asymmetric wave."""
    return np.exp(-0.3 * np.abs(t)) * np.sin(2 * np.pi * 0.7 * t) + 0.2 * t * np.exp(-(t / 2.0) ** 2)


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def interpolate_signal(
    t_original: np.ndarray,
    x_original: np.ndarray,
    t_query: np.ndarray,
) -> np.ndarray:
    """
    LINEAR interpolation of (t_original, x_original) at each time in t_query.

    If a query time lies a fraction f in [0,1) from the left sample xL to the
    right sample xR, return (1 - f)*xL + f*xR.  Query times outside the original
    range must return NaN.
    """
    dt=t_original[1]-t_original[0]
    pos=(t_query-t_original[0])/dt

    xL=np.floor(pos).astype(int)
    xR=np.ceil(pos).astype(int)
    m=len(t_original)
    # BUG (off-by-one): valid indices into x_original are 0..m-1, so this should be
    # xR<=m-1 (i.e. xR<m). As written, xR==m slips through as "valid" and would
    # index x_original out of bounds.
    valid=(xL>=0) & (xR<len(t_original))
    f=pos-xL
    y=np.full(t_query.shape,np.nan,dtype=float)
    # BUG: f has the full length of t_query, but x_original[xL[valid]] / [xR[valid]]
    # only have len(valid.nonzero()) elements -> shape mismatch whenever some points
    # are invalid (e.g. compression). Fix: use f[valid] on both terms below.
    y[valid]=(1-f[valid])*x_original[xL[valid]]+f[valid]*x_original[xR[valid]]
    return y



def time_scale(t: np.ndarray, x: np.ndarray, a: float) -> np.ndarray:
    """Return y(t) = x(a * t) using interpolate_signal."""
    y=a*t
    return interpolate_signal(t,x,y)


def plot_pair(t: np.ndarray, x: np.ndarray, y: np.ndarray, title: str) -> None:
    plt.figure()
    plt.plot(t, x, label="x(t)")
    plt.plot(t, y, label="y(t) = x(a t)")
    plt.title(title)
    plt.xlabel("t")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()


# ----------------------------
# Main  (given)
# ----------------------------
def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)

    y_exp = time_scale(t, x, 0.5)   # expansion
    plot_pair(t, x, y_exp, "P1: expansion  y(t) = x(0.5 t)")

    y_comp = time_scale(t, x, 2.0)  # compression
    plot_pair(t, x, y_comp, "P1: compression  y(t) = x(2 t)")

    plt.show()


if __name__ == "__main__":
    main()
