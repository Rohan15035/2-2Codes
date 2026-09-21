# Sampling — Additional Questions and Worked Answers

Fresh questions based on **Lecture 5 — Sampling** by Ashrafur Rahman (CSE, BUET).
These extend the earlier assignment set rather than repeating it.

Notation used throughout:

- `T` = sampling period, so `f_s = 1/T`
- `ω_s = 2π/T = 2πf_s`
- `ω_M` = highest angular frequency present in the signal
- `sinc(x) = sin(πx)/(πx)`
- `x[n] = x(nT)`

---

# Part C — New Questions and Answers

## C1. From Time-Domain Multiplication to Spectral Copies

### Question

An analog signal `x(t)` is sampled using

```math
p(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT),
\qquad x_p(t)=x(t)p(t).
```

Derive the spectrum `X_p(jω)` in terms of `X(jω)`. Explain the physical meaning of the result.

### Answer

Because multiplication in time corresponds to convolution in frequency,

```math
X_p(j\omega)=\frac{1}{2\pi}\left[X(j\omega)*P(j\omega)\right].
```

The Fourier transform of the impulse train is

```math
P(j\omega)=\frac{2\pi}{T}\sum_{k=-\infty}^{\infty}
\delta(\omega-k\omega_s),
\qquad \omega_s=\frac{2\pi}{T}.
```

Therefore,

```math
\begin{aligned}
X_p(j\omega)
&=\frac{1}{2\pi}X(j\omega)*
\left[\frac{2\pi}{T}\sum_k\delta(\omega-k\omega_s)\right]\\
&=\frac{1}{T}\sum_{k=-\infty}^{\infty}
X\!\left(j(\omega-k\omega_s)\right).
\end{aligned}
```

So sampling creates infinitely many copies of `X(jω)`:

- their centers are `0, ±ω_s, ±2ω_s, ...`;
- adjacent copies are separated by `ω_s`;
- each copy is scaled by `1/T`.

This is the central observation behind the sampling theorem.

---

## C2. Why Does the Impulse Train Have Equal Fourier-Series Coefficients?

### Question

For the periodic impulse train

```math
p(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT),
```

show that every complex Fourier-series coefficient is `1/T`.

### Answer

For a period-`T` signal,

```math
c_k=\frac{1}{T}\int_{-T/2}^{T/2}p(t)e^{-jk\omega_s t}\,dt.
```

Exactly one impulse, `δ(t)`, lies in the selected period. Hence,

```math
c_k=\frac{1}{T}\int_{-T/2}^{T/2}
\delta(t)e^{-jk\omega_s t}\,dt
=\frac{1}{T}e^0
=\frac{1}{T}.
```

Thus,

```math
p(t)=\frac{1}{T}\sum_{k=-\infty}^{\infty}e^{jk\omega_s t}.
```

Every harmonic has the same coefficient because an ideal impulse has equal contribution at all frequencies.

---

## C3. Determine Whether Spectral Copies Overlap

### Question

A signal is bandlimited to `4 kHz`.

1. What is its Nyquist rate?
2. Do spectral copies overlap if it is sampled at `10 kHz`?
3. What is the guard-band width between neighboring copies?
4. What happens if the sampling rate is reduced to `7 kHz`?

### Answer

The maximum signal frequency is

```math
f_M=4\text{ kHz}.
```

1. The Nyquist rate is

   ```math
   2f_M=8\text{ kHz}.
   ```

2. At `f_s = 10 kHz`,

   ```math
   f_s>2f_M,
   ```

   so the copies do not overlap.

3. The baseband copy ends at `4 kHz`. The next copy, centered at `10 kHz`, begins at

   ```math
   f_s-f_M=10-4=6\text{ kHz}.
   ```

   Hence the guard band is

   ```math
   6-4=2\text{ kHz}.
   ```

   Equivalently, guard-band width is `f_s - 2f_M`.

