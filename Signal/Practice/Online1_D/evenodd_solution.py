"""
ANSWER KEY -- Practice Set D
Even/odd decomposition of a sampled continuous-time signal, and the weighted
reconstruction  y(t) = xe(t) + a * xo(t).
See spec_evenodd.md for the problem statement and marks.
"""

import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX = -np.pi, np.pi          # x(t) is defined only on this range


def base_signal(t):
    """Base signal x(t) (given): asymmetric, so xe and xo are both non-trivial."""
    x = np.exp(-0.4 * t) * np.cos(2 * t) + 0.5 * t
    x[(t < T_MIN) | (t > T_MAX)] = 0
    return x


def time_reverse(t, x):
    """
    Return the samples of x(-t).
    t = linspace(-pi, pi, N) is SYMMETRIC about 0, so t[N-1-i] = -t[i] and
    reversing the sample array flips the time axis exactly (no interpolation).
    """
    return x[::-1]


def even_odd_decompose(t, x):
    """xe(t) = 1/2 (x + x(-t)),  xo(t) = 1/2 (x - x(-t)), built from time_reverse."""
    xr = time_reverse(t, x)
    xe = 0.5 * (x + xr)
    xo = 0.5 * (x - xr)
    return xe, xo


def reconstruct(xe, xo, a):
    """Weighted reconstruction y(t) = xe(t) + a * xo(t)."""
    return xe + a * xo


def main():
    t = np.linspace(T_MIN, T_MAX, 1000)
    x = base_signal(t)

    xe, xo = even_odd_decompose(t, x)

    # reconstruction sanity check: xe + xo must rebuild x exactly
    print("max |(xe + xo) - x| =", np.max(np.abs((xe + xo) - x)))   # ~0

    print("Enter a to plot y(t) = xe(t) + a*xo(t).")
    print("  a = 1 -> x(t)   a = -1 -> x(-t)   a = 0 -> even part")
    print("Type 'q' to quit.\n")

    while True:
        user_in = input("Enter value of a (or 'q' to quit): ").strip()
        if user_in.lower() == 'q':
            break
        a = float(user_in)
        y = reconstruct(xe, xo, a)

        plt.figure(figsize=(9, 5))
        plt.plot(t, x, label="x(t)")
        plt.plot(t, xe, label="xe(t) (even)", linestyle="--")
        plt.plot(t, xo, label="xo(t) (odd)", linestyle="--")
        plt.plot(t, y, label=f"y(t) = xe + {a}*xo", linewidth=2)
        plt.title("Even/Odd Decomposition and Weighted Reconstruction")
        plt.xlabel("t")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    print("Exiting.")


if __name__ == "__main__":
    main()
