"""
PRACTICE P3  --  Even/odd decomposition of a DISCRETE signal + energy check
        xe[n] = 1/2 (x[n] + x[-n]),   xo[n] = 1/2 (x[n] - x[-n])

Fill in every function marked TODO, and complete the checks in main().
See QUESTIONS.md for the full problem statement and marks.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Index axis  (given)  -- symmetric about n = 0
# ----------------------------
M = 15
n = np.arange(-M, M + 1)          # -M, ..., -1, 0, 1, ..., M


def x_of_n(n: np.ndarray) -> np.ndarray:
    """Base discrete signal x[n] (given): asymmetric so xe and xo are both non-trivial."""
    return (n >= 0) * (0.8 ** np.abs(n)) + 0.5 * (n == 1) - 0.3 * (n == -2)


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def time_reverse(x: np.ndarray) -> np.ndarray:
    return x[::-1]


def even_odd_decompose(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (xe, xo) using ONLY time_reverse."""
    xr=time_reverse(x)
    xe=0.5*(x+xr)
    xo=0.5*(x-xr)
    return xe,xo



def energy(x: np.ndarray) -> float:
    """Signal energy  E = sum |x[n]|^2."""
    return float(np.sum(abs(x)**2))




# ----------------------------
# Utility (given)
# ----------------------------
def stem_plot(ax, n, x, label):
    markerline, stemlines, baseline = ax.stem(n, x, label=label)
    baseline.set_visible(False)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("n")
    ax.set_ylabel("Amplitude")


# ----------------------------
# Main
# ----------------------------
def main():
    x = x_of_n(n)

    xe, xo = even_odd_decompose(x)

    # TODO: print reconstruction check   max|(xe + xo) - x|   (should be ~0)

    print(np.max(np.abs((xe+xo)-x)))

    # TODO: print energy check           E_x   vs   E_xe + E_xo   (should match)
    E_x=energy(x)
    E_xe=energy(xe)
    E_xo=energy(xo)

    print(E_x==E_xe+E_xo)
    # TODO: stem plot of x[n], xe[n], xo[n] on one figure
    #       (title, xlabel, ylabel, legend, grid)
    # stem_plot(x,xe,xo,stemPlot)    
    fig,ax=plt.subplots()
    stem_plot(ax,n,x,"x[n]")
    stem_plot(ax,n,xe,"xe[n]")
    stem_plot(ax,n,xo,"xo[n]")

    plt.show()


if __name__ == "__main__":
    main()
