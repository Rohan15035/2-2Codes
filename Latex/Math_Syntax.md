# LaTeX Math — Syntax Notes

How math is written in these `.tex` files. Every snippet below is taken from the actual documents.

## Required packages

```latex
\usepackage{amsmath}   % equation, align, cases, split, \text, \dfrac
\usepackage{amssymb}   % extra symbols (\lesssim, \varpi, ...)
\usepackage{mathtools} % \boxed, \xrightarrow and amsmath extensions
```

## 1. Inline math — `$...$`

```latex
$x$ , $I_{ij}$ , $e^{x^2}$
```
From `math.tex:13`. `$...$` drops into math mode inside a sentence. `_` = subscript, `^` = superscript; group multi-char scripts in braces: `e^{x^2}`, `I_{ij}`.

## 2. Unnumbered display — `\[ ... \]`

```latex
\[
    k = \frac{ab}{cd}
\]
```
From `Q1_ImageSynthesis.tex:74`. Centres the formula on its own line with **no equation number**.

## 3. Numbered equation — `equation`

```latex
\begin{equation}
    L = I_{ij}\cdot\cos(\theta) + R^2
    \label{eq:lighting}
\end{equation}
```
From `math.tex:14`. One centred, **auto-numbered** line. `\label{eq:lighting}` makes it referable. Star it — `equation*` — to drop the number (`math.tex:73` note).

## 4. Multi-line aligned — `align`, `&`, `\\`

```latex
\begin{align}
    k   &= \frac{ab}{cd}\\
    f(x) &= x^2 + 2x + 1 \nonumber \\
         &= (x+1)^2
\end{align}
```
From `math.tex:20-24`.
- `\\` ends each line; `&` marks the **alignment point** (everything lines up at the `=`).
- `\nonumber` (or `\notag`, `Q5_SolarSystem.tex:130`) suppresses the number on **that one line**.
- `align*` numbers **no** lines at all (`Q1_ImageSynthesis.tex:83`).

## 5. One number for a multi-line derivation — `split`

```latex
\begin{equation}
  \begin{split}
    \mathcal{L}\{1\} &= \int_0^\infty e^{-st}\,\mathrm{d}t \\
                     &= \frac{1}{s}.
  \end{split}
\end{equation}
```
From `Q4_Laplace.tex:79-85`. `split` aligns at `&` like `align`, but the whole block gets **one** number (it lives inside a single `equation`). Use this for a chain of `=` steps.

## 6. Piecewise — `cases`

```latex
\[
  |y| =
  \begin{cases}
    y  & \text{if } y \geq 0 \\
    -y & \text{if } y < 0
  \end{cases}
\]
```
From `math.tex:27-33`.
- `&` separates the value from its condition; `\\` ends each case.
- `\text{if } y \geq 0` — wrap words in `\text{...}`, otherwise "if" renders as italic variables (see the warning at `math.tex:30`).

## 7. `\frac` vs `\dfrac`

```latex
\dfrac{x_i^2}{\sigma^2} & \text{if } x_i \geq 0 \\[1mm]
```
From `math.tex:40`. `\frac` shrinks in cramped spots like `cases`; `\dfrac` forces **display-size** fractions so stacked cases stay readable. `\\[1mm]` adds 1 mm of extra vertical space after that line (`math.tex:35` note).

## 8. Fractions, roots, big operators

```latex
N(x_i,\mu,\sigma) = \frac{1}{\sqrt{2\pi}\sigma}\, e^{-\frac{(x_i-\mu)^2}{2\sigma^2}}
```
From `math.tex:54-55`. `\frac{num}{den}`, `\sqrt{...}`, and `\,` = a thin space.

```latex
T = \sum_{i=1}^{n} (x_i - \mu)^2      % math.tex:47
\int_0^\infty e^{-st}\,\mathrm{d}t    % Q4_Laplace.tex:59
```
`\sum_{i=1}^{n}` / `\int_0^\infty` — the `_` gives the lower limit, `^` the upper. `\mathrm{d}t` typesets an **upright** d for the differential.

## 9. Cross-referencing equations — `\eqref`

```latex
\begin{equation}\label{eq:polar}
    r(\theta) = \frac{a(1-e^2)}{1 + e\cos\theta}.
\end{equation}
Equation~\eqref{eq:polar} gives the orbital distance.
```
From `Q5_SolarSystem.tex:135-138`. `\eqref{eq:polar}` prints the number **in parentheses**, e.g. "(3)". The `~` before it is a non-breaking space so "Equation" and the number never split across a line. (Plain `\ref` gives the bare number.)

## 10. Symbols used across the files

```latex
Greek:  \theta \omega \sigma \mu \pi \alpha \beta \Delta \Lambda \varpi \varepsilon
Rel:    \geq \leq \neq \approx \propto \equiv \implies \to
Calligraphic / special:  \mathcal{L}   M_\odot   \Gamma^\mu_{\alpha\beta}
Boxed result:  \boxed{|\Delta\omega| \le K}      % Q3_Fireflies.tex:164
Arrow with label:  \xrightarrow{\ \ \mathcal{L}\ \ }   % Q4_Laplace.tex:65
Modulo:  (\theta_i(0) + \omega_i t)\bmod 2\pi    % Q3_Fireflies.tex:78
```

## Quick reference

| Syntax | Purpose | Example line |
|---|---|---|
| `$...$` | inline math | `math.tex:13` |
| `\[ ... \]` | unnumbered display | `Q1_ImageSynthesis.tex:74` |
| `equation` + `\label` | numbered, referable line | `math.tex:14` |
| `align` + `&` + `\\` | multi-line, aligned, each numbered | `math.tex:20` |
| `\nonumber` / `\notag` | drop number on one line | `math.tex:22` |
| `equation*` / `align*` | same, no numbers at all | `Q1_ImageSynthesis.tex:83` |
| `split` | many lines, one number | `Q4_Laplace.tex:80` |
| `cases` | piecewise definition | `math.tex:28` |
| `\text{...}` | words inside math | `math.tex:30` |
| `\dfrac` vs `\frac` | display vs inline fraction | `math.tex:40` |
| `\sum_{i=1}^{n}` `\int_0^\infty` | big operators + limits | `math.tex:47` |
| `\eqref{eq:...}` | reference "(n)" | `Q5_SolarSystem.tex:138` |
| `\\[1mm]` | line break + extra space | `math.tex:40` |
| `\boxed{...}` | box a result | `Q3_Fireflies.tex:164` |
