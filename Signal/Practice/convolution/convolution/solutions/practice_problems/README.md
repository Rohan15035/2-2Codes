# Practice Problems — 5 Convolution Exercises

Five extra problems you could be asked, each **reusing `signal_lti.py`**. Run any with
`python problemN_....py`. Each has its own `.md` with full explanation.

| # | File | Concept tested |
|---|------|----------------|
| 1 | `problem1_basic_convolution.py` | The convolution sum itself ("flip and slide"); library vs. by-hand |
| 2 | `problem2_smoothing_and_edges.py` | Moving-average smoother vs. first-difference edge detector |
| 3 | `problem3_echo_and_commutativity.py` | Echo/delay systems; convolution is commutative & associative |
| 4 | `problem4_step_response_roundtrip.py` | Impulse ↔ step response (running sum ↔ first difference) |
| 5 | `problem5_correlation_via_convolution.py` | Cross-correlation = convolution with a time-reversed signal |

**Shared helper** in every file:
```python
def make_signal(start_time, values):
    sig = DiscreteSignal(start_time, start_time + len(values) - 1)
    for i, v in enumerate(values):
        sig.set_value_at_time(start_time + i, float(v))
    return sig
```
This turns a plain Python list (e.g. `[1, 2, 3]`) into a `DiscreteSignal` that starts at
a chosen index — the quickest way to set up test signals.

See the top-level `../README.md` for the `signal_lti.py` reference and the Python
syntax cheat-sheet.
