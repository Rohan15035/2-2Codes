# CSE 220 — Signals & Their Properties (exam prep)

Everything for the three online problems, plus a fresh practice set.

## Original problems → solved

| PDF | Original template | Worked solution |
|---|---|---|
| `Spec_A1_A2 (1).pdf` | `template (2).py` | [`solutions/solution_A_time_subscaling.py`](solutions/solution_A_time_subscaling.py) |
| `Online_1_Spec_B1_B2 (1).pdf` | `Online_B_Template (2).py` | [`solutions/solution_B_shift_vs_phase.py`](solutions/solution_B_shift_vs_phase.py) |
| `Online_1_C1_C2 (1).pdf` | `template.py` | [`solutions/solution_C_time_reversal_even_odd.py`](solutions/solution_C_time_reversal_even_odd.py) |

**Read [`APPROACH.md`](APPROACH.md) first** — it explains the math, the coding
trick, and the mark-losing traps for each problem, plus a 90-second checklist.

## Practice set (do these yourself)

Fill in the blank templates in [`practice_exam/`](practice_exam/), then check
against `practice_exam/answer_key/`:

| # | You edit | Drills | Statement |
|---|---|---|---|
| P1 | `practice_exam/P1_time_scaling_template.py` | interpolation + axis remap | [QUESTIONS.md](practice_exam/QUESTIONS.md) |
| P2 | `practice_exam/P2_periodicity_aliasing_template.py` | discrete sinusoid properties | [QUESTIONS.md](practice_exam/QUESTIONS.md) |
| P3 | `practice_exam/P3_even_odd_discrete_template.py` | reversal + decomposition | [QUESTIONS.md](practice_exam/QUESTIONS.md) |

Run any file with `python <file>.py` (needs `numpy` and `matplotlib`).

Suggested drill: set a 30-minute timer per practice problem, implement the
`TODO`s, run it, and confirm your printed MSE / max-error matches the answer key.
