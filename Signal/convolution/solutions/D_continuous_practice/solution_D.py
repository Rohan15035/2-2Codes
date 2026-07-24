"""
Problem D: Continuous-Time Convolution -- Impulse Decomposition (practice).

IMPORTANT: This problem CANNOT reuse signal_lti.py.
  - signal_lti.py models a DISCRETE signal as a finite NumPy array of samples
    indexed by integers.
  - Here a CONTINUOUS signal x(t) is defined by a Python FUNCTION of a real
    variable t. There is no fixed array of samples, so a brand-new class
    (ContinuousSignal) is required. That is why this folder has its own code.

Goal (input decomposition only -- we do NOT compute the output here):
    A continuous signal can be approximated as a sum of tall thin rectangles:
        delta_D(t) = 1/D for 0 <= t < D, else 0        (a unit-area pulse)
        x(t) ~= sum_k  x(t_k) * D * delta_D(t - t_k),   t_k = k*D
    As the width D -> 0, the staircase reconstruction approaches x(t).
"""

import os

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mpl-cache"),
)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(HERE, "continuous_practice")


class ContinuousSignal:
    """A continuous-time signal represented by a function func(t)."""

    def __init__(self, func):
        # `func` is itself a function. In Python functions are values you can
        # store in a variable, pass around, and call later with func(t).
        self.func = func

    def shift(self, shift):
        # Return x(t - shift). We build a NEW function that, when called with t,
        # evaluates the old function at (t - shift). `lambda t: ...` is a short
        # one-line anonymous function.
        return ContinuousSignal(lambda t: self.func(t - shift))

    def add(self, other):
        return ContinuousSignal(lambda t: self.func(t) + other.func(t))

    def multiply(self, other):
        # Pointwise product of two signals: x(t) * y(t).
        return ContinuousSignal(lambda t: self.func(t) * other.func(t))

    def multiply_const_factor(self, scaler):
        # Scale by a constant: a * x(t).
        return ContinuousSignal(lambda t: scaler * self.func(t))

    def plot(self, t_min, t_max, num_points, title, ax=None, **kwargs):
        # np.linspace(a, b, n) makes n evenly spaced numbers from a to b.
        t = np.linspace(t_min, t_max, num_points)
        if ax is None:
            _, ax = plt.subplots()
        ax.plot(t, self.func(t), **kwargs)   # **kwargs forwards extra styling
        ax.set_title(title)
        ax.set_xlabel("t (Time)")
        ax.set_ylabel("x(t)")
        ax.grid(True, alpha=0.35)
        return ax


class LTIContinuous:
    """Continuous-time LTI system defined by an impulse response h(t)."""

    def __init__(self, impulse_response):
        self.impulse_response = impulse_response

    def linear_combination_of_impulses(self, input_signal, delta):
        """Decompose input_signal into rectangular impulses of width `delta`.

        Returns two lists:
            impulses:     the unit pulses delta_D(t - t_k)
            coefficients: c_k = x(t_k) * delta
        so that   x(t) ~= sum_k c_k * impulses[k](t).
        """
        # One unit rectangular pulse: height 1/delta on [0, delta), else 0.
        # np.where(condition, a, b) picks a where condition is True, else b.
        def unit_pulse(t):
            return np.where((t >= 0) & (t < delta), 1.0 / delta, 0.0)

        base_pulse = ContinuousSignal(unit_pulse)

        impulses = []
        coefficients = []
        # We cover t_k = k*delta across a window [-T, T]; T is fixed at 3 here.
        T = 3
        k_min = int(np.floor(-T / delta))
        k_max = int(np.ceil(T / delta))
        for k in range(k_min, k_max + 1):
            t_k = k * delta
            c_k = float(input_signal.func(np.array([t_k]))[0]) * delta
            impulses.append(base_pulse.shift(t_k))   # delta_D(t - t_k)
            coefficients.append(c_k)
        return impulses, coefficients

    def output_approx(self, input_signal, delta):
        # Not required in this practice -- kept as a stub.
        raise NotImplementedError