4. At `f_s = 7 kHz`, the next copy begins at

   ```math
   7-4=3\text{ kHz}.
   ```

   It overlaps the original band from `3 kHz` to `4 kHz`. Aliasing occurs, and ideal low-pass filtering cannot recover the original signal.

---

## C4. Design the Ideal Reconstruction Filter

### Question

A signal is bandlimited to `3 kHz` and sampled at `8 kHz`.

1. Find the valid range of cutoff frequencies for an ideal reconstruction LPF.
2. State the conventional cutoff used in the lecture.
3. State the required passband gain.

### Answer

The baseband signal occupies `|f| ≤ 3 kHz`. The nearest shifted copy begins at

```math
f_s-f_M=8-3=5\text{ kHz}.
```

Therefore, any cutoff satisfying

```math
3\text{ kHz}<f_c<5\text{ kHz}
```

can isolate the baseband copy.

The conventional midpoint choice is

```math
f_c=\frac{f_s}{2}=4\text{ kHz}.
```

Because sampling scaled every spectral copy by `1/T`, the filter must have gain

```math
T=\frac{1}{f_s}=\frac{1}{8000}\text{ s}
```

inside its passband to restore the original spectrum.

---

## C5. Why Must the Reconstruction Filter Have Gain `T`?

### Question

Why is a unity-gain ideal low-pass filter not sufficient for exact reconstruction from `x_p(t)`?

### Answer

The central copy in the sampled spectrum is not `X(jω)` itself. It is

```math
\frac{1}{T}X(j\omega).
```

If a unity-gain LPF isolates it, the output spectrum remains `X(jω)/T`. To undo the sampling scale factor, the LPF must multiply the baseband by `T`:

```math
T\cdot\frac{1}{T}X(j\omega)=X(j\omega).
```

Thus the ideal reconstruction response is

```math
H(j\omega)=
\begin{cases}
T, & |\omega|<\omega_c,\\
0, & |\omega|>\omega_c.
\end{cases}
```

---

## C6. Prove That Sinc Interpolation Passes Through Every Sample

### Question

Ideal reconstruction is

```math
x_r(t)=\sum_{n=-\infty}^{\infty}x(nT)
\operatorname{sinc}\!\left(\frac{t-nT}{T}\right).
```

Prove that `x_r(mT) = x(mT)` for every integer `m`.

### Answer

Set `t = mT`:

```math
x_r(mT)=\sum_{n=-\infty}^{\infty}x(nT)
\operatorname{sinc}(m-n).
```

For integers,

```math
\operatorname{sinc}(m-n)=
\begin{cases}
1, & m=n,\\
0, & m\ne n.
\end{cases}
```

Every term vanishes except the term with `n=m`. Therefore,

```math
x_r(mT)=x(mT).
```

This is why each shifted sinc contributes its own sample value at its center but contributes zero at every other sampling instant.

---

## C7. A Sampled Sine Disappears

### Question

Let

```math
x(t)=\sin(2\pi\cdot500t).
```

The signal is sampled at `f_s = 1000 Hz`, starting at `t=0`.

1. Find `x[n]`.
2. Why does this demonstrate the danger of sampling exactly at the Nyquist rate?
3. Would a phase-shifted 500 Hz cosine necessarily disappear?

### Answer

Since `T=1/1000`,

```math
x[n]=\sin\left(2\pi\cdot500\frac{n}{1000}\right)
=\sin(\pi n)=0.
```

The entire sample sequence is zero, even though the analog signal is not zero. Therefore the samples do not uniquely identify the signal.

This is why the lecture states the safe condition as the strict inequality

```math
f_s>2f_M.
```

A cosine does not necessarily disappear:

```math
\cos(\pi n)=(-1)^n.
```

More generally, at exactly the Nyquist frequency the observed sequence depends critically on phase. That phase sensitivity prevents a universal recovery guarantee.

---

## C8. Find Every Analog Tone Consistent with a Sampled Tone

### Question

A discrete-time cosine has normalized angular frequency

```math
\Omega=0.4\pi
```

