# PROBLEM: Associativity Property
# Prove: (x * h1) * h2 == x * (h1 * h2)

import numpy as np

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

def solve_associativity_problem():
    INF = 10
    x = Signal(INF)
    x.set_value_at_time(0, 5) # Input x[n] = 5*delta[n]
    
    h1 = Signal(INF)
    h1.set_value_at_time(0, 1); h1.set_value_at_time(1, 1) # h1 = [1, 1]
    
    h2 = Signal(INF)
    h2.set_value_at_time(0, 1); h2.set_value_at_time(1, -1) # h2 = [1, -1]
    
    sys1 = LTI_System(h1)
    sys2 = LTI_System(h2)
    
    # Method A: Step-by-step
    y_step1 = sys1.output(x)
    y_final_A = sys2.output(y_step1)
    
    # Method B: Combine h1 and h2 first
    # We convolve h1 and h2 to get a single equivalent system
    h_combined = sys1.output(h2) 
    combined_sys = LTI_System(h_combined)
    y_final_B = combined_sys.output(x)
    
    print("Method A (Step-by-step) at n=0, 1, 2:", 
          [y_final_A.get_value_at_time(n) for n in [0, 1, 2]])
    print("Method B (Combined h) at n=0, 1, 2: ", 
          [y_final_B.get_value_at_time(n) for n in [0, 1, 2]])

# Expected: Both should result in [5.0, 0.0, -5.0]
# Explanation: (1+z^-1)(1-z^-1) = 1 - z^-2. So output is 5*delta[n] - 5*delta[n-2]