"""
transforms.py  --  YOUR CODE GOES HERE.

The shared transform core used by BOTH tasks. Write it once; bigmul.py
(Task A) and image_conv.py (Task B) import it.

Nothing in this file may call numpy.fft, scipy.fft, numpy.convolve,
scipy.signal, or any other library routine that performs a Fourier
transform, a convolution or a correlation for you. NumPy is for array
arithmetic only.

A quick self-test you should run before touching either application:

    import numpy as np
    from transforms import DFTAnalyzer, FFTTransformer
    x = np.random.randn(64) + 1j * np.random.randn(64)
    d, f = DFTAnalyzer(), FFTTransformer()
    assert np.max(np.abs(d.transform(x) - f.transform(x))) < 1e-9
    assert np.max(np.abs(d.inverse(d.transform(x)) - x)) < 1e-9
"""

import numpy as np


def next_power_of_two(n):
    """
    Return the smallest power of two that is >= ``n`` (and at least 1).

    Both tasks need this to choose a transform length for the radix-2 FFT.
    """
    size = 1
    while size < int(n):
        size *= 2
    return size


def as_complex_vector(x):
    """Return ``x`` as a flat complex128 array."""
    return np.asarray(x, dtype=np.complex128).ravel()


class DFTAnalyzer:
    """
    The Discrete Fourier Transform, computed straight from its definition.

        Analysis:   X[k] = sum_{n=0}^{N-1} x[n] * exp(-2j*pi*k*n/N)
        Synthesis:  x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * exp(+2j*pi*k*n/N)

    How you write it is up to you -- a literal double loop, a precomputed
    table of twiddle factors indexed by (k*n) % N, or a NumPy expression --
    as long as it computes these sums directly and is not secretly an FFT.
    """

    name = "dft"

    def __init__(self):
        self._tables = {}

    def _twiddle_table(self, N, sign):
        """Table of exp(sign * 2j*pi*m/N) for m = 0 .. N-1, built once per (N, sign)."""
        key = (N, sign)
        if key not in self._tables:
            self._tables[key] = np.exp(sign * 2j * np.pi * np.arange(N) / N).tolist()
        return self._tables[key]

    def _sums(self, x, sign):
        """Evaluate the defining N-term sum for every output index."""
        values = as_complex_vector(x).tolist()
        N = len(values)
        if N <= 1:
            return np.array(values, dtype=np.complex128)

        table = self._twiddle_table(N, sign)
        out = []
        for k in range(N):
            total = 0j
            for n in range(N):
                total += values[n] * table[(k * n) % N]
            out.append(total)
        return np.array(out, dtype=np.complex128)

    def transform(self, x):
        """
        Forward DFT.

        Parameters
        ----------
        x : 1D array_like, length N (real or complex)

        Returns
        -------
        numpy.ndarray of complex128, shape (N,)
        """
        return self._sums(x, -1)

    def inverse(self, spectrum):
        """
        Inverse DFT, including the 1/N factor.

        Parameters
        ----------
        spectrum : 1D array_like, length N (complex)

        Returns
        -------
        numpy.ndarray of complex128, shape (N,)
            Do NOT discard the imaginary part here -- the caller decides when
            it is safe to take .real.
        """
        spectrum = as_complex_vector(spectrum)
        if spectrum.size <= 1:
            return spectrum.copy()
        return self._sums(spectrum, +1) / spectrum.size


