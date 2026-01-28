"""Problem 2: Cascaded LTI Systems
Scenario: Signals often pass through multiple systems in a row (a "cascade"). 
If you have two systems, the output of the first system becomes the input 
for the second."""

# tasks:
# 1. create a function output_cascade(input_signal, system_list) that takes a Signal
# and a list of lti_system objects
# 2. if system 1 is a moving average(h1 = [0.5, 0.5]) and system 2 is an "amplifier"(h2=[2.0]),
# find the final output for an impulse.

import numpy as np
import matplotlib.pyplot as plt

# Todo: Define Signal class

class Signal:
    def __init__(self, INF):
        self.INF = INF
        self.values = np.zeros(2*INF + 1)
    
    def set_value_at_time(self, time, value):
        if -self.INF <= time <= self.INF:
            self.values[time+self.INF] = value
    
    def get_value_at_time(self, time):
        if -self.INF <= time <= self.INF:
             return self.values[time+self.INF] 
        return 0
        
class SuperSignal:
    def __init__(self):
        self.components = []

    def add(self, signal: Signal, coefficient=1.0):
        self.components.append((coefficient, signal))
        
# Todo: Define LTI class

class LTI_System:
    def __init__(self, h:Signal):
        self.h=h

    def output(self, x:Signal):
        inf = x.INF
        result = Signal(inf)
        for n in range(-inf, inf+1):
            sum_val = 0
            for k in range(-inf, inf+1):
                sum_val += x.get_value_at_time(k) * self.h.get_value_at_time(n-k)
            result.set_value_at_time(n, sum_val)
        return result
    
    def output_super(self, super_signal:SuperSignal):
        first_sig = super_signal.components[0][1]
        final_output = Signal(first_sig.INF)

        for coeff, x_i in super_signal.components:
            y_i = self.output(x_i)

            for n in range(-final_output.INF, final_output.INF+1):
                cur_val = final_output.get_value_at_time(n)
                new_val = cur_val + (coeff * y_i.get_value_at_time(n))
                final_output.set_value_at_time(n, new_val)
        return final_output

def output_cascade(input_signal, systems_list):
    current_signal = input_signal
    for system in systems_list:
        # The output of the previous system becomes the input of the next
        current_signal = system.output(current_signal)
    return current_signal

def solve_cascade_problem():
    INF = 10
    
    # Input: Unit Impulse delta[n]
    x = Signal(INF)
    x.set_value_at_time(0, 1)
    
    # System 1: Moving Average (Averages current and previous value)
    h1 = Signal(INF)
    h1.set_value_at_time(0, 0.5)
    h1.set_value_at_time(1, 0.5)
    sys1 = LTI_System(h1)
    
    # System 2: Amplifier (Multiplies signal by 2)
    h2 = Signal(INF)
    h2.set_value_at_time(0, 2.0)
    sys2 = LTI_System(h2)
    
    # Execute Cascade
    final_y = output_cascade(x, [sys1, sys2])
    
    print("Cascade System Output:")
    for t in range(-1, 3):
        print(f"y[{t}] = {final_y.get_value_at_time(t):.1f}")

# Expected Logic:
# x convolved with h1 gives [0.5, 0.5]
# That result convolved with h2 ([2.0]) gives [1.0, 1.0]

if __name__=="__main__":
    solve_cascade_problem()