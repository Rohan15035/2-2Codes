# LaTeX Exam Reference — One-Page Master Sheet

A single, exam-ready reference distilled from every syntax note in this repo
(`Math_Syntax.md`, `Tables_Syntax.md`, `Figures_Syntax.md`, `Algorithms_Syntax.md`).
All snippets come from the actual question `.tex` files. Line refs use the file basename.

## Contents
1. [Document skeleton + packages](#1-document-skeleton--packages)
2. [Text formatting](#2-text-formatting)
3. [Math](#3-math)
4. [Tables](#4-tables)
5. [Figures](#5-figures)
6. [Algorithms](#6-algorithms)
7. [Cross-references, links, bibliography](#7-cross-references-links-bibliography)
8. [Common mistakes (read before the exam)](#8-common-mistakes-read-before-the-exam)
9. [Master quick-reference table](#9-master-quick-reference-table)

---

## 1. Document skeleton + packages

```latex
\documentclass[11pt]{article}
\usepackage{amsmath, amssymb, mathtools}   % math
\usepackage{graphicx}                       % \includegraphics
\usepackage{subcaption}                     % side-by-side subfigures
\usepackage{wrapfig}                        % text-wrapped figures
\usepackage{multirow, booktabs, array}      % table spanning + rules + p-columns
\usepackage[table]{xcolor}                  % \rowcolor
\usepackage{algorithm, algpseudocode}       % pseudocode
\usepackage{listings}                       % verbatim code
\usepackage{enumitem, hyperref}             % lists + clickable refs

\begin{document}
% content
\end{document}
```
This is the **union** of packages used across the repo. Load `amsmath` before you use any `align`/`equation`; load `xcolor` with `[table]` before `\rowcolor`; load `subcaption` before `subfigure`.

---

## 2. Text formatting

```latex
\textbf{bold}  \textit{italic}  \underline{underlined}  \texttt{monospace}
\emph{emphasis}                       % LaTeX_Cheatsheet.tex:92
% \% = literal percent; a blank line = new paragraph
```
Structure: `\section{}`, `\subsection{}`, `\subsection*{}` (starred = unnumbered, `Q4_Laplace.tex:136`). Lists via `enumitem`: `\begin{itemize}` / `\begin{enumerate}`.

---

## 3. Math

**Inline vs display**
```latex
$x$, $I_{ij}$, $e^{x^2}$                    % inline — math.tex:13
\[ k = \frac{ab}{cd} \]                     % unnumbered display — Q1_ImageSynthesis.tex:74
```

**Numbered / aligned**
```latex
\begin{equation}
    L = I_{ij}\cdot\cos(\theta) + R^2 \label{eq:lighting}   % math.tex:14
\end{equation}

\begin{align}
    k    &= \frac{ab}{cd} \\                 % & = alignment point, \\ ends line
    f(x) &= x^2 + 2x + 1 \nonumber \\        % \nonumber drops this line's number
         &= (x+1)^2
\end{align}                                  % math.tex:20-24
```
`equation*` / `align*` = no numbers at all (`Q1_ImageSynthesis.tex:83`). One number for a whole derivation → `split` inside `equation` (`Q4_Laplace.tex:80`).

**Piecewise + fractions**
```latex
\[ |y| = \begin{cases}
    y  & \text{if } y \geq 0 \\             % \text{} for words in math — math.tex:30
    -y & \text{if } y < 0
\end{cases} \]

\dfrac{x_i^2}{\sigma^2}                      % \dfrac = display-size fraction — math.tex:40
```

**Operators & symbols**
```latex
\sum_{i=1}^{n} (x_i-\mu)^2      \int_0^\infty e^{-st}\,\mathrm{d}t   % _ lower, ^ upper
\sqrt{...}   \frac{a}{b}   \,thin-space   \mathrm{d}t (upright d)
\boxed{|\Delta\omega| \le K}                 % box a result — Q3_Fireflies.tex:164
\geq \leq \neq \approx \propto \implies \to  \theta \omega \sigma \mu \pi \Delta
```

---

## 4. Tables

```latex
\begin{table}[h]
  \centering
  \begin{tabular}{|l|c|c|}          % l/c/r align, | = vertical rule
    \hline
    Method & Accuracy & Time \\      % & separates cells, \\ ends row
    \hline
    Rasterization & Medium & $O(n)$ \\
    \hline
  \end{tabular}
  \caption{Comparison of Image Synthesis Techniques}
  \label{tab:comparison}
\end{table}
```

**Spanning**
```latex
\multirow{2}{*}{Ray Tracing} & High & $O(n^2)$ \\   % span rows — Q1_ImageSynthesis.tex:104
                             & Very High & $O(n^3)$ \\
\multicolumn{2}{|c|}{Hybrid Method} & $O(n^2)$ \\    % span cols — table.tex:48
\cline{2-3}                                          % partial rule — table.tex:62
```

**Booktabs (no vertical lines) + colour + wrapping column**
```latex
\begin{tabular}{lcr}
  \toprule Item & Qty & Price \\ \midrule
  Apples & 10 & \$5.00 \\ \bottomrule
\end{tabular}                                        % table.tex:117-125
\rowcolor{gray!15}                                   % shade a row — Q5_SolarSystem.tex:231
>{\raggedright\arraybackslash}p{4.3cm}               % fixed-width wrapping col — Q3_Fireflies.tex:115
```

---

## 5. Figures

```latex
\begin{figure}[ht]
    \centering
    \includegraphics[width=0.6\textwidth]{img.png}  % scale to \textwidth
    \caption{...}\label{fig:x}                       % caption BEFORE label
\end{figure}                                         % LaTeX_Cheatsheet.tex:211
```

**Side-by-side (subfigure)**
```latex
\begin{figure}[ht]\centering
  \begin{subfigure}{0.3\textwidth}\centering
      \includegraphics[width=\textwidth]{a}\caption{Output A}   % sub-caption (a)
  \end{subfigure}\hfill                              % \hfill spreads them
  \begin{subfigure}{0.3\textwidth} ... \end{subfigure}
  \caption{Comparison of three rendering outputs.}\label{fig:outputs}   % main caption
\end{figure}                                         % Q1_ImageSynthesis.tex:119-140
```
Blank line between subfigures = **new row** (`Q5_SolarSystem.tex:83`); mix widths (`0.6` + `0.35`) for asymmetric layouts (`Q2_LaTeXIntro.tex:109`); `\label{}` inside a subfigure references one panel (`Q5_SolarSystem.tex:100`).

**Text-wrapped figure**
```latex
\begin{wrapfigure}{r}{0.45\textwidth}               % {r}=right, then column width
    \centering
    \includegraphics[width=0.43\textwidth]{rc_circuit.png}  % image < column
    \caption{A simple series RC circuit.}\label{fig:rc}
\end{wrapfigure}                                     % Q4_Laplace.tex:137
```

---

## 6. Algorithms

```latex
\begin{algorithm}[ht]
    \caption{Simulate the Kuramoto model}\label{alg:kuramoto}
    \begin{algorithmic}[1]                           % [1] = line numbers
        \Require Phases $\theta_i$, coupling $K$, steps $M$
        \For{$m \gets 1$ \textbf{to} $M$}            % \gets = assignment ←
            \For{each firefly $i$}
                \State $v_i \gets \omega_i + \frac{K}{N} q_i$
            \EndFor
            \State $\theta_i \gets (\theta_i + h v_i)\bmod 2\pi$
        \EndFor
        \State \Return $\theta_1,\dots,\theta_N$
    \end{algorithmic}
\end{algorithm}                                       % Q3_Fireflies.tex:198-213
```
Every step starts with `\State`; every `\For` needs `\EndFor`. Sibling keywords (same package): `\While/\EndWhile`, `\If/\ElsIf/\Else/\EndIf`, `\Function/\EndFunction`, `\Comment{}`, `\Ensure`. For literal source code use `lstlisting` instead (`Q4_Laplace.tex:20`).

---

## 7. Cross-references, links, bibliography

**One rule for all floats:** `\label{}` **after** the `\caption` (or equation), then reference with `~\ref`:
```latex
Figure~\ref{fig:rc}      Table~\ref{tab:comparison}    Algorithm~\ref{alg:kuramoto}
Equation~\eqref{eq:polar}     % \eqref adds parentheses: "(3)" — Q5_SolarSystem.tex:138
```
The `~` is a **non-breaking space** so the label word and its number never split across a line.

**Prefix convention:** `fig:` `tab:` `eq:` `alg:` — keeps labels from colliding.

**Links, footnotes, citations** (`LaTeX_Cheatsheet.tex:303-315`)
```latex
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}
\href{https://...}{clickable text}
A remark.\footnote{The note text.}
Reference~\cite{sarfati2021}.
\begin{thebibliography}{9}
  \bibitem{sarfati2021} Author. ``Title''. \emph{Journal} (2021).
\end{thebibliography}
```

---

## 8. Common mistakes (read before the exam)

- **`\label` before `\caption`** → the reference grabs the wrong number. Always caption first, then label.
- **Words in math render as italic letters** → wrap them: `\text{if } y \ge 0`, not `if y \ge 0` (`math.tex:30`).
- **`\hline` vs `\cline`** → `\hline` is full-width; use `\cline{2-3}` so a rule doesn't cut through a `\multirow` cell (`table.tex:62`).
- **Mixing `booktabs` with `|`** → with `\toprule/\midrule/\bottomrule`, drop all vertical `|` rules; that's the convention.
- **Multirow's next row** → leave its first column empty (start the row with `&`), or you get a doubled cell.
- **`\includegraphics` fills the whole page inside a subfigure** → inside `subfigure`, `\textwidth` means the *subfigure* box; that's why `width=\textwidth` there ≠ full page.
- **`wrapfigure` image touching the text** → make the image slightly narrower than the reserved column (`0.43` inside `0.45`).
- **Missing `\EndFor`/`\EndIf`** → every algorithm opener needs its `\End...`; unbalanced pairs won't compile.
- **`\frac` unreadable in `cases`/inline** → use `\dfrac` for display-size fractions (`math.tex:40`).
- **Hard-coding "Figure 3"** → always `\ref{}`; numbers renumber automatically when floats move.
- **Forgetting the package** → `align` needs `amsmath`; `subfigure` needs `subcaption`; `\rowcolor` needs `\usepackage[table]{xcolor}`; `\multirow` needs `multirow`.
- **Float placement `[h]` alone is fragile** → prefer `[ht]` or `[htbp]` so LaTeX has fall-backs.

---

## 9. Master quick-reference table

| Task | Syntax | Example line |
|---|---|---|
| Inline math | `$...$` | `math.tex:13` |
| Unnumbered display | `\[ ... \]` | `Q1_ImageSynthesis.tex:74` |
| Numbered equation | `equation` + `\label` | `math.tex:14` |
| Aligned equations | `align`, `&`, `\\` | `math.tex:20` |
| One number, many lines | `split` | `Q4_Laplace.tex:80` |
| Piecewise | `cases` | `math.tex:28` |
| Words in math | `\text{...}` | `math.tex:30` |
| Display fraction | `\dfrac{}{}` | `math.tex:40` |
| Sum / integral | `\sum_{i=1}^{n}`, `\int_0^\infty` | `math.tex:47` |
| Boxed result | `\boxed{...}` | `Q3_Fireflies.tex:164` |
| Basic table | `table` + `tabular{|l|c|c|}` | `table.tex:36` |
| Row / cell sep | `\\` / `&` | `table.tex:40` |
| Full / partial rule | `\hline` / `\cline{2-3}` | `table.tex:62` |
| Span rows / cols | `\multirow` / `\multicolumn` | `Q1_ImageSynthesis.tex:104` |
| Booktabs rules | `\toprule \midrule \bottomrule` | `table.tex:118` |
| Shade a row | `\rowcolor{gray!15}` | `Q5_SolarSystem.tex:231` |
| Wrapping column | `>{\raggedright\arraybackslash}p{4.3cm}` | `Q3_Fireflies.tex:115` |
| Basic figure | `figure` + `\includegraphics` | `LaTeX_Cheatsheet.tex:211` |
| Side-by-side | `subfigure` + `\hfill` | `Q1_ImageSynthesis.tex:121` |
| Text-wrapped figure | `wrapfigure{r}{0.45\textwidth}` | `Q4_Laplace.tex:137` |
| Algorithm float | `algorithm` + `algorithmic[1]` | `Q3_Fireflies.tex:198` |
| Step / loop | `\State` / `\For ... \EndFor` | `Q3_Fireflies.tex:203` |
| Input / return | `\Require` / `\State \Return` | `Q3_Fireflies.tex:201` |
| Verbatim code | `lstlisting` | `Q4_Laplace.tex:20` |
| Cross-ref | `Figure~\ref{}`, `\eqref{}` | `Q5_SolarSystem.tex:138` |
| Footnote / cite | `\footnote{}` / `\cite{}` | `LaTeX_Cheatsheet.tex:305` |
