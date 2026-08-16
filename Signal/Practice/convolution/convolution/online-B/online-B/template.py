"""
Instructions:
- Reuse the same DiscreteSignal and LTISystem classes from the offline.
- x, h1, the stored window of h2, and the observation range are given below.
- Complete the TODOs.
- Do NOT use numpy.convolve / scipy.signal / any built-in convolution.

Finite-window note:
Mathematically, h2[n] = u[n] continues forever. The code stores enough samples
of h2 for every input sample to affect the complete graded observation window.
Compare results only on OBSERVATION_START...OBSERVATION_END.
"""

import numpy as np
import matplotlib.pyplot as plt


def readable_time_ticks(time_values, max_labels=18):
    if len(time_values) <= max_labels:
        return time_values

    step = int(np.ceil(len(time_values) / max_labels))
    ticks = time_values[::step]

    if ticks[-1] != time_values[-1]:
        ticks.append(time_values[-1])

    return ticks


class DiscreteSignal:
    """Finite discrete-time signal with integer indices."""

    # Create a finite discrete-time signal over the given integer range.
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.values = np.zeros(end_time - start_time + 1)

    # Return the number of stored samples in the signal.
    def __len__(self):
        return len(self.values)
        
       

    # Return the integer time indices covered by the signal.
    def times(self):
        return np.arange(self.start_time,self.end_time+1)
    
    # Return the signal value at the given time index.
    def get_value_at_time(self, t):
        if t < self.start_time or t > self.end_time:
            return 0.0
        return self.values[t-self.start_time]

    # Set the signal value at the given time index.
    def set_value_at_time(self, t, value):
        if t < self.start_time or t > self.end_time:
            raise IndexError(f"time index {t} is outside the signal range [{self.start_time}, {self.end_time}]")
        self.values[t-self.start_time]=value


    # Return a shifted copy of the signal.
    def shift(self, k):

        shiftedValue=DiscreteSignal(self.start_time+k,self.end_time+k)
        shiftedValue.values=self.values.copy()
        # # loop diye :
        # for i in range(len(self.values)):
        #     shiftedValue.values[i]=self.values[i]
        return shiftedValue
        



      
      
    # Return the sum of this signal and another signal.
    def add(self, other):
       
        new_start=min(self.start_time,other.start_time)
        new_end=max(self.end_time,other.end_time)
        result=DiscreteSignal(new_start,new_end)

        for t in range (new_start,new_end+1):
            tmpA,tmpB=0,0
            if(self.start_time<=t<=self.end_time):
               tmpA=self.get_value_at_time(t)
            if(other.start_time<=t<=other.end_time):
                tmpB=other.get_value_at_time(t)
            result.set_value_at_time(t,tmpA+tmpB)
        return result

    # Return a scaled copy of the signal.
    def multiply(self, scalar):
       
        result=DiscreteSignal(self.start_time,self.end_time)
        result.values=scalar*self.values
        return result
        
        raise NotImplementedError("Complete multiply")

    # Return the nonzero samples of the signal.
    def nonzero_samples(self, tolerance=1e-12):
      mask=np.abs(self.values)>tolerance
      return self.times()[mask],self.values[mask]
        
    def plot(self, title, save_path=None, ax=None):
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots()

        time_values = list(self.times())
        markerline, stemlines, baseline = ax.stem(time_values, self.values)
        markerline.set_markersize(6)
        baseline.set_color("black")
        baseline.set_linewidth(1)

        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_ylabel("value")
        ax.grid(True, alpha=0.35)
        ax.set_xticks(readable_time_ticks(time_values))
        ax.tick_params(axis="x", labelsize=9)

        if save_path is not None:
            plt.savefig(save_path, bbox_inches="tight", dpi=150)

        return ax


