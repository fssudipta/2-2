import numpy as np
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, INF):
        # Initialize

    def set_value_at_time(self, t, value):
        # Set the value at time index t

    def shift(self, k):
        # Shift the signal and return the resultant signal

    def add(self, other):
        # Add two signals and return the resultant signal

    def multiply(self, scalar):
        # Multiply a constant value with the signal

    def plot(self, title="Discrete Signal"):
        # Plot the signal

class LTI_System:
    def __init__(self, impulse_response: Signal):
        # Initialize

    def linear_combination_of_impulses(self, input_signal: Signal):
        # Decompose the signal into impulses and corresponding coefficients

    def output(self, input_signal: Signal):
        # Calculate and return the output signal


if __name__ == "__main__":
    INF = 10

    # Input signal x(n)
    x = Signal(INF)
    x.set_value_at_time(-2, 1)
    x.set_value_at_time(0, 2)
    x.set_value_at_time(3, -1)

    x.plot("Input Signal x(n)")

    # Impulse response h(n)
    h = Signal(INF)
    h.set_value_at_time(0, 1)
    h.set_value_at_time(1, 0.5)

    h.plot("Impulse Response h(n)")

    # LTI System
    system = LTI_System(h)

    # Output
    y = system.output(x)
    y.plot("Output Signal y(n)")

