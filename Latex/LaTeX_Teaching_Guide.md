# LaTeX Guide for CSE200 "Reproduce this Article" Online Exams

This guide teaches every LaTeX skill needed to solve the five online questions in
this folder. Each section explains the concept, gives the minimal command, and
points to the question where it appears. If you can do everything here, you can
reproduce any of these articles from scratch.

The five solved solutions live at:

| Q | Article | Solution file |
|---|---------|---------------|
| 1 | Mathematical Foundations of Image Synthesis | `Solutions/Q1_ImageSynthesis.tex` |
| 2 | CSE200: Online-1 on LaTeX | `Solutions/Q2_LaTeXIntro.tex` |
| 3 | Fireflies in Unison | `A2_Online_1/A2_Online_1/Q3_Fireflies.tex` |
| 4 | Laplace Analysis and Applications | `Online1_B1/Online1_B1/Q4_Laplace.tex` |
| 5 | The Solar System | `Online1_C2/Online1_C2/Q5_SolarSystem.tex` |

---

## 0. How to compile

These are Windows/MiKTeX machines. From a terminal in the folder that holds the
`.tex` file **and its images/bib**:

```bash
pdflatex Q3_Fireflies.tex     # run once
pdflatex Q3_Fireflies.tex     # run AGAIN to resolve \ref, \cite, table of contents
```

Anything with `\ref`, `\cite`, `\tableofcontents`, or subfigure letters must be
compiled **twice** — the first pass writes an `.aux` file, the second reads it.
If you use real BibTeX/biber (Section 15), the sequence is
`pdflatex → bibtex → pdflatex → pdflatex`.

**Overleaf** does all of this automatically — just click *Recompile*.

---

## 1. Document skeleton

Every file has the same shape:

```latex
\documentclass[11pt]{article}   % preamble starts here
\usepackage{...}                % load features
\title{...}\author{...}\date{...}
\begin{document}                % body starts here
\maketitle
...content...
\end{document}
```

- `\documentclass{article}` — the class used by **all five** questions.
- The **preamble** (before `\begin{document}`) is where you load packages and
  define settings. Content goes between `\begin{document}` and `\end{document}`.
- Comments start with `%`.

### The packages you will almost always want

```latex
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}      % lets you type accents like é directly
\usepackage[margin=1in]{geometry}% page margins
\usepackage{amsmath, amssymb}    % all serious math
\usepackage{graphicx}            % \includegraphics
\usepackage{xcolor}              % colours
\usepackage{hyperref}            % \href, clickable \ref/\cite
```

Load `hyperref` **last** (it patches many other commands).

---

## 2. Title, authors, affiliations

`\maketitle` typesets whatever you put in `\title`, `\author`, `\date`.

**Simple** (Q1, Q2):
```latex
\title{Mathematical Foundations of Image Synthesis}
\author{Your Name (Your Student ID)}
\date{January 4, 2026}       % \date{\today} for today; \date{} for none
```

**Subtitle + coloured title** (Q3). Use `\\` for a line break inside the title
and `\textcolor` for colour:
```latex
\title{\textbf{\textcolor{titleblue}{Fireflies in Unison}}\\[0.3em]
       \large How Simple Timing Rules Create a Collective Rhythm}
```

**Multiple authors with numbered affiliations** (Q3, Q4). `\textsuperscript{1}`
makes the little raised number; put the affiliation list on its own line:
```latex
\author{Pierre-Simon Laplace\textsuperscript{1}, Oliver Heaviside\textsuperscript{2}\\[0.6em]
        \textsuperscript{1}Académie des Sciences, Paris, France\\
        \textsuperscript{2}Royal Society, London, United Kingdom}
```

**Small-caps title** (Q5): `\title{\textsc{\LARGE The Solar System}}`.

---

## 3. Sections and structure

```latex
\section{Introduction}          % numbered: "1 Introduction"
\subsection{The Laplace Transform}   % "1.1 ..."
\subsubsection{...}             % "1.1.1 ..."
\section*{Conclusion}           % starred = NO number (used in Q2)
\subsection*{Circuit Model}     % starred subsection (Q4)
```

The `*` versions appear in **Q2** ("Conclusion") and **Q4** ("Circuit Model") —
they print the heading but skip the number and the table of contents.

---

## 4. Text formatting and emphasis

| You want | Command | Appears in |
|----------|---------|-----------|
| **bold** | `\textbf{...}` | all |
| *italic* | `\textit{...}` | all |
| *emphasis* (italic, but flips in italic context) | `\emph{...}` | Q2, Q3 |
| underline | `\underline{...}` | Q1, Q2 |
| `monospace/code` | `\texttt{...}` | Q4 (`resistor--capacitor`) |
| small caps | `\textsc{...}` | Q5 title, "doi" |

