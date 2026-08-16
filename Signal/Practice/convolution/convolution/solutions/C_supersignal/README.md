# Problem C (C1/C2) — Superposition of Multiple Signals

**File:** `solution_C.py`

## What the problem asks

1. Make a `SuperSignal` class that stores several component signals, each with a scalar
   coefficient (given in the template).
2. Add a method `output_super` to the LTI system that takes a `SuperSignal` and returns
   the corresponding output.
3. Test it in `main()`.

Example combination: `x(n) = 2·x1(n) − 1·x2(n)`.

## The idea — linearity of LTI systems

An LTI system is **linear**, which means:

```
output( a·x1 + b·x2 )  =  a·output(x1) + b·output(x2)
```

So a `SuperSignal` (a weighted sum of pieces) can be handled either by:
- **(A)** collapsing it into one signal first, then convolving once; or
- **(B)** convolving each piece separately, scaling, and adding.

Both give the identical answer — that's the whole point of the problem, and the code
verifies it.

## How the code solves it

**`SuperSignal`** stores `(coefficient, signal)` tuples in a list and can `combine()`
them into a single `DiscreteSignal`:
```python
def combine(self):
    total = None
    for coeff, sig in self.components:
        scaled = sig.multiply(coeff)               # coeff * sig
        total = scaled if total is None else total.add(scaled)
    return total
```
> `total = scaled if total is None else total.add(scaled)` is a **ternary expression**:
> "use `scaled` on the first pass (nothing to add yet), otherwise accumulate". This is a
> common pattern for summing a list of objects that don't start at zero.

**`output_super`** is added by **subclassing** your `LTISystem` (so we don't edit
`signal_lti.py`):
```python
class LTISystemSuper(LTISystem):      # inherits everything from LTISystem
    def output_super(self, super_signal):
        combined_input = super_signal.combine()
        return self.output(combined_input)     # one convolution
```
> `class Child(Parent):` means `Child` **inherits** all of `Parent`'s methods and can add
> more. Here we add just `output_super` and reuse the existing `output`.

**Verification (method B):** the code also convolves each component separately, scales by
its coefficient, and adds — then checks it equals `output_super`.

## Result when you run it

```
Combined input: [2.0, 0.0, -1.0] over [0, 1, 2]
Output y: [2.0, 1.0, -1.0, -0.5] over [0, 1, 2, 3]
Max |output_super - manual superposition| = 0.000e+00
Linearity holds: True
```

Hand check: `x = {0:2, 2:-1}`, `h = {0:1, 1:0.5}` →
`y = {0:2, 1:1, 2:-1, 3:-0.5}` ✓.

Plots (`outputs/`): combined input and the output.

## Mapping to the original template (`template.py`)

The template already gives `SuperSignal` with an `add(signal, coefficient)` method and
asks you to build `x(n)=2·x1−x2` and produce the output via superposition. We keep that
`SuperSignal`, add `combine()`, and provide `output_super` on the LTI subclass.
