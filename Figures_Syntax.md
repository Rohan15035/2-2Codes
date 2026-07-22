# LaTeX Figures — Syntax Notes

How figures are placed in these `.tex` files. Every snippet below is taken from the actual documents.

## Required packages

```latex
\usepackage{graphicx}      % \includegraphics — the core image command
\usepackage{subcaption}    % subfigure environment for side-by-side images
\usepackage{wrapfig}       % wrapfigure — let text flow around a figure
```
`graphicx` is loaded everywhere (`Q1_ImageSynthesis.tex:13`). `subcaption` is added when a figure holds several images (`Q1_ImageSynthesis.tex:14`, `Q5_SolarSystem.tex:17`); `wrapfig` when text should wrap around one (`Q4_Laplace.tex:15`, `Q3_Fireflies.tex:15`).

## 1. The skeleton — `figure` wraps `\includegraphics`

```latex
\begin{figure}[ht]                              % float: h=here, t=top, b=bottom, p=float page
    \centering                                  % centre the image in the column
    \includegraphics[width=0.6\textwidth]{img.png}
    \caption{...}\label{fig:x}                  % caption + cross-ref target
\end{figure}
```
- Pattern from `LaTeX_Cheatsheet.tex:211-215`. `figure` is the **float** (gives the caption/label + lets LaTeX move the image); `\includegraphics` is the image itself.
- Caption + label go **inside** `figure`, **after** the image so the number reads "Figure N" and points at the picture above it.

## 2. Float placement — `[ht]`, `[h]`, `[htbp]`

```latex
\begin{figure}[ht]      % Q1_ImageSynthesis.tex:119 — try here, else top
\begin{figure}[h]       % DemoTry/main.tex:129 — "place exactly here if it fits"
\begin{figure}[htbp]    % DemoTry/subfigures.tex:10 — here / top / bottom / float page
```
The bracket letters are LaTeX's *preferences*, tried left to right. `[h]` alone is fragile; `[ht]` (used in Q1/Q2/Q5) or `[htbp]` give LaTeX fall-backs so the figure doesn't get stranded.

## 3. `\centering` — centre the contents

```latex
\begin{figure}[ht]
    \centering                                  % Q1_ImageSynthesis.tex:120
```
Put `\centering` right after `\begin{figure}`. It centres everything below it in that float — use it instead of a `center` environment (which adds extra vertical space).

## 4. `\includegraphics[width=...]` — size control

```latex
\includegraphics[width=\textwidth]{example-image-a}      % Q1_ImageSynthesis.tex:123
\includegraphics[width=0.6\textwidth]{sun.png}           % Q5_SolarSystem.tex:87
\includegraphics[width=0.40\textwidth]{fireflies.jpg}    % Q3_Fireflies.tex:54
```
- `width=\textwidth` = full column width; `width=0.6\textwidth` = 60% of it. Scaling to `\textwidth` keeps images responsive if the layout changes (better than fixed `cm`).
- Inside a `subfigure`, `\textwidth` means the **subfigure's** box, not the page — so `width=\textwidth` fills whatever fraction the subfigure was given (`Q1_ImageSynthesis.tex:123`).

## 5. `\caption` + `\label` — number and cross-ref

```latex
    \caption{Comparison of three rendering outputs.}     % Q1_ImageSynthesis.tex:138
    \label{fig:outputs}                                  % Q1_ImageSynthesis.tex:139
\end{figure}
```
- `\caption{}` prints "Figure N: ..." and **must come before** `\label{}`, or the label captures the wrong number.
- `fig:` is just a naming convention (`fig:rc`, `fig:solar`, `fig:asym`) so labels don't collide with `tab:` or `eq:`.
- Captions can carry attribution text too: `\caption{... Photograph by Bernd Thaller, via Wikimedia Commons.}` (`Q3_Fireflies.tex:55`).

## 6. Cross-reference — `Figure~\ref{fig:x}`

```latex
Figure~\ref{fig:outputs} compares three different rendering outputs.  % Q1_ImageSynthesis.tex:142
Figure~\ref{fig:rc} shows a simple ... circuit                       % Q4_Laplace.tex:144
The photograph in fig.~\ref{fig:fireflies} records light trails      % Q3_Fireflies.tex:60
```
`\ref{fig:x}` prints the auto-number; the `~` is a **non-breaking space** so "Figure" and its number never split across a line break. Never hard-code "Figure 3" — `\ref` renumbers automatically if figures move.

## 7. Side-by-side images — `subfigure`

```latex
\begin{figure}[ht]
    \centering
    \begin{subfigure}{0.3\textwidth}
        \centering
        \includegraphics[width=\textwidth]{example-image-a}
        \caption{Output A}                       % sub-caption: (a)
    \end{subfigure}
    \hfill
    \begin{subfigure}{0.3\textwidth}
        \centering
        \includegraphics[width=\textwidth]{example-image-b}
        \caption{Output B}
    \end{subfigure}
    \hfill
    \begin{subfigure}{0.3\textwidth} ... \end{subfigure}
    \caption{Comparison of three rendering outputs.}   % main caption
    \label{fig:outputs}
\end{figure}
```
- From `Q1_ImageSynthesis.tex:119-140`. Each `\begin{subfigure}{0.3\textwidth}` reserves a **fraction of the line**; three at `0.3` fit in one row.
- Two caption levels: the `\caption` **inside** each subfigure gives `(a) (b) (c)`; the `\caption` **after** all subfigures is the figure's overall caption.
- Needs `\usepackage{subcaption}`.