and was produced by sampling at `f_s = 2000 Hz`. Find the analog frequencies that can generate exactly the same cosine samples. Give the first four nonnegative possibilities.

### Answer

The basic physical frequency is

```math
f_0=\frac{\Omega}{2\pi}f_s
=\frac{0.4\pi}{2\pi}(2000)
=400\text{ Hz}.
```

For a cosine, identical samples occur for

```math
f=|kf_s\pm f_0|,
\qquad k\in\mathbb Z.
```

The first four nonnegative frequencies are

```math
400,\quad 1600,\quad 2400,\quad 3600\text{ Hz}.
```

For example,

```math
\cos\left(2\pi\frac{1600}{2000}n\right)
=\cos(1.6\pi n)
=\cos(2\pi n-0.4\pi n)
=\cos(0.4\pi n).
```

Without a bandlimit assumption, the samples alone cannot reveal which analog frequency was present.

---

## C9. Explain the ZOH Phase Factor

### Question

The zero-order-hold response is

```math
H_0(j\omega)=T e^{-j\omega T/2}
\operatorname{sinc}\!\left(\frac{\omega T}{2\pi}\right).
```

What does the factor `e^{-jωT/2}` mean physically? Does it affect the magnitude droop?

### Answer

A linear phase factor

```math
e^{-j\omega t_0}
```

represents a time delay of `t_0`. Therefore `e^{-jωT/2}` represents a delay of `T/2`.

It appears because the ZOH rectangle occupies `[0,T]` and is centered at `T/2`, not at zero.

Its magnitude is

```math
|e^{-j\omega T/2}|=1,
```

so it does not cause amplitude droop. The droop comes entirely from the sinc factor. The delay changes phase only.

---

## C10. Compare ZOH and FOH at a Given Frequency

### Question

A `1 kHz` sampler reconstructs a `400 Hz` sinusoid.

1. Calculate the normalized ZOH gain.
2. Calculate the normalized first-order-hold gain.
3. Convert both to decibels.
4. Which has the flatter in-band amplitude response?

### Answer

Here,

```math
\frac{f}{f_s}=0.4.
```

The ZOH gain is

```math
G_{ZOH}=|\operatorname{sinc}(0.4)|
=\frac{\sin(0.4\pi)}{0.4\pi}
\approx0.7568.
```

The FOH gain is

```math
G_{FOH}=\operatorname{sinc}^2(0.4)
\approx0.5728.
```

In decibels,

```math
20\log_{10}(0.7568)\approx-2.42\text{ dB},
```

```math
20\log_{10}(0.5728)\approx-4.84\text{ dB}.
```

Thus ZOH has the flatter passband amplitude at this frequency. FOH attenuates high-frequency images faster outside the baseband, but its in-band sinc-squared droop is stronger. “Smoother in time” does not mean “flatter in-band magnitude.”

---

## C11. Why Is FOH a Better Low-Pass Approximation Yet More Droopy?

### Question

The lecture calls linear interpolation a better low-pass approximation than ZOH, even though FOH has greater attenuation near Nyquist. Resolve this apparent contradiction.

### Answer

The two statements concern different desired properties:

- **Passband flatness:** ZOH is better because `|sinc(f/f_s)|` falls less than `sinc²(f/f_s)`.
- **Suppression of unwanted spectral images:** FOH is better because the squared sinc rolls off faster outside the baseband.
- **Time-domain smoothness:** FOH joins adjacent samples continuously with straight lines, whereas ZOH creates abrupt steps.

Therefore FOH looks smoother and rejects high-frequency images more strongly, but it also causes more in-band amplitude droop. A practical system may compensate this droop with an equalizer.

---

## C12. Anti-Aliasing Filter Design

### Question

A sensor contains useful frequencies from `0` to `3.2 kHz`, but it also contains noise above that range. An ADC samples at `8 kHz`.

1. What is the Nyquist frequency of the ADC?
2. Why is an analog anti-aliasing filter needed before sampling?
3. Where should its transition band lie?

### Answer