**Font sizes** (Q2) — declared inside braces so they switch off again:
```latex
{\Large Large text}, {\small small text}, {\huge huge text}
```
Size ladder: `\tiny \scriptsize \footnotesize \small \normalsize \large \Large \LARGE \huge \Huge`.

**Dashes & quotes** (important for exact reproduction):
- `-` hyphen, `--` en-dash (number ranges: `1645--1662`), `---` em-dash (—).
- Quotes: use `` `` `` and `''` → "like this". Straight `"` is wrong in LaTeX.

---

## 5. Lists

### Bulleted / numbered / description
```latex
\begin{itemize} \item ... \end{itemize}      % bullets •
\begin{enumerate} \item ... \end{enumerate}  % numbers 1. 2. 3.
\begin{description} \item[Term] text \end{description}  % bold term + text
```

### Nesting
Just put a list inside an `\item`. LaTeX changes the marker automatically at each
depth (bullets: • – ∗; numbers: 1 → a → i). **Q1** and **Q2** are built entirely
from nested `itemize`/`enumerate`:
```latex
\begin{enumerate}
    \item Ray Construction
    \begin{enumerate}      % becomes (a), (b)
        \item Primary Rays
        \item Secondary Rays
    \end{enumerate}
\end{enumerate}
```

### Custom item labels — the "Important"/"Note" trick
`\item[...]` overrides the marker for that one item. A long label sticks out to
the left, which is exactly the "**Important** Shading Model" look in **Q1** and the
"**Note**" in **Q2**:
```latex
\item[\textbf{Important}] Shading Model
```

### Custom markers with `enumitem`
`\usepackage{enumitem}` lets you set the marker for a whole list. Used heavily in
**Q3/Q4/Q5**:
```latex
\begin{itemize}[label=$\dagger$]     ...  % † bullets (Q5)
\begin{itemize}[label=$\diamond$]    ...  % ⋄ bullets (Q3, Q5)
\begin{itemize}[label=$\oplus$]      ...  % ⊕ bullets (Q4)
\begin{itemize}[label=$\triangleright$] ... % ▷ bullets (Q4)
\begin{enumerate}[label=(\Roman*)]   ...  % (I), (II)  (Q5)
\begin{enumerate}[label=\Roman*.]    ...  % I.  II.  III. (Q3)
```
Counter styles: `\arabic* \alph* \Alph* \roman* \Roman*`. Add `nosep` for tight
lists, `leftmargin=2em` to control indent.

`\begin{description}[style=nextline]` (Q3) puts the definition on the **next
line**, indented — that's the "Internal clock / Coupling strength" layout.

---

## 6. Inline vs display math

- **Inline**: `$...$` → variables in a sentence, e.g. `Consider $x_i$, $y$, $z^2$.`
- **Display, unnumbered**: `\[ ... \]`
- **Display, numbered**: `\begin{equation} ... \end{equation}` (auto number `(1)`)

Every question mixes these. Common building blocks:

| Math | Code |
|------|------|
| subscript / superscript | `x_i`, `x^2`, `x_i^2`, `x^{n+1}` (braces for >1 char) |
| fraction | `\frac{a}{b}`, bigger `\dfrac{a}{b}` |
| square root | `\sqrt{x}`, `\sqrt[3]{x}` |
| Greek | `\alpha \beta \theta \omega \mu \sigma \pi \Delta \Lambda \varpi` |
| sum / integral | `\sum_{j=1}^{N}`, `\int_0^\infty` |
| operators | `\cdot \times \pm \le \ge \approx \propto \implies \bmod` |
| roman "d" for derivatives | `\frac{\mathrm{d}\theta}{\mathrm{d}t}` |
| text inside math | `\text{if } x\ge 0` |
| symbols | `\infty \partial \nabla \odot \Theta` |

**Always** wrap subscripts that are words in `\mathrm`: `T_{\mathrm{E}}` (Q5), and
function names like `\sin, \cos, \ln, \exp` use the backslash form so they print
upright.

---

## 7. Multi-line and aligned equations

### `align` — align at the `&`, one number per line
```latex
\begin{align}
    \frac{d\theta_1}{dt} &= \omega_1 + \tfrac{K}{2}\sin(\theta_2-\theta_1), \\
    \frac{d\theta_2}{dt} &= \omega_2 + \tfrac{K}{2}\sin(\theta_1-\theta_2).
\end{align}
```
`&` marks the alignment column (usually just before `=`); `\\` ends a line.
`\notag` on a line suppresses its number (Q4, Q5 use this so only the last line is
numbered). `align*` gives **no** numbers at all (Q5 Earth–Mars block).