class FFTTransformer(DFTAnalyzer):
    """
    Radix-2 decimation-in-time (Cooley-Tukey) FFT, in O(N log N).

    It inherits from DFTAnalyzer so that both applications can treat the two
    interchangeably: they call ``engine.transform(...)`` and
    ``engine.inverse(...)`` without caring which engine they hold.

    Requirements:
      * Recursive or iterative (with bit-reversal permutation) -- your choice.
      * N must be a power of two; raise ValueError for any other length.
        The caller is responsible for zero-padding up to next_power_of_two.
      * The inverse must reuse the same butterfly machinery (conjugated
        twiddles, or conjugate-transform-conjugate), not a second copy of it.
      * Twiddle factors for a stage are computed once per stage, never once
        per butterfly.
    """

    name = "fft"

    def __init__(self):
        DFTAnalyzer.__init__(self)
        self._orders = {}

    def _bit_reversed_order(self, N):
        """Permutation that reorders the input by bit-reversed index."""
        if N not in self._orders:
            index = np.arange(N, dtype=np.int64)
            order = np.zeros(N, dtype=np.int64)
            for bit in range(N.bit_length() - 1):
                order = (order << 1) | ((index >> bit) & 1)
            self._orders[N] = order
        return self._orders[N]

    def _butterflies(self, x, sign):
        """One iterative radix-2 Cooley-Tukey pass, without the 1/N factor."""
        a = as_complex_vector(x)
        N = a.size
        if N == 0 or N & (N - 1):
            raise ValueError("FFT length must be a power of two, got %d" % N)
        if N == 1:
            return a.copy()

        a = a[self._bit_reversed_order(N)]
        half = 1
        while half < N:
            twiddles = np.exp(sign * 1j * np.pi * np.arange(half) / half)
            blocks = a.reshape(-1, 2 * half)
            even = blocks[:, :half]
            odd = blocks[:, half:] * twiddles
            a = np.concatenate((even + odd, even - odd), axis=1).reshape(N)
            half *= 2
        return a

    def transform(self, x):
        """Forward FFT. Same contract as DFTAnalyzer.transform."""
        return self._butterflies(x, -1)

    def inverse(self, spectrum):
        """Inverse FFT, including the 1/N factor."""
        spectrum = as_complex_vector(spectrum)
        return self._butterflies(spectrum, +1) / spectrum.size


# ---------------------------------------------------------------------------
# BONUS (optional) -- arbitrary-length FFT.
#
# Delete this class if you are not attempting the bonus. If you do attempt it,
# run both tasks with --engine arbitrary and leave those output directories in
# your submission as the evidence.
# ---------------------------------------------------------------------------
class ArbitraryLengthFFT(FFTTransformer):
    """
    Bonus: an O(N log N) transform for ANY length N, not just powers of two.

    Bluestein's chirp-z algorithm is the usual route: rewrite the DFT as a
    convolution of two chirp sequences, and evaluate that convolution with a
    radix-2 FFT of length >= 2N-1. A mixed-radix Cooley-Tukey that factorises
    N is equally acceptable.

    With this engine, Task A no longer has to pad the digit arrays up to a
    power of two, and Task B no longer has to pad the image up to one.
    """

    name = "arbitrary"

    def __init__(self):
        FFTTransformer.__init__(self)
        self._chirps = {}

    def _chirp(self, N):
        """Table of exp(-1j*pi*n^2/N), with the exponent reduced modulo 2N."""
        if N not in self._chirps:
            n = np.arange(N, dtype=np.int64)
            self._chirps[N] = np.exp(-1j * np.pi * ((n * n) % (2 * N)) / N)
        return self._chirps[N]

    def transform(self, x):
        """Forward transform of any length, in O(N log N)."""
        x = as_complex_vector(x)
        N = x.size
        if N <= 1:
            return x.copy()
        if not N & (N - 1):
            return self._butterflies(x, -1)

        chirp = self._chirp(N)
        M = next_power_of_two(2 * N - 1)

        signal = np.zeros(M, dtype=np.complex128)
        signal[:N] = x * chirp

        weights = np.zeros(M, dtype=np.complex128)
        weights[:N] = chirp.conjugate()
        weights[M - N + 1:] = chirp[:0:-1].conjugate()

        spectrum = self._butterflies(signal, -1) * self._butterflies(weights, -1)
        convolved = self._butterflies(spectrum, +1)[:N] / M
        return convolved * chirp

    def inverse(self, spectrum):
        """Inverse transform of any length, including the 1/N factor."""
        spectrum = as_complex_vector(spectrum)
        if spectrum.size <= 1:
            return spectrum.copy()
        return self.transform(spectrum.conjugate()).conjugate() / spectrum.size
