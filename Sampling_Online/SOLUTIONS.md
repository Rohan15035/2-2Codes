# Sampling — Assignment Solutions

Solutions to the two set assignments, plus six new questions in the same style
built from *Lecture 5 — Sampling* (Ashrafur Rahman, CSE BUET).

Every function below was run; the outputs quoted here are real.

Notation follows the lecture: `T = 1/fs` is the sampling period, `ws = 2*pi/T`
the sampling frequency in rad/s, `wM` the bandlimit. `np.sinc` is the
**normalised** sinc, `np.sinc(x) = sin(pi*x)/(pi*x)`, which is exactly the
`sinc(w*T/(2*pi))` of the slides when `w = 2*pi*f`.

---

# Part A — The Two Assignments

## A1. Two Tones, One Sample Set (`alias.py`)

**The idea (slides 3, 14, 18).** Sampling replicates the spectrum every `ws`:
`Xp(jw) = (1/T) * sum_k X(j(w - k*ws))`. A cosine at `f` therefore lands on the
same sample set as one at `f + k*fs` *and* at `-f + k*fs`, because the spectrum
of a real cosine has lines at both `+f` and `-f` and every one of them gets
copied. This is slide 3's "infinitely many signals, one sequence".

### Part 1 — `lowest_alias_pair(f, fs)`

With `0 < f < fs/2` the positive partners are `fs - f`, `fs + f`, `2*fs - f`, …
The smallest is `fs - f`.

Proof it works — for integer `n`:

```
cos(2*pi*(fs - f)*n/fs) = cos(2*pi*n - 2*pi*f*n/fs) = cos(2*pi*f*n/fs)
```

The two continuous-time signals are genuinely different; only their samples
coincide.

```python
def lowest_alias_pair(f, fs):
    """Smallest positive frequency other than f giving identical samples at fs.

    Assumes 0 < f < fs/2.
    """
    return fs - f
```

### Part 2 — `max_sample_difference(f1, f2, fs, duration)`

```python
def max_sample_difference(f1, f2, fs, duration):
    """Largest absolute difference between samples of two cosines."""
    n = int(duration * fs)
    t = np.arange(n) / fs
    x1 = np.cos(2 * np.pi * f1 * t)
    x2 = np.cos(2 * np.pi * f2 * t)
    return float(np.max(np.abs(x1 - x2)))
```

**Verified output** (`python alias.py`):

```
    f (Hz)    fs (Hz)   partner (Hz)     max |diff|   result
----------------------------------------------------------------
       300       1000            700      1.146e-13   identical
       100       1000            900      5.407e-14   identical
       440       8000           7560      9.559e-13   identical
        50        400            350      3.418e-14   identical
      1200       3000           1800      2.722e-13   identical
----------------------------------------------------------------
All cases produced identical samples.
```

The residual ~1e-13 is floating-point error in a phase angle of a few thousand
radians, not a difference between the signals.

---

## A2. The Staircase Droops (`zoh.py`)

**The idea (slides 23–26).** A DAC holds each sample for a full period, so
reconstruction is `xp(t)` filtered by a rectangle `h0(t) = 1` on `[0, T]`. The
lecture integrates it directly:

```
H0(jw) = (1 - e^{-jwT}) / (jw) = T * e^{-jwT/2} * sinc(w*T / (2*pi))
```

Magnitude only: `|H0(jw)| / T = |sinc(w*T/(2*pi))| = |sinc(f/fs)|`. It is 1 at
dc and falls to `2/pi ≈ 0.637` (−3.92 dB) at Nyquist — the "sinc droop" quoted
in converter datasheets.

### Part 1 — `zoh_gain(f, fs)`

```python
def zoh_gain(f, fs):
    """Predicted zero-order-hold gain at frequency f, sampling at rate fs.

    gain = |sinc(f / fs)|
    """
    return float(np.abs(np.sinc(f / fs)))
```

### Part 2 — `measured_zoh_gain(f, fs, upsample, duration)`

Sample, hold each value for `upsample` fine steps with `np.repeat` (that *is*
the staircase), then read the amplitude of the `f` bin.

