# Sampling — 12 More Python Questions and Solutions

Based on *Lecture 5 — Sampling*, Ashrafur Rahman, CSE BUET.

This set extends the earlier A1–B6 assignments. Every question asks you to implement a Python function, then explains a reference solution and provides a runnable check.

Format reference: [Sampling_Online/SOLUTIONS.md](https://github.com/Rohan15035/2-2Codes/blob/main/Sampling_Online%2FSOLUTIONS.md). The linked page could not be retrieved during preparation; the structure follows the solutions text supplied in the conversation instead. Slide numbers below refer to the lecture's printed slide numbers, not PDF page positions.

## Setup

Requires Python 3 and NumPy. Run the Python blocks in document order in a notebook or concatenate them into one script. All shared imports are here; no external `tone_amplitude` helper is needed.

```python
import numpy as np
```

Notation: `fs` is in Hz, `T = 1/fs`, and `np.sinc(u) = sin(pi*u)/(pi*u)`. Array comparisons use tolerances because trigonometric calculations introduce floating-point roundoff.

---

## Q1. Where Are the Copies? — Spectral Support and Guard Bands

**Background (slides 14–19).** Sampling produces copies centered at `k*fs`. If the original spectrum occupies `[-fmax, fmax]`, copy `k` occupies `[k*fs-fmax, k*fs+fmax]`.

**Task.** Implement `spectral_layout(fmax, fs, copies)`. Return the intervals for indices `-copies` through `copies`, and a status: `separated`, `touching`, or `overlapping`. Also return the signed gap `fs-2*fmax`. Distinguish touching from overlap; neither gives the lecture's strict universal recovery guarantee.

**Solution.** Construct the copy centers as an array and subtract/add the bandlimit.

```python
def spectral_layout(fmax, fs, copies):
    if fmax < 0 or fs <= 0:
        raise ValueError("Require fmax >= 0 and fs > 0")
    if not isinstance(copies, (int, np.integer)) or copies < 0:
        raise ValueError("copies must be a nonnegative integer")
    centers = np.arange(-copies, copies + 1) * fs
    intervals = np.column_stack((centers - fmax, centers + fmax))
    gap = fs - 2 * fmax
    status = "separated" if gap > 0 else "overlapping" if gap < 0 else "touching"
    return intervals, status, gap

intervals, status, gap = spectral_layout(300, 800, 1)
np.testing.assert_array_equal(intervals, [[-1100, -500], [-300, 300], [500, 1100]])
assert (status, gap) == ("separated", 200)
assert spectral_layout(300, 600, 1)[1] == "touching"
assert spectral_layout(300, 500, 1)[1] == "overlapping"
print(status, gap)
```

**Output:** `separated 200`

The gap is between neighboring spectral supports, not the distance between their centers.

---

## Q2. Aliasing with Phase — Not Just Frequency Folding

**Background (slides 3, 18).** A zero-phase cosine folds without changing its samples. With nonzero phase, reflecting a frequency also changes the phase sign.

**Task.** Implement `fold_cosine(f, phase, fs)` for `cos(2*pi*f*t + phase)`. Return a nonnegative frequency in `[0, fs/2]` and a phase giving identical samples. Normalize the returned phase to `[-pi, pi)`.

**Solution.** First reduce the frequency modulo `fs`. If it is above Nyquist, reflect it and negate its phase, using `cos(-a+b)=cos(a-b)`.

```python
def fold_cosine(f, phase, fs):
    if fs <= 0:
        raise ValueError("fs must be positive")
    r = f % fs
    if r > fs / 2:
        r = fs - r
        phase = -phase
    phase = (phase + np.pi) % (2 * np.pi) - np.pi
    return float(r), float(phase)

fa, pa = fold_cosine(700, np.pi / 3, 1000)
n = np.arange(100)
original = np.cos(2 * np.pi * 700 * n / 1000 + np.pi / 3)
aliased = np.cos(2 * np.pi * fa * n / 1000 + pa)
np.testing.assert_allclose(original, aliased, atol=1e-11)
print(f"frequency={fa:.1f} Hz, phase={pa:.6f} rad")
```

**Output:** `frequency=300.0 Hz, phase=-1.047198 rad`

Simply replacing 700 Hz with 300 Hz while retaining the original phase generally gives different samples. At DC or Nyquist, phase is not uniquely identifiable from the samples; this function returns one valid representation.

---

## Q3. Two Tones Cancel After Sampling

**Background (slides 15–18).** Overlapping copies add algebraically. Aliasing can cause reinforcement or cancellation, not merely a misplaced frequency peak.

**Task.** Implement `sample_tones(freqs, amplitudes, phases, fs, count)`. Use it to demonstrate that `cos(2*pi*300*t) - cos(2*pi*700*t)` becomes zero when sampled at 1000 Hz.

**Solution.** Build one row per tone and sum down the rows.

```python
def sample_tones(freqs, amplitudes, phases, fs, count):
    f = np.asarray(freqs, dtype=float)
    a = np.asarray(amplitudes, dtype=float)
    p = np.asarray(phases, dtype=float)
    if f.ndim != 1 or a.shape != f.shape or p.shape != f.shape:
        raise ValueError("Tone parameters must be equal-length 1-D arrays")
    if fs <= 0 or not isinstance(count, (int, np.integer)) or count <= 0:
        raise ValueError("Require positive fs and integer count")
    t = np.arange(count) / fs
    return np.sum(a[:, None] * np.cos(2 * np.pi * f[:, None] * t + p[:, None]), axis=0)

x = sample_tones([300, 700], [1, -1], [0, 0], 1000, 100)
assert np.max(np.abs(x)) < 1e-11
print("Cancellation:", bool(np.allclose(x, 0, atol=1e-11)))
```

**Output:** `Cancellation: True`

The continuous signal is not identically zero; for example, at `t=0.0005 s` its value is about `1.1756`. Only its samples cancel.

---

## Q4. Choose a Safe Reconstruction Cutoff

**Background (slide 19).** An ideal reconstruction filter must pass the baseband and stop before the next spectral copy: `fmax < fc < fs-fmax`. Its gain is `T=1/fs`.

**Task.** Implement `reconstruction_filter(fmax, fs, fc=None)`, returning `(fc, gain)`. Default to `fs/2`; reject an unsafe sampling rate or a cutoff outside the strict interval.

**Solution.** Check the sampling condition before choosing the cutoff.

```python
def reconstruction_filter(fmax, fs, fc=None):
    if fmax < 0 or fs <= 2 * fmax:
        raise ValueError("Require fmax >= 0 and fs > 2*fmax")
    fc = fs / 2 if fc is None else fc
    if not fmax < fc < fs - fmax:
        raise ValueError("Cutoff must satisfy fmax < fc < fs-fmax")
    return float(fc), 1.0 / fs

fc, gain = reconstruction_filter(3000, 8000)
assert fc == 4000 and gain == 1 / 8000
try:
    reconstruction_filter(3000, 8000, 5500)
except ValueError:
    rejected = True
else:
    rejected = False
assert rejected
print(f"cutoff={fc:.0f} Hz, gain={gain:.6f}, unsafe cutoff rejected={rejected}")
```

**Output:** `cutoff=4000 Hz, gain=0.000125, unsafe cutoff rejected=True`

The gain cancels the `1/T` scale factor introduced by impulse-train sampling.

---

## Q5. Evaluate a Staircase at Arbitrary Times

**Background (slides 23–25).** ZOH holds sample `x[n]` on the half-open interval `[nT, (n+1)T)`.

**Task.** Implement `zoh_at(samples, fs, times)`. Return zero outside the available record, including at `len(samples)/fs`. Assume the first sample occurs at zero.

**Solution.** The active sample index is `floor(fs*t)`. A validity mask prevents negative indices from wrapping around to the end of the array.

```python
def zoh_at(samples, fs, times):
    x = np.asarray(samples, dtype=float)
    t = np.asarray(times, dtype=float)
    if x.ndim != 1 or x.size == 0 or fs <= 0:
        raise ValueError("Require nonempty 1-D samples and positive fs")
    idx = np.floor(fs * t).astype(int)
    valid = (idx >= 0) & (idx < x.size)
    safe = np.clip(idx, 0, x.size - 1)
    return np.where(valid, x[safe], 0.0)

y = zoh_at([2, -1, 3], 2, [-0.1, 0, 0.25, 0.5, 1, 1.49, 1.5])
np.testing.assert_array_equal(y, [0, 2, 2, -1, 3, 3, 0])
print(y.tolist())
```

**Output:** `[0.0, 2.0, 2.0, -1.0, 3.0, 3.0, 0.0]`

Boundary convention matters: at exactly `t=T`, sample 1 replaces sample 0. Inputs very near a boundary are subject to ordinary floating-point rounding.

---

## Q6. Implement FOH from Triangular Basis Functions

**Background (slides 27–30).** The lecture's centered interpolation kernel is `h1(t)=max(1-|t|/T, 0)`. Each sample scales a shifted triangle.

**Task.** Implement `triangle_interpolate(samples, fs, times)` without `np.interp`. Treat unavailable samples as zero. Support scalar or array evaluation times.

**Solution.** Form a matrix of distances from sampling instants. Only the two closest triangles can be nonzero between adjacent samples.

```python
def triangle_interpolate(samples, fs, times):
    x = np.asarray(samples, dtype=float)
    t = np.asarray(times, dtype=float)
    if x.ndim != 1 or x.size == 0 or fs <= 0:
        raise ValueError("Require nonempty 1-D samples and positive fs")
    distances = fs * t[..., None] - np.arange(x.size)
    weights = np.maximum(1.0 - np.abs(distances), 0.0)
    return weights @ x

y = triangle_interpolate([2, 6, 0], 2, [-0.25, 0, 0.25, 0.5, 0.75, 1])
np.testing.assert_allclose(y, [1, 2, 4, 6, 3, 0])
print(y.tolist())
```

**Output:** `[1.0, 2.0, 4.0, 6.0, 3.0, 0.0]`

The value at `-0.25 s` comes from the first triangle extending left of zero. This centered interpolator is noncausal: between two samples it requires the next sample. A real-time implementation needs delay or a different convention.

---

## Q7. Measure Tone Amplitude without an FFT-Bin Assumption

**Background (slides 25–31; numerical extension).** Reconstruction changes tone amplitude. Reading the nearest FFT bin can be inaccurate when the tone does not complete an integer number of cycles in the record.

**Task.** Implement `fit_tone(x, fs, f)` using least squares. Fit `c*cos(2*pi*f*t) + s*sin(2*pi*f*t) + dc`; return amplitude, phase, and DC offset. Require `0 < f < fs/2` and a full-rank fit.

**Solution.** Since `A*cos(theta+phi)=A*cos(phi)*cos(theta)-A*sin(phi)*sin(theta)`, amplitude is `hypot(c,s)` and phase is `atan2(-s,c)`.

```python
def fit_tone(x, fs, f):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size < 3 or fs <= 0 or not 0 < f < fs / 2:
        raise ValueError("Require 1-D data, >=3 samples, and 0 < f < fs/2")
    theta = 2 * np.pi * f * np.arange(x.size) / fs
    basis = np.column_stack((np.cos(theta), np.sin(theta), np.ones(x.size)))
    coeffs, _, rank, _ = np.linalg.lstsq(basis, x, rcond=None)
    if rank != 3:
        raise ValueError("Tone fit is rank deficient")
    c, s, dc = coeffs
    return float(np.hypot(c, s)), float(np.arctan2(-s, c)), float(dc)

t = np.arange(137) / 1000
x = 2.5 * np.cos(2 * np.pi * 73 * t + 0.4) + 1.2
amp, phase, dc = fit_tone(x, 1000, 73)
np.testing.assert_allclose([amp, phase, dc], [2.5, 0.4, 1.2], atol=1e-12)
print(f"amplitude={amp:.3f}, phase={phase:.3f}, dc={dc:.3f}")
```

**Output:** `amplitude=2.500, phase=0.400, dc=1.200`

This test contains 10.001 cycles. The method is exact up to roundoff for this single-tone-plus-DC model; other tones or noise can affect the estimate.

---

## Q8. Predict Both Gain and Phase of a ZOH Experiment

**Background (slides 25–26).** The continuous ZOH has normalized gain `sinc(f/fs)` and phase `-pi*f/fs` inside the baseband. Repeating each sample `L` times produces a fine-grid approximation, not an exact continuous waveform transform.

**Task.** Implement `held_tone_prediction(f, fs, L)` returning the continuous gain/phase and the exact gain/phase of the discrete repeat operation. Verify the latter using Q7.

**Solution.** A length-`L` discrete rectangular pulse has a geometric-series frequency response. After normalization its gain is `sinc(f/fs)/sinc(f/(L*fs))`, with delay `(L-1)/2` fine samples.

```python
def held_tone_prediction(f, fs, L):
    if fs <= 0 or not 0 < f < fs / 2:
        raise ValueError("Require 0 < f < fs/2")
    if not isinstance(L, (int, np.integer)) or L < 1:
        raise ValueError("L must be a positive integer")
    r = f / fs
    continuous = (float(np.sinc(r)), -np.pi * r)
    discrete = (float(np.sinc(r) / np.sinc(r / L)), -np.pi * r * (L - 1) / L)
    return continuous, discrete

fs, f, L = 1000, 200, 20
samples = np.cos(2 * np.pi * f * np.arange(1000) / fs)
staircase = np.repeat(samples, L)
amp, phase, _ = fit_tone(staircase, L * fs, f)
continuous, discrete = held_tone_prediction(f, fs, L)
np.testing.assert_allclose([amp, phase], discrete, atol=1e-11)
print(f"continuous: gain={continuous[0]:.4f}, phase={continuous[1]:.4f}")
print(f"repeat:     gain={amp:.4f}, phase={phase:.4f}")
```

**Output:**

```text
continuous: gain=0.9355, phase=-0.6283
repeat:     gain=0.9356, phase=-0.5969
```

The record contains whole cycles, so the tone and images are orthogonal over the measured interval. As `L` increases, the repeat-operation prediction approaches the continuous ZOH prediction.

---

## Q9. How Fast Must We Sample to Limit ZOH Droop?

**Background (slides 25–26).** Oversampling reduces passband droop because `sinc(f/fs)` approaches 1 as `f/fs` approaches zero.

**Task.** Implement `minimum_zoh_fs(fmax, max_drop_db)`. Using bisection, find the smallest rate at or above `2*fmax` whose gain at `fmax` is at least `10**(-max_drop_db/20)`. Limit this exercise to `0 < max_drop_db < 3.9`, so the answer lies strictly above `2*fmax`.

**Solution.** Above the Nyquist-rate boundary, the gain increases monotonically with `fs`. Expand an upper bound, then bisect.

```python
def minimum_zoh_fs(fmax, max_drop_db):
    if fmax <= 0 or not 0 < max_drop_db < 3.9:
        raise ValueError("Require fmax > 0 and 0 < max_drop_db < 3.9")
    target = 10 ** (-max_drop_db / 20)
    lo, hi = 2 * fmax, 4 * fmax
    while np.sinc(fmax / hi) < target:
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if np.sinc(fmax / mid) >= target:
            hi = mid
        else:
            lo = mid
    return hi

rate = minimum_zoh_fs(100, 1.0)
drop = -20 * np.log10(np.sinc(100 / rate))
assert rate > 200
np.testing.assert_allclose(drop, 1.0, atol=1e-10)
print(f"droop={drop:.6f} dB; above Nyquist={rate > 200}")
```

**Output:** `droop=1.000000 dB; above Nyquist=True`

This is a droop-only design criterion. Practical anti-aliasing and reconstruction filters introduce additional constraints.

---

## Q10. Separate DC, Nyquist, and Ordinary DFT Amplitudes

**Background (slides 36–41).** A real sinusoid normally splits across positive and negative bins. DC and the even-length Nyquist bin are their own partners and must not be doubled.

**Task.** Implement `one_sided_amplitudes(x, fs)` using `rfft`. Return frequencies and amplitudes. Handle both odd and even lengths correctly.

**Solution.** Divide by `N`, double ordinary positive-frequency bins, and leave DC and an existing Nyquist bin unchanged.

```python
def one_sided_amplitudes(x, fs):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size == 0 or fs <= 0:
        raise ValueError("Require nonempty 1-D samples and positive fs")
    N = x.size
    amp = np.abs(np.fft.rfft(x)) / N
    if N % 2 == 0:
        amp[1:-1] *= 2
    else:
        amp[1:] *= 2
    return np.fft.rfftfreq(N, d=1 / fs), amp

n = np.arange(8)
x = 3 + 2 * np.cos(2 * np.pi * n / 8) + 0.5 * (-1.0) ** n
freq, amp = one_sided_amplitudes(x, 800)
np.testing.assert_allclose(amp, [3, 2, 0, 0, 0.5], atol=1e-12)
_, odd_amp = one_sided_amplitudes(np.cos(2 * np.pi * 3 * np.arange(7) / 7), 700)
np.testing.assert_allclose(odd_amp[-1], 1.0, atol=1e-12)
print(np.round(amp, 6).tolist())
```

**Output:** `[3.0, 2.0, 0.0, 0.0, 0.5]`

These are accurate tone amplitudes for bin-centered tones with a rectangular record window. Off-bin tones leak across bins; zero-padding alone does not remove that leakage.

---

## Q11. Predict Aliased Fourier-Series Coefficients

**Background (slides 37–40).** When harmonics exceed the Nyquist band, harmonics separated by `N` merge. The general relation is `X[r]/N = sum_m a[r+m*N]`, not necessarily one original coefficient.

**Task.** Implement `aliased_coefficients(harmonics, coeffs, N)`. Return `N` complex coefficients in ordinary DFT order by adding all input harmonics modulo `N`. Check the result against an FFT of one sampled period.

**Solution.** Use `np.add.at` because ordinary indexed `+=` does not reliably accumulate repeated indices.

```python
def aliased_coefficients(harmonics, coeffs, N):
    h = np.asarray(harmonics)
    a = np.asarray(coeffs, dtype=complex)
    if not isinstance(N, (int, np.integer)) or N <= 0:
        raise ValueError("N must be a positive integer")
    if h.ndim != 1 or a.shape != h.shape or not np.issubdtype(h.dtype, np.integer):
        raise ValueError("Require integer harmonics and matching 1-D coefficients")
    result = np.zeros(N, dtype=complex)
    np.add.at(result, h % N, a)
    return result

N = 8
h = np.array([1, 9, -1, -9])
a = np.array([1, 0.5, 1, 0.5])
predicted = aliased_coefficients(h, a, N)
n = np.arange(N)
x = np.sum(a[:, None] * np.exp(2j * np.pi * h[:, None] * n / N), axis=0)
np.testing.assert_allclose(np.fft.fft(x) / N, predicted, atol=1e-12)
print(f"bin 1={predicted[1].real:.1f}, bin 7={predicted[7].real:.1f}")
```

**Output:** `bin 1=1.5, bin 7=1.5`

Harmonics 1 and 9 reinforce each other; harmonics -1 and -9 do likewise. Their individual original coefficients cannot be recovered from these eight samples alone.

---

## Q12. Reconstruct Between Samples with Fourier-Series Interpolation

**Background (slides 39–41).** For an odd-length record covering exactly one period, signed harmonic indices are unambiguous. Under the harmonic bandlimit, `a_k = X[k]/N` lets us evaluate the signal at arbitrary times.

**Task.** Implement `periodic_interpolate(samples, period, times)`. Use an FFT and the Fourier-series sum, not `np.interp`. Require odd `N` to avoid deciding how to split an even-length Nyquist coefficient. Return complex values so the function also supports complex signals.

**Solution.** `fftfreq(N)*N` supplies signed harmonic indices. Multiply each coefficient by its complex exponential and sum.

```python
def periodic_interpolate(samples, period, times):
    x = np.asarray(samples, dtype=complex)
    t = np.asarray(times, dtype=float)
    if x.ndim != 1 or x.size == 0 or x.size % 2 == 0 or period <= 0:
        raise ValueError("Require nonempty odd-length samples and positive period")
    N = x.size
    k = np.fft.fftfreq(N) * N
    a = np.fft.fft(x) / N
    return np.exp(2j * np.pi * t[..., None] * k / period) @ a

period, N = 0.2, 9
def signal(t):
    return 1 + 2 * np.cos(2 * np.pi * t / period) - 0.4 * np.sin(6 * np.pi * t / period)

samples = signal(np.arange(N) * period / N)
t = np.array([-0.013, 0.017, 0.083, 0.241])
reconstructed = periodic_interpolate(samples, period, t)
np.testing.assert_allclose(reconstructed.real, signal(t), atol=1e-12)
np.testing.assert_allclose(reconstructed.imag, 0, atol=1e-12)
print("Off-grid and outside-period reconstruction passed")
```

**Output:** `Off-grid and outside-period reconstruction passed`

The largest harmonic is 3, below `N/2=4.5`, and the samples span exactly one period without duplicating the endpoint. This method periodically extends the record. It is not a replacement for infinite sinc reconstruction of a general nonperiodic signal; if higher harmonics are present, it reconstructs the aliased trigonometric interpolant.

---

## Common Implementation Traps

| Mistake | Consequence | Correction |
|---|---|---|
| Use `linspace(0, duration, N)` with its default endpoint | Sample spacing becomes `duration/(N-1)` | Use `arange(N)/fs` |
| Treat `np.sinc(x)` as `sin(x)/x` | Wrong scale in interpolation and hold gains | Remember the factor of pi |
| Reflect cosine frequency but keep arbitrary phase | Different sample sequence | Negate phase when reflecting |
| Double every `rfft` bin | Wrong DC and Nyquist amplitudes | Special-case self-conjugate bins |
| Treat touching spectral supports as guaranteed safe | Nyquist-edge sine can disappear | Apply the lecture's strict inequality |
| Assume passing through samples guarantees analog recovery | Aliased and distorted signals can fit all samples | State bandlimit and reconstruction assumptions |
| Assume a finite repeated array exactly equals a continuous ZOH transform | Small gain and phase discrepancy | Use Q8's finite-grid prediction |

## Verification

All 12 exercise checks were executed together using the Python blocks in this document. Printed outputs were checked against the displayed values. The assertions test numerical results, phase-aware aliasing, cancellation, invalid cutoff rejection, odd/even DFT handling, and off-grid periodic reconstruction.
