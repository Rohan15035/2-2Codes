import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX = -np.pi, np.pi          # x(t) is defined only on this range


def base_signal(t):
    # Asymmetric signal, so both the even and odd parts are non-trivial. (given)
    x = np.exp(-0.4 * t) * np.cos(2 * t) + 0.5 * t
    x[(t < T_MIN) | (t > T_MAX)] = 0
    return x


def time_reverse(t, x):
    # TODO: return the samples of x(-t).
    #       The grid is symmetric about 0, so reversing the array flips the time axis.
    return x[::-1]
    pass


def even_odd_decompose(t, x):
    # TODO: return (xe, xo) using time_reverse
    #       xe = 1/2 (x + x(-t)),   xo = 1/2 (x - x(-t))
    xr=time_reverse(t,x)
    xe=0.5*(x+xr)
    xo=0.5*(x-xr)
    return xe,xr
    pass


def reconstruct(xe, xo, a):
    # TODO: return y(t) = xe + a * xo
    return xe+a*xo
    pass


def main():
    t = np.linspace(T_MIN, T_MAX, 1000)
    x = base_signal(t)

    xe, xo = even_odd_decompose(t, x)

    # TODO: print reconstruction check  max|(xe + xo) - x|  (should be ~0)

    print(np.max(np.abs((xe+xo)-x)))

    print("Enter a to plot y(t) = xe(t) + a*xo(t).")
    print("  a = 1 -> x(t)   a = -1 -> x(-t)   a = 0 -> even part")
    print("Type 'q' to quit.\n")

    while True:
        # TODO: complete the loop
        #   - read input, quit on 'q'
        #   - convert to float a
        #   - y = reconstruct(xe, xo, a)
        #   - plot x, xe, xo, y  (title, xlabel, ylabel, legend, grid)
        pass


if __name__ == "__main__":
    main()