1. The Nyquist frequency is

   ```math
   \frac{f_s}{2}=4\text{ kHz}.
   ```

2. Any analog energy above `4 kHz` can fold into `0–4 kHz`. Once folded, it becomes inseparable from genuine baseband content; a digital filter after sampling cannot undo the mixing.

3. The filter should preserve the useful band through `3.2 kHz` and strongly attenuate by `4 kHz`. Hence its transition band is approximately

   ```math
   3.2\text{ kHz}<f<4\text{ kHz}.
   ```

The `0.8 kHz` gap is the engineering transition band. This is one reason practical systems sample above the theoretical minimum: a realizable analog filter cannot change from full pass to full stop instantaneously.

---

## C13. Why Real Captures Are Never Strictly Bandlimited

### Question

The lecture says a signal cannot be both exactly time-limited and strictly bandlimited. What does this imply for real measurements and the sampling theorem?

### Answer

A finite recording window makes the signal time-limited. Abruptly beginning and ending a signal is equivalent to multiplying it by a finite-duration window. Multiplication in time becomes convolution in frequency, spreading the spectrum and producing tails that extend indefinitely.

Therefore real finite captures are not perfectly bandlimited, so some spectral overlap is theoretically unavoidable. In practice we make aliasing small rather than exactly zero by using:

- an analog anti-aliasing filter;
- a sufficiently high sampling rate;
- a guard band;
- suitable windowing when performing spectral analysis.

The ideal theorem is still the design foundation, but practical systems satisfy it approximately.

---

## C14. DTFT Periodicity in Physical Frequency

### Question

Starting from

```math
X_p(j\omega)=\sum_{n=-\infty}^{\infty}x[n]e^{-j\omega nT},
```

prove that `X_p(jω)` is periodic with period `ω_s = 2π/T`.

### Answer

Evaluate the spectrum at `ω+ω_s`:

```math
\begin{aligned}
X_p(j(\omega+\omega_s))
&=\sum_n x[n]e^{-j(\omega+\omega_s)nT}\\
&=\sum_n x[n]e^{-j\omega nT}e^{-j\omega_s nT}.
\end{aligned}
```

Since `ω_sT=2π`,

```math
e^{-j\omega_s nT}=e^{-j2\pi n}=1
```

for every integer `n`. Thus,

```math
X_p(j(\omega+\omega_s))=X_p(j\omega).
```

Under the normalized substitution `Ω=ωT`, the period becomes `2π`, which is the familiar DTFT periodicity.

---

## C15. DFT Bin Frequencies and the Nyquist Bin

### Question

An `N=8` point DFT is calculated from samples taken at `f_s=800 Hz`.

1. List the signed physical frequency of every bin.
2. Which bin represents the Nyquist frequency?
3. Why is that bin special for a real signal?

### Answer

The bin spacing is

```math
\Delta f=\frac{f_s}{N}=100\text{ Hz}.
```

For even `N`, bins `0` through `N/2` are read as nonnegative frequencies, while the remaining bins wrap to negative frequencies:

| Bin `k` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Frequency (Hz) | 0 | 100 | 200 | 300 | 400 | -300 | -200 | -100 |

Bin `k=N/2=4` is the Nyquist bin at `400 Hz`.

Positive and negative Nyquist frequencies produce the same sample sequence because

```math
e^{j\pi n}=e^{-j\pi n}=(-1)^n.
```

So the Nyquist bin is its own negative-frequency partner. For a real sequence, its DFT value must therefore be real, just like the DC bin.

---

## C16. Frequency Resolution Versus Sampling Rate

### Question

Two recordings use `N=1000` DFT points.

- Recording A: `f_s=10 kHz`
- Recording B: `f_s=20 kHz`

Compare their Nyquist frequencies and DFT bin spacings. Does the larger sampling rate automatically give better frequency resolution when `N` is fixed?

### Answer

For Recording A,

```math
f_N=5\text{ kHz},
\qquad \Delta f=\frac{10000}{1000}=10\text{ Hz}.
```

