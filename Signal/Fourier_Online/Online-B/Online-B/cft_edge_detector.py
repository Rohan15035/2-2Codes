import numpy as np
import matplotlib.pyplot as plt
from imageio.v2 import imread
import sys


# =====================================================================
# Given classes — paste your Task 2 implementations where indicated
# =====================================================================

class ContinuousImage:
    """Represents a grayscale image as a continuous 2D spatial signal. (Given)"""

    def __init__(self, image_path):
        self.image = imread(image_path, mode='L').astype(float)
        self.image = self.image / np.max(self.image)
        self.x = np.linspace(-1, 1, self.image.shape[1])
        self.y = np.linspace(-1, 1, self.image.shape[0])


class CFT2D:
    """2D Continuous Fourier Transform. (Given — paste your Task 2 solution)"""

    def __init__(self, image_obj: ContinuousImage):
        self.I = image_obj.image
        self.x = image_obj.x
        self.y = image_obj.y
        dx = self.x[1] - self.x[0]
        dy = self.y[1] - self.y[0]
        self.u = np.linspace(-1 / (2 * dx), 1 / (2 * dx), self.I.shape[1])
        self.v = np.linspace(-1 / (2 * dy), 1 / (2 * dy), self.I.shape[0])

    def compute_cft(self):
        """Separable trapezoidal evaluation of the 2D CFT (O(N^3), no FFT)."""
        n_y, n_x = self.I.shape
        n_u = len(self.u)
        n_v = len(self.v)

        # Stage 1: integrate over x for every (y, u) pair.
        Ac = np.empty((n_y, n_u))
        As = np.empty((n_y, n_u))
        for j in range(n_u):
            phase_x = 2.0 * np.pi * self.u[j] * self.x
            Ac[:, j] = np.trapezoid(self.I * np.cos(phase_x), self.x, axis=1)
            As[:, j] = np.trapezoid(self.I * np.sin(phase_x), self.x, axis=1)

        # Stage 2: integrate over y for every (u, v) pair.
        real = np.empty((n_v, n_u))
        imag = np.empty((n_v, n_u))
        for i in range(n_v):
            phase_y = 2.0 * np.pi * self.v[i] * self.y
            cos_vy = np.cos(phase_y)[:, np.newaxis]
            sin_vy = np.sin(phase_y)[:, np.newaxis]

            real[i, :] = np.trapezoid(Ac * cos_vy - As * sin_vy, self.y, axis=0)
            imag[i, :] = -np.trapezoid(As * cos_vy + Ac * sin_vy, self.y, axis=0)

        return real, imag

    def plot_magnitude(self):
        real, imag = self.compute_cft()
        magnitude = np.sqrt(real ** 2 + imag ** 2)

        plt.imshow(np.log(1 + magnitude), cmap='inferno',
                   extent=[self.u[0], self.u[-1], self.v[0], self.v[-1]],
                   origin='lower', aspect='auto')
        plt.title("2D CFT Magnitude Spectrum (log-scaled)")
        plt.axis('off')
        plt.show()


class InverseCFT2D:
    """Inverse 2D-CFT. (Given — paste your Task 2 solution)"""

    def __init__(self, real, imag, u, v, x, y):
        self.real = real
        self.imag = imag
        self.u = u
        self.v = v
        self.x = x
        self.y = y

    def reconstruct(self):
        """Separable trapezoidal evaluation of the inverse 2D CFT."""
        n_y = len(self.y)
        n_x = len(self.x)
        n_u = len(self.u)

        # Stage 1: integrate over v for every (y, u) pair.
        Pc = np.empty((n_y, n_u))
        Ps = np.empty((n_y, n_u))
        for i in range(n_y):
            phase_v = 2.0 * np.pi * self.v * self.y[i]
            cos_vy = np.cos(phase_v)[:, np.newaxis]
            sin_vy = np.sin(phase_v)[:, np.newaxis]

            Pc[i, :] = np.trapezoid(self.real * cos_vy - self.imag * sin_vy, self.v, axis=0)
            Ps[i, :] = np.trapezoid(self.real * sin_vy + self.imag * cos_vy, self.v, axis=0)

        # Stage 2: integrate over u for every (x, y) pair, keeping the real part.
        image = np.empty((n_y, n_x))
        for j in range(n_x):
            phase_u = 2.0 * np.pi * self.u * self.x[j]
            image[:, j] = np.trapezoid(Pc * np.cos(phase_u) - Ps * np.sin(phase_u),
                                       self.u, axis=1)

        return image


