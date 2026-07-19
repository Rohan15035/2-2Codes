import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX = -np.pi, np.pi          # x(t) is defined only on this range


def base_signal(t):
    x = np.sin(t)                     # (given)
    x[(t < T_MIN) | (t > T_MAX)] = 0
    return x


def energy(t, x, a, b):
    # TODO: E[a,b] = integral_a^b |x|^2 dt, approximated as
    #       ( sum of |x|^2 over samples with t in [a,b] ) * dt
    #       Hint: dt = t[1] - t[0];  mask = (t >= a) & (t <= b)
    pass


def average_power(t, x, a, b):
    # TODO: P[a,b] = energy(t, x, a, b) / (b - a)
    pass


def main():
    t = np.linspace(T_MIN, T_MAX, 2001)
    x = base_signal(t)

    print("Enter interval a,b to compute energy and average power on [a,b].")
    print("Type 'q' to quit.\n")

    while True:
        # TODO: complete the loop
        #   - read input, quit on 'q'
        #   - split on ',' and convert a, b to float
        #   - compute E and P, print them
        #   - plot x(t) and the shaded |x|^2 over [a,b] (plt.fill_between)
        pass


if __name__ == "__main__":
    main()