class LTISystem:
    """Discrete-time LTI system described by a finite impulse response."""

    # Store the impulse response that defines the LTI system.
    def __init__(self, impulse_response):
        self.impulse_response=impulse_response
        
       
    # Return the output time range for the convolution result.
    def output_range(self, input_signal):
      
        n_min=self.impulse_response.start_time+input_signal.start_time
        n_max=self.impulse_response.end_time+input_signal.end_time
        return n_min,n_max
      
    # Return all shifted and scaled impulse-response components for the input.
    def get_response_components(self, input_signal):
        components=[]
        for k in input_signal.times():
            xk=input_signal.get_value_at_time(k)
            if abs(xk)<=1e-12:
                continue
            component_k=self.impulse_response.shift(k).multiply(xk)
            components.append((k,component_k))
        return components

    # Return the system output using superposition of response components.
    def output_by_superposition(self, input_signal):
        components=self.get_response_components(input_signal)
        start,end=self.output_range(input_signal)
        result=DiscreteSignal(start,end)

        for k,comp in components:
            result=result.add(comp)
        return result

    # Return the nonzero product terms that contribute to one output sample.
    def get_contributions_at_time(self, input_signal, n):
        contributions=[]
        for k in input_signal.times():
            xk=input_signal.get_value_at_time(k)

            h_idx=n-k
            if self.impulse_response.start_time<=h_idx<=self.impulse_response.end_time:
                hn_k=self.impulse_response.get_value_at_time(h_idx)
                term=xk*hn_k
                if abs(term)>1e-12:
                    contributions.append((k,xk,hn_k,term))
        return contributions

    # Return one output sample of the LTI system.
    def output_at_time(self, input_signal, n):
        contributions=self.get_contributions_at_time(input_signal,n)

        total=0
        for k,xk,hn_k,term in contributions:
            total+=term
        return total

    # Return the complete output signal of the LTI system.
    def output(self, input_signal):
      
        n_min,n_max=self.output_range(input_signal)
        result=DiscreteSignal(n_min,n_max)
        for n in range(n_min,n_max+1):
            y_n=self.output_at_time(input_signal,n)
            result.set_value_at_time(n,y_n)
        return result
        raise NotImplementedError("Complete output")




def make_signal(start_time, end_time, values):
    """Helper: build a DiscreteSignal from a list of values."""
    signal = DiscreteSignal(start_time, end_time)
    for offset, value in enumerate(values):
        signal.set_value_at_time(start_time + offset, value)
    return signal


def max_absolute_difference_in_range(first_signal, second_signal, start_time, end_time):
    """Largest |first[n] - second[n]| for start_time <= n <= end_time."""
    # WHAT WENT WRONG (2 bugs, both in the loop body):
    #
    # 1. `np.abs(a, b)` is NOT "absolute difference of a and b".
    #    numpy's second positional argument is `out` (the destination
    #    array), not a second operand. So the old line asked numpy to
    #    compute |first[n]| and write it into second[n] -- which raises
    #    "TypeError: return arrays must be of ArrayType" because a
    #    np.float64 scalar is not a writable output array. The function
    #    crashed before it could return anything.
    #    Fix: subtract FIRST, then take the absolute value: abs(a - b).
    #
    # 2. The comparison was inverted: `if diff < worst`. Starting from
    #    worst = 0 and only keeping values SMALLER than the best so far,
    #    the running maximum can never grow -- the function would always
    #    return 0.0. That is the worst kind of bug here, because 0.0 is
    #    exactly the answer that makes the identity test print "passed".
    #    It would have silently faked a correct result.
    #    Fix: keep the LARGER value, `if diff > worst`.
    worst = 0.0
    for n in range(start_time, end_time + 1):
        diff = abs(first_signal.get_value_at_time(n) - second_signal.get_value_at_time(n))
        if diff > worst:
            worst = diff
    return worst


def samples_in_range(signal, start_time, end_time):
    """Return [(n, signal[n]), ...] over an inclusive time range."""
    return [
        (n, signal.get_value_at_time(n))
        for n in range(start_time, end_time + 1)
    ]


def cascade(first_system, second_system, input_signal):
    """Apply first_system, then second_system, and return both outputs."""
    # This function itself was already correct: the defining property of a
    # cascade is that the SECOND system is driven by the FIRST system's
    # output, not by the original input.
    #
    # WHAT WENT WRONG: nothing here -- but main() never called it, and
    # hand-wired the two systems in parallel instead. See main().
    intermediate_output = first_system.output(input_signal)
    final_output = second_system.output(intermediate_output)
    return intermediate_output, final_output


def plot_cascade_responses(
    input_signal,
    accumulator_output,
    difference_output,
    start_time,
    end_time,
):
    """Plot the input, accumulator response, and first-difference response."""
    times = np.arange(start_time, end_time + 1)

    input_values = [
        input_signal.get_value_at_time(n)
        for n in times
    ]
    accumulator_values = [
        accumulator_output.get_value_at_time(n)
        for n in times
    ]
    difference_values = [
        difference_output.get_value_at_time(n)
        for n in times
    ]

    fig, axes = plt.subplots(3, 1, figsize=(8, 7), sharex=True)

    axes[0].stem(times, input_values)
    axes[0].set_title("Input signal $x[n]$")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True)

    axes[1].stem(times, accumulator_values)
    axes[1].set_title("Accumulator response $v[n]$")
    axes[1].set_ylabel("Amplitude")
    axes[1].grid(True)

    axes[2].stem(times, difference_values)
    axes[2].set_title("First-difference response $y[n]$")
    axes[2].set_xlabel("n")
    axes[2].set_ylabel("Amplitude")
    axes[2].grid(True)

    fig.suptitle("Accumulator and First-Difference Cascade")
    plt.tight_layout()
    plt.show()