# =====================================================================
# Task 1 — band_pass and band_stop filters
# =====================================================================

class FrequencyFilter:

    def high_pass(self, real, imag, cutoff):
        """Given."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real = real.copy()
        imag = imag.copy()
        for i in range(rows):
            for j in range(cols):
                if np.sqrt((i - cx) ** 2 + (j - cy) ** 2) <= cutoff:
                    real[i, j] = 0
                    imag[i, j] = 0
        return real, imag

    def band_pass(self, real, imag, r_low, r_high):
        """Retain entries with r_low < d(i,j) <= r_high, zero the rest."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real = real.copy()
        imag = imag.copy()
        for i in range(rows):
            for j in range(cols):
                d = np.sqrt((i - cx) ** 2 + (j - cy) ** 2)
                if not (r_low < d <= r_high):
                    real[i, j] = 0
                    imag[i, j] = 0
        return real, imag

    def band_stop(self, real, imag, r_low, r_high):
        """Zero entries with r_low < d(i,j) <= r_high, retain the rest."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real = real.copy()
        imag = imag.copy()
        for i in range(rows):
            for j in range(cols):
                d = np.sqrt((i - cx) ** 2 + (j - cy) ** 2)
                if r_low < d <= r_high:
                    real[i, j] = 0
                    imag[i, j] = 0
        return real, imag

    def shift_brightness(self, real, imag, shift_amount):
        """Task 3. Add shift_amount to the real component of the exact center pixel."""
        rows, cols = real.shape
        cx, cy = rows // 2, cols // 2
        real = real.copy()
        imag = imag.copy()
        real[cx, cy] += shift_amount
        return real, imag


# =====================================================================
# Task 2 — complementarity check on raw spatial reconstructions
# =====================================================================

class ReconstructionValidator:

    def verify_complementarity(self, I_recon, I_bp, I_bs):
        """delta = max |I_bp + I_bs - I_recon|; valid when delta < 1e-9."""
        delta = np.max(np.abs(I_bp + I_bs - I_recon))
        is_valid = bool(delta < 1e-9)
        return is_valid, delta


# =====================================================================
# Entry point (given — do not modify)
# =====================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cft_edge_detector.py <input_image>")
        sys.exit(1)

    input_path = sys.argv[1]
    r_low, r_high = 10, 50

    img   = ContinuousImage(input_path)
    cft2d = CFT2D(img)
    real, imag = cft2d.compute_cft()

    filt = FrequencyFilter()
    real_bp, imag_bp = filt.band_pass(real, imag, r_low, r_high)
    real_bs, imag_bs = filt.band_stop(real, imag, r_low, r_high)

    def reconstruct(r, im):
        return InverseCFT2D(r, im, cft2d.u, cft2d.v, img.x, img.y).reconstruct()

    I_recon = reconstruct(real,    imag)
    I_bp    = reconstruct(real_bp, imag_bp)
    I_bs    = reconstruct(real_bs, imag_bs)

    validator = ReconstructionValidator()
    is_valid, delta = validator.verify_complementarity(I_recon, I_bp, I_bs)
    print(f"Complementarity check: {is_valid} | max delta: {delta:.2e}")

    def save_edge_map(I_raw, path):
        edge_map = np.abs(I_raw)
        if edge_map.max() > 0:
            edge_map = edge_map / edge_map.max()
        plt.imsave(path, 1 - edge_map, cmap='gray')
        print(f"Saved {path}")

    save_edge_map(I_bp, "pikachu_bandpass.png")
    save_edge_map(I_bs, "pikachu_bandstop.png")

    # Task 3 execution
    real_shifted, imag_shifted = filt.shift_brightness(real, imag, shift_amount=2.0)
    I_brightened = reconstruct(real_shifted, imag_shifted)
    
    # Save brightened image (clip to [0,1], no edge-map inversion)
    I_brightened_clipped = np.clip(I_brightened, 0, 1)
    plt.imsave("pikachu_brightened.png", I_brightened_clipped, cmap='gray')
    print("Saved pikachu_brightened.png")