For Recording B,

```math
f_N=10\text{ kHz},
\qquad \Delta f=\frac{20000}{1000}=20\text{ Hz}.
```

Recording B covers a wider analog frequency range, but its bins are farther apart. Thus increasing `f_s` while keeping `N` fixed makes frequency resolution coarser, not finer.

Since the observation duration is `T_0=N/f_s`,

```math
\Delta f=\frac{f_s}{N}=\frac{1}{T_0}.
```

Frequency resolution is improved by observing for longer, equivalently by increasing `N` without proportionally increasing `f_s`.

---

## C17. Recover Fourier-Series Coefficients from DFT Bins

### Question

The periodic signal

```math
x(t)=4+6\cos(2\pi f_0t)+2\sin(4\pi f_0t)
```

is sampled `N=16` times over exactly one period. Assume all harmonics lie inside the Nyquist band.

1. Find its nonzero complex Fourier-series coefficients `a_k`.
2. Find the corresponding nonzero DFT bins `X[k]`.

### Answer

Use

```math
\cos(\theta)=\frac{e^{j\theta}+e^{-j\theta}}{2},
\qquad
\sin(\theta)=\frac{e^{j\theta}-e^{-j\theta}}{2j}.
```

For the constant term,

```math
a_0=4.
```

For `6cos(2πf_0t)`,

```math
a_1=a_{-1}=3.
```

For `2sin(4πf_0t)=2sin(2ω_0t)`,

```math
a_2=\frac{2}{2j}=-j,
\qquad
a_{-2}=j.
```

The lecture gives

```math
X[k]=Na_k.
```

Therefore,

```math
X[0]=16(4)=64,
```

```math
X[1]=16(3)=48,
\qquad X[15]=X[-1]=48,
```

```math
X[2]=16(-j)=-16j,
\qquad X[14]=X[-2]=16j.
```

All other bins are zero. The negative harmonic `k=-r` is stored at DFT index `N-r`.

---

## C18. What Happens When Periodic Harmonics Exceed the Nyquist Band?

### Question

A periodic signal is sampled `N=8` times per period. It contains a harmonic at `k=6`. Into which DFT harmonic index does it alias? Show the sampled-sequence argument.

### Answer

DFT harmonic indices are periodic modulo `N`, so

```math
6\equiv6-8=-2\pmod 8.
```

Thus the `k=6` harmonic aliases to signed harmonic `k=-2`, stored at ordinary DFT index `6`.

At sample `n`, the original harmonic produces

```math
e^{j2\pi(6)n/8}.
```

The aliased harmonic produces

```math
e^{j2\pi(-2)n/8}.
```

Their ratio is

```math
e^{j2\pi(8)n/8}=e^{j2\pi n}=1,
```

so their samples are identical. Harmonics whose indices differ by an integer multiple of `N` collapse into the same DFT bin.

---

## C19. Coding Task — Generate the Replicated-Spectrum Intervals

### Question

Write a Python function `copy_intervals(f_max, fs, copies)` that returns the frequency interval occupied by each spectral copy from index `-copies` to `+copies`. Also report whether adjacent copies overlap.

### Answer

```python
def copy_intervals(f_max, fs, copies):
    """Return intervals [k*fs-f_max, k*fs+f_max] and overlap status."""
    intervals = []

    for k in range(-copies, copies + 1):
        left = k * fs - f_max
        right = k * fs + f_max
        intervals.append((k, left, right))

    overlap = fs <= 2 * f_max
    return intervals, overlap
```

Example:

```python
intervals, overlap = copy_intervals(4000, 10000, 2)
for item in intervals:
    print(item)
print("overlap:", overlap)
```

Output:

```text
(-2, -24000, -16000)
(-1, -14000,  -6000)
( 0,  -4000,   4000)
( 1,   6000,  14000)
( 2,  16000,  24000)
overlap: False
```

The test uses `<=` because, following the lecture’s strict recovery condition, touching at `f_s=2f_max` is not treated as a guaranteed recoverable case.

