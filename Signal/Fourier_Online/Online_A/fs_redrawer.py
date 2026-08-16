import numpy as np

from svg_utils import load_svg_path
from epicycle_animation import plot_comparison


class FourierEpicycles:
    def __init__(self, t, signal, n_harmonics):
        """
        Step 1: Store the sampled signal and set up everything the other
        methods will need.

        Parameters
        ----------
        t : 1D numpy array, shape (M,)
            Uniformly spaced sample times covering ONE FULL PERIOD of the
            signal, as a *closed* interval: t[0] == 0 and t[-1] == T (the
            period). This is exactly what svg_utils.load_svg_path(...)
            returns.
        signal : 1D complex numpy array, shape (M,)
            signal[i] = f(t[i]) = x(t[i]) + 1j * y(t[i]). Periodic, so
            signal[-1] == signal[0].
        n_harmonics : int (call it N)
            The series will use every integer harmonic n with
            -N <= n <= N (i.e. 2N+1 terms in total -- do not forget the
            negative harmonics).

        You must set at least the following attributes, since the rest of
        this class (and the provided plotting/animation code) expects
        them to exist:
            self.t, self.signal, self.N
            self.T      -- the period (a float)
            self.omega  -- the fundamental angular frequency, 2*pi/T
            self.coeffs -- an (initially empty) dict that will map
                           n -> c_n once calculate_all_coefficients() has
                           been called
        """
        self.t = np.asarray(t, dtype=float)
        self.signal = np.asarray(signal, dtype=complex)
        self.N = int(n_harmonics)

        self.T = float(self.t[-1] - self.t[0])
        self.omega = 2.0 * np.pi / self.T

        self.coeffs = {}

    def calculate_cn(self, n):
        """
        Step 2: Compute a single complex Fourier coefficient c_n using
        numerical integration (np.trapezoid) over the stored samples
        self.t, self.signal.

            c_n = (1/T) * integral_0^T  f(t) * exp(-j*n*omega*t)  dt

        n may be zero, positive, or negative.
        """
        kernel = np.exp(-1j * n * self.omega * self.t)
        return np.trapezoid(self.signal * kernel, self.t) / self.T

    def calculate_all_coefficients(self):
        """
        Step 3: Populate self.coeffs with c_n for every harmonic
        n = -N, ..., -1, 0, 1, ..., N by repeatedly calling calculate_cn(n).
        """
        self.coeffs = {}
        for n in range(-self.N, self.N + 1):
            self.coeffs[n] = self.calculate_cn(n)

        # Pristine snapshot of the full 2N+1 spectrum. Pruning is destructive
        # (it zeroes coefficients in self.coeffs), so keeping the originals
        # here lets prune_harmonics_by_energy() be called repeatedly with
        # different target ratios without recomputing every integral.
        self.full_coeffs = dict(self.coeffs)
        return self.coeffs

    def approximate(self, t):
        """
        Step 4: Reconstruct (an approximation of) the signal at time(s) t
        from the coefficients already stored in self.coeffs:

            f_hat(t) = sum_{n=-N}^{N} c_n * exp(j*n*omega*t)

        t may be a single number or a numpy array of times -- your
        implementation must support both, since the provided
        plotting/animation code calls this both ways.
        """
        t_arr = np.asarray(t, dtype=float)
        f_hat = np.zeros(t_arr.shape, dtype=complex)

        for n, c_n in self.coeffs.items():
            f_hat = f_hat + c_n * np.exp(1j * n * self.omega * t_arr)

        return f_hat[()]

    def prune_harmonics_by_energy(self, energy_ratio):
        """
        Task 1: Energy-preserving harmonic pruning.

        The total energy of the signal in terms of its Fourier coefficients is

            E_total = sum_{n=-N}^{N} |c_n|^2

        Given a target ratio r in (0, 1], keep the *smallest* set of the most
        energetic harmonics whose cumulative energy is at least r * E_total,
        and set every discarded coefficient to zero.

        Pruning always restarts from the full spectrum captured by
        calculate_all_coefficients(), so this may be called several times in a
        row with different targets.

        Parameters
        ----------
        energy_ratio : float in (0, 1]
            Fraction r of the total energy that must be preserved.

        Returns
        -------
        (retained, actual_ratio) : (int, float)
            How many non-zero harmonics survived, and the fraction of the
            total energy those harmonics actually carry.
        """
        r = float(energy_ratio)
        if r <= 0.0 or r > 1.0:
            raise ValueError("energy_ratio must be in (0, 1]")

        # Always start from the untouched spectrum, never from an
        # already-pruned one.
        source = self.full_coeffs

        # Step 1: energy of every harmonic, E_n = |c_n|^2, and their sum.
        energies = {}
        total = 0.0
        for n in source:
            energies[n] = abs(source[n]) ** 2
            total += energies[n]

        if total == 0.0:            # all-zero signal: nothing worth keeping
            self.coeffs = {}
            for n in source:
                self.coeffs[n] = 0j
            return 0, 0.0

        # Step 2: list the harmonics with the most energetic one first.
        ranked = sorted(energies, key=lambda n: energies[n], reverse=True)

        # Step 3: walk down that list, keeping harmonics until the energy
        # collected reaches the target. If round-off keeps the running sum a
        # hair below the target (possible when r == 1.0), the loop simply
        # runs out of harmonics and every one of them is kept.
        target = r * total
        kept = []
        kept_energy = 0.0
        for n in ranked:
            kept.append(n)
            kept_energy += energies[n]
            if kept_energy >= target:
                break

        # Step 4: zero everything, then write the survivors back unchanged.
        self.coeffs = {}
        for n in source:
            self.coeffs[n] = 0j          # 0j is just complex zero
        for n in kept:
            self.coeffs[n] = source[n]

        return len(kept), kept_energy / total

    def evaluate_reconstruction_error(self):
        """
        Task 2: Mean squared reconstruction error.

            MSE = (1/M) * sum_{i=1}^{M} |f(t_i) - f_hat(t_i)|^2

        f is the ground-truth sampled signal and f_hat is the reconstruction
        produced by approximate() from whatever coefficients are currently
        stored in self.coeffs (so calling this after pruning measures the
        pruned reconstruction).

        Returns
        -------
        float : the MSE (a real, non-negative number).
        """
        f_hat = self.approximate(self.t)
        squared_errors = np.abs(self.signal - f_hat) ** 2
        return float(np.mean(squared_errors))