```python
def measured_zoh_gain(f, fs, upsample, duration):
    """Gain of the zero-order hold, measured rather than predicted."""
    n = int(duration * fs)
    t = np.arange(n) / fs
    samples = np.cos(2 * np.pi * f * t)
    staircase = np.repeat(samples, upsample)
    return float(tone_amplitude(staircase, upsample * fs, f))
```

**Verified output** (`python zoh.py`) — matches the expected output exactly:

```
  f (Hz)    f/fs   predicted   measured    |error|      droop
------------------------------------------------------------
      50    0.05      0.9959     0.9959   4.10e-07   -0.04 dB
     100    0.10      0.9836     0.9836   1.62e-06   -0.14 dB
     200    0.20      0.9355     0.9355   6.16e-06   -0.58 dB
     300    0.30      0.8584     0.8584   1.27e-05   -1.33 dB
     450    0.45      0.6986     0.6987   2.33e-05   -3.11 dB
------------------------------------------------------------
Prediction matches measurement at every frequency.
```

---

# Part B — Six New Questions

Same shape as the two above: a short background from the lecture, a function to
write, and the solution.

## B1. Where Does It Land? — spectral folding

**Background (slides 17–18).** Undersampling folds a high frequency into the
baseband. Every `f` shows up somewhere in `[0, fs/2]`: reduce mod `fs`, then
reflect anything past `fs/2`, because the copy at `k*ws` and the
negative-frequency copy both reach into the band.

**Task.** `folded_frequency(f, fs)` — the apparent frequency in `[0, fs/2]` of a
sinusoid at `f` sampled at `fs`.

**Solution.**

```python
def folded_frequency(f, fs):
    """Apparent (baseband) frequency of a sinusoid at f sampled at fs.

    Returns a value in [0, fs/2].
    """
    r = f % fs                 # copies sit every fs
    return min(r, fs - r)      # the mirror copy folds anything past fs/2
```

**Check** — samples of `cos(2*pi*f*t)` and `cos(2*pi*folded*t)` agree to
floating-point precision:

```
  f=1200 fs=1000  ->  200 Hz   max|diff| 1.705e-13
  f= 700 fs=1000  ->  300 Hz   max|diff| 2.163e-13
  f= 500 fs=1000  ->  500 Hz   max|diff| 0.000e+00   (exactly Nyquist)
  f= 300 fs=1000  ->  300 Hz   max|diff| 0.000e+00   (no folding)
  f=2500 fs=1000  ->  500 Hz   max|diff| 0.000e+00
  f=6000 fs=8000  -> 2000 Hz   max|diff| 1.705e-13
```

The 6000 Hz / 8000 Hz row is the classic one: a 6 kHz tone recorded at 8 kHz
comes back as 2 kHz and cannot be told apart from a genuine 2 kHz tone.

---

## B2. Rate Check — Nyquist rate and the strict inequality

**Background (slide 16).** `x(t)` bandlimited to `wM` is recoverable iff
`ws > 2*wM`. The bound is **strict**: at `ws = 2*wM` neighbouring copies touch,
and a sine sampled exactly at its zero crossings disappears entirely. `2*wM` is
the *Nyquist rate* (a property of the signal); `ws/2` is the *Nyquist
frequency* (a property of the sampler).

**Task.** `nyquist_rate(f_max)` and `is_recoverable(f_max, fs)`.

**Solution.**

```python
def nyquist_rate(f_max):
    """Minimum sampling rate for a signal bandlimited to f_max."""
    return 2 * f_max


def is_recoverable(f_max, fs):
    """True iff sampling at fs allows exact reconstruction.

    Strict: fs == 2*f_max is NOT enough (slide 16, ws > 2*wM).
    """
    return fs > 2 * f_max
```

**Check.**

```
  f_max= 300  nyquist_rate= 600   fs=1000 -> True
  f_max= 500  nyquist_rate=1000   fs=1000 -> False   (equality fails)
  f_max=1200  nyquist_rate=2400   fs=1000 -> False
```

---

## B3. Putting the Sincs Back — ideal reconstruction