### `split` — several lines, ONE number for the whole block
Used for the `f(x)=…=(x+1)^2` derivation (Q1) and `L{1}=…=1/s` (Q4):
```latex
\begin{equation}
  \begin{split}
     f(x) &= x^2 + 2x + 1 \\
          &= (x+1)^2
  \end{split}
\end{equation}
```

### `cases` — piecewise functions (Q1, Q2)
```latex
|y| = \begin{cases} y  & \text{if } y \ge 0 \\
                    -y & \text{if } y < 0 \end{cases}
```

### `\boxed` — a box around a result (Q3, eq. 9)
```latex
\begin{equation}\boxed{\,|\Delta\omega| \le K.\,}\end{equation}
```

### Labels and cross-references
Put `\label{eq:key}` in an equation, refer to it with `\eqref{eq:key}` → `(3)`.
Use a naming convention like `eq:`, `fig:`, `tab:`, `lst:`, `prop:`.

---

## 8. Tables — the biggest source of marks

Basic anatomy:
```latex
\begin{table}[ht]                 % float; ht = "here or top"
  \centering
  \caption{...}\label{tab:key}    % caption ABOVE the tabular for tables
  \begin{tabular}{|l|c|c|}        % column spec: l/c/r align, | = vertical rule
     \hline
     A & B & C \\                 % & separates cells, \\ ends a row
     \hline
  \end{tabular}
\end{table}
```
- Column letters: `l` left, `c` centre, `r` right, `p{4cm}` fixed-width paragraph
  (needed when a cell must **wrap** — see the last column of Q3's table).
- `\hline` = full horizontal rule; `\cline{2-3}` = partial rule under columns 2–3.

### `\multirow` — one cell spanning several rows (needs `\usepackage{multirow}`)
Q1 "Ray Tracing", Q2 "Module B", Q4 "Algebraic/Exponential", Q5 "Planet":
```latex
\multirow{2}{*}{Ray Tracing} & High      & $O(n^2)$ \\
                             & Very High & $O(n^3)$ \\   % leave first cell blank
```
`{2}` = number of rows, `{*}` = natural width.

### `\multicolumn` — one cell spanning several columns
Q1 "Hybrid Method", Q2/Q4/Q5 header groups ("Score", "Transform Equation"):
```latex
\multicolumn{2}{|c|}{\textbf{Score}} \\   % span 2 cols, centred, with borders
```

A header that is *both* stacked and grouped (Q2, Q4, Q5) combines them:
```latex
\multirow{2}{*}{\textbf{Module}} & \multicolumn{2}{c|}{\textbf{Score}} \\
\cline{2-3}
                                 & Theory & Lab \\
```

### Coloured tables (Q3, Q5) — `\usepackage[table]{xcolor}`
`\rowcolor{color}` at the **start** of a row shades it; colour a word with
`\textcolor`:
```latex
\rowcolor{green!10}
Neighbor ahead & $0<\theta_j-\theta_i<\pi$ &
    \textbf{\textcolor{green!55!black}{Positive}} & Speeds up its phase. \\
```
`green!10` means "10% green, 90% white" — handy for pale backgrounds.
`\usepackage{booktabs}` gives the nicer `\toprule \midrule \bottomrule` rules
(used in Q3 instead of `\hline`).

---

## 9. Figures and images

```latex
\usepackage{graphicx}
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.5\textwidth]{fireflies.jpg}
  \caption{...}\label{fig:key}     % caption BELOW image for figures
\end{figure}
```
- Sizing: `[width=0.5\textwidth]`, `[width=4cm]`, or `[scale=0.8]`.
- The image file must sit next to the `.tex` (or give a relative path). That's why
  the Q3/Q4/Q5 solutions live **in the same folder** as their images.

### Placeholder images (Q1, Q2)
`\usepackage{mwe}` gives ready-made demo images `example-image-a`, `-b`, `-c`
(grey boxes labelled A/B/C) — exactly the placeholders those two articles show.

### Subfigures (Q1, Q2, Q5) — `\usepackage{subcaption}`
Each `subfigure` is a mini-figure with its own `(a)`, `(b)`… caption:
```latex
\begin{figure}[ht]\centering
  \begin{subfigure}{0.3\textwidth}\centering
     \includegraphics[width=\textwidth]{example-image-a}
     \caption{Output A}
  \end{subfigure}\hfill        % \hfill spreads them across the line
  \begin{subfigure}{0.3\textwidth}\centering
     \includegraphics[width=\textwidth]{example-image-b}
     \caption{Output B}
  \end{subfigure}
  \caption{Comparison of three rendering outputs.}   % the MAIN caption
\end{figure}
```
Tips:
- A blank line (or `\\`) between subfigure rows starts a **new row** — that is how
  Q2's "one big + two small" and Q5's **nine planets in three rows** are built.
- The subfigure letters count in order, so Q5's Mars is automatically `(e)` and
  Jupiter `(f)`; `\ref{fig:mars}` then prints `1e`.
- Plain bold lines like `{\large\textbf{Inner Planets}}\par\medskip` between rows
  create the group headings inside Q5's figure.

### Wrapped figure — text flows around it (Q3, Q4) — `\usepackage{wrapfig}`
```latex
\begin{wrapfigure}{r}{0.42\textwidth}   % r = right side, then width
   \centering
   \includegraphics[width=0.40\textwidth]{fireflies.jpg}
   \caption{...}\label{fig:fireflies}
\end{wrapfigure}
```
Put it just **before** the paragraph you want wrapped. `{r}` right, `{l}` left.

---

## 10. Cross-references

1. Tag the thing: `\label{fig:rc}` (right after its `\caption`).
2. Refer to it: `Figure~\ref{fig:rc}`, equation `\eqref{eq:kvl}`, proposition
   `Proposition~\ref{prop:weak}`.

The `~` is a non-breaking space so "Figure" and its number never split across a
line. All of Q3/Q4/Q5 rely on this. Remember: **compile twice** or numbers show as
`??`.

---

## 11. Footnotes

```latex
... an approximation.\footnote{Pulse-coupled models represent each flash ...}
```
Appears in Q3, Q4, Q5. The mark and the text are produced together; numbering is
automatic. In the **title/author** block use `\thanks{...}` instead of
`\footnote`.

---

## 12. Hyperlinks — `\usepackage{hyperref}`

```latex
\href{https://mathworld.wolfram.com/LaplaceTransform.html}{Laplace Transform entry on MathWorld}
\url{https://example.com}          % prints the raw URL
```
Control link colours in the preamble:
```latex
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue}
```
`linkcolor` = internal `\ref`/TOC links, `citecolor` = `\cite`, `urlcolor` =
`\href`. Q3 colours cross-references blue; Q4/Q5 keep them black and only colour
URLs. `hyperref` also makes `\ref`, `\cite`, and the table of contents clickable.

---

## 13. Colours — `\usepackage{xcolor}`

```latex
\textcolor{red}{red words}
\definecolor{titleblue}{RGB}{40,80,170}   % define your own
\textcolor{titleblue}{...}
green!10          % 10% green mixed with white
red!70!black      % 70% red, 30% black (a darker red)
```
Q3 (title, stage labels, table), Q4 (the blue/red sentence), Q5 (title colours,
blue/red sentence, coloured table) all use these. `[table]{xcolor}` additionally
enables `\rowcolor`/`\cellcolor` (Section 8).

---

## 14. Algorithms, code, theorems

### Algorithm pseudocode (Q3) — `\usepackage{algorithm, algpseudocode}`
```latex
\begin{algorithm}[ht]
  \caption{Simulate the Kuramoto model}
  \begin{algorithmic}[1]                 % [1] = number the lines
     \Require Phases $\theta_i$, ...
     \For{$m \gets 1$ \textbf{to} $M$}
        \State $q_i \gets \sum_j \sin(\theta_j-\theta_i)$
     \EndFor
     \State \Return $\theta_1,\dots,\theta_N$
  \end{algorithmic}
\end{algorithm}
```
Key macros: `\State \If \ElsIf \Else \EndIf \For \EndFor \While \Require \Return`.
`\gets` prints `←`.

### Code listings (Q4) — `\usepackage{listings}`
Define a style once, then include the external file:
```latex
\lstdefinestyle{pystyle}{language=Python, numbers=left, frame=single,
   keywordstyle=\color{blue!70!black}\bfseries, stringstyle=\color{red!65!black},
   commentstyle=\color{green!45!black}\itshape, basicstyle=\ttfamily\small}
...
\lstinputlisting[style=pystyle, caption={...}, label=lst:rc]{rc_response.py}
```
`\lstinputlisting{file}` pulls in an external file (what Q4 asks for). For inline
code use `\begin{lstlisting}...\end{lstlisting}`.

### Theorems & proofs (Q5) — `\usepackage{amsthm}`
```latex
\newtheorem{proposition}{Proposition}[section]   % numbers as 3.1, 3.2, ...
...
\begin{proposition}[Weak-field circular orbit]\label{prop:weak}
   For a circular orbit of radius $r$, ...
\end{proposition}
\begin{proof}
   ... \qedhere is automatic; a ∎ box ends the proof.
\end{proof}
```
`[section]` makes the number reset per section, giving "Proposition 3.1".

---

## 15. Table of contents (Q5)

```latex
\tableofcontents
\newpage
```
Built automatically from your `\section`/`\subsection` titles — **compile twice**.
Starred sections (`\section*`) are excluded. Q5 colours the word "Contents" with:
```latex
\renewcommand{\contentsname}{\textcolor{tocblue}{Contents}}
```

---

## 16. Bibliography and citations

You cite with `\cite{key}` → `[1]`, and list the sources at the end. Two routes:

### A. Manual `thebibliography` (used in the solutions — always compiles)
```latex
\begin{thebibliography}{9}     % "9" = widest label is one digit
\bibitem{ogata2010}
   K.~Ogata, \emph{Modern Control Engineering}, 5th ed.\ Prentice Hall, 2010.
\end{thebibliography}
```
`\cite{ogata2010}` then prints the number in citation order. This reproduces the
exact look with no extra tools.

### B. Real BibTeX with the provided `.bib` files
The exam ships `firefly_refs.bib`, `laplace.bib`, `solar_system.bib`. To use them:
```latex
\bibliographystyle{ieeetr}     % IEEE look: "E. Kreyszig, Advanced ... 2011."
\bibliography{laplace}         % file name without .bib
```
Compile: `pdflatex → bibtex → pdflatex → pdflatex`.
The **biblatex** alternative (nicer, what produces Q3's "In: *Journal* … doi:"
format):
```latex
\usepackage[backend=biber, style=numeric]{biblatex}
\addbibresource{firefly_refs.bib}
...
\printbibliography             % where the list appears
```
Compile with `biber` instead of `bibtex`.

> Note: `solar_system.bib` in this folder is wrapped in ```` ```bibtex ```` fences
> — delete the first and last lines (the back-ticks) before running bibtex/biber,
> or bibtex will error.

Which style to imitate:
- **Q3 (Fireflies)** — `biblatex` `numeric` (author full names, `In:`, `doi:`).
- **Q4 (Laplace), Q5 (Solar)** — IEEE style (`ieeetr` in bibtex): initials,
  italic title, `"quoted"` article titles.

---

## 17. Special characters you must escape

These characters are reserved; type them as shown to print them literally:

| Print | Type |
|-------|------|
| # $ % & _ { } | `\#  \$  \%  \&  \_  \{  \}` |
| ~ ^ | `\textasciitilde  \textasciicircum` |
| \ (backslash) | `\textbackslash` |

Accents outside `inputenc`: `\'e` (é), `\"a` (ä), `\^o` (ô), `\`a` (à). With
`utf8` input you can usually just type `é` directly.

---

## 18. A 10-minute battle plan for the exam

1. **Skeleton first**: documentclass, the packages from Section 1, `\title`
   block, `\begin{document}\maketitle`. Compile — get a blank titled page working.
2. **Pour in the text** section by section with `\section`/`\subsection`. Compile
   often; fix errors while they are small.
3. **Lists** — copy the nesting exactly; use `\item[...]` for odd labels.
4. **Equations** — inline `$...$` in prose; `equation`/`align`/`split`/`cases`
   for displays. Add `\label`s as you go.
5. **Tables** — draw the grid, then add `\multirow`/`\multicolumn`, then colour.
6. **Figures** — `figure`+`subcaption`, or `wrapfigure`; check image file names.
7. **Extras** — footnotes, `\href`, algorithm/listing/theorem, `\tableofcontents`.
8. **References** — `\cite` + `thebibliography` (or the `.bib`).
9. **Final**: compile **twice** (or thrice with bibtex); confirm no `??` and no
   `Undefined` warnings.

### Debugging tips
- Read the **first** error line — it usually names the file and line number.
- `Missing $ inserted` → a math symbol (`_`, `^`, `\alpha`) used outside `$…$`.
- `Undefined control sequence` → a typo, or a missing `\usepackage`.
- `!  ==>  Fatal error` at the end → scroll up to the real first error.
- Numbers show as `??` / citations as `[?]` → you didn't compile a second time.
- A stray `&` or missing `\\` breaks tables — count cells per row.

---

Study the five solved `.tex` files alongside this guide — every technique above is
demonstrated there in context, and all five compile cleanly with MiKTeX/Overleaf.
Good luck!
