"""
ANSWER KEY -- Practice Set E
Energy and average power of a sampled continuous-time signal over [a, b].
See spec_energy.md for the problem statement and marks.
"""

import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX = -np.pi, np.pi          # x(t) is defined only on this range


def base_signal(t):
    """Base signal x(t) (given)."""
    x = np.sin(t)
    x[(t < T_MIN) | (t > T_MAX)] = 0
    return x


def energy(t, x, a, b):
    """
    E[a,b] = integral_a^b |x(t)|^2 dt, approximated on the sample grid:
    square the in-range samples, add them up, multiply by the sample spacing dt.
    """
    dt = t[1] - t[0]
    mask = (t >= a) & (t <= b)
    return float(np.sum(np.abs(x[mask]) ** 2) * dt)


def average_power(t, x, a, b):
    """P[a,b] = E[a,b] / (b - a)."""
    return energy(t, x, a, b) / (b - a)


def main():
    t = np.linspace(T_MIN, T_MAX, 2001)
    x = base_signal(t)

    print("Enter interval a,b to compute energy and average power on [a,b].")
    print("Type 'q' to quit.\n")

    while True:
        raw = input("Enter a,b (or 'q' to quit): ").strip()
        if raw.lower() == 'q':
            break
        a_str, b_str = raw.split(',')
        a, b = float(a_str), float(b_str)

        E = energy(t, x, a, b)
        P = average_power(t, x, a, b)
        print(f"  E[{a}, {b}] = {E:.6f}    P[{a}, {b}] = {P:.6f}")

        mask = (t >= a) & (t <= b)
        plt.figure(figsize=(9, 5))
        plt.plot(t, x, label="x(t)")
        plt.fill_between(t[mask], 0, np.abs(x[mask]) ** 2, alpha=0.3,
                         label="|x(t)|^2 on [a, b]")
        plt.title(f"Energy = {E:.4f},  Avg Power = {P:.4f}  on [{a}, {b}]")
        plt.xlabel("t")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    print("Exiting.")


if __name__ == "__main__":
    main()