**Background (slides 19–22).** The ideal LPF with cutoff `wc = pi/T` and height
`T` has impulse response `h(t) = sinc(t/T)`, so

```
xr(t) = sum_n x(nT) * sinc((t - nT) / T)
```

Each sample gets a sinc centred on it, scaled by the sample value. Every sinc
is 1 at its own sample instant and 0 at all the others, so the sum passes
exactly through every sample and fills in between.

**Task.** `sinc_interpolate(samples, fs, t)` — reconstruct at arbitrary times
`t` from samples taken at rate `fs` starting at `t = 0`.

**Solution.**

```python
def sinc_interpolate(samples, fs, t):
    """Ideal band-limited reconstruction at times t.

    samples[n] is x(n/fs).  Builds sum_n x[n] * sinc(fs*t - n), the matrix
    form of xr(t) = sum_n x(nT) * sinc((t - nT)/T).
    """
    t = np.asarray(t, dtype=float)
    n = np.arange(len(samples))
    kernel = np.sinc(fs * t[:, None] - n[None, :])   # (len(t), len(samples))
    return kernel @ np.asarray(samples, dtype=float)
```

**Check** with `x(t) = cos(2*pi*60*t) + 0.5*sin(2*pi*140*t)` (bandlimited to
140 Hz, Nyquist rate 280 Hz), 8 s of samples, reconstructed in the middle of
the record:

```
 fs (Hz)       N    max |err|
     400    3200    3.543e-06
     500    4000    6.300e-05
     800    6400    6.566e-05
    1000    8000    6.089e-05
    2000   16000    3.854e-13

     250    2000    9.992e-01   <- below the Nyquist rate: reconstruction fails
```

The small residuals above Nyquist are truncation: the true sum is infinite and
`sinc` decays only as `1/t`, which is exactly why slide 22 calls the ideal
filter unrealisable. The 250 Hz row is not truncation — it is aliasing, and no
amount of extra samples fixes it.

---

## B4. The Triangle Droops Harder — first-order hold

**Background (slides 27–30).** Linear interpolation is filtering `xp(t)` with a
triangle `h1(t)` on `[-T, T]`. The triangle is two ZOH rectangles convolved, so
by the convolution property its transform is the ZOH's squared:
`H1(jw) = T * sinc^2(w*T/(2*pi))`. It therefore droops harder in the passband
but rolls off much faster outside it (slide 31) — the better low-pass
approximation.

**Task.** `foh_gain(f, fs)`, and `measured_foh_gain(f, fs, upsample, duration)`
measuring the same thing off an actual interpolated waveform.

**Solution.**

```python
def foh_gain(f, fs):
    """Predicted linear-interpolation (first-order hold) gain.

    H1 = T * sinc^2(w*T/2pi), so the gain is sinc(f/fs)**2 -- the ZOH gain
    squared, because the triangle is two rectangles convolved.
    """
    return float(np.sinc(f / fs) ** 2)


def measured_foh_gain(f, fs, upsample, duration):
    """The same gain, measured off a linearly interpolated waveform."""
    n = int(duration * fs)
    t = np.arange(n) / fs
    samples = np.cos(2 * np.pi * f * t)

    fs_fine = upsample * fs
    t_fine = np.arange(n * upsample) / fs_fine
    # period= wraps the final segment round to the first sample, which is what
    # the two-sided triangle does at the edges.
    ramp = np.interp(t_fine, t, samples, period=duration)
    return float(tone_amplitude(ramp, fs_fine, f))
```

**Check** (fs = 1000 Hz, upsample = 100, duration = 0.1 s):

```
  f (Hz)   predicted   measured    |error|      droop
      50      0.9918     0.9918   8.16e-07   -0.07 dB
     100      0.9675     0.9675   3.18e-06   -0.29 dB
     200      0.8751     0.8752   1.15e-05   -1.16 dB
     300      0.7368     0.7369   2.18e-05   -2.65 dB
     450      0.4881     0.4881   3.25e-05   -6.23 dB
```

