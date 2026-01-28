"""Problem 1: The Echo System (Delay & Gain)
Scenario: In audio processing, an echo can be modeled as an LTI system. 
Suppose a system takes an input and adds an echo that is 50% of the volume 
and delayed by 3 time units."""

# define the impulse response h[n] for this system
# use the lti_system class to find the output when 
# the imput is a signal x[n] where x[0]=1, x[1]=2

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

def solve_echo_problem():
    INF = 10
    x = Signal(INF)
    x.set_value_at_time(0,1)
    x.set_value_at_time(1,2)
    x.set_value_at_time(2,3)

    """"defining the impulse signal"""
    h = Signal(INF)
    h.set_value_at_time(0, 1.0)
    h.set_value_at_time(3, 0.5)

    system = LTI_System(h)
    y = system.output(x)

    print("Echo System Output: ")
    for t in range(0, 7):
        print(f"y[{t}] = {y.get_value_at_time(t):.1f}")

if __name__=="__main__":
    solve_echo_problem()