# LaTeX Algorithms — Syntax Notes

How pseudocode is typeset in these `.tex` files. Every snippet below is taken from the actual documents (the Kuramoto/firefly algorithm in `Q3_Fireflies.tex`).

## Required packages

```latex
\usepackage{algorithm}       % the float: caption + numbering + lets it move
\usepackage{algpseudocode}   % the pseudocode commands (\State, \For, \Require ...)
```
Loaded together — `algorithm` gives the wrapper, `algpseudocode` gives the keywords (`Q3_Fireflies.tex:21-22`, also `try.tex:16-17`). For **verbatim source code** instead of pseudocode, `\usepackage{listings}` is used (`Q4_Laplace.tex:20`) — see §8.

## 1. The skeleton — `algorithm` wraps `algorithmic`

```latex
\begin{algorithm}[ht]
    \caption{Simulate the Kuramoto model}
    \begin{algorithmic}[1]
        ... pseudocode ...
    \end{algorithmic}
\end{algorithm}
```
- From `Q3_Fireflies.tex:198-213`. `algorithm` is the **float** (like `figure`/`table`): it prints "Algorithm N", takes a `\caption`, and can be referenced. `algorithmic` is the **body** that holds the steps.
- `[ht]` is the same float placement as figures (here / top). `\caption` goes **inside** `algorithm`, usually at the top for algorithms.

## 2. Line numbers — `algorithmic[1]`

```latex
\begin{algorithmic}[1]      % Q3_Fireflies.tex:200
```
The optional `[1]` turns on **line numbering**, starting at 1 and stepping by 1 (`[2]` = number every 2nd line, `[0]` or omitting = no numbers). Numbered lines are what you cross-reference and cite in an exam answer.

## 3. Inputs — `\Require` (and `\Ensure`)

```latex
\Require Phases $\theta_i$, frequencies $\omega_i$, coupling $K$, step
         size $h$, and number of steps $M$
```
From `Q3_Fireflies.tex:201-202`. `\Require` prints a bold **"Require:"** line for preconditions/inputs. Its sibling `\Ensure` prints **"Ensure:"** for postconditions/outputs. A long requirement can wrap onto the next source line freely — LaTeX ignores the break.

## 4. Statements — `\State`

```latex
\State Update all phases simultaneously:
       $\theta_i \gets (\theta_i + h v_i) \bmod 2\pi$
```
From `Q3_Fireflies.tex:208-209`. **Every ordinary line of pseudocode must start with `\State`** — it's what makes the line a numbered step. Plain text and inline math `$...$` mix freely inside it.

## 5. Loops — `\For ... \EndFor`

```latex
\For{$m \gets 1$ \textbf{to} $M$}
    \For{each firefly $i$}
        \State $q_i \gets \displaystyle\sum_{j=1}^{N}\sin(\theta_j-\theta_i)$
    \EndFor
    \State Update all phases simultaneously: ...
\EndFor
```
- From `Q3_Fireflies.tex:203-210`. `\For{condition}` opens a loop and **must** be closed by `\EndFor`; the body auto-indents.
- Loops **nest** — the inner `\For`/`\EndFor` sits inside the outer one. Keep the pairing exact or compilation fails.
- `\gets` prints the assignment arrow `←`; `\textbf{to}` bolds the keyword "to" so it reads like a keyword, not a variable.

## 6. Return — `\State \Return`

```latex
\State \Return $\theta_1,\dots,\theta_N$
```
From `Q3_Fireflies.tex:211`. `\Return` prints a bold **"return"**; it still needs a leading `\State` because it's a numbered step. `\dots` is the low ellipsis for lists.

## 7. Math inside pseudocode

```latex
\State $q_i \gets \displaystyle\sum_{j=1}^{N}\sin(\theta_j-\theta_i),
        \quad v_i \gets \omega_i + \frac{K}{N} q_i$
```
From `Q3_Fireflies.tex:205-206`. Everything mathematical stays in `$...$`. `\displaystyle` forces full-size sums/fractions inside the line; `\quad` inserts a wide gap between two statements on one step; `\bmod` gives the binary "mod" operator (`Q3_Fireflies.tex:209`).

## 8. Verbatim code instead of pseudocode — `listings`

```latex
\usepackage{listings}        % Q4_Laplace.tex:20
\begin{lstlisting}
    ...source code, kept exactly as typed...
\end{lstlisting}
```
Use `algorithmic` for **abstract steps** (what the algorithm does); use `lstlisting` when you need **real code printed literally** (spaces, symbols, no interpretation). The cheatsheet itself is built from `lstlisting` blocks (`LaTeX_Cheatsheet.tex:59-74`).

## 9. Referencing an algorithm

```latex
\begin{algorithm}[ht]
    \caption{Simulate the Kuramoto model}\label{alg:kuramoto}
\end{algorithm}
...
Algorithm~\ref{alg:kuramoto} repeats the interaction and update steps.
```
Add `\label{alg:...}` after the `\caption`, then `Algorithm~\ref{alg:...}` in the text — same non-breaking-space (`~`) and auto-numbering rule as figures/tables. (The repo introduces the block in prose at `Q3_Fireflies.tex:196`; add the label to make it a live cross-ref.)

## Sibling keywords (standard `algpseudocode`, same family)

Not used in these files, but from the same package — likely needed in an exam:

```latex
\While{condition} ... \EndWhile
\If{condition} ... \ElsIf{condition} ... \Else ... \EndIf
\Function{Name}{args} ... \EndFunction
\Procedure{Name}{args} ... \EndProcedure
\State \Call{Name}{args}          % call another routine
\Comment{note}                    % right-hand comment on a line
\Ensure                           % output / postcondition (pairs with \Require)
```
Each opener pairs with its `\End...`; all bodies auto-indent like `\For`.

## Quick reference

| Syntax | Purpose | Example line |
|---|---|---|
| `\usepackage{algorithm, algpseudocode}` | float + pseudocode commands | `Q3_Fireflies.tex:21-22` |
| `\begin{algorithm}[ht]` | float, caption, numbering | `Q3_Fireflies.tex:198` |
| `\caption{...}` | names it "Algorithm N" | `Q3_Fireflies.tex:199` |
| `\begin{algorithmic}[1]` | body + line numbers | `Q3_Fireflies.tex:200` |
| `\Require` / `\Ensure` | inputs / outputs | `Q3_Fireflies.tex:201` |
| `\State` | one numbered step | `Q3_Fireflies.tex:208` |
| `\For{...} ... \EndFor` | loop (nestable) | `Q3_Fireflies.tex:203-210` |
| `\gets` | assignment arrow ← | `Q3_Fireflies.tex:203` |
| `\State \Return` | return value | `Q3_Fireflies.tex:211` |
| `\displaystyle` `\quad` `\bmod` | full-size math / gap / mod | `Q3_Fireflies.tex:205-209` |
| `\label{alg:} \ref{alg:}` | cross-reference | (add after `\caption`) |
| `lstlisting` | verbatim source code | `Q4_Laplace.tex:20` |