Compare with A2: at 450 Hz the ZOH loses 3.11 dB and the triangle 6.23 dB —
exactly double, because squaring a gain doubles its value in dB.

---

## B5. Which Frequency Is Bin *k*? — the DFT's wrapped axis

**Background (slide 36).** An `N`-point DFT samples one `ws`-wide period of
`Xp(jw)` at spacing `ws/N`. For even `N`, bins `k = 0 … N/2` run from dc up to
the highest positive frequency; bins `k = N/2+1 … N-1` are the *wrapped
negative* frequencies, most negative first.

**Task.** `bin_frequency(k, N, fs)` and its inverse `bin_index(f, N, fs)`.

**Solution.**

```python
def bin_frequency(k, N, fs):
    """Physical frequency (Hz, signed) of DFT bin k."""
    signed = k if k <= N // 2 else k - N   # unwrap the top half
    return signed * fs / N


def bin_index(f, N, fs):
    """DFT bin holding frequency f (Hz, may be negative)."""
    return int(round(f * N / fs)) % N
```

**Check** (`N = 16`, `fs = 1600`, bin spacing 100 Hz):

```
k    :  0    1    2    3    4    5    6    7    8     9    10    11    12    13    14    15
f(Hz):  0  100  200  300  400  500  600  700  800  -700  -600  -500  -400  -300  -200  -100
```

A real cosine at 60 Hz with `N = 32`, `fs = 320` puts its two peak bins at
`k = 6` and `k = 26`, which map back to `+60` and `−60` Hz — the conjugate pair
every real signal must have.

---

## B6. DFT Bins Are Scaled Fourier Coefficients

**Background (slides 37–41).** For a periodic `x(t)` sampled `N` times in one
period `T0`, if the signal is bandlimited to the Nyquist band then the copied
harmonic lines do not overlap and `X[k] = N * a_k`, where `a_k` are the
Fourier-series coefficients. The DFT *is* the Fourier series, scaled.

**Task.** `series_coefficients(x)` — return `(k, a_k)` for one period of `N`
samples, with `k` ordered from most negative to most positive.

**Solution.**

```python
def series_coefficients(x):
    """Fourier-series coefficients a_k from one period of N samples.

    a_k = X[k] / N (slide 40), returned on the signed harmonic axis.
    """
    N = len(x)
    a = np.fft.fft(x) / N
    k = np.arange(N)
    k = np.where(k <= N // 2, k, k - N)   # same unwrap as B5
    order = np.argsort(k)
    return k[order], a[order]
```

**Check** with `x(t) = 3 + 2*cos(w0*t) - sin(3*w0*t)`, `N = 16` samples in one
period. By hand: `a_0 = 3`, `a_{±1} = 1`, `a_3 = +j/2`, `a_{-3} = -j/2`.
Computed:

```
   a[ -3] = +0.0000 -0.5000j
   a[ -1] = +1.0000 +0.0000j
   a[  0] = +3.0000 +0.0000j
   a[  1] = +1.0000 -0.0000j
   a[  3] = +0.0000 +0.5000j
```

All other bins are zero to machine precision — the line spectrum of slide 37,
read straight off the DFT.

---

## Quick reference

| Quantity | Formula | Slide |
|---|---|---|
| Impulse-train sampling | `xp(t) = x(t) * sum_n d(t - nT)` | 4 |
| Spectrum of the train | `P(jw) = (2*pi/T) * sum_k d(w - k*ws)` | 12 |
| Sampled spectrum | `Xp(jw) = (1/T) * sum_k X(j(w - k*ws))` | 14 |
| Nyquist condition | `ws > 2*wM` | 16 |
| Ideal LPF | `H(jw) = T` for `\|w\| < ws/2`, else 0 | 19 |
| Ideal interpolation | `xr(t) = sum_n x(nT) * sinc((t - nT)/T)` | 22 |
| Zero-order hold | `H0(jw) = T * e^{-jwT/2} * sinc(w*T/2pi)` | 25 |
| Linear interp (FOH) | `H1(jw) = T * sinc^2(w*T/2pi)` | 29 |
| DFT vs Fourier series | `X[k] = N * a_k` | 40 |