def main():
    tolerance = 1e-9

    # ---- Given observation window (do not change) ----
    OBSERVATION_START = -2
    OBSERVATION_END = 8

    # ---- Given input signal (do not change) ----
    # x[n] is a non-impulse input with values [2, -1, 3, 1, -2] on n = -2...2 and is zero afterward.
    x = make_signal(
        OBSERVATION_START,
        OBSERVATION_END,
        [2.0, -1.0, 3.0, 1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    )

    # ---- Impulse responses ----
    # h1[n] = delta[n] - delta[n-1] = [1, -1]  on n = 0...1   (first difference)
    h1 = make_signal(0, 1, [1.0, -1.0])

    # h2[n] = u[n], the running-sum accumulator: h2[n] = 1 for ALL n >= 0.
    #
    # WHAT WENT WRONG: this was `np.arange(0, 11, 1)`, i.e. [0,1,2,...,10].
    # That is the ramp n*u[n], not the unit step u[n]. Convolving with a
    # ramp does not accumulate x -- it computes a weighted running sum,
    # so v[n] came out completely wrong and the cascade could never
    # collapse to the identity.
    # Fix: every stored sample of the unit step is 1.0, so use np.ones.
    #
    # On the finite window: u[n] runs forever and cannot be stored, but
    # y[n] on n = -2...8 only ever needs h2 at index n - k for k in the
    # support of x (-2...2), i.e. up to 8 - (-2) = 10. Storing n = 0...10
    # is therefore exact on the whole graded window -- as the spec says.
    h2 = make_signal(0, 10, np.ones(11))

    # ---- The two LTI systems ----
    differentiator = LTISystem(h1)
    accumulator = LTISystem(h2)

    # ---- Apply x[n] through Accumulator -> First difference ----
    # WHAT WENT WRONG: the old code was
    #     accumulator_output = accumulator.output(x)
    #     difference_output  = differentiator.output(x)
    # Both systems were fed the SAME input x. That wires them in
    # PARALLEL, not in cascade -- the first difference never saw the
    # accumulator's output at all, so `difference_output` was just
    # x[n] - x[n-1] and had nothing to do with the identity being tested.
    # The cascade() helper written above was also never called.
    # Fix: use cascade(), which feeds system 1's output into system 2.
    accumulator_output, difference_output = cascade(accumulator, differentiator, x)

    # ---- Compare the FINAL cascade output with the ORIGINAL input ----
    # WHAT WENT WRONG (2 bugs):
    #
    # 1. Wrong pair of signals. The old call compared accumulator_output
    #    against difference_output -- two intermediate signals that have
    #    no reason to be equal. The spec's claim is (h1 * h2)[n] = delta[n],
    #    so the thing to verify is  final output  ==  x  itself.
    #
    # 2. Wrong range. It used the union of the two signals' full supports
    #    (n = -2...19). Outside the observation window the finite stored
    #    window of h2 makes v[n] fall away from the true running sum, so
    #    y[n] there is a truncation artifact, not a real mismatch --
    #    comparing over it would report a large difference and fail a
    #    system that is actually correct. The spec says explicitly:
    #    "Compare results only on OBSERVATION_START...OBSERVATION_END".
    max_difference = max_absolute_difference_in_range(
        difference_output,
        x,
        OBSERVATION_START,
        OBSERVATION_END,
    )

    print("=== Input x[n] -> Accumulator -> First difference ===")
    print("Input samples:")
    print(samples_in_range(x, OBSERVATION_START, OBSERVATION_END))
    print("Accumulator response samples:")
    print(samples_in_range(accumulator_output, OBSERVATION_START, OBSERVATION_END))
    print("First-difference response samples:")
    print(samples_in_range(difference_output, OBSERVATION_START, OBSERVATION_END))
    print(f"Maximum absolute difference from x[n]: {max_difference}")

    # Plot x[n], the accumulator response v[n], and the cascade output y[n].
    plot_cascade_responses(
        x,
        accumulator_output,
        difference_output,
        OBSERVATION_START,
        OBSERVATION_END,
    )


    print()
    # WHAT WENT WRONG: `conclusion = None` printed the literal word "None".
    # The spec asks for a stated conclusion, so write the actual finding.
    conclusion = (
        "Conclusion: on n = -2...8 the cascade output y[n] equals the input x[n]\n"
        "(maximum absolute difference = {:.3e}). Convolving the two impulse\n"
        "responses gives (h1 * h2)[n] = u[n] - u[n-1] = delta[n], so the cascade\n"
        "is the identity system. The accumulator and the first difference are\n"
        "therefore inverse systems under zero initial conditions: running the\n"
        "sum and then differencing it returns the original signal unchanged."
    ).format(max_difference)
    print(conclusion)

    if max_difference is not None:
        print("Identity test passed:", max_difference < tolerance)


if __name__ == "__main__":
    main()
