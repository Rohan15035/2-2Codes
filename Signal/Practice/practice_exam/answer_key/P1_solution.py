"""ANSWER KEY -- P1  Time scaling by a real factor with linear interpolation."""

import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -5.0, 5.0, 5001


def x_of_t(t: np.ndarray) -> np.ndarray:
    return np.exp(-0.3 * np.abs(t)) * np.sin(2 * np.pi * 0.7 * t) + 0.2 * t * np.exp(-(t / 2.0) ** 2)


def interpolate_signal(t_original, x_original, t_query):
    t0 = t_original[0]
    dt = t_original[1] - t_original[0]
    M = len(x_original)

    pos = (t_query - t0) / dt          # fractional sample position of each query
    left = np.floor(pos).astype(int)   # index of the left neighbour
    frac = pos - left                  # distance from left neighbour, in [0, 1)

    y = np.full(t_query.shape, np.nan, dtype=float)
    valid = (left >= 0) & (left + 1 < M)          # need both neighbours in range
    L = left[valid]
    f = frac[valid]
    y[valid] = (1.0 - f) * x_original[L] + f * x_original[L + 1]

    # Handle a query landing exactly on the LAST sample (left+1 would be out of range).
    on_last = np.isclose(pos, M - 1)
    y[on_last] = x_original[M - 1]
    return y


def time_scale(t, x, a):
    return interpolate_signal(t, x, a * t)   # y(t) = x(a t)


def plot_pair(t, x, y, title):
    plt.figure()
    plt.plot(t, x, label="x(t)")
    plt.plot(t, y, label="y(t) = x(a t)")
    plt.title(title)
    plt.xlabel("t")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()


def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)

    y_exp = time_scale(t, x, 0.5)
    plot_pair(t, x, y_exp, "P1: expansion  y(t) = x(0.5 t)")

    y_comp = time_scale(t, x, 2.0)
    plot_pair(t, x, y_comp, "P1: compression  y(t) = x(2 t)")

    # a < 1 stretches (each feature of x is reached at a LATER t); a > 1 squeezes.
    # For a = 2, y needs x(2t) up to t = 5 -> x(10), which is outside [-5,5],
    # so the outer half of the compressed signal is NaN (correctly ignored).
    print("NaNs in expansion  (a=0.5):", np.isnan(y_exp).sum())
    print("NaNs in compression(a=2.0):", np.isnan(y_comp).sum())
    plt.show()


if __name__ == "__main__":
    main()
