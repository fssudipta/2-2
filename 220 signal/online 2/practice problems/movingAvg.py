# PROBLEM: Moving Average Filter
# Formula: y[n] = (x[n] + x[n-1] + x[n-2]) / 3
# This implies h[n] = 1/3 for n=0, 1, 2 and 0 elsewhere.
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

def solve_smoothing_problem():
    INF = 10
    system_h = Signal(INF)
    # Define h[n] = [0.33, 0.33, 0.33]
    for t in [0, 1, 2]:
        system_h.set_value_at_time(t, 1/3)
    
    # Input signal with a sudden "spike" (noise)
    # x = [0, 0, 10, 0, 0]
    x = Signal(INF)
    x.set_value_at_time(2, 10) 
    
    filter_sys = LTI_System(system_h)
    y = filter_sys.output(x)
    
    print("Smoothing Filter Output (Spike Spread):")
    for t in range(0, 6):
        print(f"y[{t}] = {y.get_value_at_time(t):.2f}")

# Expected: The spike at n=2 is spread across n=2, 3, 4 with value 3.33

if __name__=="__main__":
    solve_smoothing_problem()