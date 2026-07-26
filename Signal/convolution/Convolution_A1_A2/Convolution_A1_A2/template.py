"""
Instructions:
- x1, x2, a, b, k, and h are already given below.
- Complete the TODOs.
- Do NOT use numpy.convolve / scipy.signal / any built-in convolution.
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


def max_absolute_difference(first_signal, second_signal):
    """Helper: largest |difference| between two signals over their combined range."""
    # TODO: reuse your offline implementation of this function.
    start_time=min(first_signal.start_time,second_signal.start_time)
    end_time=max(first_signal.end_time,second_signal.end_time)
    worst = 0.0
    for n in range(start_time, end_time + 1):
        diff = abs(first_signal.get_value_at_time(n) - second_signal.get_value_at_time(n))
        if diff > worst:
            worst = diff
    return worst
    raise NotImplementedError


# ---- Generic property testers ----
# These must work for ANY apply_system callable
# method such as system_a.output. Do not assume apply_system is an LTISystem.

# You shoulb be able to use this function like: test_linearity(sys_a.output, x1, x2, a, b) 
# or test_linearity(system_b, x1, x2, a, b)

def test_linearity(apply_system, x1, x2, a, b):

    #TODO: Return max| apply_system(a*x1 + b*x2)  -  (a*apply_system(x1) + b*apply_system(x2)) |
    # NOTE: apply_system is a FUNCTION here. You never write `apply_system.output(...)`
    # or `LTISystem(...)` inside this function -- you just call it: apply_system(some_signal).
    # The caller decides which function gets passed in (see main()).
    #
    # Also: a*x1 does not work. DiscreteSignal has no __mul__ / __add__ / __sub__.
    # Use the methods you already wrote: .multiply(scalar) and .add(other_signal).
    #
    #   lhs_input = x1.multiply(a).add(x2.multiply(b))      # a*x1 + b*x2
    #   lhs       = apply_system(lhs_input)                  # S{a*x1 + b*x2}
    #   rhs       = apply_system(x1).multiply(a).add(apply_system(x2).multiply(b))
    #   return max_absolute_difference(lhs, rhs)
    lhs=x1.multiply(a).add(x2.multiply(b))
    lhs_o=apply_system(lhs)
    rhs_o=apply_system(x1).multiply(a).add(apply_system(x2).multiply(b))
    return max_absolute_difference(lhs_o,rhs_o)
    raise NotImplementedError


def test_time_invariance(apply_system, x, k):

    #TODO: Return max| apply_system(x shifted by k)  -  (apply_system(x) shifted by k) |
    # This one is already fine: apply_system is called as a plain function, and
    # .shift(k) returns a DiscreteSignal, so both arguments are signals.
    lhs=apply_system(x).shift(k)
    rhs=apply_system(x.shift(k))
    return max_absolute_difference(lhs,rhs)

    

# ---- System B: y[n] = n * x[n] ----

def system_b(input_signal):
    # TODO: build and return a DiscreteSignal where output[n] = n * input_signal[n]
    output=DiscreteSignal(input_signal.start_time,input_signal.end_time)
    
    for i in input_signal.times():
        output.set_value_at_time(i,i*input_signal.get_value_at_time(i))
    return output
    raise NotImplementedError


def main():
    tolerance = 1e-9

    # ---- Given signals and scalars (do not change) ----
    x1 = make_signal(-2, 2, [1, 0, 2, -1, 3])
    x2 = make_signal(-1, 3, [2, -3, 0, 1, 1])
    a, b = 2.0, -3.0
    k = 3

    h = make_signal(0, 2, [1.0, 0.5, 0.25])
    #TODO: Test both properties for system A
    system_a=LTISystem(h)
    print("=== System A: genuine LTI system (LTISystem.output) ===")
    # HOW TO PASS A FUNCTION:
    #   system_a          -> an LTISystem OBJECT. Not callable. system_a(x) is a TypeError.
    #   system_a.output   -> the bound METHOD, written WITHOUT parentheses.
    #                        This is the function object itself. Passing it means the
    #                        tester can later do apply_system(sig), which runs
    #                        system_a.output(sig) with self already bound to system_a.
    #   system_a.output(x1) -> parentheses = CALL IT NOW. That returns a DiscreteSignal,
    #                        which is NOT a function, so the tester would crash.
    #
    # Rule of thumb: no parentheses == pass the recipe. Parentheses == pass the cooked meal.
    #
    #   diff_linear_a = test_linearity(system_a.output, x1, x2, a, b)
    #   diff_ti_a     = test_time_invariance(system_a.output, x1, k)
    diff_linear_a = test_linearity(system_a.output,x1,x2,a,b)
    diff_ti_a = test_time_invariance(system_a.output,x1,k)
    print(f"Linearity max diff:        {diff_linear_a}")
    print(f"Time-invariance max diff:  {diff_ti_a}")

    print()

    #TODO: Test both properties for system B
    print("=== System B: y[n] = n * x[n] ===")
    # Same idea, but System B is already a plain function -- no object, no .output needed.
    #   system_b      -> the function object. THIS is what the tester wants.
    #   system_b(x1)  -> calls it now and gives back a DiscreteSignal. Wrong thing to pass.
    #
    # So the line below is the bug: System_b is a signal, and the tester then tries
    # to do System_b(...) on it, which fails.
    #
    #   diff_linear_b = test_linearity(system_b, x1, x2, a, b)
    #   diff_ti_b     = test_time_invariance(system_b, x1, k)
    #
    # If you ever need to adapt a function whose signature does not match, wrap it:
    #   diff_linear_b = test_linearity(lambda sig: system_b(sig), x1, x2, a, b)
    
    diff_linear_b = test_linearity(system_b,x1,x2,a,b)

    diff_ti_b = test_time_invariance(system_b,x1,k)
    print(f"Linearity max diff:        {diff_linear_b}")
    print(f"Time-invariance max diff:  {diff_ti_b}")

    print()
    # TODO: print a short conclusion stating which property System B fails
    # (linearity or time-invariance).


if __name__ == "__main__":
    main()