def reconstruct(impulses, coefficients):
    """Sum of c_k * impulse_k -> the staircase approximation x_hat(t)."""
    def x_hat(t):
        total = np.zeros_like(np.asarray(t, dtype=float))
        for c_k, imp in zip(coefficients, impulses):   # zip pairs the two lists
            total = total + c_k * imp.func(t)
        return total

    return ContinuousSignal(x_hat)


def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    T = 3

    # ---- Step 1: input signal x(t) = e^{-t} u(t), impulse response h(t)=u(t)
    unit_step = lambda t: np.where(t >= 0, 1.0, 0.0)
    x = ContinuousSignal(lambda t: np.exp(-t) * unit_step(t))
    h = ContinuousSignal(unit_step)          # built but not used for output here
    system = LTIContinuous(h)

    # ---- Figure 1: the input signal ----
    ax = x.plot(-T, T, 1000, "x(t), INF = 3")
    ax.figure.savefig(os.path.join(SAVE_DIR, "figure1_input.png"),
                      bbox_inches="tight", dpi=150)
    plt.close(ax.figure)

    # ---- Figure 2: components c_k * delta_D(t-t_k) and the reconstruction ----
    delta = 0.5
    impulses, coefficients = system.linear_combination_of_impulses(x, delta)
    x_hat = reconstruct(impulses, coefficients)

    # Show the components whose t_k lies in [0, ~2.5] (the visible non-zero ones)
    show = [k for k in range(len(impulses))
            if 0 <= (int(np.floor(-T / delta)) + k) * delta <= 2.5]
    n_show = len(show) + 1                    # +1 subplot for the reconstruction
    cols = 3
    rows = int(np.ceil(n_show / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(11, 2.4 * rows),
                             constrained_layout=True)
    axes = np.atleast_1d(axes).ravel()        # flatten grid into a 1-D list
    for plot_i, k in enumerate(show):
        comp = impulses[k].multiply_const_factor(coefficients[k])
        t_k = (int(np.floor(-T / delta)) + k) * delta
        comp.plot(-T, T, 1000, f"c_k * delta(t - {t_k:.1f})", ax=axes[plot_i])
        axes[plot_i].set_ylim(-0.1, 1.1)
    x_hat.plot(-T, T, 1000, "Reconstructed x_hat(t)", ax=axes[len(show)])
    axes[len(show)].set_ylim(-0.1, 1.1)
    for j in range(n_show, len(axes)):        # hide unused subplots
        axes[j].axis("off")
    fig.suptitle("Impulses multiplied by coefficients")
    fig.savefig(os.path.join(SAVE_DIR, "figure2_components.png"), dpi=150)
    plt.close(fig)

    # ---- Figure 3: reconstruction gets better as delta shrinks ----
    deltas = [0.5, 0.1, 0.05, 0.01]
    fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
    axes = axes.ravel()
    for i, d in enumerate(deltas):
        imps, coeffs = system.linear_combination_of_impulses(x, d)
        xh = reconstruct(imps, coeffs)
        xh.plot(-T, T, 2000, f"delta = {d}", ax=axes[i], label="Reconstructed")
        x.plot(-T, T, 2000, f"delta = {d}", ax=axes[i], label="x(t)")
        axes[i].legend()
    fig.savefig(os.path.join(SAVE_DIR, "figure3_varying_delta.png"), dpi=150)
    plt.close(fig)

    print("Reconstruction check (smaller delta -> smaller error):")
    t_grid = np.linspace(-T, T, 2000)
    for d in deltas:
        imps, coeffs = system.linear_combination_of_impulses(x, d)
        xh = reconstruct(imps, coeffs)
        err = float(np.max(np.abs(xh.func(t_grid) - x.func(t_grid))))
        print(f"  delta = {d:<5}  max|x_hat - x| = {err:.4f}")
    print(f"Figures saved in: {SAVE_DIR}")


if __name__ == "__main__":
    main()
