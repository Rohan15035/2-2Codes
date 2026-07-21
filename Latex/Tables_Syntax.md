# LaTeX Tables — Syntax Notes

How tables are built in these `.tex` files. Every snippet below is taken from the actual documents.

## Required packages

```latex
\usepackage{multirow}          % \multirow — cell spanning several rows
\usepackage{booktabs}          % \toprule \midrule \bottomrule
\usepackage{array}             % >{...}p{width} column types
\usepackage[table]{xcolor}     % \rowcolor — colour a row (loads colortbl)
```

## 1. The skeleton — `table` wraps `tabular`

```latex
\begin{table}[h]              % float: h=here, t=top, b=bottom, p=float page, ht=here-or-top
  \centering                  % centre the whole table
  \begin{tabular}{|l|c|c|}    % one letter per column
    ...rows...
  \end{tabular}
  \caption{Comparison of Image Synthesis Techniques}
  \label{tab:comparison}      % target for \ref{tab:comparison}
\end{table}
```
- `table` is the **float** (gives caption/label + lets LaTeX move it); `tabular` is the **grid**. `[h]` from `table.tex:36` asks LaTeX to place it *here* if it fits.
- Caption + label go **inside** `table`, not `tabular`.

## 2. Column spec `{|l|c|c|}`

Inside `\begin{tabular}{...}` each character defines one column:
- `l` `c` `r` = left / centre / right aligned.
- `|` = a vertical rule between columns. `{|l|c|c|}` = 3 columns fully boxed; `{lcr}` (`table.tex:117`) = 3 columns, **no** vertical lines.

## 3. Cells and rows — `&` and `\\`

```latex
Method & Accuracy & Time Complexity \\
```
- `&` separates columns, `\\` ends a row (`table.tex:40`).
- Leave a cell empty for a blank: `Alice & 90 & & 88 \\` gives an empty Q2 cell (`table.tex:151`).

## 4. Horizontal rules — `\hline`

```latex
\hline
Method & Accuracy & Time Complexity \\
\hline
```
`\hline` draws a full-width line (`table.tex:39`). Put one before the first row and after each row for a fully-ruled table.

## 5. `\multirow` — one cell, several rows

```latex
\multirow{2}{*}{Ray Tracing} & High      & $O(n^2)$ \\
                             & Very High & $O(n^3)$ \\
```
- From `Q1_ImageSynthesis.tex:104`. `\multirow{2}{*}{Ray Tracing}` = "Ray Tracing" spans **2** rows; `*` = natural width.
- The **next** row leaves that first column empty (just start with `&`) because the multirow already filled it.

## 6. `\multicolumn` — one cell, several columns

```latex
\multicolumn{2}{|c|}{Hybrid Method} & $O(n^2)$ \\
```
- From `table.tex:48`. `\multicolumn{2}` merges **2** columns; `{|c|}` re-declares that merged cell's borders + alignment; `{Hybrid Method}` is its content.
- Common header use — merge two data columns under one title:
  ```latex
  \multirow{2}{*}{Module} & \multicolumn{2}{c|}{Score} \\   % table.tex:61
  ```

## 7. `\cline{a-b}` — partial horizontal line

```latex
\multirow{2}{*}{Module} & \multicolumn{2}{c|}{Score} \\
\cline{2-3}                                  % rule under columns 2 and 3 only
 & Theory & Lab \\
```
From `table.tex:61-63`. Unlike `\hline`, `\cline{2-3}` rules **only** columns 2–3 — used so the line doesn't cut through the `\multirow` cell on the left.

## 8. `booktabs` style — no vertical lines

```latex
\begin{tabular}{lcr}
  \toprule
  Item & Quantity & Price \\
  \midrule
  Apples & 10 & \$5.00 \\
  \bottomrule
\end{tabular}
```
From `table.tex:117-125`. `\toprule` / `\midrule` / `\bottomrule` replace `\hline`; the convention is **no `|` vertical rules** with booktabs. Note `\$` = a literal dollar sign (escaped so it isn't read as math).

## 9. `\rowcolor` — shade a row

```latex
\rowcolor{gray!15}
\multirow{2}{*}{\textbf{Planet}} & \multicolumn{2}{c|}{...} \\
```
From `Q5_SolarSystem.tex:231`. Put `\rowcolor{gray!15}` at the **start of a row** to shade it. `gray!15` = 15% grey; `green!10`, `red!10` work the same (`Q3_Fireflies.tex:120-127`). Needs `\usepackage[table]{xcolor}`.

## 10. Wrapping / fixed-width column — `p{width}`

```latex
\begin{tabular}{l l l >{\raggedright\arraybackslash}p{4.3cm}}
```
From `Q3_Fireflies.tex:115`. `p{4.3cm}` = a **fixed 4.3 cm** column whose text wraps onto multiple lines (plain `l/c/r` never wrap). The `>{\raggedright\arraybackslash}` prefix (from `array`) left-aligns that column and restores `\\` inside it.

## 11. Math inside cells

Just use inline math `$...$` in any cell:
```latex
Rasterization & Medium & $O(n)$ \\          % table.tex:42
& $a$ & $e$ & $\dfrac{1}{ac^2}GM_\odot$ \\  % Q5_SolarSystem.tex:237
```

## Quick reference

| Syntax | Purpose | Example line |
|---|---|---|
| `\begin{table}[h]` | float + caption/label | `table.tex:36` |
| `{\|l\|c\|c\|}` | column align + rules | `table.tex:38` |
| `&` / `\\` | column sep / row end | `table.tex:40` |
| `\hline` | full horizontal rule | `table.tex:39` |
| `\multirow{2}{*}{}` | span rows | `Q1_ImageSynthesis.tex:104` |
| `\multicolumn{2}{\|c\|}{}` | span columns | `table.tex:48` |
| `\cline{2-3}` | partial rule | `table.tex:62` |
| `\toprule \midrule \bottomrule` | booktabs rules | `table.tex:118-124` |
| `\rowcolor{gray!15}` | shade a row | `Q5_SolarSystem.tex:231` |
| `>{\raggedright\arraybackslash}p{4.3cm}` | wrapping column | `Q3_Fireflies.tex:115` |
| `\caption{} \label{}` | caption + cross-ref | `table.tex:51-52` |