## 8. `\hfill` — spread subfigures across the row

```latex
    \end{subfigure}
    \hfill                                       % Q1_ImageSynthesis.tex:126
    \begin{subfigure}{0.3\textwidth}
```
`\hfill` between subfigures soaks up the leftover horizontal space, pushing them to the row's edges with even gaps. In the compact inline form it sits at the line end (`Q5_SolarSystem.tex:94`): `...\end{subfigure}\hfill`.

## 9. New row — a blank line (or `\bigskip`)

```latex
    \begin{subfigure}{0.30\textwidth} ... \end{subfigure}

    \bigskip                                     % Q5_SolarSystem.tex:91 — gap + new row
    \begin{subfigure}{0.22\textwidth}\centering
```
A **blank line** between subfigures breaks to a new row (`Q5_SolarSystem.tex:83-93`). `Q5` stacks the Sun, then a row of inner planets, then a row of outer planets, using blank lines + `\bigskip` between groups and `{\large\textbf{Inner Planets}}\par\medskip` as section titles inside the float.

## 10. Asymmetric layout — mixed widths + `\vspace`

```latex
    \begin{subfigure}{0.6\textwidth}            % one dominant image
        \centering \includegraphics[width=\textwidth]{example-image-a}
        \caption{Main Diagram}
    \end{subfigure}

    \vspace{1em}                                 % Q2_LaTeXIntro.tex:117
    \begin{subfigure}{0.35\textwidth} ... \end{subfigure}
    \hfill
    \begin{subfigure}{0.35\textwidth} ... \end{subfigure}
```
From `Q2_LaTeXIntro.tex:109-131`. One big `0.6\textwidth` subfigure on top, then two `0.35\textwidth` ones below split by `\hfill`. `\vspace{1em}` adds a controlled vertical gap between the rows.

## 11. Labelling one subfigure — `\label` inside it

```latex
\begin{subfigure}{0.22\textwidth}\centering
    \includegraphics[width=\textwidth]{mars.png}\caption{Mars}\label{fig:mars}\end{subfigure}
```
From `Q5_SolarSystem.tex:99-100`. Put `\label{}` **after that subfigure's own `\caption`** to reference a single panel: `Compare Mars in Figure~\ref{fig:mars} with Jupiter in Figure~\ref{fig:jupiter}.` (`Q5_SolarSystem.tex:80`). `\ref` then prints the sub-number like `2b`.

## 12. Text wrapping around a figure — `wrapfigure`

```latex
\begin{wrapfigure}{r}{0.45\textwidth}           % Q4_Laplace.tex:137
    \centering
    \includegraphics[width=0.43\textwidth]{rc_circuit.png}
    \caption{A simple series RC circuit.}
    \label{fig:rc}
\end{wrapfigure}
```
- `\begin{wrapfigure}{r}{0.45\textwidth}` — first arg `{r}` = float to the **right** (`{l}` = left); second arg = width of the wrap column. Body text then flows alongside it.
- Keep `\includegraphics` a touch **narrower** than the reserved column (`0.43` inside `0.45`) so text doesn't touch the image — same trick in `Q3_Fireflies.tex:52-54` (`0.40` inside `0.42`).
- Needs `\usepackage{wrapfig}`. Place it **just before** the paragraph it should sit beside.

## Quick reference

| Syntax | Purpose | Example line |
|---|---|---|
| `\begin{figure}[ht]` | float + caption/label | `Q1_ImageSynthesis.tex:119` |
| `\centering` | centre contents | `Q1_ImageSynthesis.tex:120` |
| `\includegraphics[width=0.6\textwidth]{}` | insert + size image | `Q5_SolarSystem.tex:87` |
| `\caption{} \label{fig:x}` | number + cross-ref target | `Q1_ImageSynthesis.tex:138-139` |
| `Figure~\ref{fig:x}` | reference in text | `Q1_ImageSynthesis.tex:142` |
| `\begin{subfigure}{0.3\textwidth}` | side-by-side image | `Q1_ImageSynthesis.tex:121` |
| `\hfill` | spread subfigures | `Q1_ImageSynthesis.tex:126` |
| blank line / `\bigskip` | start a new row | `Q5_SolarSystem.tex:91` |
| `\vspace{1em}` | vertical gap between rows | `Q2_LaTeXIntro.tex:117` |
| `\label{}` inside subfigure | reference one panel | `Q5_SolarSystem.tex:100` |
| `\begin{wrapfigure}{r}{0.45\textwidth}` | text wraps around figure | `Q4_Laplace.tex:137` |