if __name__ == "__main__":
    import sys
    from pathlib import Path

    import matplotlib.pyplot as plt

    # Usage: python3 fs_redrawer.py [path_to_svg] [n_harmonics]
    svg_path = sys.argv[1] if len(sys.argv) > 1 else "svgs/heart.svg"
    N_HARMONICS = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    stem = Path(svg_path).stem

    TARGET_RATIOS = [0.96, 0.98, 0.99, 1.00]

    t, z = load_svg_path(svg_path, num_points=1000)
    fs = FourierEpicycles(t, z, n_harmonics=N_HARMONICS)
    fs.calculate_all_coefficients()

    print(f"{svg_path}  (N = {N_HARMONICS}, {2 * N_HARMONICS + 1} harmonics, "
          f"{len(t)} samples)")
    print()
    print("Target Ratio | Harmonics Retained | Actual Energy Ratio | MSE")
    print("-" * 66)

    saved = []
    for r in TARGET_RATIOS:
        retained, actual_ratio = fs.prune_harmonics_by_energy(r)
        mse = fs.evaluate_reconstruction_error()

        print(f"{r:12.2f} | {retained:18d} | {actual_ratio:19.4f} | {mse:.6e}")

        fig, ax = plt.subplots(figsize=(5, 5))
        plot_comparison(fs, z, ax=ax)
        # plot_comparison labels the reconstruction with the full N; after
        # pruning only `retained` of those harmonics are actually non-zero.
        ax.get_lines()[1].set_label(f"Reconstruction ({retained} harmonics)")
        ax.legend(loc="upper right")
        ax.set_title(f"Pruned to r = {r:.2f}\n"
                     f"{retained} / {2 * N_HARMONICS + 1} harmonics, "
                     f"actual energy = {actual_ratio:.4f}, MSE = {mse:.3e}",
                     fontsize=9)
        out_path = f"{stem}_pruned_{r:.2f}.png"
        fig.tight_layout()
        fig.savefig(out_path, dpi=120)
        plt.close(fig)
        saved.append(out_path)

    print()
    print("Saved:")
    for out_path in saved:
        print(f"  {out_path}")