---

## C20. Coding Task — Predict Reconstruction Gains

### Question

Write a function that returns the ideal, ZOH, and FOH normalized magnitude gains for a tone of frequency `f` sampled at `fs`.

### Answer

```python
import numpy as np


def reconstruction_gains(f, fs):
    """Normalized magnitude gains of ideal, ZOH, and FOH reconstruction."""
    if fs <= 0:
        raise ValueError("fs must be positive")

    r = f / fs
    zoh = abs(np.sinc(r))
    foh = np.sinc(r) ** 2

    return {
        "ideal": 1.0,
        "zoh": float(zoh),
        "foh": float(foh),
    }
```

For `f=400 Hz` and `fs=1000 Hz`, the result is approximately

```python
{
    "ideal": 1.0,
    "zoh": 0.7568,
    "foh": 0.5728,
}
```

The ideal value assumes the signal satisfies the sampling theorem and is reconstructed by the ideal brick-wall LPF.

---

# Part D — Quick Concept Checks

## D1. True or False

**Statement:** If a signal is sampled faster, the copies of its spectrum move closer together.

**Answer:** False. Since `ω_s=2π/T`, faster sampling means smaller `T` and larger `ω_s`, so the copies move farther apart.

## D2. True or False

**Statement:** After aliasing has occurred, an ideal digital low-pass filter can always recover the original signal.

**Answer:** False. Aliasing adds different original frequency components into the same observed frequency. Filtering cannot unmix information that has already become indistinguishable.

## D3. True or False

**Statement:** The Nyquist rate and Nyquist frequency mean the same thing.

**Answer:** False. The Nyquist rate is `2f_M`, a requirement determined by the signal. The Nyquist frequency is `f_s/2`, determined by the sampler.

## D4. True or False

**Statement:** The DTFT of a sampled sequence repeats every `2π` in normalized angular frequency.

**Answer:** True. In physical angular frequency the corresponding sampled spectrum repeats every `ω_s=2π/T`.

## D5. True or False

**Statement:** Linear interpolation has no amplitude distortion because it exactly joins adjacent samples.

**Answer:** False. It passes through the sample values, but its frequency response is `T sinc²(ωT/2π)`, so it attenuates higher baseband frequencies.

## D6. True or False

**Statement:** An `N`-point DFT creates `N` new physical frequencies that were absent from the DTFT.

**Answer:** False. It evaluates the already-existing periodic DTFT at `N` uniformly spaced frequency points.

---

# Compact Formula Sheet

| Concept | Formula |
|---|---|
| Sampling train | `p(t) = Σ_n δ(t-nT)` |
| Impulse-train spectrum | `P(jω) = (2π/T) Σ_k δ(ω-kω_s)` |
| Sampling frequency | `ω_s = 2π/T`, `f_s = 1/T` |
| Sampled spectrum | `X_p(jω) = (1/T) Σ_k X(j(ω-kω_s))` |
| Safe sampling condition used in the lecture | `ω_s > 2ω_M`, equivalently `f_s > 2f_M` |
| Ideal reconstruction cutoff | `ω_M < ω_c < ω_s-ω_M`; common choice `ω_c=ω_s/2` |
| Ideal LPF | `H(jω)=T` in its passband |
| Ideal interpolation | `x_r(t)=Σ_n x(nT)sinc((t-nT)/T)` |
| ZOH | `H_0(jω)=T e^{-jωT/2}sinc(ωT/2π)` |
| FOH | `H_1(jω)=T sinc²(ωT/2π)` |
| DFT bin spacing | `Δf=f_s/N=1/T_0` |
| DFT and Fourier series | `X[k]=Na_k` when the periodic signal satisfies Nyquist |

---

# Suggested Practice Order

1. Derivation: C1, C2, C14
2. Nyquist and aliasing: C3, C7, C8, C12, C13
3. Reconstruction: C4, C5, C6, C9, C10, C11
4. DFT connection: C15, C16, C17, C18
5. Implementation: C19, C20

